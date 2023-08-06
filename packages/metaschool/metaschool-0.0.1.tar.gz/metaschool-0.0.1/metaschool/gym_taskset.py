#!/usr/bin/env python3


class GymTaskset(object):
    """docstring for GymTaskset"""

    def __init__(
        self,
        env,
        action_wrapper_factory=None,
        state_wrapper_factory=None,
        reward_wrapper_factory=None,
    ):
        super(GymTaskset, self).__init__()
        self.env = env
        self.action_wrapper_factory = action_wrapper_factory
        self.state_wrapper_factory = state_wrapper_factory
        self.reward_wrapper_factory = reward_wrapper_factory

    def sample(self):
        env = self.env
        if self.action_wrapper_factory is not None:
            env = self.action_wrapper_factory(env)
        if self.state_wrapper_factory is not None:
            env = self.state_wrapper_factory(env)
        if self.reward_wrapper_factory is not None:
            env = self.reward_wrapper_factory(env)
        return env
