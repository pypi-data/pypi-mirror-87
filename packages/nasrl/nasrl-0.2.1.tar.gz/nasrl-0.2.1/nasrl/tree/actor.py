import functools

import more_itertools
import torch
import torch.nn as nn
import torch.distributions, torch.nn.init
import torch.optim

from .policy import CNNDecisionTree, FullDecisionTree, MLPDecisionTree, TreePolicy

# Actor that generates weightings for nasrl.tree.MLPDecisionTree
class MLPTreeActor(nn.Module):
    def __init__(self, neural_module,  observation_space, output_dimension=(10,)):
        super(MLPTreeActor, self).__init__()
        self.observation_space = observation_space
        self.decision_tree = MLPDecisionTree()

        self.input_dimension = list(more_itertools.always_iterable(neural_module.output_dimension))
        self.__input_size = functools.reduce(lambda x,y: x*y, self.input_dimension, 1)
        self.neural_module = neural_module
        self.output_dimension = output_dimension
        self.__output_size = functools.reduce(lambda x,y: x*y, self.output_dimension, 1)
        self.__output_size = torch.tensor(self.__output_size, requires_grad=True, dtype=torch.float)

        # Our output layers are used as the seed for some set of random number generators.
        # These random number generators are used to generate edge pairs.
        self.layer_size = nn.Linear(self.__input_size, 1)
        self.w_mlp_del = nn.Linear(self.__input_size, 1)
        self.w_mlp_add = nn.Linear(self.__input_size, 1)

        # Initialize NN
        for x in self.parameters():
            if x.dim() > 1:
                nn.init.kaiming_normal_(x)

    def recurrent(self):
        return self.neural_module.recurrent()
        
    def save_hidden(self):
        assert self.recurrent()
        return self.neural_module.save_hidden()

    def restore_hidden(self, state=None):
        assert self.recurrent()
        self.neural_module.restore_hidden(state)
    def get_policy_weights(self, input):
        output = self.neural_module(input).view(-1, self.__input_size)

        # TODO: Figure out how to make inputs/outputs sane sizes.
        weight_dict = {}
        w_mlp_del, w_mlp_add = self.w_mlp_del(output), self.w_mlp_add(output)
        weight_dict['mlp_count'] = self.__output_size
        weight_dict['w_mlp_del'] = w_mlp_del
        weight_dict['w_mlp_add'] = w_mlp_add
        # TODO: Make min/max number of neurons a parameter of the NN.
        # Probably pull from observation space.
        base = 25
        max = torch.clamp((self.layer_size(output)+1)**2 + base, 0, 400)
        weight_dict['mlp_size_dist'] = torch.distributions.Uniform(base, max)

        return weight_dict

    def forward(self, input):
        weight_dict = self.get_policy_weights(input)
        # Encapsulate our poliy in an object so downstream classes don't
        # need to know what kind of distribution to re-create.
        policy = TreePolicy(self.decision_tree, weight_dict)

        actions = policy.sample(1)
        # Each actions is drawn independtly of others, so joint prob
        # is all of them multiplied together. However, since we have logprobs,
        # we need to sum instead.
        log_prob = sum(policy.log_prob(actions)) # type: ignore

        return actions, log_prob, policy

# Actor that generates weightings for nasrl.tree.CNNDecisionTree
class CNNTreeActor(nn.Module):
    def __init__(self, neural_module,  observation_space, output_dimension=(10,)):
        super(CNNTreeActor, self).__init__()
        self.observation_space = observation_space
        self.decision_tree = CNNDecisionTree()

        self.input_dimension = list(more_itertools.always_iterable(neural_module.output_dimension))
        self.__input_size = functools.reduce(lambda x,y: x*y, self.input_dimension, 1)
        self.neural_module = neural_module
        self.output_dimension = output_dimension
        self.__output_size = functools.reduce(lambda x,y: x*y, self.output_dimension, 1)
        self.__output_size = torch.tensor(self.__output_size, requires_grad=True, dtype=torch.float)

        # Our output layers are used as the seed for some set of random number generators.
        # These random number generators are used to generate edge pairs.
        self.w_conv_del = nn.Linear(self.__input_size, 1)
        self.w_conv_add = nn.Linear(self.__input_size, 1)
        self.w_conv_add_conv = nn.Linear(self.__input_size, 1)
        self.w_conv_add_max = nn.Linear(self.__input_size, 1)
        self.w_conv_add_avg = nn.Linear(self.__input_size, 1)
        self.kernel_dist_layer = nn.Linear(self.__input_size, 1)
        self.channel_dist_layer = nn.Linear(self.__input_size, 1)
        self.stride_dist_layer = nn.Linear(self.__input_size, 1)
        self.padding_dist_layer = nn.Linear(self.__input_size, 1)
        self.dilation_dist_layer = nn.Linear(self.__input_size, 1)

        # Initialize NN
        for x in self.parameters():
            if x.dim() > 1:
                nn.init.kaiming_normal_(x)

    def recurrent(self):
        return self.neural_module.recurrent()
        
    def save_hidden(self):
        assert self.recurrent()
        return self.neural_module.save_hidden()

    def restore_hidden(self, state=None):
        assert self.recurrent()
        self.neural_module.restore_hidden(state)

    def get_policy_weights(self, input):
        output = self.neural_module(input).view(-1, self.__input_size)

        # TODO: Figure out how to make inputs/outputs sane sizes.
        weight_dict = {}
        w_conv_del, w_conv_add = self.w_conv_del(output), self.w_conv_add(output)
        w_conv_add_conv, w_conv_add_max, w_conv_add_avg = self.w_conv_add_conv(output), self.w_conv_add_max(output), self.w_conv_add_avg(output)
        weight_dict['conv_count'] = self.__output_size
        weight_dict['w_conv_del'] = w_conv_del
        weight_dict['w_conv_add'] = w_conv_add
        weight_dict['w_conv_add_conv'] = w_conv_add_conv
        weight_dict['w_conv_add_max'] = w_conv_add_max
        weight_dict['w_conv_add_avg'] = w_conv_add_avg
        # TODO: Make min a parameter of the NN.
        # Probably pull from observation space.
        min = torch.tensor(1., requires_grad=True)
        sane = lambda x,y: torch.clamp(min + (x**2 + 1)**2, max=y)
        weight_dict['kernel_dist'] = torch.distributions.Uniform(min,  sane(self.kernel_dist_layer(output), 8))
        weight_dict['channel_dist'] = torch.distributions.Uniform(min, sane(self.channel_dist_layer(output), 128))
        weight_dict['stride_dist'] = torch.distributions.Uniform(min,  sane(self.stride_dist_layer(output), 8))
        weight_dict['padding_dist'] = torch.distributions.Uniform(min, sane(self.padding_dist_layer(output), 8))
        weight_dict['dilation_dist'] = torch.distributions.Uniform(min, sane(self.dilation_dist_layer(output), 2))
        
        return weight_dict
        
    def forward(self, input):
        # Encapsulate our policy in an object so downstream classes don't
        # need to know what kind of distribution to re-create.
        weight_dict = self.get_policy_weights(input)
        policy = TreePolicy(self.decision_tree, weight_dict)
        actions = policy.sample(1)
        #print(actions)
        # Each actions is drawn independtly of others, so joint prob
        # is all of them multiplied together. However, since we have logprobs,
        # we need to sum instead.
        log_prob = sum(policy.log_prob(actions)) # type: ignore

        return actions, log_prob, policy

class JointTreeActor(nn.Module):
    # In order to choose weights for `w_conv` and `w_mlp`, we need to consider both CNN and MLP network configs.
    # Enter the fusion_kernel. The fusion_kernel should take as arguments the full CNN and MLP network descrptions.
    def __init__(self, cnn_module, mlp_module, fusion_kernel,  observation_space, output_dimension=(10,)):
        super(JointTreeActor, self).__init__()
        self.observation_space = observation_space
        self.decision_tree = FullDecisionTree()
        self.cnn_actor = CNNTreeActor(cnn_module, observation_space[0])
        self.mlp_actor = MLPTreeActor(mlp_module, observation_space[1])
        self.fusion_kernel = fusion_kernel

        self.input_dimension = list(more_itertools.always_iterable(fusion_kernel.output_dimension))
        self.__input_size = functools.reduce(lambda x,y: x*y, self.input_dimension, 1)

        self.output_dimension = output_dimension
        self.__output_size = functools.reduce(lambda x,y: x*y, self.output_dimension, 1)
        self.__output_size = torch.tensor(self.__output_size, requires_grad=True, dtype=torch.float)
        self.w_mlp = nn.Linear(self.__input_size, 1)
        self.w_conv = nn.Linear(self.__input_size, 1)

        # Initialize NN
        for x in self.parameters():
            if x.dim() > 1:
                nn.init.kaiming_normal_(x)

    def recurrent(self):
        return self.cnn_module.recurrent() or self.mlp_module.recurrent()
        
    def save_hidden(self):
        ret = {}
        assert self.recurrent()
        if self.cnn_module.recurrent(): ret[id(self.cnn_module)] = self.cnn_module.save_hidden()
        if self.mlp_module.recurrent(): ret[id(self.mlp_module)] = self.mlp_module.save_hidden()
        return ret

    def restore_hidden(self, state_dict=None):
        if self.cnn_module.recurrent():
            id_cnn = id(self.cnn_module)
            if state_dict != None and id_cnn in state_dict: self.cnn_module.restore_hidden(state_dict[id_cnn])
            else: self.cnn_module.restore_hidden()
        if self.mlp_module.recurrent():
            id_mlp = id(self.mlp_module)
            if state_dict != None and id_mlp in state_dict: self.mlp_module.restore_hidden(state_dict[id_mlp])
            else: self.mlp_module.restore_hidden()

    def get_policy_weights(self, cnn_input, mlp_input):
        weight_dict = {}
        weight_dict.update(self.cnn_actor.get_policy_weights(cnn_input))
        weight_dict.update(self.mlp_actor.get_policy_weights(mlp_input))
        output = self.fusion_kernel(cnn_input, mlp_input)
        weight_dict['w_mlp'] = self.w_mlp(output)
        weight_dict['w_conv'] = self.w_conv(output)

        return weight_dict

    def forward(self, input):
        cnn_input, mlp_input = input
        weight_dict = self.get_policy_weights(cnn_input, mlp_input)
        policy = TreePolicy(self.decision_tree, weight_dict)
        actions = policy.sample(1)
        # Each actions is drawn independtly of others, so joint prob
        # is all of them multiplied together. However, since we have logprobs,
        # we need to sum instead.
        log_prob = sum(policy.log_prob(actions)) # type: ignore
        return actions, log_prob, policy