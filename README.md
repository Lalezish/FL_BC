# Decentralized Blockchain driven Federated Learning approach for sensative network data

## Description
This project implements a federated learning approach in a blockchain environment in order to keep sensitive network data locally while still 
sharing valuable machine learning models with other contributors within the network. The approach aims to create a global model for anomaly detection
while keeping training data local within each device. The developed approach demonstrates a functional simulated setup but it should NOT be considered an optimal solution for deployment.

## Setup
The developed setup uses a smart contract deployed by a central node known as the aggregator. This aggregator, being the contract's owner, can freely choose which nodes to include 
as collaborators. Only these collaborators (which are trusted by the aggregator) are able to upload their models to the blockchain for aggregation.
Once the aggregator has added their chosen collaborators, each federated learning round can be described by the following steps.

### Process steps:
- Each node trains a model on their local data.
- Each node uploads their local model weights to the blockchain while keeping the data locally.
- A central aggregator downloads the model weights from the blockchain, merges them and redistributes the aggregated model weights.
- Each node replaces their local model with the downloaded aggregated model weights.

### Setup overview
 ![FL_BC (1)](https://github.com/Lalezish/FL_BC/assets/78786599/134cc094-f690-47bb-b25a-526b670eb2ba)

## Simulation necessities
- Python (with mentioned libraries)
- Ganache
- IPFS
- Truffle
