from constructs import Construct

class ComputeConstruct(Construct):
    def __init__(self, scope: Construct, construct_id: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)