# PYTHONPATH='.' AWS_PROFILE=dpa luigi --module orquestador-modelling CreateModelCancelled --local-scheduler

import luigi
import luigi.contrib.s3
from luigi import Event, Task, build # Utilidades para acciones tras un task exitoso o fallido
import os

from pyspark.sql import SparkSession
from src.models.train_model import get_processed_train_test, init_data_luigi

from luigi.contrib.postgres import CopyToTable,PostgresQuery



# ===============================
CURRENT_DIR = os.getcwd()
# ===============================

class DataLocalStorage():
    def __init__(self, X_train= None, X_test= None, y_train= None, y_test= None):
        self.X_train =X_train
        self.X_test =  X_test
        self.y_test =  y_train
        self.y_train = y_test

    def get_sets():
        return self.X_train, self.X_test, self.y_train, self.y_test

CACHE = DataLocalStorage()


class GetDataSets(luigi.Task):

    def output(self):
        dir = CURRENT_DIR + "/target/gets_data_sets.txt"
        return luigi.local_target.LocalTarget(dir)

    def run(self):
        X_train, X_test, y_train, y_test = init_data_luigi(True)
        CACHE.X_train = X_train
        CACHE.X_test = X_test
        CACHE.y_train = y_train
        CACHE.y_test = y_test

        z = "Obtiene Datos"
        with self.output().open('w') as output_file:
            output_file.write(z)

class CreateModelCancelled(luigi.Task):

    def requires(self):
        return GetDataSets()

    def output(self):
        # Chance y aqui podemos guardar el mejor modelo en una S3
        dir = CURRENT_DIR + "/target/model_cancelled.txt"
        return luigi.local_target.LocalTarget(dir)

    def run(self):
        objetivo = "cancelled"
        X_train, X_test, y_train, y_test = CACHE.get_sets()

        gridSearch_bins(X_train, X_test, y_train, y_test, objetivo)

        z = str(objetivo)
        with self.output().open('w') as output_file:
            output_file.write(z)
