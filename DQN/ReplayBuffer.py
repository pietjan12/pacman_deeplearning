import numpy as np


# class responsible for allowing the model to store "memories" so it can learn from past events.
class ReplayBuffer:
    def __init__(self, mem_size, input_dims):
        self.mem_size = mem_size
        # keeps track of first unsaved memory.
        self.mem_cntr = 0

        # keeps track of the states the agent sees
        self.state_memory = np.zeros((self.mem_size, *input_dims),
                                     dtype=np.float32)
        # memory for state transition
        self.new_state_memory = np.zeros((self.mem_size, *input_dims),
                                         dtype=np.float32)
        # memory for actions
        self.action_memory = np.zeros(self.mem_size, dtype=np.int32)
        # memory for episode rewards
        self.reward_memory = np.zeros(self.mem_size, dtype=np.float32)

        self.terminal_memory = np.zeros(self.mem_size, dtype=np.int32)

    def store_transition(self, state, action, reward, new_state, done):
        index = self.mem_cntr % self.mem_size
        self.state_memory[index] = state;
        self.new_state_memory[index] = new_state;
        self.reward_memory[index] = reward;
        self.action_memory[index] = action;
        self.terminal_memory[index] = 1 - int(done)
        self.mem_cntr += 1

    def sample_memory_buffer(self, batch_size):
        max_mem = min(self.mem_cntr, self.mem_size)
        batch = np.random.choice(max_mem, batch_size, replace=True)

        states = self.state_memory[batch]
        new_states = self.new_state_memory[batch];
        rewards = self.reward_memory[batch];
        actions = self.action_memory[batch];
        terminal = self.terminal_memory[batch];

        return states, actions, rewards, new_states, terminal
