import sys
from collections import defaultdict

class State:
    def __init__(self, ):
        self.value_state = defaultdict(list) # dict.fromkeys([i for i in range(num_joints)])
        self.idx_state = []

    def append(self, idx, cur):
        self.value_state[idx].append(cur)
        self.idx_state.append(idx)
        return cur
    
    def pop(self):
        idx = self.idx_state.pop()
        value = self.value_state[idx].pop()
        return idx, value
