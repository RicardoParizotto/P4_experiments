from scapy.all import sendp, srp, srp1, conf, Ether, IP, UDP
import torch
import time
from protocol import Gradient, SspHeader, assemble_multicast_pkt, assemble_pkt, unquantize
from scapy.all import sniff


import matplotlib

matplotlib.use("Agg")

CHUNK_SIZE = 500
conf.use_pcap = True
conf.verb = 0
conf.layers.filter([Ether, IP, UDP, SspHeader, Gradient])
conf.checkIPaddr = False

def chunkify(iterable, size=CHUNK_SIZE):
    for i in range(0, len(iterable), size):
        yield iterable[i : i + size]


def read_rows(n, worker_id, worker_clock, veth):
    """Read the first n rows"""
    pkts = [assemble_pkt(worker_id, worker_clock, x, "read_row") for x in range(n)]
    responses = []

    for chunk in chunkify(pkts):
        res, nres = srp(chunk, timeout=3, iface = veth, retry=-1000, filter="udp")
        answers = [answer.answer for answer in res]
        
        if len(answers) != len(chunk):
            raise RuntimeError("Deu ruim! Pacotes sem resposta: {}".format(nres))
        responses.extend(answers)

    
    #print("collecting tensors")   
    responses = sorted(responses, key=lambda obj: obj.grad_segment)
    grads = [res.getlayer(Gradient).get_grads() for res in responses]
    tensors = [torch.tensor(grad) for grad in grads]

    # Concatenating all tensors into one
    return unquantize(torch.cat(tensors))


def inc_rows(n, values, worker_id, worker_clock, veth):
    """Increment the value of the first n rows"""
    #i = 0
    #achei = False
    #for x in values:
    #    for y in x:
    #        if y != 0:
    #            achei = True
    #    if achei:
    #        break
    #    i = i + 1

    #if not achei:
    #    i = i - 1
  
    #print(values[i])
    pkts = [
        assemble_pkt(worker_id, worker_clock, x, "inc", value)
        for x, value in zip(range(n), values)
    ]
    #pkts[i].show2()
    print("inc rows")
    sendp(pkts, iface=veth)

def clock(worker_id, worker_clock, veth):
    """Inform the switch that the worker has completed one clock.
    Only return when the worker can proceed training"""
    
    pkt = assemble_multicast_pkt(worker_id, worker_clock, 0, "clock")
    #print("send packet") 
    response = srp1(pkt, iface=veth, verbose=True)
   
    #pkt = assemble_pkt(worker_id, worker_clock, 0, "clock")
    #print("send packet") 
    #response = srp1(pkt, iface=veth, verbose=False)
    
    if response is None:
        print("abacate")
        raise RuntimeError(
            f"Clock response {worker_clock} for worker {worker_id} timed out"
        )
