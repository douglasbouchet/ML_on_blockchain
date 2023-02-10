import json
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import make_interp_spline
import plotly.express as px
import os
from matplotlib.ticker import ScalarFormatter


def plot_max_array_length():
    # model_length_range = np.arange(1000, 49000, 1000)
    model_length_range = np.arange(
        1000, 50000, 2000)  # select half of the points
    # 1000, 49000, 2000)  # select half of the points
    all_perc_committed = []
    # n_runs = 9
    n_runs = 20
    for run_nb in range(1, n_runs+1):
        waiting_times = []
        percentages_committed = []
        n_txs = []
        for model_length in model_length_range:
            print("run_nb:", run_nb, "model_length:", model_length)
            with open("/home/user/ml_on_blockchain/results/aws/varying_array_length/run_{}/{}.txt".format(run_nb, model_length)) as json_file:
                data = json.load(json_file)
                tx_submitted = 0
                tx_committed = 0
                tot_commit_time = 0
                for tx in data["Locations"][0]["Clients"][0]["Interactions"]:
                    submit_time = tx["SubmitTime"]
                    commit_time = tx["CommitTime"]
                    tx_submitted += 1
                    if commit_time != -1:
                        tx_committed += 1
                        tot_commit_time += commit_time - submit_time
                perc_committed = tx_committed / tx_submitted * 100
                if (perc_committed == 0):
                    print("model_length:", model_length, "i:", i)
                percentages_committed.append(perc_committed)
        all_perc_committed.append(percentages_committed)

    mean_commited = np.mean(all_perc_committed, axis=0)
    min_commited = mean_commited - np.min(all_perc_committed, axis=0)
    max_commited = np.max(all_perc_committed, axis=0) - mean_commited

    asymmetric_error = [min_commited, max_commited]
    print("min_commited:", min_commited)
    print("max_commited:", max_commited)

    fig = plt.figure()
    # set fig size
    fig.set_size_inches(18.5, 10.5)
    graph = plt.bar(
        model_length_range,
        mean_commited,
        width=1000,
        label="mean over 20 runs",
        color='royalblue',
    )
    # add error bars
    plt.errorbar(
        model_length_range + 80,
        mean_commited,
        yerr=asymmetric_error,
        fmt='none',
        ecolor='black',
        marker='o',
        elinewidth=3,
        capsize=6,
        label="Range of values over 20 runs",
    )
    i = 0
    for p in graph:
        width = p.get_width()
        height = p.get_height()
        x, y = p.get_xy()

        plt.text(x+width/2 - 450,
                 y+height*1.01,
                 str(int(mean_commited[i])),
                 ha='center',
                 weight='bold',
                 fontsize=14)
        i += 1
    # plt.ylim(50, 100)
    plt.ylim(40, 100)
    fontsize = 18
    plt.xticks(model_length_range, [str(int(x/1000)) + 'k'
               for x in model_length_range])
    plt.title("Percentage of commited transactions for different array size",
              fontsize=fontsize+2)
    plt.xlabel("Array size",
               fontsize=fontsize)
    plt.ylabel("Commit %", fontsize=fontsize)
    plt.rcParams.update({'font.size': 14})
    plt.xticks(fontsize=fontsize - 3)
    plt.yticks(fontsize=fontsize)
    # plt.grid(True)
    plt.legend()

    plt.savefig(
        "/home/user/ml_on_blockchain/results/images/aws/max_array_length.png")


def plot_varying_perf():
    # model_length_range = [50_000, 300_000, 600_000, 1_000_000]
    # model_length_range = [50_000, 100_000, 300_000, 600_000, 1_000_000]
    model_length_range = [50_000, 100_000, 300_000, 600_000, 1_000_000]
    workers_range = [2**i for i in range(10)]
    print("workers_range:", workers_range)
    n_runs = 1
    model_perf = []
    for model_length in model_length_range:
        model_length_committed = []
        for n_worker in workers_range:
            all_perc_committed = []
            for run_nb in np.arange(1, n_runs + 1):
                waiting_times = []
                percentages_committed = []
                path = "/home/user/ml_on_blockchain/results/aws/varying_workers/varying_time/model_length_{}/run_{}/{}.txt".format(
                    model_length, run_nb, n_worker)
                # print("path:", path)
                with open(path) as json_file:
                    # with open("/home/user/ml_on_blockchain/results/max_model_size/{}.txt".format(model_length)) as json_file:
                    data = json.load(json_file)
                    tx_submitted = 0
                    tx_committed = 0
                    tot_commit_time = 0
                    for tx in data["Locations"][0]["Clients"][0]["Interactions"]:
                        submit_time = tx["SubmitTime"]
                        commit_time = tx["CommitTime"]
                        tx_submitted += 1
                        if commit_time != -1:
                            tx_committed += 1
                            tot_commit_time += commit_time - submit_time
                    perc_committed = tx_committed / tx_submitted * 100
                    avg_commit_time = tot_commit_time / tx_committed if tx_committed != 0 else 0
                    waiting_times.append(avg_commit_time)
                    percentages_committed.append(perc_committed)  # for 1 truc
                all_perc_committed.append(percentages_committed)
            # we finished all runs for this worker number, so compute the mean and append it inside model_length_committed
            worker_mean = np.mean(all_perc_committed, axis=0)
            model_length_committed.append(worker_mean)
            # print("model_length_committed:", model_length_committed)
        print("final model_length_committed:", model_length_committed)
        model_perf.append(model_length_committed)
    fontsize = 18
    fig, ax = plt.subplots()
    fig.set_size_inches(12.5, 8)
    plt.title(
        "% commited transactions by varying number of workers for different model lengths",
        fontsize=fontsize)
    plt.xlabel("Number of workers", fontsize=fontsize)
    plt.ylabel("Commit %", fontsize=fontsize)
    plt.xticks(fontsize=fontsize-2)
    plt.yticks(fontsize=fontsize-2)
    plt.xscale("log")
    plt.ylim(-2, 100)
    plt.grid(True)
    for i in range(len(model_perf)):
        plt.plot(
            workers_range,
            model_perf[i],
            marker="o",
            label="model length {}".format(model_length_range[i]),
        )
    textstr = '\n'.join((
        "Time used for one learning step",
        "Model length 50k Time: 50s",
        "Model length 100k ; Time: 100s",
        "Model length 300k ; Time: 300s",
        "Model length 600k ; Time: 600s",
        "Model length 1000k ; Time: 1000s"))
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    ax.legend(loc="lower left")
    ax.set_xticks(workers_range)
    ax.set_xticklabels(workers_range)
    print("model_perf:", model_perf)
    # flat modle_perf
    flat_model_perf = [item for sublist in model_perf for item in sublist]
    # [str(int(length / 1000)) + "k" for length in workers_range])
    # ax.set_yticks(flat_model_perf)
    # ax.set_yticklabels(flat_model_perf)
    # [str(worker) for worker in max_n_workers])
    plt.savefig(
        "/home/user/ml_on_blockchain/results/images/aws/varying_time/all.png".format(model_length))


def plot_varying_perf_constant_time():
    model_perf = []
    model_length_range = [50_000, 100_000, 200_000,
                          300_000, 600_000, 1_000_000, 5_000_000]
    workers_range = [2**(i) for i in range(9)]
    print("model_length_range:", model_length_range)
    print("workers_range:", workers_range)
    n_runs = 1
    for model_length in model_length_range:
        model_length_committed = []
        for n_worker in workers_range:
            all_perc_committed = []
            for run_nb in np.arange(1, n_runs + 1):
                waiting_times = []
                percentages_committed = []
                # path = "/home/user/ml_on_blockchain/results/varying_workers/model_length_{}/run_{}/{}.txt".format(
                path = "/home/user/ml_on_blockchain/results/aws/varying_workers/constant_time/model_length_{}/run_{}/{}.txt".format(
                    model_length, run_nb, n_worker)
                if os.stat(path).st_size == 0:
                    percentages_committed.append(0.0)
                else:
                    with open(path) as json_file:
                        data = json.load(json_file)
                        tx_submitted = 0
                        tx_committed = 0
                        tot_commit_time = 0
                        for tx in data["Locations"][0]["Clients"][0]["Interactions"]:
                            submit_time = tx["SubmitTime"]
                            commit_time = tx["CommitTime"]
                            tx_submitted += 1
                            if commit_time != -1:
                                tx_committed += 1
                                tot_commit_time += commit_time - submit_time
                        perc_committed = tx_committed / tx_submitted * 100
                        avg_commit_time = tot_commit_time / tx_committed if tx_committed != 0 else 0
                        waiting_times.append(avg_commit_time)
                        percentages_committed.append(
                            perc_committed)  # for 1 truc
                all_perc_committed.append(percentages_committed)
            # we finished all runs for this worker number, so compute the mean and append it inside model_length_committed
            worker_mean = np.mean(all_perc_committed, axis=0)
            model_length_committed.append(worker_mean)
        model_perf.append(model_length_committed)

        # flat model_length_committed
        model_length_committed = [
            item for sublist in model_length_committed for item in sublist]
    fig, ax = plt.subplots()
    fig.set_size_inches(12.5, 8)
    fontsize = 18
    plt.title(
        "% transactions commited with different # workers, different model lengths, \n constant training time",
        fontdict={'fontsize': fontsize})
    # increase font size of title
    plt.rcParams.update({'font.size': 14})
    plt.xlabel("Number of workers", fontsize=fontsize)
    plt.ylabel("Commit %", fontsize=fontsize)
    plt.xticks(fontsize=fontsize-2)
    plt.yticks(fontsize=fontsize-2)
    plt.xscale("log")
    plt.ylim(-2, 100)
    for i in range(len(model_perf)):
        plt.plot(
            workers_range,
            model_perf[i],
            marker="o",
            label="model length {}k".format(int(model_length_range[i] / 1e3)),
            linewidth=3
        )
    plt.grid(True, which="both", ls="-")
    legend = ax.legend(loc="center left")
    ax.set_facecolor("whitesmoke")
    # increase size of x and y ticks
    plt.xticks(fontsize=fontsize)
    plt.yticks(fontsize=fontsize)
    ax.set_xticks(workers_range)
    ax.set_xticklabels(workers_range)
    # add border to legend
    plt.savefig(
        "/home/user/ml_on_blockchain/results/images/aws/constant_time/all.png")


def plot_max_n_workers_as_model_length():
    model_length_range = [50_000, 100_000, 200_000,
                          300_000, 600_000, 1_000_000, 5_000_000]
    max_n_workers = [64, 32, 16, 8, 4, 4, 0]
    fig, ax = plt.subplots()
    fig.set_size_inches(12.5, 8)
    fontsize = 18
    plt.title(
        "Max number of workers to get at least 90% commited txs",
        # "Max number of workers as a function of model length \n and constant training time",
        fontdict={'fontsize': fontsize})
    plt.ylabel("Number of workers", fontsize=fontsize)
    plt.xlabel("Model # parameters", fontsize=fontsize)
    plt.xscale("log")
    # plt.ylim(-2, 100)
    plt.plot(
        model_length_range,
        max_n_workers,
        marker="o",
        linewidth=3
    )
    plt.grid(True, which="both", ls="-")
    ax.set_facecolor("whitesmoke")
    # increase size of x and y ticks
    plt.xticks(fontsize=fontsize)
    plt.yticks(fontsize=fontsize)
    ax.set_xticks(model_length_range)
    ax.set_xticklabels(
        [str(int(length / 1000)) + "k" for length in model_length_range])
    ax.set_yticks(max_n_workers)
    ax.set_yticklabels(
        [str(worker) for worker in max_n_workers])
    # write the number of workers on the plot on x axis

    # add border to legend
    plt.savefig(
        "/home/user/ml_on_blockchain/results/images/aws/constant_time/max_workers.png")


git inimum index of percentages_committed such that element >= 85
        index = next((i for i, x in enumerate(
            percentages_committed) if x >= 85), None)
        if index is None:
            print("No index found")
        else:
            print("Min pace value to get at least 85% committed txs:",
                  pace_range[index])
    x = workers_range[:-1]
    y = [0.05, 0.1, 0.1, 0.25, 1]
    fig, ax = plt.subplots()
    fig.set_size_inches(12.5, 8)
    fontsize = 18
    plt.title(
        "Redundancy/Pace trade-off to get at least 85% committed transactions",
        fontdict={'fontsize': fontsize})
    # increase font size of title
    plt.rcParams.update({'font.size': 14})
    plt.xlabel("Redundancy", fontsize=fontsize)
    plt.ylabel("Minimum Pace(s)", fontsize=fontsize)
    plt.xticks(fontsize=fontsize-2)
    plt.yticks(fontsize=fontsize-2)
    # plt.xscale("log")
    plt.plot(
        x,
        y,
        marker="o",
        linewidth=3
    )
    plt.grid(True, which="both", ls="-")
    # legend = ax.legend(loc="center left")
    ax.set_facecolor("whitesmoke")
    ax.set_xticks(x)
    ax.set_xticklabels(x)
    ax.set_yticks(y)
    ax.set_yticklabels(y)
    # add border to legend
    plt.savefig(
        "/home/user/ml_on_blockchain/results/images/aws/redundancy_pace.png")


if __name__ == "__main__":
    # plot_max_array_length()
    # plot_varying_perf()
    # plot_varying_perf_constant_time()
    # plot_max_n_workers_as_model_length()
    plot_latency_as_redundancy()
