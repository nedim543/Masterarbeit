from pm4py.objects.log.importer.xes import importer as xes_importer
from pm4py.algo.discovery.dfg import algorithm as dfg_discovery
from pm4py.visualization.dfg.variants import frequency as dfg_vis_frequency
from pm4py.visualization.dfg import visualizer as dfg_visualization

XES_PATH = "BPI_Challenge_2012.xes"  

def main():
    log = xes_importer.apply(XES_PATH)
    dfg = dfg_discovery.apply(log)

    THRESHOLD = 500
    # Filter Kanten nach Schwellenwert
    dfg_filtered = {k: v for k, v in dfg.items() if v >= THRESHOLD}

    # Reflexive Kanten entfernen
    dfg_filtered = {k: v for k, v in dfg_filtered.items() if k[0] != k[1]}

    # Visualisieren
    gviz = dfg_visualization.apply(dfg_filtered, log=log, variant=dfg_vis_frequency)
    dfg_visualization.view(gviz)

    dfg_visualization.save(gviz, "dfg_from_xes.png")
    print("Graph gespeichert unter: dfg_from_xes.png")

if __name__ == "__main__":
    main()
