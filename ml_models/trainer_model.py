"""
- idea is to make it as close as pytorch as it can be
- training loop
- optimizer
- scheduler
- model in one go

the trainer requires a dataset class and a model class

"""
import torch
import torch.nn as nn

class Model(nn.Module):
    def __init__(self, *args, **kwargs):
        super().__init(*args, **kwargs)
        self.optimizer = None
        self.scheduler = None
        self.train_loader = None
        self.valid_loader = None

    def forward(self, *args, **kwargs):
        super().forward(*args, **kwargs)

    # def fetch_optimizer(self, *args, **kwargs):
    #     return 

    #  def fetch_scheduler(self, *args, **kwargs):
    #     return 
    
    def train_one_step(data, device):
        """
        We zero_grad the optimizer first.
        We obtain all items into the device all at once
        Calculate the loss.
        """
        self.optimizer.zero_grad()
        for key, value in data.items():
            data[key] = value.to(device)
        _, loss = self(**data)
        loss.backward()
        self.optimizer.step()
        self.scheduler.step()
        return loss
    
    def train_one_epoch(self, data_loader, device):
        """
        Returns the average loss of model.
        """
        self.train()
        epoch_loss = 0
        for data in data_loader:
            loss = self.train_one_step(data, device)
            epoch_loss = epoch_loss + loss
        average_epoch = epoch_loss / len(data_loader)
        return average_epoch
        
    
    def fit(self, train_dataset, batch_size, epochs, device):
        """
        Fit function that takes in the train_dataset.

        We could also create a train_loader but it can be done inside the fit().

        Device checks were the model is on
        """

        if  self.train_loader is None:
            self.train_loader = torch.utils.data.DataLoader(
                train_dataset,
                batch_size = batch_size,
                shuffle=True
            )
        if next(self.parameters()).device != device:
            self.to(device)

        self.optimizer = self.fetch_optimizer()
        self.scheduler = self.fetch_scheduler()

        
        for _ in range(epochs):
            train_loss = self.train_one_epoch(self.train_loader, device)

# inherits from above
class MyModel(Model):
    super().__init__()
    def __init__(self, num_classes):
        # define network layers
        self.out = nn.Linear(128, num_classes)
    def loss(self, outputs, targets):
        if targets iis None:
            return None
        return nn.BCEWithLogitsLoss()(outputs, targets)
    
    def fetch_scheduler(self):
        sch = torch.optom.lr_scheduler.StepLR(self.optimizer)
        return sch

    def fetch_optimizer(self):
        #params = self.parameters()
        # define opt here
        opt = torch.optim.Adam(self.parameters())
        return opt

    def forward(self, features, targets = None):
        x = self.something(forward)
        # x = ....
        # out = ....
        loss = self.loss(out, targets)
        return out, loss


