class Event:
    def __init__(self, timestamp, activity, case_id, node, group_id):
        self.timestamp = timestamp
        self.activity: any = activity
        self.caseid: str = case_id
        self.node: str = node
        self.group: str = group_id

    def get_case(self):
        return self.caseid

    def get_activity(self):
        return self.activity

    def get_timestamp(self):
        return self.timestamp

    def __str__(self):
        return str(self.__dict__)