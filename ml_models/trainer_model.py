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
   def _init_model(
        self,
        device,
        train_dataset,
        valid_dataset,
        train_sampler,
        valid_sampler,
        train_bs,
        valid_bs,
        n_jobs,
        callbacks,
        fp16,
        train_collate_fn,
        valid_collate_fn,
    ):

        if callbacks is None:
            callbacks = list()

        if n_jobs == -1:
            n_jobs = psutil.cpu_count()

        self.device = device

        if next(self.parameters()).device != self.device:
            self.to(self.device)

        if self.train_loader is None:
            self.train_loader = torch.utils.data.DataLoader(
                train_dataset,
                batch_size=train_bs,
                num_workers=n_jobs,
                sampler=train_sampler,
                shuffle=True,
                collate_fn=train_collate_fn,
            )
        if self.valid_loader is None:
            if valid_dataset is not None:
                self.valid_loader = torch.utils.data.DataLoader(
                    valid_dataset,
                    batch_size=valid_bs,
                    num_workers=n_jobs,
                    sampler=valid_sampler,
                    shuffle=False,
                    collate_fn=valid_collate_fn,
                )

        if self.optimizer is None:
            self.optimizer = self.fetch_optimizer()

        if self.scheduler is None:
            self.scheduler = self.fetch_scheduler()

        self.fp16 = fp16
        if self.fp16:
            self.scaler = torch.cuda.amp.GradScaler()

        self._callback_runner = CallbackRunner(callbacks, self)
        self.train_state = enums.TrainingState.TRAIN_START


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


