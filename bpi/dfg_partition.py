from pm4py.objects.log.importer.xes import importer as xes_importer
from pm4py.algo.discovery.dfg import algorithm as dfg_discovery
from pm4py.visualization.dfg.variants import frequency as dfg_vis_frequency
from pm4py.visualization.dfg import visualizer as dfg_visualization


# Pfad zur XES-Datei
XES_PATH = "BPI_Challenge_2012.xes"  

def filter_dfg_by_activities_and_no_reflexive(dfg, allowed_activities):
    filtered_dfg = {}
    for (act1, act2), count in dfg.items():
        if act1 in allowed_activities and act2 in allowed_activities and act1 != act2:
            filtered_dfg[(act1, act2)] = count
    return filtered_dfg


def filter_log_by_activities(log, allowed_activities):
    filtered_log = []
    for trace in log:
        filtered_trace = [event for event in trace if event["concept:name"] in allowed_activities]
        if filtered_trace:  # Nur Spuren behalten, die Events enthalten
            filtered_log.append(filtered_trace)
    return filtered_log


def main():
    log = xes_importer.apply(XES_PATH)
    dfg = dfg_discovery.apply(log)

    allowed_activities = [
        "A_SUBMITTED", "A_PARTLYSUBMITTED", "A_PREACCEPTED", "W_Completeren aanvraag", "A_ACCEPTED"
    ]

    # Log filtern
    filtered_log = filter_log_by_activities(log, allowed_activities)

    # DFG filtern
    dfg_filtered = filter_dfg_by_activities_and_no_reflexive(dfg, allowed_activities)

    # Visualisieren, aber nur mit dem gefilterten Log
    gviz = dfg_visualization.apply(dfg_filtered, log=filtered_log, variant=dfg_vis_frequency)
    dfg_visualization.view(gviz)


if __name__ == "__main__":
    main()
