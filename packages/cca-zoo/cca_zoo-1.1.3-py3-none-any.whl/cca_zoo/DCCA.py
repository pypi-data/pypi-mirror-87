from torch import nn
from torch import optim
from cca_zoo.configuration import Config

"""
All of my deep architectures have forward methods inherited from pytorch as well as a method:

loss(): which calculates the loss given some inputs and model outputs i.e.

loss(inputs,model(inputs))

This allows me to wrap them all up in the deep wrapper. Obviously this isn't required but it is helpful
for standardising the pipeline for comparison
"""


def create_encoder(config, i):
    encoder = config.encoder_models[i](config.hidden_layer_sizes[i], config.input_sizes[i], config.latent_dims).double()
    return encoder


class DCCA(nn.Module):

    def __init__(self, config: Config = Config):
        super(DCCA, self).__init__()
        views = len(config.encoder_models)
        self.config = config
        self.encoders = [create_encoder(config, i) for i in range(views)]
        self.objective = config.objective(config.latent_dims)
        self.optimizers = [optim.Adam(list(encoder.parameters()), lr=config.learning_rate) for encoder in self.encoders]

    def encode(self, *args):
        z = []
        for i, arg in enumerate(args):
            z.append(self.encoders[i](arg))
        return tuple(z)

    def forward(self, *args):
        z = self.encode(*args)
        return z

    def update_weights(self, *args):
        [optimizer.zero_grad() for optimizer in self.optimizers]
        loss = self.loss(*args)
        loss.backward()
        [optimizer.step() for optimizer in self.optimizers]
        return loss

    def update_weights_als(self, *args):
        [optimizer.zero_grad() for optimizer in self.optimizers]
        loss = self.als_loss(*self(x_1, x_2))
        loss.backward()
        [optimizer.step() for optimizer in self.optimizers]
        return loss

    def loss(self, *args):
        z = self(*args)
        return self.objective.loss(*z)

    def als_loss(self, *args):
        # Make a shared target = mean
        self.shared_target = 0
        # Least squares for each projection in same manner as linear from before
        z = self(args)
        nn.mse_loss()
        return self.objective.loss(*z)
