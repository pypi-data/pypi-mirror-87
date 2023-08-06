import joblib

from ows_language_model import pipeline as pipe
from ows_language_model.config import config
from ows_language_model.processing import data_management as dm
from ows_language_model.processing import preprocessors as pp


def run_training(save_result: bool = True):
    """Train a language model."""


    if save_result:
        joblib.dump(enc, config.ENCODER_PATH)
        dm.save_pipeline_keras(pipe.pipe)


if __name__ == '__main__':
    run_training(save_result=True)
