import logging
import os
import typing as t
from pathlib import Path

import pandas as pd

import joblib
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder

from ows_language_model import model as m
from ows_language_model.config import config

_logger = logging.getLogger(__name__)



def save_pipeline(model) -> None:
    """Persist keras model to disk."""

    joblib.dump(model.named_steps['dataset'], config.PIPELINE_PATH)
    joblib.dump(model.named_steps['cnn_model'].classes_, config.CLASSES_PATH)
    model.named_steps['cnn_model'].model.save(str(config.MODEL_PATH))

    remove_old_pipelines(
        files_to_keep=[config.MODEL_FILE_NAME, config.ENCODER_FILE_NAME,
                       config.PIPELINE_FILE_NAME, config.CLASSES_FILE_NAME])


def load_pipeline() -> Pipeline:
    """Load a Pytorch Pipeline from disk."""

    return


def load_encoder() -> LabelEncoder:
    encoder = joblib.load(config.ENCODER_PATH)

    return encoder


def remove_old_pipelines(*, files_to_keep: t.List[str]) -> None:
    """
    Remove old model pipelines, models, encoders and classes.

    This is to ensure there is a simple one-to-one
    mapping between the package version and the model
    version to be imported and used by other applications.
    """
    do_not_delete = files_to_keep + ['__init__.py']
    for model_file in Path(config.TRAINED_MODEL_DIR).iterdir():
        if model_file.name not in do_not_delete:
            model_file.unlink()
