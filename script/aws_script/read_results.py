import json
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import make_interp_spline
import plotly.express as px


# waiting_times = []
# percentages_committed = []
# n_txs = []
# scenario = "10k_model"
# # workers = [10 * pow(10, i) for i in range(4)]
# # workers = [10 * pow(2, i) for i in range(16)]
# model_lengths = [10_000, 100_000, 1_600_000]

# i = 0
# # for n_workers in workers:
# for model_length in model_lengths:
#     i += 1
#     # print("n_workers:", n_workers)
#     # with open("res/{}/{}_workers.txt".format(scenario, n_workers)) as json_file:
#     with open("res/{}/100_workers_70_redundancy_{}_model_length.txt".format(scenario, model_length)) as json_file:
#         data = json.load(json_file)
#         tx_submitted = 0
#         tx_committed = 0
#         tot_commit_time = 0
#         for tx in data["Locations"][0]["Clients"][0]["Interactions"]:
#             submit_time = tx["SubmitTime"]
#             commit_time = tx["CommitTime"]
#             tx_submitted += 1
#             if commit_time != -1:
#                 tx_committed += 1
#                 tot_commit_time += commit_time - submit_time
#         perc_committed = tx_committed / tx_submitted * 100
#         avg_commit_time = tot_commit_time / tx_committed if tx_committed != 0 else 0
#         print("tx_submitted:", tx_submitted)
#         print("tx_committed:", tx_committed)
#         print("avg_commit_time", avg_commit_time)
#         print("perc_committed:", perc_committed)
#         waiting_times.append(avg_commit_time)
#         percentages_committed.append(perc_committed)
#         # if tx_commited is bigger than 1000, replace thsousands with k
#         if tx_committed > 1000:
#             n_txs.append("{}k txs".format(tx_committed // 1000))
#         else:
#             n_txs.append("{} txs".format(tx_committed))

# print("i:", i)
# fig, axs = plt.subplots(2, 1, figsize=(15, 7.5))
# # add vertical padding
# fig.subplots_adjust(hspace=0.5)

# axs[0].set_title("Average waiting time")
# axs[1].set_title("Percentage committed")
# fig.suptitle("Results")

# #axs[0].plot(workers, waiting_times, linestyle="dashed", marker="o")
# axs[0].plot(model_lengths, waiting_times, linestyle="dashed", marker="o")
# axs[0].set_xlabel("Number of model_lengths")
# axs[0].set_ylabel("Average waiting time (s)")
# axs[1].plot(
#     # workers,
#     model_lengths,
#     percentages_committed,
#     linestyle="dashed",
#     marker="o",
# )
# #axs[1].set_xlabel("Number of workers")
# axs[1].set_xlabel("Number of model_lengths")
# axs[1].set_ylabel("Percentage committed")
# for i, ax in enumerate(axs):
#     ax.grid(True)
#     ax.set_xscale("log")
#     for x, y, label in zip(
#         # workers,
#         model_lengths,
#         waiting_times if i == 0 else percentages_committed,
#         n_txs,
#     ):
#         ax.text(x, y, label, ha="center", va="bottom", fontsize=12, color="b")
# # save figure
# plt.savefig("res/{}/results.png".format(scenario))
# plt.show()


def plot_model_length_perf():
    all_perc_committed = []
    for i in range(10):
        waiting_times = []
        percentages_committed = []
        n_txs = []
        # model_length_range = np.arange(1000, 51000, 1000)
        model_length_range = np.arange(1000, 51000, 1000)
        for model_length in model_length_range:
            with open("/home/user/ml_on_blockchain/results/max_model_size_{}/{}.txt".format(i, model_length)) as json_file:
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
                # print("tx_submitted:", tx_submitted)
                # print("tx_committed:", tx_committed)
                # print("avg_commit_time", avg_commit_time)
                # print("i:", i, "model_length:", model_length,
                #       "perc_committed:", perc_committed)
                if (perc_committed == 0):
                    print("model_length:", model_length, "i:", i)
                # print("perc_committed:", perc_committed)
                waiting_times.append(avg_commit_time)
                percentages_committed.append(perc_committed)
        # print("percentage commited:", percentages_committed)
        all_perc_committed.append(percentages_committed)
        # print("all_perc_committed:", all_perc_committed)

    mean_commited = np.mean(all_perc_committed, axis=0)
    # print("mean:", mean_commited)
    # TODO check if this is correct
    # fig = plt.figure(figsize=(15, 7.5))
    fig = plt.figure()
    plt.title("Percentage of committed transactions for different model lengths")
    plt.xlabel("Model number of parameters (uint256)")
    plt.ylabel("Commit %")
    plt.plot(
        # workers,
        model_length_range,
        mean_commited,
        linestyle="dashed",
        marker="o",
        label="mean over 10 runs",
    )
    smoothed = make_interp_spline(model_length_range, mean_commited)
    X = np.linspace(model_length_range.min(),
                    model_length_range.max(), 1000)
    commited_smoothed = smoothed(X)
    plt.plot(X, commited_smoothed, label="smoothed")
    plt.grid(True)
    # add legend
    plt.legend()

    # save figure
    plt.savefig(
        "/home/user/ml_on_blockchain/results/images/max_model_length.png")


def plot_varying_perf():
    # model_length_range = [50_000, 300_000, 600_000, 1_000_000]
    model_length_range = [50_000, 300_000]
    # workers_range = [5*2**i for i in range(10)]
    # workers_range = [5*2**i for i in range(9)]
    # workers_range = [5*2**i for i in range(8)]
    workers_range = [2**i for i in range(10)]
    print("workers_range:", workers_range)
    n_runs = 2
    for model_length in model_length_range:
        model_length_committed = []
        for n_worker in workers_range:
            all_perc_committed = []
            for run_nb in np.arange(1, n_runs + 1):
                waiting_times = []
                percentages_committed = []
                path = "/home/user/ml_on_blockchain/results/varying_workers/model_length_{}/run_{}/{}.txt".format(
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
        # fig = plt.figure()
        # plt.title(
        #     "% commited txs by varying number of workers for model length {}".format(model_length))
        # plt.xlabel("Number of workers")
        # plt.ylabel("Commit %")
        # plt.plot(
        #     workers_range,
        #     model_length_committed,
        #     linestyle="dashed",
        #     marker="o",
        #     label="mean over xx runs",
        # )
        # plt.ylim(-2, 100)
        # plt.xscale("log")

        print(len(workers_range), len(model_length_committed))
        print("workers_range:", workers_range)
        print("model_length_committed:", model_length_committed)
        # flat model_length_committed
        model_length_committed = [
            item for sublist in model_length_committed for item in sublist]
        print("model_length_committed:", model_length_committed)
        img_path = "/home/user/ml_on_blockchain/results/images/varying_worker/{}_model_length_plotly".format(
            model_length)
        fig = px.line(x=workers_range, y=model_length_committed, log_x=True, title="% commited txs by varying number of workers for model length {}".format(
            model_length), labels={'x': "Number of workers", 'y': "Commit %"})
        fig.update_traces(
            mode="lines+markers", hovertemplate="Number of Workers: %{x}<br>Commit %: %{y}", name="xxx")
        fig.update_layout(yaxis=dict(
            range=[-2, 100], autorange=False), legend=dict(title="Legend", font=dict(size=14)), showlegend=True)

        fig.write_image(
            "/home/user/ml_on_blockchain/results/images/varying_worker/{}_model_length_plotly.png".format(model_length))

        # save figure
        # print("saving path:", "/home/user/ml_on_blockchain/results/images/varying_worker/{}_model_length.png".format(model_length))
        # plt.savefig(
        #     "/home/user/ml_on_blockchain/results/images/varying_worker/{}_model_length.png".format(model_length))


def plot_varying_perf_constant_time():
    # model_length_range = [50_000, 300_000, 600_000, 1_000_000]
    model_length_range = [50_000, 100_000, 300_000, 600_000, 1_000_000]
    # workers_range = [2**i for i in range(10)]
    workers_range = [2**(i+1) for i in range(9)]
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
                path = "/home/user/ml_on_blockchain/results/varying_workers/constant_time/model_length_{}/run_{}/{}.txt".format(
                    model_length, run_nb, n_worker)
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
                    percentages_committed.append(perc_committed)  # for 1 truc
                all_perc_committed.append(percentages_committed)
            # we finished all runs for this worker number, so compute the mean and append it inside model_length_committed
            worker_mean = np.mean(all_perc_committed, axis=0)
            model_length_committed.append(worker_mean)
            # print("model_length_committed:", model_length_committed)
        print("final model_length_committed:", model_length_committed)
        # fig = plt.figure()
        # plt.title(
        #     "% commited txs by varying number of workers for model length {}".format(model_length))
        # plt.xlabel("Number of workers")
        # plt.ylabel("Commit %")
        # plt.plot(
        #     workers_range,
        #     model_length_committed,
        #     linestyle="dashed",
        #     marker="o",
        #     label="mean over xx runs",
        # )
        # plt.ylim(-2, 100)
        # plt.xscale("log")

        print(len(workers_range), len(model_length_committed))
        print("workers_range:", workers_range)
        print("model_length_committed:", model_length_committed)
        # flat model_length_committed
        model_length_committed = [
            item for sublist in model_length_committed for item in sublist]
        print("model_length_committed:", model_length_committed)
        img_path = "/home/user/ml_on_blockchain/results/images/varying_worker/constant_time/{}_model_length_plotly".format(
            model_length)
        fig = px.line(x=workers_range, y=model_length_committed, log_x=True, title="% commited txs by varying number of workers for model length {}".format(
            model_length), labels={'x': "Number of workers", 'y': "Commit %"})
        fig.update_traces(
            mode="lines+markers", hovertemplate="Number of Workers: %{x}<br>Commit %: %{y}", name="xxx")
        fig.update_layout(yaxis=dict(
            range=[-2, 100], autorange=False), legend=dict(title="Legend", font=dict(size=14)), showlegend=True)

        fig.write_image(
            "/home/user/ml_on_blockchain/results/images/varying_worker/constant_time/{}_model_length.png".format(model_length))

        # save figure
        # print("saving path:", "/home/user/ml_on_blockchain/results/images/varying_worker/{}_model_length.png".format(model_length))
        # plt.savefig(
        #     "/home/user/ml_on_blockchain/results/images/varying_worker/{}_model_length.png".format(model_length))


if __name__ == "__main__":
    # plot_model_length_perf()
    # plot_varying_perf()
    plot_varying_perf_constant_time()
