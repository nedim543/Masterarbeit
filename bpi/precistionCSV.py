from pm4py.objects.log.importer.xes import factory as xes_importer
from pm4py.algo.discovery.alpha import factory as alpha_miner
from pm4py.evaluation.fitness import factory as fitness_factory
from pm4py.evaluation.precision import factory as precision_factory

# 1. Log laden
log = xes_importer.apply("path/zur/deiner_datei.xes")

# 2. Prozessmodell (Petri-Netz) entdecken
net, initial_marking, final_marking = alpha_miner.apply(log)

# 3. Fitness berechnen (Token-based Replay)
fitness = fitness_factory.apply(log, net, initial_marking, final_marking)
print("Fitness:", fitness["fitness"])  # meist als dict mit mehreren Metriken

# 4. Precision berechnen
precision = precision_factory.apply(log, net, initial_marking, final_marking)
print("Precision:", precision)
