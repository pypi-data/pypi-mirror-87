from abc import ABC, abstractmethod

from sklearn.metrics import classification_report, log_loss, roc_auc_score, make_scorer, confusion_matrix, roc_curve, auc, precision_recall_curve
from sklearn.decomposition import PCA
from sklearn.calibration import calibration_curve
from mlxtend.plotting import plot_decision_regions
from dask_ml.model_selection import GridSearchCV as DaskGridSearchCV
import pandas as pd
import numpy as np
from copy import deepcopy

from sklearn.pipeline import make_pipeline

import matplotlib.pyplot as plt
import seaborn as sns
plt.style.use("ggplot")

import keras
from keras.layers import Dense, Activation, Dropout
from keras.models import Sequential
from keras import backend as K
from keras import regularizers
from keras.utils import to_categorical

from sklearn.ensemble import GradientBoostingClassifier

from sklearn.experimental import enable_hist_gradient_boosting
from sklearn.ensemble import HistGradientBoostingClassifier

from sklearn.linear_model import LogisticRegression

from sklearn.neural_network import MLPClassifier

from sklearn.naive_bayes import MultinomialNB

from sklearn.ensemble import RandomForestClassifier

from sklearn.svm import SVC

from xgboost import XGBClassifier

from vecstack import stacking


class Model(ABC):
  @abstractmethod
  def train(self, train_vector, labels, params):
    '''
    Args:
      train_vector: numpy array with transformed fingerprint data
      labels:       numpy array of labels 0 and 1
      params:       parameters needed to train the model

    Returns:
      None
    '''
    pass

  @abstractmethod
  def performance_metrics(self, test_vector, labels):
    '''
    Args:
      test_vector: numpy array with transformed fingerprint data
      labels:      numpy array of labels 0 and 1

    Returns:
      metrics: dictionary of important metrics
    '''
    pass

  @abstractmethod
  def predict(self, vector):
    '''
    Args:
      vector: numpy array containing the transformed fingerprint(s) data
      list:   list

    Returns:
      predictions: Dictionary containing fingerprint, prediction, prediction probability as lists
    '''
    pass

  @abstractmethod
  def grid_search_train(self, train_vector, labels, param_grid, scorer):
    '''
    Args:
      train_vector: numpy array with transformed fingerprint data
      labels:       numpy array of labels 0 and 1
      param_grid:   dictionary of parameters to pass in
    Returns:
      None
    '''
    pass

class BaseModel(Model):
  def __init__(self, classification_threshold=0.5):
    self.fit_model            = None
    self.untrained_classifier = None
    self.train_vector         = None
    self.train_labels         = None
    self.threshold            = classification_threshold

  def train(self, train_vector, labels, classifier):
    '''
    Args:
      train_vector: numpy array with transformed fingerprint data
      labels:       numpy array of labels 0 and 1
      classifier:   the model to fit on

    Returns:
      fit_model: the trained model with parameters
    '''
    self.untrained_classifier = classifier
    self.fit_model            = classifier.fit(train_vector, labels)
    self.train_vector         = train_vector
    self.train_labels         = labels

  def performance_metrics(self, test_vector, labels):
    '''
    Args:
      test_vector: numpy array with transformed data
      labels:      numpy array of labels 0 and 1

    Returns:
      metrics: dictionary of important metrics
    '''
    y_pred_prob = self.fit_model.predict_proba(test_vector)
    y_pred = [1 if prob>=self.threshold else 0 for prob in y_pred_prob[:, 1]] ## will need to make THRESHOLD VARIABLE

    cr  = classification_report(labels, y_pred, output_dict=True)
    classification_report_df = round(pd.DataFrame(cr),3)

    ## ROC AUC
    ##==============
    try:
      roc_auc = round(roc_auc_score(labels,  y_pred_prob[:,1]),3)
    except ValueError:
      roc_auc = None
    ## Log Loss
    ##==============
    try:
      model_log_loss = round(log_loss(labels, y_pred_prob),3)
    except ValueError:
      model_log_loss = None

    ## THRESHOLD VALUE
    ##==============
    # calculate roc curves, convert to f score, locate the index of the largest f score
    precision, recall, thresholds = precision_recall_curve(labels, np.array(y_pred_prob[:,1]))
    fscore = (2 * precision * recall) / (precision + recall)
    ix = np.argmax(fscore)
    best_threshold = round(thresholds[ix], 3)

    ## Avg Metrics
    ##==============
    precision = classification_report_df['macro avg']['precision']
    recall    = classification_report_df['macro avg']['recall']
    f1_score  = classification_report_df['macro avg']['f1-score']
    accuracy  = classification_report_df['accuracy'][0]

    ## Recall on Crash and Non-crash
    ##==============================
    specificity = classification_report_df.loc['recall'][0]
    sensitivity = classification_report_df.loc['recall'][1]

    ## Precision on Crash and Non-crash
    ##==============================
    prec_noncrash = classification_report_df.loc['precision'][0]
    prec_crash    = classification_report_df.loc['precision'][1]

    ## F1 Score on Crash and Non-crash
    ##==============================
    f1_noncrash = classification_report_df.loc['f1-score'][0]
    f1_crash    = classification_report_df.loc['f1-score'][1]

    ## John's Accuracy
    ##================
    measure_1 = 1 - specificity
    john_accuracy = round(sensitivity - measure_1,3)

    all_metrics ={'accuracy'                   : accuracy,
                  'precision_overall'          : precision,
                  'recall_overall'             : recall,
                  'f1_score_overall'           : f1_score,
                  'precision_negclass'         : prec_noncrash,
                  'precision_posclass'         : prec_crash,
                  'recall_negclass_specificity': specificity,
                  'recall_posclass_sensitivity': sensitivity,
                  'f1_score_negclass'          : f1_noncrash,
                  'f1_score_posclass'         : f1_crash,
                  'suggested_predict_thresh'   : best_threshold,
                  'log_loss'                   : model_log_loss,
                  'roc_auc'                    : roc_auc,
                  'discrepancy_metric'         : john_accuracy,}

    return all_metrics

  def predict(self, vector):
    '''
    Args:
      vector: numpy array containing the non-transformed or transformed data

    Returns:
      predictions: Dictionary containing prediction, prediction probability as lists
    '''
    y_pred_prob    = self.fit_model.predict_proba(vector)
    y_pred = [1 if prob>=self.threshold else 0 for prob in y_pred_prob[:, 1]]
    predictions = {'predictions' : np.array(y_pred), 'probabilities' : np.array(y_pred_prob[:,1])}

    return predictions

  def grid_search_train(self, train_vector, labels, classifier, param_grid, scorer=None):
    '''
    Args:
      train_vector: numpy array with transformed data
      labels:       numpy array of labels 0 and 1
      classifier:   the model to fit on
      param_grid:   dictionary of parameters to pass in
      scorer:

    Returns:
      None
    '''
    if scorer is None:
      custom_scorer = make_scorer(self._discrepancy_metric, greater_is_better=True)
      best_model = DaskGridSearchCV(estimator = classifier, param_grid = param_grid, scoring=custom_scorer, refit=True, cv=5)
      print('maximizing for', custom_scorer)
    else:
      best_model = DaskGridSearchCV(estimator = classifier, param_grid = param_grid, scoring=scorer, refit=True, cv=5)
      print('maximizing for', scorer)

    self.fit_model = best_model.fit(train_vector, labels)
    print('best grid search parameters:', best_model.best_params_)

    self.untrained_classifier = classifier.set_params(**best_model.best_params_)
    self.train_vector         = train_vector
    self.train_labels         = labels

  def _discrepancy_metric(self, labels, predictions):
    cr  = classification_report(labels, predictions, output_dict=True)
    classification_report_df = pd.DataFrame(cr)
    specificity = classification_report_df.loc['recall'][0]
    sensitivity = classification_report_df.loc['recall'][1]
    measure_1 = 1 - specificity
    john_accuracy = sensitivity - measure_1
    return john_accuracy

  def visualize(self, vector, labels):
    '''
    Args:
      vector: numpy array with non-transformed or transformed data
      labels: numpy array of labels 0 and 1

    Returns:
      None
      Plots and Visualizations
    '''

    predictions = self.predict(vector)
    metrics     = self.performance_metrics(vector, labels)

    ## 1) Confusion Matrix
    print('Confusion Matrix:')
    print(confusion_matrix(labels, predictions['predictions']))

    ## 2) Classification Report
    print('\nClassification Report:')
    print(classification_report(labels, predictions['predictions']))

    ## 3) Performance Metrics
    print('\nMetrics:')
    df_metrics = pd.DataFrame.from_dict(metrics, orient='index')
    print(df_metrics)

    ## 4) Calibration Plot
    fraction_of_positives, mean_predicted_value = calibration_curve(labels, predictions['probabilities'], n_bins=10)
    plt.figure(figsize=(18, 10))
    ax1 = plt.subplot2grid((3, 1), (0, 0), rowspan=3)
    ax1.plot([0, 1], [0, 1], "k:", label="Perfectly calibrated")
    ax1.plot(mean_predicted_value, fraction_of_positives, "s-",
              label="%s" % ('Model', ))
    ax1.set_ylabel("Fraction of positives")
    ax1.set_ylim([-0.05, 1.05])
    ax1.legend(loc="lower right")
    ax1.set_title('Calibration plots  (reliability curve)')
    plt.tight_layout()

    ## 5) PREDICTION PROBABILITY CHART
    plt.figure(figsize=(18,6))
    rc={'font.size': 20, 'axes.labelsize': 20, 'legend.fontsize': 20, 'axes.titlesize': 25, 'xtick.labelsize': 15, 'ytick.labelsize': 15, }
    sns.set_context(rc=rc, )
    plt.hist(predictions['probabilities'], bins=10, histtype="step", lw=2 )
    plt.grid(True)
    plt.xticks(np.arange(0, 1, step=0.1))
    plt.xlabel("Prediction Probability Distribution")

    ## 6) True Positive Rate vs False Positive Rate
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(nrows=2, ncols=2, sharex=False, sharey=False )
    fig.set_size_inches(15,15)
    fpr, tpr, thresh_roc = roc_curve(labels, predictions['probabilities'])
    roc_auc = auc(fpr, tpr)
    ax1.plot(fpr, tpr, color='darkorange', lw=2, label='AUC = %0.2f'% roc_auc)
    ax1.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
    ax1.set_xlim([-0.05, 1.0])
    ax1.set_ylim([0.0, 1.05])
    ax1.set_xlabel('False Positive Rate')
    ax1.set_ylabel('True Positive Rate')
    ax1.legend(loc="lower right", fontsize='small')

    ## 7) Precision-Recall Curve
    precision, recall, thresh_prc = precision_recall_curve(labels, predictions['probabilities'])
    ax2.plot(recall, precision, color='blue', lw=2, label='Precision-Recall curve')
    ax2.set_xlim([0.0, 1.0])
    ax2.set_ylim([0.0, 1.05])
    ax2.set_xlabel('Recall')
    ax2.set_ylabel('Precision')
    ax2.legend(loc="lower left", fontsize='small')

    ## 8) Percentage of False Positives and True Positives as you increase threshold for crashing
    ax3.plot(thresh_roc, fpr, color='red', lw=2, label='FPR')
    ax3.plot(thresh_roc, tpr, color='green',label='TPR')
    ax3.set_xlim([0.0, 1.0])
    ax3.set_ylim([0.0, 1.05])
    ax3.set_xlabel('Threshold')
    ax3.set_ylabel('%')
    ax3.legend(loc='upper right', fontsize='small')

    ## 9) Balance of Precision and Recall
    thresh_prc = np.append(thresh_prc,1)
    ax4.plot(thresh_prc, precision, color='red', lw=2, label='Precision')
    ax4.plot(thresh_prc, recall, color='green',label='Recall')
    ax4.set_xlim([0.0, 1.0])
    ax4.set_ylim([0.0, 1.05])
    ax4.set_xlabel('Threshold')
    ax4.set_ylabel('%')
    ax4.legend(loc='lower left', fontsize='small')

    # 10) Decision Boundary Plots
    pca, pca_model = self._pca_reduce()
    pca_vector     = pca.transform(vector)
    fig            = plt.figure(figsize=(18, 10))
    plot_decision_regions(pca_vector, labels, clf=pca_model, legend=1)

  def _pca_reduce(self):
    pca = PCA(n_components = 2)
    pca.fit(self.train_vector)
    train_pca_vector = pca.transform(self.train_vector)
    pca_classifier   = deepcopy(self.untrained_classifier) ## get a deep copy of the untrained classifier
    pca_model        = pca_classifier.fit(train_pca_vector, self.train_labels)
    return pca, pca_model

class DeepLearningModel(BaseModel):
    def __init__(self, val_vector = None, val_labels = None, saved_model = None):
        self.history    = None
        self.val_vector = val_vector
        self.val_labels = val_labels
        self.validation_data = None

        if self.val_vector is not None: # if self.val_vector.any():
            self.validation_data = (self.val_vector, to_categorical(self.val_labels))
        else:
            self.validation_data = None

        if saved_model:
            self.fit_model = saved_model

    def train(self, train_vector, labels, params):

        ## SHOULD THESE BE USED AS PARAMETERS?
        input_dim = train_vector.shape[1]
        model = Sequential(
                [Dense(1268, input_dim=input_dim), # Layer List then pass to sequential
                 Activation('relu'),
                 Dropout(0.2),
                 Dense(512, kernel_regularizer=regularizers.l2(0.02)),
                 Activation('relu'),
                 Dropout(0.2),
                 Dense(2),
                 Activation('sigmoid'),])

        ## THIS CAN BE KEPT THE SAME
        model.compile(loss='binary_crossentropy',
                      optimizer='adam',
                      metrics=['accuracy', self.recall]) # change to John Accuracy?

        ## DOES THIS NEED TO BE CHANGED?
        self.history = model.fit(train_vector, to_categorical(labels), batch_size=16, epochs=20, verbose=1,
                                 validation_data=self.validation_data)
        self.fit_model = model

    def recall(self, y_true, y_pred):
            true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
            possible_positives = K.sum(K.round(K.clip(y_true, 0, 1)))
            recall = true_positives / (possible_positives + K.epsilon())
            return recall

    def predict(self, vector):
        y_pred_prob    = self.fit_model.predict(vector)
        y_pred         = self.fit_model.predict_classes(vector)
        predictions = {'predictions' : y_pred, 'probabilities' : y_pred_prob}
        return predictions

    def performance_metrics(self, test_vector, labels):

        ## recompile, just in case
        self.fit_model.compile(loss='binary_crossentropy', optimizer='adam',
                                metrics=['accuracy', self.recall])

        y_pred_prob = self.fit_model.predict(test_vector)
        y_pred      = self.fit_model.predict_classes(test_vector)

        cr  = classification_report(labels, y_pred, output_dict=True)
        classification_report_df = round(pd.DataFrame(cr),3)

        ## ROC AUC
        ##==============
        roc_auc = round(roc_auc_score(labels,  y_pred_prob[:, 1]),3)
        ## Binary Cross Entropy Loss
        ##==============
        loss = round(self.fit_model.evaluate(test_vector, to_categorical(labels))[0], 3)

        ## Avg Metrics
        ##==============
        precision = classification_report_df['macro avg']['precision']
        recall    = classification_report_df['macro avg']['recall']
        f1_score  = classification_report_df['macro avg']['f1-score']
        accuracy  = classification_report_df['accuracy'][0]

        ## Recall on Crash and Non-crash
        ##==============================
        specificity = classification_report_df.loc['recall'][0]
        sensitivity = classification_report_df.loc['recall'][1]

        ## Precision on Crash and Non-crash
        ##==============================
        prec_noncrash = classification_report_df.loc['precision'][0]
        prec_crash    = classification_report_df.loc['precision'][1]

        ## F1 Score on Crash and Non-crash
        ##==============================
        f1_noncrash = classification_report_df.loc['f1-score'][0]
        f1_crash    = classification_report_df.loc['f1-score'][1]

        ## John's Accuracy
        ##================
        measure_1 = 1 - specificity
        john_accuracy = round(sensitivity - measure_1,3)

        all_metrics ={'accuracy'                   : accuracy,
                      'precision_overall'          : precision,
                      'recall_overall'             : recall,
                      'f1_score_overall'           : f1_score,
                      'precision_negclass'         : prec_noncrash,
                      'precision_posclass'         : prec_crash,
                      'recall_negclass_specificity': specificity,
                      'recall_posclass_sensitivity': sensitivity,
                      'f1_score_negclass'          : f1_noncrash,
                      'f1_score_posclass'          : f1_crash,
                      'log_loss'                   : loss,
                      'roc_auc'                    : roc_auc,
                      'discrepancy_metric'         : john_accuracy,}

        return all_metrics

    def visualize(self, vector, labels):
        '''
        Args:
          vector: numpy array with transformed data
          labels: numpy array of labels 0 and 1

        Returns:
          None
          Plots and Visualizations
        '''
        predictions = self.predict(vector)
        metrics     = self.performance_metrics(vector, labels)

        ## 1) Confusion Matrix
        print('Confusion Matrix:')
        print(confusion_matrix(labels, predictions['predictions']))

        ## 2) Classification Report
        print('\nClassification Report:')
        print(classification_report(labels, predictions['predictions']))

        ## 3) Performance Metrics
        print('\nMetrics:')
        df_metrics = pd.DataFrame.from_dict(metrics, orient='index')
        print(df_metrics)

        ## 4) Calibration Plot
        fraction_of_positives, mean_predicted_value = calibration_curve(labels, predictions['probabilities'][:, 1], n_bins=10)
        plt.figure(figsize=(18, 10))
        ax1 = plt.subplot2grid((3, 1), (0, 0), rowspan=3)
        ax1.plot([0, 1], [0, 1], "k:", label="Perfectly calibrated")
        ax1.plot(mean_predicted_value, fraction_of_positives, "s-",
                  label="%s" % ('Model', ))
        ax1.set_ylabel("Fraction of positives")
        ax1.set_ylim([-0.05, 1.05])
        ax1.legend(loc="lower right")
        ax1.set_title('Calibration plots  (reliability curve)')
        plt.tight_layout()

        ## 5) PREDICTION PROBABILITY CHART
        plt.figure(figsize=(18,6))
        rc={'font.size': 20, 'axes.labelsize': 20, 'legend.fontsize': 20, 'axes.titlesize': 25, 'xtick.labelsize': 15, 'ytick.labelsize': 15, }
        sns.set_context(rc=rc, )
        plt.hist(predictions['probabilities'][:, 1], bins=10, histtype="step", lw=2 )
        plt.grid(True)
        plt.xticks(np.arange(0, 1, step=0.1))
        plt.xlabel("Prediction Probability Distribution")

        ## 6) True Positive Rate vs False Positive Rate
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(nrows=2, ncols=2, sharex=False, sharey=False )
        fig.set_size_inches(15,15)
        fpr, tpr, thresh_roc = roc_curve(labels, predictions['probabilities'][:, 1])
        roc_auc = auc(fpr, tpr)
        ax1.plot(fpr, tpr, color='darkorange', lw=2, label='AUC = %0.2f'% roc_auc)
        ax1.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
        ax1.set_xlim([-0.05, 1.0])
        ax1.set_ylim([0.0, 1.05])
        ax1.set_xlabel('False Positive Rate')
        ax1.set_ylabel('True Positive Rate')
        ax1.legend(loc="lower right", fontsize='small')

        ## 7) Precision-Recall Curve
        precision, recall, thresh_prc = precision_recall_curve(labels, predictions['probabilities'][:, 1])
        ax2.plot(recall, precision, color='blue', lw=2, label='Precision-Recall curve')
        ax2.set_xlim([0.0, 1.0])
        ax2.set_ylim([0.0, 1.05])
        ax2.set_xlabel('Recall')
        ax2.set_ylabel('Precision')
        ax2.legend(loc="lower left", fontsize='small')

        ## 8) Percentage of False Positives and True Positives as you increase threshold for crashing
        ax3.plot(thresh_roc, fpr, color='red', lw=2, label='FPR')
        ax3.plot(thresh_roc, tpr, color='green',label='TPR')
        ax3.set_xlim([0.0, 1.0])
        ax3.set_ylim([0.0, 1.05])
        ax3.set_xlabel('Threshold')
        ax3.set_ylabel('%')
        ax3.legend(loc='upper right', fontsize='small')

        ## 9) Balance of Precision and Recall
        thresh_prc = np.append(thresh_prc,1)
        ax4.plot(thresh_prc, precision, color='red', lw=2, label='Precision')
        ax4.plot(thresh_prc, recall, color='green',label='Recall')
        ax4.set_xlim([0.0, 1.0])
        ax4.set_ylim([0.0, 1.05])
        ax4.set_xlabel('Threshold')
        ax4.set_ylabel('%')
        ax4.legend(loc='lower left', fontsize='small')

        ## 10) Plot training & validation loss values and Plot training & validation accuracy values
        if self.history:
            fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(15, 6))
            axes[0].plot(self.history.history['accuracy'], )
            if 'val_accuracy' in self.history.history:
                axes[0].plot(self.history.history['val_accuracy'])
            axes[0].title.set_text('Model accuracy')
            axes[0].set_ylabel('Accuracy')
            axes[0].set_xlabel('Epoch')
            if 'val_accuracy' in self.history.history:
                axes[0].legend(['Train', 'Test'], loc='lower right')
            else:
                axes[0].legend(['Train'], loc='lower right')
            axes[0].set_ylim(top =1.0)
            axes[0].set_ylim( bottom=0.0)

            axes[1].plot(self.history.history['loss'])
            if 'val_loss' in self.history.history:
                axes[1].plot(self.history.history['val_loss'])
            axes[1].title.set_text('Model loss')
            axes[1].set_ylabel('Loss')
            axes[1].set_xlabel('Epoch')
            if 'val_loss' in self.history.history:
                axes[1].legend(['Train', 'Test'], loc='upper left')
            else:
                axes[1].legend(['Train'], loc='lower right')
            axes[1].set_ylim(top =1.0)
            axes[1].set_ylim( bottom=0.0)

class GBC(BaseModel):
  def train(self, train_vector, labels, params):
    classifier = GradientBoostingClassifier(**params)
    super().train(train_vector, labels, classifier)

  def grid_search_train(self, train_vector, labels, param_grid, scorer=None):
    classifier = GradientBoostingClassifier()
    super().grid_search_train(train_vector, labels, classifier, param_grid, scorer)

class HGB(BaseModel):
  def train(self, train_vector, labels, params):
    classifier = HistGradientBoostingClassifier(**params)
    super().train(train_vector, labels, classifier)

  def grid_search_train(self, train_vector, labels, param_grid, scorer=None):
    classifier = HistGradientBoostingClassifier()
    super().grid_search_train(train_vector, labels, classifier, param_grid, scorer)

class LR(BaseModel):
  def train(self, train_vector, labels, params):
    classifier = LogisticRegression(**params)
    super().train(train_vector, labels, classifier)

  def grid_search_train(self, train_vector, labels, param_grid, scorer=None):
    classifier = LogisticRegression()
    super().grid_search_train(train_vector, labels, classifier, param_grid, scorer)

class MLP(BaseModel):
  def train(self, train_vector, labels, params):
    classifier = MLPClassifier(**params)
    super().train(train_vector, labels, classifier)

  def grid_search_train(self, train_vector, labels, param_grid, scorer=None):
    classifier = MLPClassifier()
    super().grid_search_train(train_vector, labels, classifier, param_grid, scorer)

class MNB(BaseModel):
  def train(self, train_vector, labels, params):
    classifier = MultinomialNB(**params)
    super().train(train_vector, labels, classifier)

  def grid_search_train(self, train_vector, labels, param_grid, scorer=None):
    classifier = MultinomialNB()
    super().grid_search_train(train_vector, labels, classifier, param_grid, scorer)

class RFC(BaseModel):
  def train(self, train_vector, labels, params):
    classifier = RandomForestClassifier(**params)
    super().train(train_vector, labels, classifier)

  def grid_search_train(self, train_vector, labels, param_grid, scorer=None):
    classifier = RandomForestClassifier()
    super().grid_search_train(train_vector, labels, classifier, param_grid, scorer)

class SVClassifier(BaseModel):
  def train(self, train_vector, labels, params):
    classifier = SVC(**params)
    super().train(train_vector, labels, classifier)

  def grid_search_train(self, train_vector, labels, param_grid, scorer=None):
    classifier = SVC()
    super().grid_search_train(train_vector, labels, classifier, param_grid, scorer)

class XGB(BaseModel):
  def train(self, train_vector, labels, params):
    classifier = XGBClassifier(**params)
    super().train(train_vector, labels, classifier)

  def grid_search_train(self, train_vector, labels, param_grid, scorer=None):
    classifier = XGBClassifier()
    super().grid_search_train(train_vector, labels, classifier, param_grid, scorer)

class Blender(BaseModel):
    def __init__(self, trained_classifiers, classification_threshold=0.5):
        super().__init__(classification_threshold)
        self.base_models          = trained_classifiers
        self.blender_model        = LogisticRegression(C=1.0, solver='liblinear')
        self.untrained_classifier = LogisticRegression(C=1.0, solver='liblinear')

    def blender_train(self, train_vector, labels):
        train_preds = pd.DataFrame()
        for classifier in self.base_models:
            train_preds = pd.concat([train_preds, pd.Series(classifier.predict_proba(train_vector)[:, 0])], axis=1)
        self.fit_model = self.blender_model.fit(train_preds, labels)
        self.train_vector = train_preds
        self.train_labels = labels

    def blender_performance_metrics(self, vector, labels):
        preds = pd.DataFrame()
        for classifier in self.base_models:
            preds = pd.concat([preds, pd.Series(classifier.predict_proba(vector)[:, 0])], axis=1)
        metrics = self.performance_metrics(preds, labels)
        return metrics

    def blender_visualize(self, vector, labels):
        preds = pd.DataFrame()
        for classifier in self.base_models:
            preds = pd.concat([preds, pd.Series(classifier.predict_proba(vector)[:, 0])], axis=1)
        self.visualize(preds, labels)

    def blender_predict(self, vector):
        preds = pd.DataFrame()
        for classifier in self.base_models:
            preds = pd.concat([preds, pd.Series(classifier.predict_proba(vector)[:, 0])], axis=1)
        predictions = self.predict(preds)
        return predictions

class Stacker(BaseModel):
    def __init__(self, untrained_classifiers, test_vector, classification_threshold=0.5):
        super().__init__(classification_threshold)
        self.base_models = untrained_classifiers
        self.test_vector = test_vector
        self.stacker_model        = LogisticRegression(C=1.0, solver='liblinear')
        self.untrained_classifier = LogisticRegression(C=1.0, solver='liblinear')

    def stacker_train(self, train_vector, labels):
        S_train, S_test = stacking(self.base_models,                         # list of models
                                   train_vector, labels, self.test_vector,   # data
                                   regression=False,                         # classification task (if you need
                                                                             #     regression - set to True)
                                   mode='oof_pred',                          # mode: oof for train set, fit on full
                                                                             #     train and predict test set once
                                   needs_proba=True,                         # predict probabilities (if you need
                                                                             #     class labels - set to False)
                                   n_folds=5,                                # number of folds
                                   stratified=True,                          # stratified split for folds
                                   shuffle=True,                             # shuffle the data
                                   random_state=0,
                                   verbose =1)


        self.fit_model    = self.stacker_model.fit(S_train, labels)
        self.train_vector = S_train
        self.train_labels = labels
        return S_test

    def stacker_visualize(self, vector, labels):
        self.visualize(vector, labels)

    def stacker_predict(self, vector):
        self.predict(vector)
