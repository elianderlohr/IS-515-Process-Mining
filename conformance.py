import pm4py
from pathlib import Path
from pm4py.algo.conformance.alignments.petri_net import algorithm as alignments
from pm4py.algo.evaluation.replay_fitness import algorithm as replay_fitness

def _append(title, content):
    path = str(Path(__file__).parents[0]) + "/export/conformance/"
    with open(path + "conformance.txt", "a") as file:
        file.write("\n\n\n" + title + "\n" + content)
        file.close()


if __name__ == "__main__":
    log = pm4py.read_xes(
        str(Path(__file__).parents[0]) + "/data/BPI_Challenge_2019-3-w-after.xes.gz"
    )

    pn_name = "pn003_adj_80"

    net, im, fm = pm4py.read_pnml(str(Path(__file__).parents[0]) + "/pn/" + pn_name + ".pnml")

    print("Start alignments based:")

    aligned_traces = alignments.apply_log(log, net, im, fm)

    alignment_fitness = replay_fitness.evaluate(aligned_traces, variant=replay_fitness.Variants.ALIGNMENT_BASED)

    print(alignment_fitness)

    print(
        "alignment_fitness"
        + str(alignment_fitness
        )
    )
    _append(
        "alignment_fitness",
        str(alignment_fitness
        ),
    )

#%%
