#!/usr/bin/env python3

import random
import gym


class RewardScalerWrapper(gym.RewardWrapper):

    def __init__(self, env, scaling=1.0):
        self.scaling = scaling
        super(RewardScalerWrapper, self).__init__(env)

    def reward(self, reward):
        return self.scaling * reward


class RewardScalerFactory(object):

    def __init__(self, min_range=-1, max_range=1.0):
        self.min_range = min_range
        self.max_range = max_range

    def __call__(self, env):
        scaling = random.uniform(self.min_range, self.max_range)
        return RewardScalerWrapper(env, scaling=scaling)
