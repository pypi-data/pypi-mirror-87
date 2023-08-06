# -*- coding: utf-8 -*-
# *******************************************************
#   ____                     _               _
#  / ___|___  _ __ ___   ___| |_   _ __ ___ | |
# | |   / _ \| '_ ` _ \ / _ \ __| | '_ ` _ \| |
# | |__| (_) | | | | | |  __/ |_ _| | | | | | |
#  \____\___/|_| |_| |_|\___|\__(_)_| |_| |_|_|
#
#  Sign up for free at http://www.comet.ml
#  Copyright (C) 2015-2020 Comet ML INC
#  This file can not be copied and/or distributed without the express
#  permission of Comet ML Inc.
# *******************************************************
import copy
import logging

from .._logging import check_module

LOGGER = logging.getLogger(__name__)


def pre_process_params(params):
    try:
        if "random_state" in params:
            our_params = copy.copy(params)
            if our_params["random_state"].__class__.__name__ == "RandomState":
                del our_params["random_state"]
                return our_params

    except Exception as e:
        LOGGER.info(
            "failed to remove RandomState from sklearn object with error %s",
            e,
            exc_info=True,
        )

    return params


def fit_logger(experiment, original, ret_val, *args, **kwargs):
    if experiment.auto_param_logging:
        try:
            params = ret_val.get_params()
            processed_params = pre_process_params(params)
            experiment._log_parameters(processed_params, framework="sklearn")
        except Exception:
            LOGGER.error("Failed to extract parameters from estimator", exc_info=True)


def pipeline_fit_logger(experiment, original, ret_val, *args, **kwargs):
    if experiment.auto_param_logging:
        try:
            params = ret_val.get_params()
            if params is not None and "steps" in params:
                for step in params["steps"]:
                    step_name, step_mdl = step
                    params = step_mdl.get_params()
                    processed_params = pre_process_params(params)
                    experiment._log_parameters(
                        processed_params, prefix=step_name, framework="sklearn"
                    )
        except Exception:
            LOGGER.error("Failed to extract parameters from Pipeline", exc_info=True)


FIT_MODULES = [
    # Deprecated locations in sklearn 0.22; to be removed in 0.24:
    ("sklearn.linear_model.base", "LinearRegression.fit"),
    ("sklearn.linear_model.bayes", "ARDRegression.fit"),
    ("sklearn.linear_model.bayes", "BayesianRidge.fit"),
    ("sklearn.linear_model.coordinate_descent", "ElasticNet.fit"),
    ("sklearn.linear_model.coordinate_descent", "ElasticNetCV.fit"),
    ("sklearn.linear_model.coordinate_descent", "Lasso.fit"),
    ("sklearn.linear_model.coordinate_descent", "LassoCV.fit"),
    ("sklearn.linear_model.coordinate_descent", "MultiTaskElasticNet.fit"),
    ("sklearn.linear_model.coordinate_descent", "MultiTaskElasticNetCV.fit"),
    ("sklearn.linear_model.coordinate_descent", "MultiTaskLasso.fit"),
    ("sklearn.linear_model.coordinate_descent", "MultiTaskLassoCV.fit"),
    ("sklearn.linear_model.huber", "HuberRegressor.fit"),
    ("sklearn.linear_model.least_angle", "Lars.fit"),
    ("sklearn.linear_model.least_angle", "LarsCV.fit"),
    ("sklearn.linear_model.least_angle", "LassoLars.fit"),
    ("sklearn.linear_model.least_angle", "LassoLarsCV.fit"),
    ("sklearn.linear_model.least_angle", "LassoLarsIC.fit"),
    ("sklearn.linear_model.logistic", "LogisticRegression.fit"),
    ("sklearn.linear_model.logistic", "LogisticRegressionCV.fit"),
    ("sklearn.linear_model.omp", "OrthogonalMatchingPursuit.fit"),
    ("sklearn.linear_model.omp", "OrthogonalMatchingPursuitCV.fit"),
    ("sklearn.linear_model.passive_aggressive", "PassiveAggressiveClassifier.fit"),
    ("sklearn.linear_model.passive_aggressive", "PassiveAggressiveRegressor.fit"),
    ("sklearn.linear_model.perceptron", "Perceptron.fit"),
    ("sklearn.linear_model.ransac", "RANSACRegressor.fit"),
    ("sklearn.linear_model.ridge", "Ridge.fit"),
    ("sklearn.linear_model.ridge", "RidgeCV.fit"),
    ("sklearn.linear_model.ridge", "RidgeClassifier.fit"),
    ("sklearn.linear_model.ridge", "RidgeClassifierCV.fit"),
    ("sklearn.linear_model.stochastic_gradient", "SGDClassifier.fit"),
    ("sklearn.linear_model.stochastic_gradient", "SGDRegressor.fit"),
    ("sklearn.linear_model.theil_sen", "TheilSenRegressor.fit"),
    # New locations in 0.22:
    ("sklearn.linear_model._base", "LinearRegression.fit"),
    ("sklearn.linear_model._bayes", "ARDRegression.fit"),
    ("sklearn.linear_model._bayes", "BayesianRidge.fit"),
    ("sklearn.linear_model._coordinate_descent", "ElasticNet.fit"),
    ("sklearn.linear_model._coordinate_descent", "ElasticNetCV.fit"),
    ("sklearn.linear_model._coordinate_descent", "Lasso.fit"),
    ("sklearn.linear_model._coordinate_descent", "LassoCV.fit"),
    ("sklearn.linear_model._coordinate_descent", "MultiTaskElasticNet.fit"),
    ("sklearn.linear_model._coordinate_descent", "MultiTaskElasticNetCV.fit"),
    ("sklearn.linear_model._coordinate_descent", "MultiTaskLasso.fit"),
    ("sklearn.linear_model._coordinate_descent", "MultiTaskLassoCV.fit"),
    ("sklearn.linear_model._huber", "HuberRegressor.fit"),
    ("sklearn.linear_model._least_angle", "Lars.fit"),
    ("sklearn.linear_model._least_angle", "LarsCV.fit"),
    ("sklearn.linear_model._least_angle", "LassoLars.fit"),
    ("sklearn.linear_model._least_angle", "LassoLarsCV.fit"),
    ("sklearn.linear_model._least_angle", "LassoLarsIC.fit"),
    ("sklearn.linear_model._logistic", "LogisticRegression.fit"),
    ("sklearn.linear_model._logistic", "LogisticRegressionCV.fit"),
    ("sklearn.linear_model._omp", "OrthogonalMatchingPursuit.fit"),
    ("sklearn.linear_model._omp", "OrthogonalMatchingPursuitCV.fit"),
    ("sklearn.linear_model._passive_aggressive", "PassiveAggressiveClassifier.fit"),
    ("sklearn.linear_model._passive_aggressive", "PassiveAggressiveRegressor.fit"),
    ("sklearn.linear_model._perceptron", "Perceptron.fit"),
    ("sklearn.linear_model._ransac", "RANSACRegressor.fit"),
    ("sklearn.linear_model._ridge", "Ridge.fit"),
    ("sklearn.linear_model._ridge", "RidgeCV.fit"),
    ("sklearn.linear_model._ridge", "RidgeClassifier.fit"),
    ("sklearn.linear_model._ridge", "RidgeClassifierCV.fit"),
    ("sklearn.linear_model._stochastic_gradient", "SGDClassifier.fit"),
    ("sklearn.linear_model._stochastic_gradient", "SGDRegressor.fit"),
    ("sklearn.linear_model._theil_sen", "TheilSenRegressor.fit"),
    # TODO: see if these new linear_models need to be monkey patched:
    # sklearn.linear_model._cd_fast
    # sklearn.linear_model._sag
    # sklearn.linear_model._sag_fast
    # sklearn.linear_model._sgd_fast
    ("sklearn.calibration", "CalibratedClassifierCV.fit"),
    ("sklearn.cross_decomposition.cca_", "CCA.fit"),
    ("sklearn.cross_decomposition.pls_", "PLSCanonical.fit"),
    ("sklearn.cross_decomposition.pls_", "PLSRegression.fit"),
    ("sklearn.discriminant_analysis", "LinearDiscriminantAnalysis.fit"),
    ("sklearn.discriminant_analysis", "QuadraticDiscriminantAnalysis.fit"),
    ("sklearn.ensemble.bagging", "BaggingClassifier.fit"),
    ("sklearn.ensemble.bagging", "BaggingRegressor.fit"),
    ("sklearn.ensemble.forest", "ExtraTreesClassifier.fit"),
    ("sklearn.ensemble.forest", "ExtraTreesRegressor.fit"),
    ("sklearn.ensemble.forest", "RandomForestClassifier.fit"),
    ("sklearn.ensemble.forest", "RandomForestRegressor.fit"),
    ("sklearn.ensemble.gradient_boosting", "GradientBoostingClassifier.fit"),
    ("sklearn.ensemble.gradient_boosting", "GradientBoostingRegressor.fit"),
    ("sklearn.ensemble.weight_boosting", "AdaBoostClassifier.fit"),
    ("sklearn.ensemble.weight_boosting", "AdaBoostRegressor.fit"),
    ("sklearn.gaussian_process.gaussian_process", "GaussianProcess.fit"),
    ("sklearn.gaussian_process.gpc", "GaussianProcessClassifier.fit"),
    ("sklearn.gaussian_process.gpr", "GaussianProcessRegressor.fit"),
    ("sklearn.kernel_ridge", "KernelRidge.fit"),
    ("sklearn.naive_bayes", "BernoulliNB.fit"),
    ("sklearn.naive_bayes", "GaussianNB.fit"),
    ("sklearn.naive_bayes", "MultinomialNB.fit"),
    ("sklearn.neighbors.classification", "KNeighborsClassifier.fit"),
    ("sklearn.neighbors.classification", "RadiusNeighborsClassifier.fit"),
    ("sklearn.neighbors.nearest_centroid", "NearestCentroid.fit"),
    ("sklearn.neighbors.regression", "KNeighborsRegressor.fit"),
    ("sklearn.neighbors.regression", "RadiusNeighborsRegressor.fit"),
    ("sklearn.neural_network.multilayer_perceptron", "MLPClassifier.fit"),
    ("sklearn.neural_network.multilayer_perceptron", "MLPRegressor.fit"),
    ("sklearn.semi_supervised.label_propagation", "LabelPropagation.fit"),
    ("sklearn.semi_supervised.label_propagation", "LabelSpreading.fit"),
    ("sklearn.svm.classes", "LinearSVC.fit"),
    ("sklearn.svm.classes", "LinearSVR.fit"),
    ("sklearn.svm.classes", "NuSVC.fit"),
    ("sklearn.svm.classes", "NuSVR.fit"),
    ("sklearn.svm.classes", "SVC.fit"),
    ("sklearn.svm.classes", "SVR.fit"),
    ("sklearn.tree.tree", "DecisionTreeClassifier.fit"),
    ("sklearn.tree.tree", "DecisionTreeRegressor.fit"),
    ("sklearn.tree.tree", "ExtraTreeClassifier.fit"),
    ("sklearn.tree.tree", "ExtraTreeRegressor.fit"),
]

PIPELINE_FIT_MODULES = [("sklearn.pipeline", "Pipeline.fit")]


def patch(module_finder):
    check_module("sklearn")

    # Register the pipeline fit methods
    for module, object_name in PIPELINE_FIT_MODULES:
        module_finder.register_before(module, object_name, pipeline_fit_logger)
        module_finder.register_after(module, object_name, pipeline_fit_logger)

    # Register the fit methods
    for module, object_name in FIT_MODULES:
        module_finder.register_before(module, object_name, fit_logger)
        module_finder.register_after(module, object_name, fit_logger)


check_module("sklearn")
