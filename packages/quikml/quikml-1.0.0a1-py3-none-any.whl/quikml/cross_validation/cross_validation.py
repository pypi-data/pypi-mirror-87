from sklearn.utils import shuffle
import matplotlib.pyplot as plt
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
import itertools
import pandas as pd
import numpy as np

from imblearn.under_sampling import RandomUnderSampler
from imblearn.pipeline import Pipeline
import operator

def downsample(X, y, downsample_ratio=1):

    # need to balance this dataset
    X, y = pd.DataFrame(X), pd.DataFrame(y)
    dataset = pd.concat([X, y], axis=1)

    majority_label, minority_label = _minority_majority(y)
    dataset_majority_label=dataset[dataset[y.columns[0]]==majority_label]
    dataset_minority_label=dataset[dataset[y.columns[0]]==minority_label]
    print('num majority class: ', len(dataset_majority_label))
    print("num minority class: ", len(dataset_minority_label))

    current_ratio = (len(dataset_minority_label)/len(dataset_majority_label))
    if downsample_ratio <= current_ratio:
        print("cannot downsample lower than " + str(current_ratio) + ". returning actual ratio.")
        print(y[y.columns[0]].value_counts())
        return X, y
    else:
        under = RandomUnderSampler(sampling_strategy=downsample_ratio)
        pipeline = Pipeline(steps=[('u', under)]) ##  add it later
        X_resampled, y_resampled = pipeline.fit_resample(X, y)
        dataset_balanced=pd.concat([X_resampled,y_resampled], axis=1)
        # reset index
        df = dataset_balanced[dataset_balanced.columns].reset_index().drop(['index'],axis=1)
        X = df.drop([df.columns[-1]], inplace=False, axis=1)
        y = df[[df.columns[-1]]]
        print("Final Ratio")
        print(y[y.columns[0]].value_counts())
    return X, y

def _minority_majority(y):
    sample_dict={}
    for idx,count in enumerate(y[y.columns[0]].value_counts()):
        sample_dict[idx]=count
    majority_label = max(sample_dict.items(), key=operator.itemgetter(1))[0]
    minority_label = min(sample_dict.items(), key=operator.itemgetter(1))[0]

    return majority_label, minority_label

def cross_validation(X, y, model, model_params, transformer=None,fold=3):

    print("===============Performing K-Fold=======================")

    # How many folds?
    skf = StratifiedKFold(n_splits=fold,random_state=0)
    skf.get_n_splits(X, y)
    print(skf)

    # Storing the results from each fold
    cm_total = np.array([[0,0],[0,0]])
    y_test_all = []
    y_pred_all = []

    performance_metrics_all = []

    count_fold = 1
    # Performing K-fold
    for train_index, test_index in skf.split(X, y):
        print("Fold {}:".format(count_fold))
        X_train, X_test = X[train_index], X[test_index]
        y_train, y_test = y[train_index], y[test_index]

        if transformer:
            transformer.fit(X_train)
            X_vectorized_train = transformer.transform(X_train)
            X_vectorized_test  = transformer.transform(X_test)

            # Pass classifier and params
            model.train(X_vectorized_train, y_train, model_params)
            metrics_model = model.performance_metrics(X_vectorized_test, y_test)

            # save results
            performance_metrics_all.append(metrics_model)
            print(metrics_model)
            y_pred = model.predict(X_vectorized_test)['predictions']
            cm = confusion_matrix(y_test, y_pred)
            cm_total = np.add(cm_total,cm)
            y_test_all+=list(y_test)
            y_pred_all+=list(y_pred)

            count_fold += 1
        else:
            model.train(X_train, y_train, model_params)
            metrics_model = model.performance_metrics(X_test, y_test)
            performance_metrics_all.append(metrics_model)
            print(metrics_model)
            y_pred = model.predict(X_test)['predictions']
            cm = confusion_matrix(y_test, y_pred)
            cm_total = np.add(cm_total,cm)
            y_test_all+=list(y_test)
            y_pred_all+=list(y_pred)

            count_fold += 1

    keys= ['accuracy', 'precision_overall', 'recall_overall',
    'f1_score_overall', 'precision_negclass', 'precision_posclass',
    'recall_negclass_specificity', 'recall_posclass_sensitivity',
    'f1_score_negclass', 'f1_score_posclass', 'log_loss',
    'roc_auc', 'discrepancy_metric']

    performance_metrics_mean_std = {}
    for k in keys:
        mean = round(np.mean([i[k] for i in performance_metrics_all]),2)
        std =  round(np.std([i[k] for i in performance_metrics_all]),2)
        res = [mean, std]

        performance_metrics_mean_std[k] = res

    performance_metrics_mean_std["confusion_matrix"] = cm_total

    print("====================K-Fold Done========================")
    np.set_printoptions(precision=2)
    plt.figure()
    _plot_confusion_matrix(cm_total,classes=['negative class','positive class'],normalize=True)
    print (classification_report(y_test_all,y_pred_all))
    plt.figure()
    _plot_confusion_matrix(cm_total,classes=['negative class','positive class'],normalize=False)
    plt.show()
    print (classification_report(y_test_all,y_pred_all))

    discrepancy_metric= [i['discrepancy_metric'] for i in performance_metrics_all]

    discrepancy_metric_mean = round(np.mean([i['discrepancy_metric'] for i in performance_metrics_all]),2)
    discrepancy_metric_mean

    print("discrepancy_metric:", discrepancy_metric)
    print("discrepancy_metric_mean:", discrepancy_metric_mean)


    return performance_metrics_mean_std

def _plot_confusion_matrix(cm, classes,
                          normalize=False,
                          title='Confusion matrix',
                          cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    if normalize:
        cm = np.round(cm.astype('float') / cm.sum(axis=1)[:, np.newaxis],2)
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')

    plt.imshow(cm, interpolation='nearest', cmap=cmap);
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, cm[i, j],
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')
