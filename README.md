# ml-on-blockchain

## Simple behavior

### One server multiple workers

Goal of this first milestone is to deploy a smart contract on a local quorum blockchain.
The smart contract consists of a counter that can be incremented.
Once the smart contract is deployed, a worker willing to join the learning process should call this smart contract and
increment the counter by one (this will later on be used in order to add a worker to set of workers).

#### algorithm assumptions

In order to define a simple behavior, we assume that the learning server only send new model weights to a worker if this
one has already give its optimization result, or if it just registered to learning.


## Centralized federated learning

We will have one node (the learning server) which will be handling the learning process (maintain the learning model
states, aggregate results of workers, decide which worker should be working on learning). Every node (worker) of the
process will have to send its result to the learning server.


# Federated learning using smart contract

## Goals:

Our goal would be that every person (worker) willing to join the learning process could pick up a "job" - a learning
task- from the blockchain. As a reward of this task which involves computations, the worker would be rewarded by some
etherum, if its computations where classified as correct (we detail all theses process later).

## Members:

- Learning server, create jobs. Update machine learning weights once a job is successfully completed.
- Worker: person willing to participate to learning process

## Assumptions:

These are assumptions we defined in order to design our smart contracts, and know wich goals need to be satified.

- The Learning server can be trusted (i.e workers that do a correct job get paid up to a certain probability)
- The Learning server allows everyone able to access the blockchain to see the model (as wokers need to update it)
  - We could implement connection between server and model such that model is not sent on blockchain, but as this point there isn't much justification of using a blockchain
- The Workers cannot be trusted:
  - They may never return the results of their calculations
  - They can send wrong computations results (i.e model weights)
  - (Other ?)
- If a worker make a correct computation, it gets rewarded with probability ??? TODO
- No more than half of the network's workers can be evil
- Each worker and the learning server initially possess the exact same dataset (MNIST dataset for example)

## The task

We will see if under our assumptions, blockchain and smart contract can be used to implement our goals. The task consists of training a machine learning model using federated learning. For now we will not implement the machine learning algorithm concretly (i.e we will use fake weights and model updates) for simplicity. However if we have time we will see if blockchain can be used to train a model on MNIST, and analyze the results.


## Sending a job to the worker

## Results Sending

## Workers results verification

## Payment of the workers

## The smart contracts

We will describe the smart contracts structure induced by previous parts

### Deploy Jobs

### Job
