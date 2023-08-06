import numpy as np
import sklearn as sk
from hyperas import optim
from hyperas.distributions import choice, uniform
from hyperopt import Trials, STATUS_OK, tpe
from tensorflow.keras.optimizers import SGD, RMSprop, Adagrad, Adadelta, Adam, Adamax, Nadam

import glmdisc


def data():
    """
    Data providing function:

    This function is separated from create_model() so that hyperopt
    won't reload data for each evaluation run.
    """
    n = 100
    d = 2
    theta = np.array([[0] * d] * 3)
    theta[1, :] = 3
    theta[2, :] = -3
    x_train, y_train, _ = glmdisc.Glmdisc.generate_data(n, d, theta)
    x_test, y_test, _ = glmdisc.Glmdisc.generate_data(n, d, theta)
    return x_train, y_train, x_test, y_test


def create_model(x_train, y_train, x_test, y_test):
    """
    Model providing function:

    Create Keras model with double curly brackets dropped-in as needed.
    Return value has to be a valid python dictionary with two customary keys:
        - loss: Specify a numeric evaluation metric to be minimized
        - status: Just use STATUS_OK and see hyperopt documentation if not feasible
    The last one is optional, though recommended, namely:
        - model: specify the model just created so that we can later use it again.
    """
    opt_choice = {{choice(["SGD",
                           "RMSprop",
                           "Adagrad",
                           "Adadelta",
                           "Adam",
                           "Adamax",
                           "Nadam"])}}

    lr = {{uniform(0.001, 2)}}
    momentum = {{uniform(0, 0.5)}}
    decay = {{uniform(0, 0.001)}}
    beta_1 = {{uniform(0.9, 0.999)}}
    beta_2 = {{uniform(0.9, 0.999)}}
    epsilon = {{uniform(1e-8, 1e-4)}}
    rho = {{uniform(0.7, 1)}}

    if opt_choice == "SGD":
        nesterov_sgd = {{choice([True, False])}}
        opt = SGD(learning_rate=lr,
                  momentum=momentum,
                  decay=decay,
                  nesterov=nesterov_sgd)
    elif opt_choice == "RMSprop":
        opt = RMSprop(learning_rate=lr,
                      decay=decay,
                      rho=rho,
                      epsilon=epsilon)
    elif opt_choice == "Adagrad":
        opt = Adagrad(learning_rate=lr,
                      epsilon=epsilon,
                      decay=decay)
    elif opt_choice == "Adadelta":
        opt = Adadelta(learning_rate=lr,
                       rho=rho,
                       epsilon=epsilon,
                       decay=decay)
    elif opt_choice == "Adam":
        amsgrad_adam = {{choice([True, False])}}
        opt = Adam(learning_rate=lr,
                   beta_1=beta_1,
                   beta_2=beta_2,
                   epsilon=epsilon,
                   decay=decay,
                   amsgrad=amsgrad_adam)
    elif opt_choice == "Adamax":
        opt = Adamax(learning_rate=lr,
                     beta_1=beta_1,
                     beta_2=beta_2,
                     epsilon=epsilon,
                     decay=decay)
    elif opt_choice == "Nadam":
        opt = Nadam(learning_rate=lr,
                    beta_1=beta_1,
                    beta_2=beta_2,
                    epsilon=epsilon)

    model = glmdisc.Glmdisc(algorithm="NN",
                            validation=False,
                            test=False,
                            m_start=3,
                            criterion="aic")
    model.fit(predictors_cont=x_train,
              predictors_qual=None,
              labels=y_train,
              iter=100,
              optimizer=opt)

    performance = sk.metrics.log_loss(
            y_test,
            model.predict(
                predictors_cont=x_test,
                predictors_qual=None)[:, 1],
            normalize=False
        )

    return {'loss': -performance, 'status': STATUS_OK, 'model': model}


if __name__ == "__main__":
    n = 100
    d = 2
    theta = np.array([[0] * d] * 3)
    theta[1, :] = 3
    theta[2, :] = -3

    # Optimisation
    best_run, best_model = optim.minimize(model=create_model,
                                          data=data,
                                          algo=tpe.suggest,
                                          max_evals=100,
                                          trials=Trials())

    opt_choice = ["SGD",
                  "RMSprop",
                  "Adagrad",
                  "Adadelta",
                  "Adam",
                  "Adamax",
                  "Nadam"][best_run['opt_choice']]

    lr = best_run['lr']
    momentum = best_run['momentum']
    decay = best_run['decay']
    beta_1 = best_run['beta_1']
    beta_2 = best_run['beta_2']
    epsilon = best_run['epsilon']
    rho = best_run['rho']

    if opt_choice == "SGD":
        nesterov_sgd = best_run['nesterov_sgd']
        opt = SGD(learning_rate=lr,
                  momentum=momentum,
                  decay=decay,
                  nesterov=nesterov_sgd)
    elif opt_choice == "RMSprop":
        opt = RMSprop(learning_rate=lr,
                      decay=decay,
                      rho=rho,
                      epsilon=epsilon)
    elif opt_choice == Adagrad:
        opt = Adagrad(learning_rate=lr,
                      epsilon=epsilon,
                      decay=decay)
    elif opt_choice == "Adadelta":
        opt = Adadelta(learning_rate=lr,
                       rho=rho,
                       epsilon=epsilon,
                       decay=decay)
    elif opt_choice == "Adam":
        amsgrad_adam = best_run['amsgrad_adam']
        opt = Adam(learning_rate=lr,
                   beta_1=beta_1,
                   beta_2=beta_2,
                   epsilon=epsilon,
                   decay=decay,
                   amsgrad=amsgrad_adam)
    elif opt_choice == "Adamax":
        opt = Adamax(learning_rate=lr,
                     beta_1=beta_1,
                     beta_2=beta_2,
                     epsilon=epsilon,
                     decay=decay)
    elif opt_choice == "Nadam":
        opt = Nadam(learning_rate=lr,
                    beta_1=beta_1,
                    beta_2=beta_2,
                    epsilon=epsilon)

    list_of_first_cutpoints = []
    list_of_second_cutpoints = []
    # Simulations
    for _ in range(100):
        x, y, theta = glmdisc.Glmdisc.generate_data(n, d, theta)
        model = glmdisc.Glmdisc(algorithm="NN", validation=False, test=False, m_start=3, criterion="aic")
        model.fit(predictors_cont=x, predictors_qual=None, labels=y, iter=100, plot=False, optimizer=opt)
        best_cutpoints = model.best_formula()
        best_cutpoints[0].sort()
        best_cutpoints[1].sort()
        if len(best_cutpoints[0] == 2):
            list_of_first_cutpoints.append(best_cutpoints[0][0])
            list_of_second_cutpoints.append(best_cutpoints[0][1])
        print(len(list_of_first_cutpoints))
        print(len(list_of_second_cutpoints))
        print(np.mean(list_of_first_cutpoints))
        print(np.mean(list_of_second_cutpoints))
        print(np.std(list_of_first_cutpoints))
        print(np.std(list_of_second_cutpoints))
