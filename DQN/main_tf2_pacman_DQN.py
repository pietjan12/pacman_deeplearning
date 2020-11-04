import tensorflow as tf
import numpy as np
import gym
from Agent import Agent
from utils import plotLearning


# Helpful preprocessing taken from github.com/ageron/tiny-dqn
def process_frame(frame):
    mspacman_color = np.array([210, 164, 74]).mean()
    img = frame[1:176:2, ::2]  # Crop and downsize
    img = img.mean(axis=2)  # Convert to greyscale
    img[img == mspacman_color] = 0  # Improve contrast by making pacman white
    img = (img - 128) / 128 - 1  # Normalize from -1 to 1.

    return np.expand_dims(img.reshape(88, 80, 1), axis=0)


if __name__ == '__main__':
    tf.compat.v1.disable_eager_execution()
    env = gym.make('MsPacman-v0')
    resized_input_dims = (88, 80, 1)
    lr = 0.001
    n_games = 25
    agent = Agent(gamma=0.99, epsilon=1.0, lr=lr, input_dims=resized_input_dims,
                  n_actions=env.action_space.n, mem_size=10, batch_size=64,
                  epsilon_end=0.01)

    scores = []
    eps_history = []

    for i in range(n_games):
        done = False
        score = 0
        observation = process_frame(env.reset())
        while not done:
            action = agent.choose_action(observation)
            new_observation, reward, done, info = env.step(action)
            score += reward
            new_observation = process_frame(new_observation)
            agent.store_transition(observation, action, reward, new_observation, done)
            observation = new_observation
            agent.learn()
        eps_history.append(agent.epsilon)
        scores.append(score)

        avg_score = np.mean(scores[-100:])
        print('episode: ', i, 'score %.2f' % score,
              'average_score %.2f' % avg_score,
              'epsilon %.2f' % agent.epsilon)

    filename = 'pacman_tf2.png'
    x = [i + 1 for i in range(n_games)]
    plotLearning(x, scores, eps_history, filename)
