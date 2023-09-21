# ML-on-blockchain

In this project, we will see if it is possible to use Blockchain as a consensus mecanism in order to 
perform a federated Learning task.

# Federated learning using smart contract:

## Goals:

Our goal would be that every person (worker) willing to join the learning process could pick up a "job" - a learning
task- from the blockchain. As a reward of this task which involves computations, the worker would be rewarded by some
etherum, if its computations where classified as correct (we detail all theses process later).

## Members:

- Learning server, create jobs. Update machine learning weights once a job is successfully completed.
- Worker: person willing to participate to learning process

## Assumptions:

These are assumptions we defined in order to design our smart contracts, and know wich goals need to be satified.

1. The Learning server can be trusted (i.e workers that do a correct job get paid up to a certain probability)
2. The Learning server allows everyone able to access the blockchain to see the model (as wokers need to update it)
  - We could implement connection between server and model such that model is not sent on blockchain, but at this point there isn't much justification of using a blockchain
3. The Workers cannot be trusted:
  - They may never return the results of their calculations
  - They can send wrong computations results (i.e model weights)
  - (Other ?)
4. If a worker make a correct computation, it gets rewarded with probability ??? TODO
5. No more than half of the network's workers can be evil
6. Each worker and the learning server initially possess the exact same dataset (MNIST dataset for example)

## The task

We will see if under our assumptions, blockchain and smart contract can be used to implement our goals. The task consists of training a machine learning model using federated learning. For now we will not implement the machine learning algorithm concretly (i.e we will use fake weights and model updates) for simplicity. However if we have time we will see if blockchain can be used to train a model on MNIST, and analyze the results.


## Sending a job to the worker

The data sent to worker that picked a job will be:
- model weights (float[])
- data index for the stochastic gradient descent

### Why this format ?

- Model weights: necessary as the worker needs to start with fresh new weights, i.e don't need to perform all previous work to each this model.
- Batch index vs Batch data (complete data to perform computation on)
  - Batch index:
    - Pros: **lower loading** of the blockchain (we don't need to store data on blockchain); works from asssumption **(6)**
    - Cons: Needs assumption **(6)**
  - Batch data:
    - Pros: no need of assumption **(6)**
    - Cons: **higher loading** of the blockchain (may cause performances issues).

## Results Sending

Once the workers have their updated models weights, they send them to the smart contract responsible of the job. Note that data send to smart contract is kept inside private fields of the smart contract (at least until termination). Otherwise anyone could just read the models/models hash and just replicate them, pretending to have done the job.

### Why send models weights and not only hashed ?

- Sending hashed:
  - Pros: **lower loading** of the blockchain
  - Cons: need to implement mechanism to get the models weight once the correct model update have been validated. I.e ask worker that sent correct hash to send the complete model, so we need at least one worker to save state of models.
- Sending models:
  - Pros: once worker sends their model, they don't need any extra actions; Don't leak any info as updated models are kept private on smart contract (until job ended).
  - Cons: ***heavier loading** of the blockchain. May be problematic, we will see if Quorum can handle such flow.

So we chose to send weights (implementation much easier). However depending on the results, this could show that this method isn't applicable on Quorum. We also choose to send complete model weigths - sending only frac of them could reduce blockchain workload
but in that case we would need mechanism to retrieve complete weights once correct one has been decided, so no advantages
compare to sending models hashes.


## Workers results verification

From *Results Sending* we now have that the smart contract responsible for the job has the weights sent by each workers
(kept private), and need to verify if these weights are correct.
A first mechanism we will implement is the following:
- We group by models. Group with higher number of element is selected as correct model.

What we want to have according to this result verification process is:
$$P(\text{worker paid} | \text{good worker, job pool size})\textbf{[1]}$$

Where:
- good worker is the indicator r.v equal 1 if worker pushed correct weights, 0 otherwise (evil worker)
- job pool size is the number of models weights sent to server before result verification (could also be expressed as fraction of total workers in the network)

## Payment of the workers

As workers send all their weigths, we can up to a certain probability **[1]** decide if a worker did send a correct weight.
Ideally we would like to pay workers such that in expectation, good workers get rewarded the correct amount spent for
their computations (+ benefits). One drawback would be that expectation of earning for evil workers - ressources spent
would be > 0 (TODO verify with computations).
As the point of people joining learning process would be that expected earning - ressources spent is greater than 0,
we decide to adjust paiement value according to **[1]**. Server will be spending more money, but workers will have
reason to join

## The smart contracts

We will describe the smart contracts structure induced by previous parts

### Deploy Jobs

For the moment, only one job is deployed at the time. We will see if depending on the number of worker this strategy
don't lost too much time.
Interaction between the Job smart contract and workers is made through the Job finder contract (workers don't
directly call the Job contract as we don't have its ABI).

### Job


### Communication Protocol

In this section we describe how the workers will send their results to the learning server, and how the verification from server will allows to pay only workers that did learn the correct new model.

Initial Setup:
- Each worker i has a private key $S_{k_i}$ and public key $P_{k_i}$
- Let **SC** be the smart contract handling a learning job

For each round of federated learning:
- At begining: each worker define a secret $(R_i$ for worker i$)$. This can be a big number, st probability that two workers generate same R is low.

- When worker i perform the learning task (i.e compute a new model **$M$**):
  - it creates a key: $S_i = Enc_{S_{k_i}}(R_i)$. This key should be at least as long as **$M$** (TBD)
  - it sends $M\oplus S_i$ to **SC**
     - Note that as no one knows $S_i$, no one is able to efficiently get **$M$**
     - If someone knows **M** -> Pb ?
- Then it periodically checks the **SC** until it sees that enough model have been send. Suppose now is the case, now the SC don't accept any new models submission.
  - it sends $R_i$ and $S_i$ to **SC**.
    - Using $S_i$ the *SC* can recover **$M$** = $(M\oplus S_i)\oplus S_i$
    - *SC* can now check that the model was learned by the correct worker:
      - *SC* can compute $Dec_{P_{k_i}}(S_i) = Dec_{P_{k_i}}(Enc_{S_{k_i}}(R_i')) = R_i'$
      - If $R_i' \neq R_i$ then the worker i don't get paid
      - If $R_i' = R_i$ and the model sent by worker i was selected as the best one, worker i gets paid.

### Proof that you can't impersonate a worker's job if you didn't learn the model

- If someone has M -> learned the model so legit
- Assume **MIM** previously send $M_{rdm} \oplus S_{MIM}$, with $M_{rdm}$ dumb weights
  - Man in the middle when worker 0 sends $(R_0, S_0)$
    - it can replace it with $(R_{MIM}, S_0)$ but in that case the $SC$ will not agree with the decryption of $(M_{rdm} \oplus S_0) \neq (M_{rdm} \oplus S_{MIM})$ So **MIM** don't get paid.
    - it can replace it with $(R_0, S_{MIM} = S_{k_{MIM}}(R_{0}))$. But in that case $R_0 \neq Dec_{P_{k_0}}(S_{MIM}))$ so don't get paid.
