import numpy as np
import cv2
from keras.utils import np_utils
from sklearn.preprocessing import LabelEncoder
from sklearn.base import BaseEstimator, TransformerMixin


class CreateDataset(BaseEstimator, TransformerMixin):

    def __init__(self, image_size=50):
        self.image_size = image_size

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X = X.copy()
        # in the example, resize the batch of images
        return X
