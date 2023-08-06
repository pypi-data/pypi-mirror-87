import logging

import pandas as pd
import torch.nn.functional as F
import torch
import numpy as np

from ows_language_model import __version__ as _version
from ows_language_model.processing import data_management as dm
from ows_language_model.config import config
from ows_language_model.model import tokenizer, model

_logger = logging.getLogger(__name__)
PIPELINE = dm.load_pipeline()

def make_single_prediction(*, input_text):
    """Make a single prediction using the saved model pipeline.

        Args:
            input_text: variable length sequence of text

        Returns
            Dictionary with both raw next-word predictions and readable values.
        """
    
    encoded_input = tokenizer(input_text, return_tensors='pt')
    logits = model(**encoded_input).logits
    final_logits = logits.squeeze(0).detach()[-1, :]

    prediction_vector = F.softmax(final_logits / config.temperature, dim=0)
    idx = torch.multinomial(prediction_vector, 1)
    output_sequence  = torch.cat([encoded_input['input_ids'].squeeze(0), idx])
    tokens  = tokenizer.convert_ids_to_tokens(output_sequence)
    prediction = tokenizer.convert_tokens_to_string(tokens)
    _logger.info(f'Made prediction: {prediction}'
                 f' with model version: {_version}')
    #import IPython; IPython.terminal.ipapp.launch_new_instance()
    return dict(predictions=prediction,
                version=_version)


def make_bulk_prediction(*, text_df: pd.Series) -> dict:
    """Make multiple predictions using the saved model pipeline.

    Currently, this function is primarily for testing purposes,
    allowing us to pass in a series of text examples

    Args:
        images_df: Pandas series of images

    Returns
        Dictionary with both raw predictions and their classifications.
    """

    _logger.info(f'received input df: {text_df}')

    predictions = PIPELINE.predict(text_df)

    _logger.info(f'Made predictions: {predictions}'
                 f' with model version: {_version}')

    return dict(predictions=predictions,
                version=_version)


if __name__ == '__main__':
    import argparse, re
    parser = argparse.ArgumentParser(description='Input some text')
    parser.add_argument('text', type=str, nargs='+',
                    help='a string to input')
    parser.add_argument('--N', type=int, default=1,
                    help='number of predictions')
    parser.add_argument('--temperature', type=float, default=1,
                    help='number of predictions')

    args = parser.parse_args()
    config.temperature = float(args.temperature)
    
    input_text = " ".join(args.text)

    for j in range(args.N):
        prediction = make_single_prediction(input_text=input_text)
        input_text = prediction['predictions']
        print(re.sub(r'\s', ' ', input_text))