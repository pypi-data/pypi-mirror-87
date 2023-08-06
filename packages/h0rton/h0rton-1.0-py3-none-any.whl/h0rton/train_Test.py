# -*- coding: utf-8 -*-
"""Training the Bayesian neural network (BNN).
This script trains the BNN according to the config specifications.

Example
-------
To run this script, pass in the path to the user-defined training config file as the argument::
    
    $ train h0rton/example_user_config.py

"""

import os, sys
import random
import argparse
from addict import Dict
import numpy as np # linear algebra
from tqdm import tqdm
# torch modules
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from torch.utils.tensorboard import SummaryWriter
# h0rton modules
from h0rton.trainval_data import XYData, XYTestData
from h0rton.configs import TrainValConfig
import h0rton.losses
import h0rton.models
import h0rton.h0_inference
import h0rton.train_utils as train_utils

def parse_args():
    """Parse command-line arguments
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('user_cfg_path', help='path to the user-defined training config file')
    #parser.add_argument('--n_data', default=None, dest='n_data', type=int,
    #                    help='size of dataset to generate (overrides config file)')
    args = parser.parse_args()
    # sys.argv rerouting for setuptools entry point
    if args is None:
        args = Dict()
        args.user_cfg_path = sys.argv[0]
        #args.n_data = sys.argv[1]
    return args

def seed_everything(global_seed):
    """Seed everything for reproducibility

    global_seed : int
        seed for `np.random`, `random`, and relevant `torch` backends

    """
    np.random.seed(global_seed)
    random.seed(global_seed)
    torch.manual_seed(global_seed)
    torch.cuda.manual_seed_all(global_seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False

def main():
    args = parse_args()
    cfg = TrainValConfig.from_file(args.user_cfg_path)
    # Set device and default data type
    device = torch.device(cfg.device_type)
    if device.type == 'cuda':
        torch.set_default_tensor_type('torch.cuda.' + cfg.data.float_type)
    else:
        torch.set_default_tensor_type('torch.' + cfg.data.float_type)
    train_utils.seed_everything(cfg.global_seed)

    ############
    # Data I/O #
    ############

    # Define training data and loader
    torch.multiprocessing.set_start_method('spawn', force=True)
    train_data = XYData(cfg.data.train_dir, data_cfg=cfg.data)
    train_loader = DataLoader(train_data, batch_size=cfg.optim.batch_size, shuffle=True, drop_last=True, num_workers=6, pin_memory=True)
    n_train = train_data.n_data - (train_data.n_data % cfg.optim.batch_size)

    # Define val data and loader
    val_data = XYData(cfg.data.val_dir, data_cfg=cfg.data)
    val_loader = DataLoader(val_data, batch_size=min(len(val_data), cfg.optim.batch_size), shuffle=True, drop_last=True,)
    n_val = val_data.n_data - (val_data.n_data % min(len(val_data), cfg.optim.batch_size))

    #########
    # Model #
    #########
    Y_dim = cfg.data.Y_dim
    # Instantiate loss function
    loss_fn = getattr(h0rton.losses, cfg.model.likelihood_class)(Y_dim=Y_dim, device=device)
    # Instantiate posterior (for logging)
    #bnn_post = getattr(h0rton.h0_inference.gaussian_bnn_posterior, loss_fn.posterior_name)(val_data.Y_dim, device, val_data.train_Y_mean, val_data.train_Y_std)
    # Instantiate model
    net = getattr(h0rton.models, cfg.model.architecture)(num_classes=loss_fn.out_dim, dropout_rate=cfg.model.dropout_rate, norm_layer=h0rton.models.BatchNorm2d)
    net.to(device)

    ################
    # Optimization #
    ################

    # Instantiate optimizer
    optimizer = optim.Adam(net.parameters(), lr=cfg.optim.learning_rate, amsgrad=False, weight_decay=cfg.optim.weight_decay)
    lr_scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='min', factor=cfg.optim.lr_scheduler.factor, patience=cfg.optim.lr_scheduler.patience, verbose=True)
    
    # Saving/loading state dicts
    checkpoint_dir = cfg.checkpoint.save_dir
    if not os.path.exists(checkpoint_dir):
        os.mkdir(checkpoint_dir)

    if cfg.model.load_state:
        epoch, net, optimizer, train_loss, val_loss = train_utils.load_state_dict(cfg.model.state_path, net, optimizer, cfg.optim.n_epochs, device)
        epoch += 1 # resume with next epoch
        last_saved_val_loss = val_loss
        #print(lr_scheduler.state_dict())
        #print(optimizer.state_dict())
    else:
        epoch = 0
        last_saved_val_loss = np.inf

    logger = SummaryWriter()
    model_path = ''
    print("Training set size: {:d}".format(n_train))
    print("Validation set size: {:d}".format(n_val))
    if cfg.data.test_dir is not None:
        print("Test set size: {:d}".format(n_test))
    
    progress = tqdm(range(epoch, cfg.optim.n_epochs))
    for epoch in progress:
        net.train()
        #net.apply(h0rton.models.deactivate_batchnorm)
        train_loss = 0.0

        for batch_idx, (X_tr, Y_tr) in enumerate(train_loader):
            X_tr = X_tr.to(device)
            Y_tr = Y_tr.to(device)
            # Update weights
            optimizer.zero_grad()
            pred_tr = net.forward(X_tr)
            loss = loss_fn(pred_tr, Y_tr)
            loss.backward()
            optimizer.step()
            # For logging
            train_loss += (loss.detach().item() - train_loss)/(1 + batch_idx)
        tqdm.write("Epoch [{}/{}]: TRAIN Loss: {:.4f}".format(epoch+1, cfg.optim.n_epochs, train_loss))

        net.eval()         
        with torch.no_grad():
            #net.apply(h0rton.models.deactivate_batchnorm)
            val_loss = 0.0
            test_loss = 0.0

            if cfg.data.test_dir is not None:
                for batch_idx, (X_t, Y_t) in enumerate(test_loader):
                    X_t = X_t.to(device)
                    Y_t = Y_t.to(device)
                    pred_t = net.forward(X_t)
                    nograd_loss_t = loss_fn(pred_t, Y_t)
                    test_loss += (nograd_loss_t.detach().item() - test_loss)/(1 + batch_idx)
   
            for batch_idx, (X_v, Y_v) in enumerate(val_loader):
                X_v = X_v.to(device)
                Y_v = Y_v.to(device)
                pred_v = net.forward(X_v)
                nograd_loss_v = loss_fn(pred_v, Y_v)
                val_loss += (nograd_loss_v.detach().item() - val_loss)/(1 + batch_idx)

            tqdm.write("Epoch [{}/{}]: VALID Loss: {:.4f}".format(epoch+1, cfg.optim.n_epochs, val_loss))
            if cfg.data.test_dir is not None:
                tqdm.write("Epoch [{}/{}]: TEST Loss: {:.4f}".format(epoch+1, cfg.optim.n_epochs, test_loss))
            
            if (epoch + 1)%(cfg.monitoring.interval) == 0:
                # Log train and val metrics
                loss_dict = {'train': train_loss, 'val': val_loss}
                if cfg.data.test_dir is not None:
                    loss_dict.update(test=test_loss)
                logger.add_scalars('metrics/loss', loss_dict, epoch)

            if (epoch + 1)%(cfg.checkpoint.interval) == 0:
                # FIXME compare to last saved epoch val loss
                if val_loss < last_saved_val_loss:
                    os.remove(model_path) if os.path.exists(model_path) else None
                    model_path = train_utils.save_state_dict(net, optimizer, lr_scheduler, train_loss, val_loss, checkpoint_dir, cfg.model.architecture, epoch)
                    last_saved_val_loss = val_loss
        lr_scheduler.step(train_loss)

    logger.close()
    # Save final state dict
    if val_loss < last_saved_val_loss:
        os.remove(model_path) if os.path.exists(model_path) else None
        model_path = train_utils.save_state_dict(net, optimizer, lr_scheduler, train_loss, val_loss, checkpoint_dir, cfg.model.architecture, epoch)
        print("Saved model at {:s}".format(os.path.abspath(model_path)))

if __name__ == '__main__':
    main()