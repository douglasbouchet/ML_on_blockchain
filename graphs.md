## Can we use blockhain to perform complex calculus operations ?

### from basic infos:
- avg throughput / avg load -> e.g 80/100 tx/s committed
  - If goes down, bad perf
- avg latency
  - If goes up, bad perf

### from workload trace:

- get number of commit per seconds and plot this in a graph
    - constant if workload can be handled
    - goes down if blockchain overloaded


### Graphs:

**What we do**

- Run of the Federated learning task on the blockchain, with 10 learning tasks.

**What we vary (x-axis)**

- We vary the number of workers (adjust size of majority in smart contract to match)
- Values to try TBD but probably from 5 to 100000

**What we measure (y-axis, multiple ones)**

- avg throughput / avg load = #txs/s committed -> one number
- avg latency -> one number

## other graph

For one specific configuration, one can use the workload trace to get the number of txs
commited per seconds, and plot this in a graph. -> one graph per parameter


## Scenario:
- lab vms
- AWS with 15 nodes (**try with more nodes ?**)
  - Same vm performances
    - all vm in same region
    - vm in 10? different regions
  - Some vm strong, some weaks
    - all vm in same region
    - vm in 10? different region

-> 1 + 2*2*(n different nodes conf) scenario
5 scenario atm.


## Ideas:

During learning of the 10 taks, see if learning all parallel is equivalent to learning one after the other.
