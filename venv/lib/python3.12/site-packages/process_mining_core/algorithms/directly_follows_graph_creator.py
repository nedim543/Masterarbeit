from process_mining_core.algorithms.lossy_counting.case_id_dictionary import CaseIdDictionary
from process_mining_core.datastructure.core.event import Event
from process_mining_core.algorithms.lossy_counting.lossy_counting_dictionary import LossyCountingDictionary
from process_mining_core.datastructure.core.model.directly_follows_graph import DirectlyFollowsGraph

class DirectlyFollowsGraphCreator:

    def __init__(self, sample_size, batch_size):
        self.activities = LossyCountingDictionary()
        self.relations = LossyCountingDictionary()
        self.cases = CaseIdDictionary()
        self.sample_size = sample_size
        self.batch_size = batch_size
        self.processedEvents = 0
        self.current_bucket = 1

    def process(self, event: Event) -> DirectlyFollowsGraph | None:
        self.processedEvents += 1
        case_id = event.caseid
        activity = event.activity
        sample_size = self.sample_size
        self.current_bucket = int(self.processedEvents / sample_size)

        self.activities.insert(activity, self.current_bucket)
        relation = self.cases.insert(case_id, activity)

        if relation is not None:
            self.relations.insert(relation, self.current_bucket)

        if self.processedEvents % sample_size == 0:
            self.activities.clean_up(self.current_bucket)
            self.relations.clean_up(self.current_bucket)

        if self.processedEvents % self.batch_size == 0:
            return DirectlyFollowsGraph(
                counted_relations=self.relations.get_counted(),
                start_activities=self.cases.get_start_activities(self.current_bucket),
                end_activities=self.cases.get_end_activities(self.current_bucket)
            )
        return None