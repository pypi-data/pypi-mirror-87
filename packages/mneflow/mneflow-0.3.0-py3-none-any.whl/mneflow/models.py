# -*- coding: utf-8 -*-
"""
Define mneflow.models.Model parent class and the implemented models as
its subclasses. Implemented models inherit basic methods from the
parent class.

@author: Ivan Zubarev, ivan.zubarev@aalto.fi
"""

#TODO: update vizualizations

import tensorflow as tf

import numpy as np

from mne import channels, evoked, create_info

from scipy.signal import freqz, welch
from scipy.stats import spearmanr
#from spectrum import aryule

from sklearn.covariance import ledoit_wolf
from sklearn.metrics import confusion_matrix

from matplotlib import pyplot as plt
from matplotlib import patches as ptch
from matplotlib import collections

from .layers import LFTConv, VARConv, DeMixing, Dense, TempPooling
from tensorflow.keras.layers import SeparableConv2D, Conv2D, DepthwiseConv2D
from tensorflow.keras.layers import Flatten, Dropout, BatchNormalization
from tensorflow.keras.initializers import Constant

#from .layers import LSTMv1
from tensorflow.keras import regularizers as k_reg, constraints, layers
import csv
import os
#from mneflow import Dataset

def uniquify(seq):
    un = []
    [un.append(i) for i in seq if not un.count(i)]
    return un


# ----- Base model -----
class BaseModel():
    """Parent class for all MNEflow models.

    Provides fast and memory-efficient data handling and simplified API.
    Custom models can be built by overriding _build_graph and
    _set_optimizer methods.
    """

    def __init__(self, Dataset, specs=dict()):
        """
        Parameters
        -----------
        Dataset : mneflow.Dataset
            `Dataset` object.

        specs : dict
            Dictionary of model-specific hyperparameters. Must include
            at least `model_path` - path for saving a trained model
            See `Model` subclass definitions for details. Unless otherwise 
            specified uses default hyperparameters for each implemented model. 
        """
        self.specs = specs
        self.dataset = Dataset
        self.specs.setdefault('model_path', self.dataset.h_params['savepath'])
        self.model_path = specs['model_path']
        
        self.input_shape = (self.dataset.h_params['n_seq'],
                            self.dataset.h_params['n_t'],
                            self.dataset.h_params['n_ch'])
        self.y_shape = Dataset.h_params['y_shape']
        self.out_dim = np.prod(self.y_shape)


        self.inputs = layers.Input(shape=(self.input_shape))
        self.rate = specs.setdefault('dropout', 0.0)
        #self.l1 = l1
        #self.optimizer = Optimizer
        self.trained = False
        self.y_pred = self.build_graph()


    def build(self, optimizer="adam", loss=None, metrics=None, #mapping=None, 
              learn_rate=3e-4):
        """Compile a model.
        
        Parameters
        ----------
        optimizer : str, tf.optimizers.Optimizer
            Deafults to "adam"
        
        loss : str, tf.keras.losses.Loss
            Defaults to MSE in target_type is "float" and 
            "softmax_crossentropy" if "target_type" is int
        
        metrics : str, tf.keras.metrics.Metric
            Defaults to MAE in target_type is "float" and 
                "categorical_accuracy" if "target_type" is int
        
        learn_rate : float
            Learning rate, defaults to 3e-4
        """
        # Initialize computational graph
        # if mapping:
        #     map_fun = tf.keras.activations.get(mapping)
        #     self.y_pred= map_fun(self.y_pred)
        
        self.km = tf.keras.Model(inputs=self.inputs, outputs=self.y_pred)
        
        params = {"optimizer": tf.optimizers.get(optimizer).from_config({"learning_rate":learn_rate})}
        
        if loss:
            params["loss"] = tf.keras.losses.get(loss)
        
        if metrics:
            if not isinstance(metrics, list):
                metrics = [metrics]
            params["metrics"] = [tf.keras.metrics.get(metric) for metric in metrics]
        
        # Initialize optimizer
        if self.dataset.h_params["target_type"] in ['float', 'signal']:
            params.setdefault("loss", tf.keras.losses.MeanSquaredError(name='MSE'))
            params.setdefault("metrics", tf.keras.metrics.MeanAbsoluteError(name="MAE"))
            
        elif self.dataset.h_params["target_type"] in ['int']:
            params.setdefault("loss", tf.nn.softmax_cross_entropy_with_logits)
            params.setdefault("metrics", tf.keras.metrics.CategoricalAccuracy(name="cat_ACC"))
              
        #print(params)
        self.km.compile(optimizer=params["optimizer"],
                        loss=params["loss"],
                        metrics=params["metrics"])


        print('Input shape:', self.input_shape)
        print('y_pred:', self.y_pred.shape)

#       TODO: saver
#        self.saver = tf.train.Saver(max_to_keep=1)

        print('Initialization complete!')

    def build_graph(self):
        """Build computational graph using defined placeholder self.X
        as input.

        Can be overriden in a sub-class for customized architecture.

        Returns
        --------
        y_pred : tf.Tensor
            Output of the forward pass of the computational graph.
            Prediction of the target variable.
        """



        flat = Flatten()(self.inputs)
        self.fc = Dense(size=self.out_dim, nonlin=tf.identity,
                        specs=self.specs)
        y_pred = self.fc(flat)
        #y_pred = fc_1
        #print("Built graph: y_shape", y_pred.shape)
        return y_pred

    def train(self, n_epochs, eval_step=None, min_delta=1e-6,
              early_stopping=3, mode='single_fold'):

        """
        Train a model

        Parameters
        -----------

        n_epochs : int
            Maximum number of training eopchs.

        eval_step : int, None
            iterations per epoch. If None each epoch passes the training set
            exactly once

        early_stopping : int
            Patience parameter for early stopping. Specifies the number
            of epochs's during which validation cost is allowed to
            rise before training stops.

        min_delta : float, optional
            Convergence threshold for validation cost during training.
            Defaults to 1e-6.
        
        mode : str, optional
            can be 'single_fold', 'cv', 'loso'. Defaults to 'single_fold'
        """

        stop_early = tf.keras.callbacks.EarlyStopping(monitor='val_loss',
                                                      min_delta=min_delta,
                                                      patience=early_stopping,
                                                      restore_best_weights=True)
        if not eval_step:
            train_size = self.dataset.h_params['train_size']
            eval_step = train_size // self.dataset.h_params['train_batch'] + 1
        # if val_batch:
        #     val_size = self.dataset.h_params['val_size']
        #     self.validation_steps = max(1, val_size // val_batch)
        # else:
        #     self.validation_steps = 1
            
        self.train_params = [n_epochs, eval_step, early_stopping, mode]

        
        if mode == 'single_fold':
            #self.dataset.train, self.dataset.val = self.dataset._build_dataset()
            
            self.t_hist = self.km.fit(self.dataset.train,
                                   validation_data=self.dataset.val,
                                   epochs=n_epochs, steps_per_epoch=eval_step,
                                   shuffle=True, 
                                   validation_steps=self.dataset.validation_steps,
                                   callbacks=[stop_early], verbose=2)
            self.v_loss, self.v_metric = self.evaluate(self.dataset.val)
            self.v_loss_sd = 0
            self.v_metric_sd = 0
            print("Training complete: loss: {}, Metric: {}".format(self.v_loss, self.v_metric))
            self.update_log()
        elif mode == 'cv':
            n_folds = len(self.dataset.h_params['folds'][0])
            print("Running cross-validation with {} folds".format(n_folds))
            metrics = []
            losses = []
            for jj in range(n_folds):
                print("fold:", jj)
                train, val = self.dataset._build_dataset(self.dataset.h_params['train_paths'],
                                                   train_batch=self.dataset.training_batch,
                                                   test_batch=self.dataset.validation_batch,
                                                   split=True, val_fold_ind=jj)
                self.t_hist = self.km.fit(train,
                                   validation_data=val,
                                   epochs=n_epochs, steps_per_epoch=eval_step,
                                   shuffle=True, 
                                   validation_steps=self.dataset.validation_steps,
                                   callbacks=[stop_early], verbose=2)
                
                
                loss, metric = self.evaluate(val)
                losses.append(loss)
                metrics.append(metric)
                    
                if jj < n_folds -1:
                    self.shuffle_weights()
                else:
                    "Not shuffling the weights for the last fold"
                

                print("Fold: {} Loss: {:.4f}, Metric: {:.4f}".format(jj, loss, metric))
            self.cv_losses = losses
            self.cv_metrics = metrics
            self.v_loss = np.mean(losses)
            self.v_metric = np.mean(metrics)
            self.v_loss_sd = np.std(losses)
            self.v_metric_sd = np.std(metrics)
            print("{} with {} folds completed. Loss: {:.4f} +/- {:.4f}. Metric: {:.4f} +/- {:.4f}".format(mode, n_folds, np.mean(losses), np.std(losses), np.mean(metrics), np.std(metrics)))
            self.update_log()
            return self.cv_losses, self.cv_metrics
        
        elif mode == "loso":
            n_folds = len(self.dataset.h_params['test_paths'])
            print("Running leave-one-subject-out CV with {} subject".format(n_folds))
            metrics = []
            losses = []
            for jj in range(n_folds):
                print("fold:", jj)
                
                test_subj = self.dataset.h_params['test_paths'][jj]
                train_subjs = self.dataset.h_params['train_paths'].copy()
                train_subjs.pop(jj)
                
                train, val = self.dataset._build_dataset(train_subjs,
                                                   train_batch=self.dataset.training_batch,
                                                   test_batch=self.dataset.validation_batch,
                                                   split=True, val_fold_ind=0)
                
                                
                self.t_hist = self.km.fit(train,
                                   validation_data=val,
                                   epochs=n_epochs, steps_per_epoch=eval_step,
                                   shuffle=True, 
                                   validation_steps=self.dataset.validation_steps,
                                   callbacks=[stop_early], verbose=2)
                
                
                test = self.dataset._build_dataset(test_subj,
                                                   test_batch=None,
                                                   split=False)
                
                
                loss, metric = self.evaluate(test)
                losses.append(loss)
                metrics.append(metric)
                    
                if jj < n_folds -1:
                    self.shuffle_weights()
                else:
                    "Not shuffling the weights for the last fold"
                
            self.cv_losses = losses
            self.cv_metrics = metrics
            self.v_loss = np.mean(losses)
            self.v_metric = np.mean(metrics)
            self.v_loss_sd = np.std(losses)
            self.v_metric_sd = np.std(metrics)
            self.update_log()
            print("{} with {} folds completed. Loss: {:.4f} +/- {:.4f}. Metric: {:.4f} +/- {:.4f}".format(mode, n_folds, np.mean(losses), np.std(losses), np.mean(metrics), np.std(metrics)))
            return self.cv_losses, self.cv_metrics
            
                

    
    def shuffle_weights(self):
        print("Re-shuffling weights between folds")
        weights = self.km.get_weights()
        weights = [np.random.permutation(w.flat).reshape(w.shape) for w in weights]
        # Faster, but less random: only permutes along the first dimension
        # weights = [np.random.permutation(w) for w in weights]
        self.km.set_weights(weights)
    
    
    def plot_hist(self):
        """Plot loss history during training."""
        # "Loss"
        plt.plot(self.t_hist.history['loss'])
        plt.plot(self.t_hist.history['val_loss'])
        plt.title('model loss')
        plt.ylabel('loss')
        plt.xlabel('epoch')
        plt.legend(['train', 'validation'], loc='upper left')
        plt.show()
        #plt.legend(['t_loss', 'v_loss'])
        #plt.title(self.scope.upper())
        #plt.xlabel('Epochs')
        #plt.show()

#    def load(self):
#        """Loads a pretrained model.
#
#        To load a specific model the model object should be initialized
#        using the corresponding metadata and computational graph.
#        """
#        self.saver.restore(self.sess,
#                           ''.join([self.model_path, self.scope, '-',
#                                    self.dataset.h_params['data_id']]))
#
#        self.v_acc = self.sess.run([self.accuracy],
#                                   feed_dict={self.handle: self.val_handle,
#                                              self.rate: 0.})
#        self.trained = True



    def update_log(self):
        """Logs experiment to self.model_path + self.scope + '_log.csv'.

        If the file exists, appends a line to the existing file.
        """
        appending = os.path.exists(self.model_path + self.scope + '_log.csv')

        log = dict()
        #dataset info
        log['data_id'] = self.dataset.h_params['data_id']
        log['data_path'] = self.dataset.h_params['savepath']
        #log['decim'] = str(self.dataset.h_params['decim'])

        # if self.dataset.class_subset:
        #     log['class_subset'] = '-'.join(
        #             str(self.dataset.class_subset).split(','))
        # else:
        #     log['class_subset'] = 'all'

        log['y_shape'] = np.prod(self.dataset.h_params['y_shape'])
        log['fs'] = str(self.dataset.h_params['fs'])
        
        #architecture and regularization
        log.update(self.specs)
        
        #training paramters
        log['nepochs'], log['eval_step'], log['early_stopping'], log['mode'] = self.train_params

        #v_loss, v_metric = self.evaluate(self.dataset.val)
        #self.v_loss, self.v_perf = self.km.evaluate(self.dataset.val, steps=1, verbose=0)
        log['v_metric'] = self.v_metric
        log['v_loss'] = self.v_metric
        log['v_metric_sd'] = self.v_metric_sd
        log['v_loss_sd'] = self.v_metric_sd


        tr_loss, tr_perf = self.evaluate(self.dataset.train)
        log['tr_metric'] = tr_perf
        log['tr_loss'] = tr_loss

        if 'test_paths' in self.dataset.h_params and log['mode'] != 'loso':
            t_loss, t_metric = self.evaluate(self.dataset.h_params['test_paths'])
            print("Updating log: test loss: {:.4f} test metric: {:.4f}".format(t_loss, t_metric))
            log['test_metric'] = t_metric
            log['test_loss'] = t_loss
        else:
            log['test_metric'] = "NA"
            log['test_loss'] = "NA"
        self.log = log

        with open(self.model_path + self.scope + '_log.csv', 'a') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=self.log.keys())
            if not appending:
                writer.writeheader()
            writer.writerow(self.log)
            
    def save(self):
        print("Not implemented")
        
    def restore(self):
        print("Not implemented")
    
    def predict(self, dataset=None):
        if not dataset: 
            print("No dataset specified using validation dataset (Default)")
            dataset = self.dataset.val
        elif isinstance(dataset, str) or isinstance(dataset, (list, tuple)):
            dataset = self.dataset._build_dataset(dataset, 
                                             split=False, 
                                             test_batch=None, 
                                             repeat=True)
        elif not isinstance(dataset, tf.data.Dataset):
            print("Specify dataset")
            return None, None
        
        y_pred = self.km.predict(dataset, 
                                 steps=self.dataset.validation_steps)
        y_true = [row[1] for row in dataset.take(1)][0]
        y_true = y_true.numpy()
        return y_true, y_pred
    
    def evaluate(self, dataset=False):
        if not dataset: 
            print("No dataset specified using validation dataset (Default)")
            dataset = self.dataset.val
        elif isinstance(dataset, str) or isinstance(dataset, (list, tuple)):
            dataset = self.dataset._build_dataset(dataset, 
                                             split=False, 
                                             test_batch=None, 
                                             repeat=True)
        elif not isinstance(dataset, tf.data.Dataset):
            print("Specify dataset")
            return None, None
            
        losses, metrics = self.km.evaluate(dataset, 
                                           steps=self.dataset.validation_steps)
        return  losses, metrics
        


class LFCNN(BaseModel):
    """LF-CNN. Includes basic parameter interpretation options.

    For details see [1].
    References
    ----------
        [1] I. Zubarev, et al., Adaptive neural network classifier for
        decoding MEG signals. Neuroimage. (2019) May 4;197:425-434
    """
    def __init__(self, Dataset, specs=dict()):
        """

        Parameters
        ----------
        Dataset : mneflow.Dataset

        specs : dict
                dictionary of model hyperparameters {

        n_latent : int
            Number of latent components.
            Defaults to 32.

        nonlin : callable
            Activation function of the temporal convolution layer.
            Defaults to tf.nn.relu

        filter_length : int
            Length of spatio-temporal kernels in the temporal
            convolution layer. Defaults to 7.

        pooling : int
            Pooling factor of the max pooling layer. Defaults to 2

        pool_type : str {'avg', 'max'}
            Type of pooling operation. Defaults to 'max'.

        padding : str {'SAME', 'FULL', 'VALID'}
            Convolution padding. Defaults to 'SAME'.}

        stride : int
        Stride of the max pooling layer. Defaults to 1.
        """
        self.scope = 'lfcnn'
        specs.setdefault('filter_length', 7)
        specs.setdefault('n_latent', 32)
        specs.setdefault('pooling', 2)
        specs.setdefault('stride', 2)
        specs.setdefault('padding', 'SAME')
        specs.setdefault('pool_type', 'max')
        specs.setdefault('nonlin', tf.nn.relu)
        specs.setdefault('l1', 3e-4)
        specs.setdefault('l2', 0)
        specs.setdefault('l1_scope', ['fc', 'demix', 'lf_conv'])
        specs.setdefault('l2_scope', [])
        specs.setdefault('maxnorm_scope', [])
        #specs.setdefault('model_path',  self.dataset.h_params['save_path'])
        super(LFCNN, self).__init__(Dataset, specs)



    def build_graph(self):
        """Build computational graph using defined placeholder `self.X`
        as input.

        Returns
        --------
        y_pred : tf.Tensor
            Output of the forward pass of the computational graph.
            Prediction of the target variable.
        """
        self.dmx = DeMixing(size=self.specs['n_latent'], nonlin=tf.identity,
                            axis=3, specs=self.specs)
        self.dmx_out = self.dmx(self.inputs)

        self.tconv = LFTConv(size=self.specs['n_latent'],
                             nonlin=self.specs['nonlin'],
                             filter_length=self.specs['filter_length'],
                             padding=self.specs['padding'],
                             specs=self.specs
                             )
        self.tconv_out = self.tconv(self.dmx_out)

        self.pool = TempPooling(pooling=self.specs['pooling'],
                                  pool_type=self.specs['pool_type'],
                                  stride=self.specs['stride'],
                                  padding=self.specs['padding'],
                                  )
        self.pooled = self.pool(self.tconv_out)

        dropout = Dropout(self.specs['dropout'],
                          noise_shape=None)(self.pooled)

        self.fin_fc = Dense(size=self.out_dim, nonlin=tf.identity,
                            specs=self.specs)

        y_pred = self.fin_fc(dropout)

        return y_pred

    #@tf.function
    def _get_spatial_covariance(self, dataset):
        """Compute spatial covariance matrcix from the dataset

        Parameters:
        -----------
        dataset : tf.data.Dataset
        """
        n1_covs = []
        for x, y in dataset.take(5):
            #print('x:', x.shape)
            #print('x[0,0]:', x[0,0].shape)
            n1cov = tf.tensordot(x[0,0], x[0,0], axes=[[0], [0]])
            #print('n1cov:', n1cov.shape)
            n1_covs.append(n1cov)
        #print('len(n1_covs):', len(n1_covs))
        cov = tf.reduce_mean(tf.stack(n1_covs, axis=0), axis=0)
        #print('cov:', cov.shape)
        #tf.reduce_mean(n1_covs)
        return cov


    def compute_patterns(self, data_path=None, output='patterns'):
        """Computes spatial patterns from filter weights.
        Required for visualization.

        Parameters
        ----------
        data_path : str or list of str
            Path to TFRecord files on which the patterns are estimated.

        output : str {'patterns, 'filters', 'full_patterns'}
            String specifying the output.

            'filters' - extracts weights of the spatial filters

            'patterns' - extracts activation patterns, obtained by
            left-multipying the spatial filter weights by the (spatial)
            data covariance.

            'full-patterns' - additionally multiplies activation
            patterns by the precision (inverse covariance) of the
            latent sources

        Returns
        -------
        self.patterns
            spatial filters or activation patterns, depending on the
            value of 'output' parameter.

        self.lat_tcs
            time courses of latent sourses.

        self.filters
            temporal convolutional filter coefficients.

        self.out_weights
            weights of the output layer.

        self.rfocs
            feature relevances for the output layer.
            (See self.get_output_correlations)

        Raises:
        -------
            AttributeError: If `data_path` is not specified.
        """
        #vis_dict = None
        if not data_path: 
            print("Computing patterns: No path specified, using validation dataset (Default)")
            ds = self.dataset.val
        elif isinstance(data_path, str) or isinstance(data_path, (list, tuple)):
            ds = self.dataset._build_dataset(data_path, 
                                             split=False, 
                                             test_batch=None, 
                                             repeat=True)
        elif isinstance(data_path, mneflow.data.Dataset):
            if hasattr(data_path, 'test'):
                ds = data_path.test
            else:
                ds = data_path.val
        elif isinstance(data_path, tf.data.Dataset):
            ds = data_path
        else:
            raise AttributeError('Specify dataset or data path.')

        X, y = [row for row in ds.take(1)][0]

        self.out_w_flat = self.fin_fc.w.numpy()
        self.out_weights = np.reshape(self.out_w_flat, [-1, self.dmx.size,
                                              self.out_dim])
        self.out_biases = self.fin_fc.b.numpy()
        self.feature_relevances = self.get_component_relevances(X, y)
        
        #compute temporal convolution layer outputs for vis_dics
        tc_out = self.pool(self.tconv(self.dmx(X)).numpy())
        

        #compute data covariance
        X = X - tf.reduce_mean(X, axis=-2, keepdims=True)
        X = tf.transpose(X, [3, 0, 1, 2])
        X = tf.reshape(X, [X.shape[0], -1])
        self.dcov = tf.matmul(X, tf.transpose(X))

        # get spatial extraction fiter weights
        demx = self.dmx.w.numpy()
        self.lat_tcs = np.dot(demx.T, X)
        del X

        if 'patterns' in output:
            self.patterns = np.dot(self.dcov, demx)
#            if 'full' in output:
#                self.lat_cov = ledoit_wolf(self.lat_tcs)
#                self.lat_prec = np.linalg.inv(self.lat_cov)
#                self.patterns = np.dot(self.patterns, self.lat_prec)
        else:
            self.patterns = demx

        kern = self.tconv.filters.numpy()


        #  Temporal conv stuff
        self.filters = np.squeeze(kern)
        self.tc_out = np.squeeze(tc_out)
        self.corr_to_output = self.get_output_correlations(y)
        #self.y_true = y

#        print('demx:', demx.shape,
#              'kern:', self.filters.shape,
#              'tc_out:', self.tc_out.shape,
#              'out_weights:', self.out_weights.shape)


    def get_component_relevances(self, X, y):
        """Compute component relevances by recursive elimination
        """
        model_weights = self.km.get_weights()
        base_loss, base_performance = self.km.evaluate(X, y, verbose=0)
        #if len(base_performance > 1):
        #    base_performance = bbase_performance[0]
        feature_relevances_loss = []
        n_out_t = self.out_weights.shape[0]
        n_out_y = self.out_weights.shape[-1]
        zeroweights = np.zeros((n_out_t,))
        for i in range(self.specs["n_latent"]):
            loss_per_class = []
            for jj in range(n_out_y):
                new_weights = self.out_weights.copy()
                new_bias = self.out_biases.copy()
                new_weights[:, i, jj] = zeroweights
                new_bias[jj] = 0
                new_weights = np.reshape(new_weights, self.out_w_flat.shape)
                model_weights[-2] = new_weights
                model_weights[-1] = new_bias
                self.km.set_weights(model_weights)
                loss = self.km.evaluate(X, y, verbose=0)[0]
                loss_per_class.append(base_loss - loss)
            feature_relevances_loss.append(np.array(loss_per_class))
            self.component_relevance_loss = np.array(feature_relevances_loss)


    def get_output_correlations(self, y_true):
        """Computes a similarity metric between each of the extracted
        features and the target variable.

        The metric is a Manhattan distance for dicrete targets, and
        Spearman correlation for continuous targets.
        """
        corr_to_output = []
        y_true = y_true.numpy()
        flat_feats = self.tc_out.reshape(self.tc_out.shape[0], -1)

        if self.dataset.h_params['target_type'] in ['float', 'signal']:
            for y_ in y_true.T:

                rfocs = np.array([spearmanr(y_, f)[0] for f in flat_feats.T])
                corr_to_output.append(rfocs.reshape(self.out_weights.shape[:-1]))

        elif self.dataset.h_params['target_type'] == 'int':
            y_true = y_true/np.linalg.norm(y_true, ord=1, axis=0)[None, :]
            flat_div = np.linalg.norm(flat_feats, 1, axis=0)[None, :]
            flat_feats = flat_feats/flat_div
            #print("ff:", flat_feats.shape)
            #print("y_true:", y_true.shape)
            for y_ in y_true.T:
                #print('y.T:', y_.shape)
                rfocs = 2. - np.sum(np.abs(flat_feats - y_[:, None]), 0)
                corr_to_output.append(rfocs.reshape(self.out_weights.shape[:-1]))

        corr_to_output = np.dstack(corr_to_output)

        if np.any(np.isnan(corr_to_output)):
            corr_to_output[np.isnan(corr_to_output)] = 0
        return corr_to_output

    # --- LFCNN plot functions ---
    def plot_out_weights(self, pat=None, t=None, tmin=-0.1, sorting='weight',
                         class_names=None):
        """Plots the weights of the output layer.

        Parameters
        ----------

        pat : int [0, self.specs['n_latent'])
            Index of the latent component to higlight

        t : int [0, self.h_params['n_t'])
            Index of timepoint to highlight

        """
        if not hasattr(self, 'out_weights'):
            self.compute_patterns(self.dataset)
        vmin = np.min(self.out_weights)
        vmax = np.max(self.out_weights)

        f, ax = plt.subplots(1, self.out_dim)
        f.set_size_inches([16, 3])
        if not isinstance(ax, np.ndarray):
            ax = [ax]

        for ii in range(len(ax)):
            F = self.out_weights[..., ii].T

            tstep = self.specs['stride']/float(self.dataset.h_params['fs'])
            times = tmin+tstep*np.arange(F.shape[-1])

            im = ax[ii].pcolor(times, np.arange(self.specs['n_latent'] + 1), F,
                               cmap='bone_r', vmin=vmin, vmax=vmax)

            r = []
            if np.any(pat) and np.any(t):
                r = [ptch.Rectangle((times[tt], pat[ii]), width=tstep,
                                    height=1, angle=0.0)for tt in t[ii]]

                pc = collections.PatchCollection(r, facecolor='red', alpha=.5,
                                                 edgecolor='red')
                ax[ii].add_collection(pc)

        f.colorbar(im, ax=ax[-1])
        plt.show()
        return f

    def plot_waveforms(self, sorting='compwise_loss', tmin=0, class_names=None):
        """Plots timecourses of latent components.

        Parameters
        ----------
        tmin : float
            Beginning of the MEG epoch with regard to reference event.
            Defaults to 0.
            
        sorting : str
            heuristic for selecting relevant components. See LFCNN._sorting
        """
        if not hasattr(self, 'lat_tcs'):
            self.compute_patterns(self.dataset)

        if not hasattr(self, 'uorder'):
            order, _ = self._sorting(sorting)
            self.uorder = order.ravel()
            #self.uorder = np.squeeze(order)
        if np.any(self.uorder):
            for jj, uo in enumerate(self.uorder):
                f, ax = plt.subplots(2, 2)
                f.set_size_inches([16, 16])
        
                nt = self.dataset.h_params['n_t']
                self.waveforms = np.squeeze(
                        self.lat_tcs.reshape([self.specs['n_latent'], -1, nt]).mean(1))
        
                tstep = 1/float(self.dataset.h_params['fs'])
                times = tmin + tstep*np.arange(nt)
                scaling = 3*np.mean(np.std(self.waveforms, -1))
                [ax[0, 0].plot(times, wf + scaling*i)
                 for i, wf in enumerate(self.waveforms) if i not in self.uorder]
        
                ax[0, 0].plot(times,
                              self.waveforms[uo] + scaling*uo,
                              'k', linewidth=5.)
                ax[0, 0].set_title('Latent component waveforms')
        
                bias = self.tconv.b.numpy()[uo]
                ax[0, 1].stem(self.filters.T[uo], use_line_collection=True)
                ax[0, 1].hlines(bias, 0, len(self.filters.T[uo]),
                                linestyle='--', label='Bias')
                ax[0, 1].legend()
                ax[0, 1].set_title('Filter coefficients')
        
                conv = np.convolve(self.filters.T[uo],
                                   self.waveforms[uo], mode='same')
                vmin = conv.min()
                vmax = conv.max()
                ax[1, 0].plot(times + 0.5*self.specs['filter_length']/float(self.fs),
                              conv)
                #ax[1, 0].hlines(bias, times[0], times[-1], linestyle='--', color='k')
        
                tstep = float(self.specs['stride'])/self.fs
                strides = np.arange(times[0], times[-1] + tstep/2, tstep)[1:-1]
                pool_bins = np.arange(times[0],
                                      times[-1] + tstep,
                                      self.specs['pooling']/self.fs)[1:]
        
                ax[1, 0].vlines(strides, vmin, vmax,
                                linestyle='--', color='c', label='Strides')
                ax[1, 0].vlines(pool_bins, vmin, vmax,
                                linestyle='--', color='m', label='Pooling')
                ax[1, 0].set_xlim(times[0], times[-1])
                #ax[1, 0].set_ylim(2*np.min(conv), 2*np.max(conv))
                ax[1, 0].legend()
                ax[1, 0].set_title('Convolution output')
        
                #if self.out_weights.shape[-1] > 1:
                #print(self.F.shape, pool_bins.shape)
                strides1 = np.arange(times[0], times[-1] + tstep/2, tstep)
                ax[1, 1].pcolor(strides1, np.arange(self.specs['n_latent']), 
                                self.F)
                #print()
                ax[1, 1].hlines(uo + .5, pool_bins[0], pool_bins[-1], color='r')
                # else:
                #     ax[1, 1].stem(self.out_weights[:, uo, :])
        
                ax[1, 1].set_title('Feature relevance map')
                #f.show()
                if class_names:
                    comp_name = class_names[jj]
                else:
                    comp_name = "Class " + str(jj)
                f.suptitle(comp_name, fontsize=16)
            return f

    def _sorting(self, sorting='compwise_loss', n_comp=1):
        """Specify which components to plot.

        Parameters
        ----------
        sorting : str
            Sorting heuristics.

            'l2' - plots all components sorted by l2 norm of activations in the
            output layer in descending order.

            'commpwise_loss' - compute the effect of eliminating the latent
            component on the validation loss. Perofrmed for each class
            separately.

            'weight' - plots a single component that has a maximum
            weight for each class in the output layer.

            'output_corr' - plots a single component, which produces a
            feature in the output layer that has maximum correlation
            with each target variable.

            'weight_corr' - plots a single component, has maximum relevance
            value defined as output_layer_weught*correlation.

        Returns:
        --------
        order : list of int
            indices of relevant components

        ts : list of int
            indices of relevant timepoints
        """
        order = []
        ts = []

        if sorting == 'l2':
            for i in range(self.out_dim):
                self.F = self.out_weights[..., i].T
                
                norms = np.linalg.norm(self.F, axis=1, ord=2)
                pat = np.argsort(norms)[-n_comp:]
                order.append(pat[:n_comp]) 
                ts.append(np.arange(self.F.shape[-1]))
                #ts.append(None)

        elif sorting == 'compwise_loss':
            for i in range(self.out_dim):
                self.F = self.out_weights[..., i].T
                pat = np.argsort(self.component_relevance_loss[:, i])
                #print(self.component_relevance_loss[pat, i])
                order.append(pat[:n_comp])
                ts.append(np.arange(self.F.shape[-1]))

        elif sorting == 'weight_corr':
            for i in range(self.out_dim):
                self.F = np.abs(self.out_weights[..., i].T
                                * self.corr_to_output[..., i].T)
                pat, t = np.where(self.F == np.max(self.F))
                #print('Maximum spearman r * weight:', np.max(self.F))
                order.append(pat)
                ts.append(t)

        elif sorting == 'weight':
            for i in range(self.out_dim):
                self.F = self.out_weights[..., i].T
                pat, t = np.where(self.F == np.max(self.F))
                #print('Maximum weight:', np.max(self.F))
                order.append(pat)
                ts.append(t)

        elif sorting == 'output_corr':
            for i in range(self.out_dim):
                self.F = self.corr_to_output[..., i].T
                #print('Maximum r_spear:', np.max(self.F))
                pat, t = np.where(self.F == np.max(self.F))
                order.append(pat)
                ts.append(t)
        else:
            print("Sorting {:s} not implemented".format(sorting))
            return None, None

        order = np.array(order)
        ts = np.array(ts)
        return order, ts

    def plot_patterns(self, sensor_layout=None, sorting='l2', percentile=90,
                      scale=False, class_names=None):
        """Plot informative spatial activations patterns for each class
        of stimuli.

        Parameters
        ----------

        sensor_layout : str or mne.channels.Layout
            Sensor layout. See mne.channels.read_layout for details

        sorting : str, optional
            Component sorting heuristics. Defaults to 'l2'.
            See model._sorting

        scale : bool, otional
            If True will min-max scale the output. Defaults to False.

        names : list of str, optional
            Class names.

        Returns
        -------

        Figure

        """
        order, ts = self._sorting(sorting)
        #print(order, type(order))
        self.uorder = order.ravel()
        #self.uorder = np.squeeze(self.uorder1)
        l_u = len(self.uorder)
        if sensor_layout:
            lo = channels.read_layout(sensor_layout)
            info = create_info(lo.names, 1., sensor_layout.split('-')[-1])
            self.fake_evoked = evoked.EvokedArray(self.patterns, info)
            
            if l_u > 1:
                self.fake_evoked.data[:, :l_u] = self.fake_evoked.data[:, self.uorder]
            elif l_u == 1:
                self.fake_evoked.data[:, l_u] = self.fake_evoked.data[:, self.uorder[0]]
            self.fake_evoked.crop(tmax=float(l_u))
            if scale:
                _std = self.fake_evoked.data[:, :l_u].std(0)
                self.fake_evoked.data[:, :l_u] /= _std
        else:
            print("Specify sensor layout")


        if np.any(self.uorder):
                        #f.suptitle(comp_name, fontsize=16)
            #print(len())
            nfilt = max(self.out_dim, 8)
            nrows = max(1, l_u//nfilt)
            ncols = min(nfilt, l_u)
            if class_names:
                comp_names = class_names
            else:
                comp_names = ["Class #{}".format(jj+1) for jj in range(ncols)]

            f, ax = plt.subplots(nrows, ncols, sharey=True)
            f.set_size_inches([16, 3])
            ax = np.atleast_2d(ax)
            for ii in range(nrows):
                
                fake_times = np.arange(ii * ncols,  (ii + 1) * ncols, 1.)
                vmax = np.percentile(self.fake_evoked.data[:, :l_u], 95)
                self.fake_evoked.plot_topomap(times=fake_times,
                                              axes=ax[ii],
                                              colorbar=False,
                                              vmax=vmax,
                                              scalings=1,
                                              time_format="Class #%g",
                                              title='Patterns ('+str(sorting)+')')
            # if sorting in ['output_corr', 'weight', 'weight_corr', 'compwise_loss']:
            #         [ax[0][jj].set_title(c) for jj, c in enumerate(comp_names)]


            if np.any(ts):
                self.plot_out_weights(pat=order, t=ts, sorting=sorting)
            else:
                self.plot_out_weights()
            return f

    def plot_spectra(self, fs=None, sorting='l2', norm_spectra=None,
                     log=False, class_names=None):
        """Plots frequency responses of the temporal convolution filters.

        Parameters
        ----------
        fs : float
            Sampling frequency.

        sorting : str optinal
            Component sorting heuristics. Defaults to 'l2'.
            See model._sorting

        norm_sepctra : None, str {'welch', 'ar'}
            Whether to apply normalization for extracted spectra.
            Defaults to None.

        log : bool
            Apply log-transform to the spectra.

        """
        if fs is not None:
            self.fs = fs
        elif self.dataset.h_params['fs']:
            self.fs = self.dataset.h_params['fs']
        else:
            warnings.warn('Sampling frequency not specified, setting to 1.',
                          UserWarning)
            self.fs = 1.

        if norm_spectra:
            if norm_spectra == 'welch':
                fr, psd = welch(self.lat_tcs, fs=self.fs, nperseg=256)
                self.d_psds = psd[:, :-1]

#            elif 'ar' in norm_spectra and not hasattr(self, 'ar'):
#                ar = []
#                for i, ltc in enumerate(self.lat_tcs):
#                    coef, _, _ = aryule(ltc, self.specs['filter_length'])
#                    ar.append(coef[None, :])
#                self.ar = np.concatenate(ar)

        order, ts = self._sorting(sorting)
        self.uorder = order.ravel()
        #self.uorder = np.squeeze(order)
        out_filters = self.filters[:, self.uorder]
        l_u = len(self.uorder)

        nfilt = max(self.out_dim, 8)
        nrows = max(1, l_u//nfilt)
        ncols = min(nfilt, l_u)
        if np.any(self.uorder):
            f, ax = plt.subplots(nrows, ncols, sharey=True)
            f.set_size_inches([16, 3])
            ax = np.atleast_2d(ax)
            if sorting in ['output_corr', 'weight', 'weight_corr', 'compwise_loss']:
                if class_names:
                    comp_names = class_names
                else:
                    comp_names = ["Class " + str(jj) for jj in range(self.out_dim)]
                    #f.suptitle(comp_name, fontsize=16)
                [ax[0][jj].set_title(c) for jj, c in enumerate(comp_names)]
            
            
            for i in range(nrows):
                for jj, flt in enumerate(out_filters[:, i*ncols:(i+1)*ncols].T):
                    w, h = freqz(flt, 1, worN=128)
                    fr1 = w/np.pi*self.fs/2
                    if  norm_spectra == 'welch':    
                        
                        h0 = self.d_psds[self.uorder[jj], :]*np.abs(h)
                        if log:
                            ax[i, jj].semilogy(fr1, self.d_psds[self.uorder[jj], :],
                                               label='Filter input')
                            ax[i, jj].semilogy(fr1, np.abs(h0),
                                               label='Fitler output')
                        else:
                            ax[i, jj].plot(fr1, self.d_psds[self.uorder[jj], :],
                                           label='Filter input')
                            ax[i, jj].plot(fr1, np.abs(h0), label='Fitler output')
                        #print(np.all(np.round(fr[:-1], -4) == np.round(fr1, -4)))
                    
        
                    if log:
                        ax[i, jj].semilogy(fr1, np.abs(h),
                                           label='Freq response')
                    else:
                        ax[i, jj].plot(fr1, np.abs(h),
                                       label='Freq response')
                    ax[i, jj].set_xlim(0, 125.)
                    ax[i, jj].set_xlim(0, 125.)
                    if i == 0 and jj == ncols-1:
                        ax[i, jj].legend(frameon=False)
            return f


class VARCNN(BaseModel):
    """VAR-CNN.

    For details see [1].

    References
    ----------
        [1] I. Zubarev, et al., Adaptive neural network classifier for
        decoding MEG signals. Neuroimage. (2019) May 4;197:425-434
    """
    def __init__(self, Dataset, specs=dict()):
        """
        Parameters
        ----------
        Dataset : mneflow.Dataset

        specs : dict
                dictionary of model hyperparameters {

        n_latent : int
            Number of latent components.
            Defaults to 32.

        nonlin : callable
            Activation function of the temporal convolution layer.
            Defaults to tf.nn.relu

        filter_length : int
            Length of spatio-temporal kernels in the temporal
            convolution layer. Defaults to 7.

        pooling : int
            Pooling factor of the max pooling layer. Defaults to 2

        pool_type : str {'avg', 'max'}
            Type of pooling operation. Defaults to 'max'.

        padding : str {'SAME', 'FULL', 'VALID'}
            Convolution padding. Defaults to 'SAME'.}"""
        specs.setdefault('filter_length', 7)
        specs.setdefault('n_latent', 32)
        specs.setdefault('pooling', 2)
        specs.setdefault('stride', 2)
        specs.setdefault('padding', 'SAME')
        specs.setdefault('pool_type', 'max')
        specs.setdefault('nonlin', tf.nn.relu)
        specs.setdefault('l1', 3e-4)
        specs.setdefault('l2', 0)
        specs.setdefault('l1_scope', ['fc', 'demix', 'lf_conv'])
        specs.setdefault('l2_scope', [])
        specs.setdefault('maxnorm_scope', [])
        super(VARCNN, self).__init__(Dataset, specs)

    def build_graph(self):
        """Build computational graph using defined placeholder `self.X`
        as input.

        Returns
        --------
        y_pred : tf.Tensor
            Output of the forward pass of the computational graph.
            Prediction of the target variable.
        """
        self.dmx = DeMixing(size=self.specs['n_latent'], nonlin=tf.identity,
                            axis=3, specs=self.specs)(self.inputs)
        
        
        self.tconv = VARConv(size=self.specs['n_latent'],
                             nonlin=self.specs['nonlin'],
                             filter_length=self.specs['filter_length'],
                             padding=self.specs['padding'],
                             specs=self.specs
                             )(self.dmx)

        self.pooled = TempPooling(pooling=self.specs['pooling'],
                                  pool_type=self.specs['pool_type'],
                                  stride=self.specs['stride'],
                                  padding=self.specs['padding'],
                                  )(self.tconv)

        dropout = Dropout(self.specs['dropout'],
                          noise_shape=None)(self.pooled)

        self.fin_fc = Dense(size=self.out_dim, nonlin=tf.identity,
                            specs=self.specs)

        y_pred = self.fin_fc(dropout)

        return y_pred


class LFCNN3(LFCNN):
    """Time-Invaraint LFCNN.

    For details see [1].

    References
    ----------
        [1] I. Zubarev, et al., Adaptive neural network classifier for
        decoding MEG signals. Neuroimage. (2019) May 4;197:425-434
    """
    def __init__(self, Dataset, specs=dict()):
        """
                Parameters
        ----------
        Dataset : mneflow.Dataset

        specs : dict
                dictionary of model hyperparameters {

        n_latent : int
            Number of latent components.
            Defaults to 32.

        nonlin : callable
            Activation function of the temporal convolution layer.
            Defaults to tf.nn.relu

        filter_length : int
            Length of spatio-temporal kernels in the temporal
            convolution layer. Defaults to 7.

        pooling : int
            Pooling factor of the max pooling layer. Defaults to 2

        pool_type : str {'avg', 'max'}
            Type of pooling operation. Defaults to 'max'.

        padding : str {'SAME', 'FULL', 'VALID'}
            Convolution padding. Defaults to 'SAME'.}
        """
        specs.setdefault('filter_length', 32)
        specs.setdefault('n_latent', 32)
        specs.setdefault('pooling', 6)
        specs.setdefault('stride', 6)
        specs.setdefault('pool_type', 'SAME')
        specs.setdefault('nonlin', tf.nn.relu)
        specs.setdefault('l1', 3e-4)
        specs.setdefault('l2', 3e-2)
        specs.setdefault('l1_scope', ['fc'])
        specs.setdefault('l2_scope', ['demix', 'lf_conv'])
        specs.setdefault('maxnorm_scope', [])
        specs.setdefault('model_path', self.dataset.h_params['save_path'])
        super(LFCNN, self).__init__(Dataset, specs)



    def build_graph(self):
        """Build computational graph using defined placeholder `self.X`
        as input.

        Returns
        --------
        y_pred : tf.Tensor
            Output of the forward pass of the computational graph.
            Prediction of the target variable.
        """
        self.dmx = DeMixing(size=self.specs['n_latent'], nonlin=tf.identity,
                            axis=3, specs=self.specs)(self.inputs)

        self.tconv = LFTConv(size=self.specs['n_latent'],
                             nonlin=self.specs['nonlin'],
                             filter_length=self.specs['filter_length'],
                             padding=self.specs['padding'],
                             specs=self.specs
                             )(self.dmx)

        self.pooled = TempPooling(pooling=self.specs['pooling'],
                                  pool_type=self.specs['pool_type'],
                                  stride=self.specs['stride'],
                                  padding=self.specs['padding'],
                                  )(self.tconv)

        self.pooled2 = TempPooling(pooling=self.specs['pooling'],
                                   pool_type=self.specs['pool_type'],
                                   stride=self.specs['stride'],
                                   padding=self.specs['padding'],
                                   )(self.pooled)

        self.pooled3 = TempPooling(pooling=self.specs['pooling'],
                                   pool_type='max',
                                   stride=self.specs['stride'],
                                   padding=self.specs['padding'],
                                   )(self.pooled2)

        dropout = Dropout(self.specs['dropout'],
                          noise_shape=None)(self.pooled3)

        self.fin_fc = Dense(size=self.out_dim, nonlin=tf.identity,
                            specs=self.specs)

        y_pred = self.fin_fc(dropout)

        return y_pred


class FBCSP_ShallowNet(BaseModel):
    """
    Shallow ConvNet model from [2a]_.
    References
    ----------
    .. [2a] Schirrmeister, R. T., Springenberg, J. T., Fiederer, L. D. J.,
       Glasstetter, M., Eggensperger, K., Tangermann, M., Hutter, F. & Ball, T. (2017).
       Deep learning with convolutional neural networks for EEG decoding and
       visualization.
       Human Brain Mapping , Aug. 2017. Online: http://dx.doi.org/10.1002/hbm.23730
    """
    def __init__(self, Dataset, specs=dict()):
        self.scope = 'fbcsp-ShallowNet'
        specs.setdefault('filter_length', 25)
        specs.setdefault('n_latent', 40)
        specs.setdefault('pooling', 75)
        specs.setdefault('stride', 15)
        specs.setdefault('pool_type', 'avg')
        specs.setdefault('padding', 'SAME')
        specs.setdefault('nonlin', tf.nn.relu)
        specs.setdefault('l1', 3e-4)
        specs.setdefault('l2', 3e-2)
        specs.setdefault('l1_scope', [])
        specs.setdefault('l2_scope', ['conv', 'fc'])
        specs.setdefault('maxnorm_scope', [])
        super(FBCSP_ShallowNet, self).__init__(Dataset, specs)

    def build_graph(self):

        """Temporal conv_1 25 10x1 kernels"""
        #(self.inputs)
        inputs = tf.transpose(self.inputs,[0,3,2,1])
        #print(inputs.shape)
        #df = "channels_first"
        tconv1 = DepthwiseConv2D(
                        kernel_size=(1, self.specs['filter_length']),
                        depth_multiplier = self.specs['n_latent'],
                        strides=1,
                        padding="VALID",
                        activation = tf.identity,
                        kernel_initializer="he_uniform",
                        bias_initializer=Constant(0.1),
                        data_format="channels_last",
                        kernel_regularizer=k_reg.l2(self.specs['l2'])
                        #kernel_constraint="maxnorm"
                        )

        tconv1_out = tconv1(inputs)
        print('tconv1: ', tconv1_out.shape) #should be n_batch, sensors, times, kernels

        sconv1 = Conv2D(filters=self.specs['n_latent'],
                        kernel_size=(self.dataset.h_params['n_ch'], 1),
                        strides=1,
                        padding="VALID",
                        activation = tf.square,
                        kernel_initializer="he_uniform",
                        bias_initializer=Constant(0.1),
                        data_format="channels_last",
                        #data_format="channels_first",
                        kernel_regularizer=k_reg.l2(self.specs['l2']))


        sconv1_out = sconv1(tconv1_out)
        print('sconv1:',  sconv1_out.shape)

        pool1 = TempPooling(pooling=self.specs['pooling'],
                                  pool_type="avg",
                                  stride=self.specs['stride'],
                                  padding='SAME',
                                  )(sconv1_out)

        print('pool1: ', pool1.shape)
        fc_out = Dense(size=self.out_dim,
                       nonlin=tf.identity)
        y_pred = fc_out(tf.keras.backend.log(pool1))
        return y_pred
#
#
##class LFLSTM(LFCNN):
##    # TODO! Gabi: check that the description describes the model
##    """LF-CNN-LSTM
##
##    For details see [1].
##
##    Parameters
##    ----------
##    n_latent : int
##        number of latent components
##        Defaults to 32
##
##    filter_length : int
##        length of spatio-temporal kernels in the temporal
##        convolution layer. Defaults to 7
##
##    stride : int
##        stride of the max pooling layer. Defaults to 1
##
##    pooling : int
##        pooling factor of the max pooling layer. Defaults to 2
##
##    References
##    ----------
##        [1]  I. Zubarev, et al., Adaptive neural network classifier for
##        decoding MEG signals. Neuroimage. (2019) May 4;197:425-434
##    """
##
##    def build_graph(self):
##        self.scope = 'lf-cnn-lstm'
##
##        self.demix = DeMixing(n_latent=self.specs['n_latent'], axis=1)
##        dmx = self.demix(self.X)
##        dmx = tf.reshape(dmx, [-1, self.dataset.h_params['n_t'],
##                               self.specs['n_latent']])
##        dmx = tf.expand_dims(dmx, -1)
##        print('dmx-sqout:', dmx.shape)
##
##        self.tconv1 = LFTConv(scope="conv",
##                              n_latent=self.specs['n_latent'],
##                              nonlin=tf.nn.relu,
##                              filter_length=self.specs['filter_length'],
###                              stride=self.specs['stride'],
###                              pooling=self.specs['pooling'],
##                              padding=self.specs['padding'])
##
##        features = self.tconv1(dmx)
##        pool1 = TempPooling(stride=self.specs['stride'],
##                            pooling=self.specs['pooling'],
##                            padding='SAME',
##                            pool_type='max')
##
##        pool2 = TempPooling(stride=self.specs['stride'],
##                            pooling=self.specs['pooling'],
##                            padding='SAME',
##                            pool_type='max')
##
##        pool3 = TempPooling(stride=self.specs['stride'],
##                            pooling=self.specs['pooling'],
##                            padding='SAME',
##                            pool_type='avg')
##
##        print('features:', pool3.shape)
##        pooled = pool3(pool2(pool1(features)))
##
##        fshape = tf.multiply(pooled.shape[1], pooled.shape[2])
##
##        ffeatures = tf.reshape(pooled,
##                              [-1, self.dataset.h_params['n_seq'], fshape])
##        #  features = tf.expand_dims(features, 0)
##        l1_lambda = self.optimizer.params['l1_lambda']
##        print('flat features:', ffeatures.shape)
##        self.lstm = LSTMv1(scope="lstm",
##                           size=self.specs['n_latent'],
##                           kernel_initializer='glorot_uniform',
##                           recurrent_initializer='orthogonal',
##                           recurrent_regularizer=k_reg.l1(l1_lambda),
##                           kernel_regularizer=k_reg.l2(l1_lambda),
##                           # bias_regularizer=None,
##                           # activity_regularizer= regularizers.l1(0.01),
##                           # kernel_constraint= constraints.UnitNorm(axis=0),
##                           # recurrent_constraint= constraints.NonNeg(),
##                           # bias_constraint=None,
##                           # dropout=0.1, recurrent_dropout=0.1,
##                           nonlin=tf.nn.tanh,
##                           unit_forget_bias=False,
##                           return_sequences=False,
##                           unroll=False)
##
##        lstm_out = self.lstm(ffeatures)
##        print('lstm_out:', lstm_out.shape)
##        # if 'n_seq' in self.dataset.h_params.keys():
##        #    lstm_out = tf.reshape(lstm_out, [-1,
##        #                                     self.dataset.h_params['n_seq'],
##        #                                     self.specs['n_latent']])
##
##        self.fin_fc = Dense(size=self.out_dim,
##                            nonlin=tf.identity, dropout=0.)
###        self.fin_fc = DeMixing(n_latent=self.out_dim,
###                               nonlin=tf.identity, axis=-1)
##        y_pred = self.fin_fc(lstm_out)
##        # print(y_pred)
##        return y_pred
#
#
class Deep4(BaseModel):
    """
    Deep ConvNet model from [2b]_.
    References
    ----------
    .. [2b] Schirrmeister, R. T., Springenberg, J. T., Fiederer, L. D. J.,
       Glasstetter, M., Eggensperger, K., Tangermann, M., Hutter, F. & Ball, T. (2017).
       Deep learning with convolutional neural networks for EEG decoding and
       visualization.
       Human Brain Mapping , Aug. 2017. Online: http://dx.doi.org/10.1002/hbm.23730
    """
    def __init__(self, Dataset, specs=dict()):
        self.scope = 'deep4'
        specs.setdefault('filter_length', 10)
        specs.setdefault('n_latent', 25)
        specs.setdefault('pooling', 3)
        specs.setdefault('stride', 3)
        specs.setdefault('pool_type', 'max')
        specs.setdefault('padding', 'SAME')
        specs.setdefault('nonlin', tf.nn.elu)
        specs.setdefault('l1', 3e-4)
        specs.setdefault('l2', 3e-2)
        specs.setdefault('l1_scope', [])
        specs.setdefault('l2_scope', ['conv', 'fc'])
        specs.setdefault('maxnorm_scope', [])
        specs.setdefault('model_path', './model/')
        super(Deep4, self).__init__(Dataset, specs)

    def build_graph(self):
        self.scope = 'deep4'

        inputs = tf.transpose(self.inputs,[0,3,2,1])

        tconv1 = DepthwiseConv2D(
                        kernel_size=(1, self.specs['filter_length']),
                        depth_multiplier = self.specs['n_latent'],
                        strides=1,
                        padding=self.specs['padding'],
                        activation = tf.identity,
                        kernel_initializer="he_uniform",
                        bias_initializer=Constant(0.1),
                        data_format="channels_last",
                        kernel_regularizer=k_reg.l2(self.specs['l2'])
                        #kernel_constraint="maxnorm"
                        )
        tconv1_out = tconv1(inputs)
        print('tconv1: ', tconv1_out.shape) #should be n_batch, sensors, times, kernels

        sconv1 = Conv2D(filters=self.specs['n_latent'],
                        kernel_size=(self.dataset.h_params['n_ch'], 1),
                        strides=1,
                        padding=self.specs['padding'],
                        activation=self.specs['nonlin'],
                        kernel_initializer="he_uniform",
                        bias_initializer=Constant(0.1),
                        data_format="channels_last",
                        #data_format="channels_first",
                        kernel_regularizer=k_reg.l2(self.specs['l2']))
        sconv1_out = sconv1(tconv1_out)
        print('sconv1:',  sconv1_out.shape)

        pool1 = TempPooling(pooling=self.specs['pooling'],
                                  pool_type="avg",
                                  stride=self.specs['stride'],
                                  padding='SAME',
                                  )(sconv1_out)

        print('pool1: ', pool1.shape)

        ############################################################

        tsconv2 = Conv2D(filters=self.specs['n_latent']*2,
                        kernel_size=(1, self.specs['filter_length']),
                        strides=1,
                        padding=self.specs['padding'],
                        activation=self.specs['nonlin'],
                        kernel_initializer="he_uniform",
                        bias_initializer=Constant(0.1),
                        data_format="channels_last",
                        #data_format="channels_first",
                        kernel_regularizer=k_reg.l2(self.specs['l2']))


        tsconv2_out = tsconv2(pool1)
        print('tsconv2:',  tsconv2_out.shape)

        pool2 = TempPooling(pooling=self.specs['pooling'],
                                  pool_type="avg",
                                  stride=self.specs['stride'],
                                  padding='SAME',
                                  )(tsconv2_out)

        print('pool2: ', pool2.shape)


        ############################################################

        tsconv3 = Conv2D(filters=self.specs['n_latent']*4,
                        kernel_size=(1, self.specs['filter_length']),
                        strides=1,
                        padding=self.specs['padding'],
                        activation=self.specs['nonlin'],
                        kernel_initializer="he_uniform",
                        bias_initializer=Constant(0.1),
                        data_format="channels_last",
                        #data_format="channels_first",
                        kernel_regularizer=k_reg.l2(self.specs['l2']))


        tsconv3_out = tsconv3(pool2)
        print('tsconv3:',  tsconv3_out.shape)

        pool3 = TempPooling(pooling=self.specs['pooling'],
                                  pool_type="avg",
                                  stride=self.specs['stride'],
                                  padding='SAME',
                                  )(tsconv3_out)

        print('pool3: ', pool3.shape)

        ############################################################

        tsconv4 = Conv2D(filters=self.specs['n_latent']*8,
                        kernel_size=(1, self.specs['filter_length']),
                        strides=1,
                        padding=self.specs['padding'],
                        activation=self.specs['nonlin'],
                        kernel_initializer="he_uniform",
                        bias_initializer=Constant(0.1),
                        data_format="channels_last",
                        #data_format="channels_first",
                        kernel_regularizer=k_reg.l2(self.specs['l2']))


        tsconv4_out = tsconv4(pool3)
        print('tsconv4:',  tsconv4_out.shape)

        pool4 = TempPooling(pooling=self.specs['pooling'],
                                  pool_type="avg",
                                  stride=self.specs['stride'],
                                  padding='SAME',
                                  )(tsconv4_out)

        print('pool4: ', pool4.shape)


        fc_out = Dense(size=self.out_dim, nonlin=tf.identity)
        y_pred = fc_out(pool4)
        return y_pred
#
#

class EEGNet(BaseModel):
    """EEGNet.

    Parameters
    ----------
    specs : dict

        n_latent : int
            Number of (temporal) convolution kernrels in the first layer.
            Defaults to 8

        filter_length : int
            Length of temporal filters in the first layer.
            Defaults to 32

        stride : int
            Stride of the average polling layers. Defaults to 4.

        pooling : int
            Pooling factor of the average polling layers. Defaults to 4.

        dropout : float
            Dropout coefficient.

    References
    ----------
    [3] V.J. Lawhern, et al., EEGNet: A compact convolutional neural
    network for EEG-based brain–computer interfaces 10 J. Neural Eng.,
    15 (5) (2018), p. 056013

    [4] Original EEGNet implementation by the authors can be found at
    https://github.com/vlawhern/arl-eegmodels
    """
    def __init__(self, Dataset, specs=dict()):
        self.scope = 'eegnet'
        specs.setdefault('filter_length', 64)
        specs.setdefault('depth_multiplier', 2)
        specs.setdefault('n_latent', 8)
        specs.setdefault('pooling', 4)
        specs.setdefault('stride', 4)
        specs.setdefault('dropout', 0.5)
        specs.setdefault('padding', 'same')
        specs.setdefault('nonlin', 'elu')
        specs.setdefault('maxnorm_rate', 0.25)
        specs.setdefault('model_path', './model/')
        super(EEGNet, self).__init__(Dataset, specs)

        
        
    def build_graph(self):
        self.scope = 'eegnet8'
        
        inputs = tf.transpose(self.inputs,[0,3,2,1])
        
        dropoutType = Dropout
        
        block1       = Conv2D(self.specs['n_latent'], 
                              (1, self.specs['filter_length']), 
                              padding = self.specs['padding'],
                              input_shape = (1, self.dataset.h_params['n_ch'], 
                                             self.dataset.h_params['n_t']),
                              use_bias = False)(inputs)
        block1       = BatchNormalization(axis = 1)(block1)
        print("Batchnorm:", block1.shape)
        block1       = DepthwiseConv2D((self.dataset.h_params['n_ch'], 1), 
                                       use_bias = False, 
                                       depth_multiplier = self.specs['depth_multiplier'],
                                       depthwise_constraint = constraints.MaxNorm(1.))(block1)
        block1       = BatchNormalization(axis = 1)(block1)
        block1       = layers.Activation(self.specs['nonlin'])(block1)
        block1       = layers.AveragePooling2D((1, self.specs['pooling']))(block1)
        print("Pooling 1:", block1.shape)
        block1       = dropoutType(self.specs['dropout'])(block1)
        
        block2       = SeparableConv2D(self.specs['n_latent']*self.specs['depth_multiplier'], (1, self.specs['filter_length']//self.specs["pooling"]),
                                       use_bias = False, padding = self.specs['padding'])(block1)
        block2       = BatchNormalization(axis = 1)(block2)
        print("Batchnorm 2:", block2.shape)
        
        block2       = layers.Activation(self.specs['nonlin'])(block2)
        block2       = layers.AveragePooling2D((1, self.specs['pooling']*2))(block2)
        block2       = dropoutType(self.specs['dropout'])(block2)
        print("Pooling 2:", block2.shape)
        
        fin_fc = Dense(size=self.out_dim, nonlin=tf.identity)
        y_pred = fin_fc(block2)
        
        return y_pred

