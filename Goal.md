# What are the objectives of this semester project ?


In the following questions, we assumed that we have deployed a smart contract(SC) on the Quorum blockchain.
This contract can send weights to learners, and learners can sends parts of the model they have learned back.
After having received all the fragments necessary to reconstruct a model, the SC reconstruct it
and check that it is correct.

## The questions we can ask ourselves about machine learning on blockchain:

- Is there a limit in the number of workers willing to participate in a learning ? I.e if we have 10000 fragments,
can 10000 workers interact with SC without too much loss of performances given the number of parameters of the model ?

- Is the implementation where each workers sends model weights actually a good option ? Does it create too much
workload on the blockchain ? Not sure how to measure this

- Each model is divided into fragments. Let n be the number of same fragment that must be received by the SC before
considering the fragment as valid (i.e don't accept any new weights for this fragment). What would a curve displaying
the probability that a model is correct and performances of the learning ? The x absciss is n, and in y we have
performances and probabilities of sucess.
    - Derive some formulas to compute under which probability the new model computed will be correct,
     assuming p(evil) < 50% of workers in the networks are evil (i.e can send wrong weights).

## How we will answers this questions ?

The current diablo implementation makes its difficult to handle the response of smart contracts call. In consequences,
what we need to have is a rough idea of given a number of workers and a number of fragment, how many calls
of "get model parameters", "send model fragment" we should perform in order to process one learning step. An average
of the time taken by each worker to perform one learning step is also necessary.
Having this we could easily generate a workload of the learning process.

### Fined grained analysis

We will start with a python script that will deploy SC on the quorum blockchain. We then create workers (up to 999) that
will be randomly selected to participate in the learning. We can easily tune the number of fragments needed to complete
a model, as well as the probability of an evil worker. This implementation will take care that the learning is correct.
So for example if a worker sends a fragment that was already send on the SC, it will have to send another one. I.e
create another transactions.
After performing one learning step (or multiple), we will measure how many parameters were getted by the workers, and
how many weights fragments were send by workers.
These measurements will allow us to scale our number of workers and requests using diablo (see below)


### Benchmarking using diablo

The diablo implementation would disregard the veracity of the learning, but would rather serve to measure its
performaces on a blockchain. This is because we don't care if the exact correct fragments numbers are send,
as we have an estimate of this probability event. This technique would allow us to easily vary the number of workers
in the learning process and see if blockchain can handle this process.
