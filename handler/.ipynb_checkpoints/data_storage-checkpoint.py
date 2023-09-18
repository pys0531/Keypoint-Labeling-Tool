from collections import defaultdict
from state import State

class shoes_data(State):
    def __init__(self, num_joints):
        super(shoes_data, self).__init__()
        self.value = {i: [None, None, None] for i in range(num_joints)}
        self.vis = 1
        self.circle = defaultdict(list)
        self.line_color = defaultdict(list)
