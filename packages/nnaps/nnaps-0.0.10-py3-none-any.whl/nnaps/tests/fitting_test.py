import pylab as pl
from nnaps import predictors

# setup = {
#     'datafile': '/home/joris/Python/nnaps/nnaps/tests/BesanconGalactic_summary.txt',
#     'default_encoder': 'OrdinalEncoder',
#     'features': ['M1', 'Pinit', 'qinit', 'FeHinit'],
#     'regressors': ['Pfinal', 'qfinal'],
#     'classifiers': ['product', 'binary_type']
# }
#
# predictor = predictors.XGBPredictor(setup=setup)
#
# predictor.fit()
#
# predictor.save_model('test_model_XGB.dat')



# setup = {
#     'datafile': '/home/joris/Python/nnaps/nnaps/tests/BesanconGalactic_summary.txt',
#     'features': ['M1', 'Pinit', 'qinit', 'FeHinit'],
#     'regressors': ['Pfinal', 'qfinal', 'M1final'],
#     'classifiers': ['product', 'He_ignition_type'],
# }

#predictor = predictors.FCPredictor(setup=setup)

# predictor.fit(epochs=10)

#predictor.print_score()

# predictor.plot_training_history()
# predictor.plot_confusion_matrix()
#predictor.plot_feature_range_comparison(predictor.test_data)
#pl.show()


#
# import yaml
#
# setup = """
# datafile: '/home/joris/Python/nnaps/nnaps/tests/BesanconGalactic_summary.txt'
# features:
#    M1:
#       processor: MinMaxScaler
#    qinit:
#       processor: MinMaxScaler
#    Pinit:
#       processor: MinMaxScaler
#    FeHinit:
#       processor: MinMaxScaler
# regressors:
#    Pfinal:
#       loss: mean_absolute_percentage_error
#    qfinal:
# classifiers:
#    - product
#    - binary_type
# model:
#    - {'layer':'Dense',   'args':[100], 'kwargs': {'activation':'relu', 'name':'FC_1'} }
#    - {'layer':'Dense',   'args':[75],  'kwargs': {'activation':'relu', 'name':'FC_2'} }
#    - {'layer':'Dense',   'args':[50],  'kwargs': {'activation':'relu', 'name':'FC_3'} }
#
# optimizer: adam
# """
#
# setup = yaml.safe_load(setup)
#
# predictor = predictors.FCPredictor(setup=setup)
#
# predictor.fit(epochs=500, batch_size=128, early_stopping=False, reduce_lr=False)
#
# # predictor.save_training_history('test_history.csv')
#
# predictor.save_model('test_model_FC.h5', include_history=True)

#--

# predictor = predictors.FCPredictor(setup_file='test_setup.yaml')
# predictor.load_model('test_model.h5')
#
# predictor.print_score()
#
# predictor.make_training_data_report('test_training_report.html')

# predictor.make_training_history_report('test_training_history_report.html')

# from nnaps.reports import html_reports
#
# y_true = predictor.train_data['product']
# y_pred = predictor.predict(predictor.train_data)['product']
#
# plotting.make_confusion_matrix_plot(y_true, y_pred)

# from nnaps.reports import html_reports
# #
# import pandas as pd
# from sklearn import preprocessing
# #
# # history = pd.read_csv('test_history.csv')
# #
# # plotting.plot_training_history_html(history, targets=['Pfinal', 'qfinal', 'product', 'binary_type'], filename='test_training_history.html')
#
# #
# #
# training_data = pd.read_csv('BesanconGalactic_summary.txt')
#
# from sklearn.model_selection import train_test_split
# from sklearn import utils
#
# data = utils.shuffle(training_data, random_state=42)
# data_train, data_test = train_test_split(data, test_size=0.2, random_state=42)
#
# Xpars = ['M1', 'qinit', 'Pinit', 'FeHinit']
# regressors = ['Pfinal', 'qfinal']
#
# processors = dict(M1 = preprocessing.StandardScaler,
#                   qinit = preprocessing.RobustScaler,
#                   Pinit = preprocessing.MinMaxScaler,
#                   FeHinit = preprocessing.MaxAbsScaler,
#                   Pfinal = preprocessing.RobustScaler,
#                 )
#
#
# plotting.plot_training_data_html(data_train, data_test, Xpars, regressors, [], processors, filename='/home/joris/Python/nnaps/nnaps/tests/test_training_data.html')