import pm4py
from pathlib import Path

def _append(title, content):
    path = str(Path(__file__).parents[0]) + "/export/conformance/"
    with open(path + "conformance.txt", "a") as file:
        file.write("\n\n\n" + title + "\n" + content)
        file.close()

if __name__ == "__main__":
    log = pm4py.read_xes(str(Path(__file__).parents[0]) + "/data/BPI_Challenge_2019-3-w-after.xes.gz")
    bpmn_graph = pm4py.read_bpmn(str(Path(__file__).parents[0]) + "/bpmn/BPMN_Celonis.bpmn")

    net, im, fm = pm4py.convert_to_petri_net(bpmn_graph)    

    print("Start fitness_alignments")
    fitness = pm4py.fitness_alignments(log, net, im, fm)
    _append("fitness_alignments", str(fitness))

    print(str(fitness))

    print("Start fitness_token_based_replay:")
    fitness = pm4py.fitness_token_based_replay(log, net, im, fm)
    _append("fitness_token_based_replay", str(fitness))

    print(str(fitness))

    print("Start precision_token_based_replay")
    prec = pm4py.precision_token_based_replay(log, net, im, fm)
    _append("precision_token_based_replay", str(prec))

    print(str(prec))

    print("Start precision_alignments")
    prec = pm4py.precision_alignments(log, net, im, fm)
    _append("precision_alignments", str(prec))

    print(str(prec))




    


