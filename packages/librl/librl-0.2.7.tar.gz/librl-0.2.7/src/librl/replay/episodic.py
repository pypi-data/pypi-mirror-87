
import torch
import numpy as np

import librl.utils

# Enapsulate all replay memory of a single task
# TODO: Allow data to be moved to GPU, and make device required.
class BaseEpisode:
    def __init__(self, obs_space, act_space, episode_length=200, device='cpu', enable_extra = False):
        self.state_buffer =  []
        self.action_buffer = []
        self.logprob_buffer = torch.zeros([episode_length], dtype=torch.float32).to(device) # type: ignore
        self.reward_buffer = torch.zeros([episode_length], dtype=torch.float32).to(device) # type: ignore
        self.policy_buffer = np.full([episode_length], None, dtype=object)
        self.done =  None
        self.enable_extra = enable_extra
        self.extra = {}

    def log_state(self, t, state):
        self.state_buffer[t] = state
    def log_action(self, t, action, logprob):
        self.action_buffer[t] = action
        self.logprob_buffer[t] = logprob
    def log_rewards(self, t, reward):
        assert reward.device == self.reward_buffer.device
        self.reward_buffer[t] = reward
    def log_policy(self, t, policy):
        self.policy_buffer[t]= policy
    def log_done(self, t):
        self.done = t
    def log_extra_info(self, t, info_dict):
        if not self.enable_extra: return
        assert isinstance(info_dict, dict)

        if t in self.extra: self.extra[t].update(info_dict)
        else: self.extra[t] = info_dict

    def clear_replay(self):
        map(lambda x: x.fill_(0).detach_(), [self.logprob_buffer, self.reward_buffer])
        self.policy_buffer.fill(None)
        self.done = None
        self.extra = {}

# Episode where action, state are torch contiguous and simple.
# Therefore, they are torch tensors.
class BoxEpisode(BaseEpisode):
    def __init__(self, obs_space, act_space, episode_length=200, device='cpu', enable_extra = False):
        super(BoxEpisode, self).__init__(obs_space, act_space, episode_length=episode_length,
            device=device, enable_extra=enable_extra)
        self.state_buffer = torch.zeros([episode_length, *obs_space.shape], dtype=librl.utils.convert_np_torch(obs_space.dtype)).to(device) # type: ignore
        self.action_buffer = torch.zeros([episode_length, *act_space.shape], dtype=librl.utils.convert_np_torch(act_space.dtype)).to(device) # type: ignore
    def log_state(self, t, state):
        assert state.device == self.state_buffer.device
        self.state_buffer[t] = state    
    def log_action(self, t, action, logprob):
        assert action.device == self.action_buffer.device
        self.action_buffer[t] = action
        self.logprob_buffer[t] = logprob
    def clear_replay(self):
        super(BoxEpisode, self).clear_replay()
        map(lambda x: x.fill_(0).detach_(), [self.state_buffer, self.action_buffer])
        

# Episode where action, state are cartesian products of tensors
# Therfore, we must store these elements in lists rather than tensor.
class ProductEpisode(BaseEpisode):
    def __init__(self, obs_space, act_space, episode_length=200, device='cpu', enable_extra = False):
        super(ProductEpisode, self).__init__(obs_space, act_space, episode_length=episode_length, 
            device=device, enable_extra=enable_extra)
        self.state_buffer = np.full([episode_length], None, dtype=object)# type: ignore
        self.action_buffer = np.full([episode_length], None, dtype=object)# type: ignore
    def clear_replay(self):
        super(ProductEpisode, self).clear_replay()
        map(lambda x: x.fill(0), [self.state_buffer, self.action_buffer])