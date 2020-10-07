import os
import tensorflow as tf
import numpy as np

class DeepQNetwork(object)
    def __init__(self, lr, n_actions, name, input_dims,
                 fc1_dims=256, fc2_dims=256, chkpt_dir='tmp/dqn'):
        #get values from init
        self.lr = lr
        self.n_actions = n_actions
        self.name = name
        self.fc1_dims = fc1_dims
        self.fc2_dims = fc2_dims
        self.chkpt_dir = chkpt_dir
        self.input_dims = input_dims

        #create tf session and parameters
        self.sess = tf.session()
        self.build_network()
        self.sess.run(tf.global_variables_initializer())
        self.saver = tf.train.Saver()
        self.checkpoint_file = os.path.join(chkpt_dir, 'deepqnet.ckpt')

    def build_network(self):
        with tf.variable_scope(self.name):
            #initialize placeholder variables
            self.input = tf.placeholder(tf.float32,
                                        shape=[None, *self.input_dims],
                                        name='inputs')

            self.actions = tf.placeholder(tf.float32,
                                         shape=[None, self.n_actions],
                                         name='actions_taken')

            self.q_target = tf.placeholder(tf.float32,
                                           shape=[None, self.n_actions],
                                           name='q_value')

            flat = tf.layers.flatten()
