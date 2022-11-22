import pm4py
from pathlib import Path


def _append(title, content):
    path = str(Path(__file__).parents[0]) + "/export/conformance/"
    with open(path + "conformance.txt", "a") as file:
        file.write("\n\n\n" + title + "\n" + content)
        file.close()


if __name__ == "__main__":
    log = pm4py.read_xes(
        str(Path(__file__).parents[0]) + "/data/BPI_Challenge_2019-3-w-after.xes.gz"
    )
    bpmn_graph = pm4py.read_bpmn(
        str(Path(__file__).parents[0]) + "/bpmn/BPMN_Celonis_as-is_final.bpmn"
    )

    net, im, fm = pm4py.convert_to_petri_net(bpmn_graph)

    print("Start token_based_replay")

    missing_tokens = 0
    consumed_tokens = 0
    remaining_tokens = 0
    produced_tokens = 0

    replayed_traces = pm4py.conformance_diagnostics_token_based_replay(log, net, im, fm)
    for trace in replayed_traces:
        missing_tokens += trace["missing_tokens"]
        consumed_tokens += trace["consumed_tokens"]
        remaining_tokens += trace["remaining_tokens"]
        produced_tokens += trace["produced_tokens"]

    first_eq = 0.5 * (1 - float(missing_tokens) / float(consumed_tokens))
    second_eq = 0.5 * (1 - float(remaining_tokens) / float(produced_tokens))

    fitness = first_eq + second_eq

    print(
        "token_based_replay"
        + str(
            (
                fitness,
                missing_tokens,
                consumed_tokens,
                remaining_tokens,
                produced_tokens,
            )
        )
    )
    _append(
        "token_based_replay",
        str(
            (
                fitness,
                missing_tokens,
                consumed_tokens,
                remaining_tokens,
                produced_tokens,
            )
        ),
    )

    print("Start alignment-based")
    from pm4py.algo.conformance.alignments.petri_net import algorithm as alignments

    aligned_traces = alignments.apply_log(log, net, im, fm)

    from pm4py.algo.evaluation.replay_fitness import algorithm as replay_fitness

    log_fitness = replay_fitness.evaluate(
        aligned_traces, variant=replay_fitness.Variants.ALIGNMENT_BASED
    )

    print("alignment-based" + str(log_fitness))
    _append("alignment-based", str(log_fitness))

#%%
