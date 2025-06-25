from pm4py.objects.log.importer.xes import importer as xes_importer
from pm4py.algo.discovery.alpha import algorithm as alpha_miner
from pm4py.algo.discovery.inductive import algorithm as inductive_miner
from pm4py.algo.discovery.heuristics import algorithm as heuristics_miner
from pm4py.algo.evaluation.precision import algorithm as precision_evaluator
from pm4py.algo.evaluation.replay_fitness import algorithm as fitness_evaluator
from pm4py.algo.conformance.tokenreplay import algorithm as token_replay
from pm4py.objects.conversion.process_tree import converter as pt_converter
from pm4py.objects.conversion.heuristics_net import converter as hn_converter

#Diese File berechnet Fitnes und precistion 

# 1. Log importieren
test_log = xes_importer.apply("bpi_all.xes")

# 2. Logs zur Modell-Erstellung (reduziert oder vollständig)
training_logs = [
    ("bpi_all.xes", "Modell aus Normalzustand"),
    ("bpi_ohne_A_Finalized.xes", "Modell ohne A_finalized"),
    #("bpi_ohne_W_Valideren.xes", "Modell ohne W_Valideren"),
    ("bpi_ohne_W_Completer.xes", "Modell ohne W_Completer"),
]

# Funktion zur Berechnung und Ausgabe von Fitness & Precision
def evaluate_model(miner_name, net, im, fm):
    print(f"\n--- {miner_name} ---")
    
    # Fitness berechnen
    fitness = fitness_evaluator.apply(test_log, net, im, fm)
    
    # Precision berechnen
    precision = precision_evaluator.apply(test_log, net, im, fm)
    
    # Ausgabe
    print(f"Log-Fitness (gesamt): {fitness['log_fitness']:.4f}  # Gesamtübereinstimmung Modell ↔ Log")
    print(f"Average Trace Fitness: {fitness['average_trace_fitness']:.4f}  # Ø-Fitness über alle Traces")
    print(f"Fitting Traces (%): {fitness['percentage_of_fitting_traces'] * 100:.2f}%  # Anteil perfekt passender Traces")
    print(f"Precision: {precision:.4f}  # Modell-Spezifität (wenig unnötiges Verhalten)")


# 3. Miner definieren
miners = {
    #"Alpha Miner": lambda log: alpha_miner.apply(log),
    "Heuristics Miner": lambda log: hn_converter.apply(
        heuristics_miner.apply_heu(log, parameters={"dependency_thresh": 0.99})
    )
    
}

# 4. Evaluation aller Kombinationen
for log_path, description in training_logs:
    print(f"\n\n=== Training mit: {description} ===")
    train_log = xes_importer.apply(log_path)
    
    for miner_name, miner_func in miners.items():
        try:
            net, im, fm = miner_func(train_log)
            evaluate_model(miner_name, net, im, fm)
        except Exception as e:
            print(f"\n--- {miner_name} ---")
            print(f"❌ Fehler beim Modellieren oder Bewerten: {e}")


# 2. Prozessmodell entdecken (Petri-Netz) mit Alpha-Miner
#net, im, fm = alpha_miner.apply(log)
#evaluate_model("Alpha Miner", net, im, fm)


# 2. Prozessmodell entdecken mit Inductive Miner
#tree = inductive_miner.apply(log)

#from pm4py.objects.conversion.process_tree import converter as pt_converter
#net_ind, im_ind, fm_ind = pt_converter.apply(tree, variant=pt_converter.Variants.TO_PETRI_NET)

#evaluate_model("Inductive Miner", net_ind, im_ind, fm_ind)



# 2. Prozessmodell entdecken mit Heuristics Miner
#net_heu, im_heu, fm_heu = heuristics_miner.apply(log)
#evaluate_model("Heuristics Miner", net_heu, im_heu, fm_heu)


# 3. Fitness berechnen (alte variante)
#fitness_result = token_replay.apply(log, net, im, fm)
#average_fitness = sum([x["trace_fitness"] for x in fitness_result]) / len(fitness_result)
