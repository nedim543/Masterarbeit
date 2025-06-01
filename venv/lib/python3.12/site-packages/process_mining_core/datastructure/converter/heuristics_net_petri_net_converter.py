import string
from typing import List

from process_mining_core.algorithms.petri_net_creator import PetriNetWrapper
from process_mining_core.datastructure.core.model.heuristics_net import HeuristicsNet
from process_mining_core.datastructure.core.model.petri_net import SerializablePetriNet


class HeuristicsNetPetriNetConverter:

    def _is_concurrent(self, activity, concurrent_activities: List[tuple[string, string]]):
        for concurrent_activity in concurrent_activities:
            if activity == concurrent_activity[0] or activity == concurrent_activity[1]:
                return True
        return False

    def create_petri_net(self, heuristics_result: HeuristicsNet) -> SerializablePetriNet:
        self.petri_net = PetriNetWrapper(name="my-petrinet")
        for activity in heuristics_result.all_activities:
            self.petri_net.add_transition_for_activity(activity)

        for start_activity in heuristics_result.start_activities:
            self.petri_net.add_start_activity(start_activity)

        for end_activity in heuristics_result.end_activities:
            self.petri_net.add_end_activity(end_activity)

        for relation in heuristics_result.relations:
            predecessor = relation[0]
            successor = relation[1]
            if self._is_concurrent(successor, heuristics_result.concurrent_activities):
                self.petri_net.add_concurrent_split(predecessor, successor)
            elif self._is_concurrent(predecessor, heuristics_result.concurrent_activities):
                self.petri_net.add_concurrent_join(predecessor, successor)
            else:
                self.petri_net.add_relation(predecessor, successor)

        return self.petri_net.net