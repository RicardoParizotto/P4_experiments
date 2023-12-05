# RESIST_ASPLOS

RESIST is a system that provides provides implementation of failure recovery for INCs. It includes an asynchronous replication protocol for keeping switch replicas
synchronized and uses a log-replay to recover after failures. The objective of the log-replay is to allow different notions of consistency by replaying packets 
according to the needs of the network operator. 


# Repository Organisation

./emulations - the BMv2 implementation a experiment to check the functionality of RESIST (e.g., check the detection of orphan packets using the controller and the recovery of correct round numbers)

./testbed - The tofino implementation for the two different INC systems. It includes code for x86 servers using scapy and P4-16 code for tofino. 


# Build the code

The different subprojects have their oqn requirements. 

The easiest way for running the BMv2 emulations is to copy the source code to the BMv2 tutorials virtual machine (available at https://github.com/p4lang/tutorials)

Installing the ./emulations/requirements using sudo privileges

The testbed implementation requires a tofino SDE 9.4.0 to build the switch code. 

Servers have the following requirements:

torch
torchvision
pandas
matplotlib