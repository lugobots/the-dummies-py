import sys

import numpy as np
from gym import spaces, Env

from lugo4py.rl import TrainingController

class StubEnv(Env):

    def __init__(self, training_ctrl: TrainingController):
        super().__init__()
        self.training_ctrl = training_ctrl

        # Observation: flattened 7x7 binary matrix (0 or 1) + 1
        self.observation_space = spaces.Box(low=0.0, high=1.0, shape=(50,), dtype=np.float32)
        # Action space: 8 discrete actions
        self.action_space = spaces.Discrete(8)
        self.state = None
        self.steps = 0
        self.max_steps = 50

    def reset(self):
        self.training_ctrl.set_environment([])
        self.state = self.training_ctrl.get_state()
        # print(self.state)
        return self.state

    def step(self, action):
        reward, done = self.training_ctrl.update(action)
        self.state = self.training_ctrl.get_state()
        info = {}

        reward = float(np.clip(reward, -10, 10))
        # print(f"reward: {reward}")
        if not np.isfinite(reward):
            reward = 0.0
        return self.state, reward, done, info

    def render(self, mode='human'):
        print(self.training_ctrl.get_state())
