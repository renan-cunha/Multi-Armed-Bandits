from typing import List, Callable, Tuple
from src.arm import Arm
from src.testbed import Testbed
import random
import numpy as np
from copy import deepcopy


class Bandit:

    def __init__(self, testbed: Testbed):
        self.testbed = testbed
    
    def run(self, num_steps: int, epsilon: float, 
            step_size_function: Callable, 
            random_walk_stddev: float) -> np.ndarray:
        """Returns an array with rewards per step"""
        
        testbed = deepcopy(self.testbed)
        num_actions = testbed.get_num_actions()
        rewards = np.zeros(num_steps, dtype=float)

        self.action_estimates = np.zeros(num_actions, dtype=float)
        for step in range(num_steps):
            
            step_size = step_size_function(step)

            action = self.action_policy()
            reward = testbed.act(action)
            rewards[step] = reward
            self.update_action_estimate(action, reward, step_size)
            testbed.random_walk(0, random_walk_stddev)
        return rewards

    def action_policy(self, epsilon: float) -> int:
        coin = random.uniform(0, 1)
        if coin > epsilon:
            action = np.argmax(self.action_estimates)
        else:
            action = self.testbed.random_action()
        return action

    def update_action_estimate(self, action: int, reward: float, 
                               step_size: float) -> None:
        action_estimate = self.action_estimates[action]
        action_estimate += step_size*(reward-action_estimate)
        self.action_estimates[action] = action_estimate
