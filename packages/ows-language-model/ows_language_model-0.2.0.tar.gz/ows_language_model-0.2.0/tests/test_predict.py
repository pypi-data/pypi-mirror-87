from ows_language_model import __version__ as _version
from ows_language_model.predict import make_single_prediction


def test_make_single_prediction(text_input_data):
    # When
    results = make_single_prediction(input_text=text_input_data)

    # Then
    assert results['predictions'] is not None
    assert isinstance(results['predictions'], str)
    assert results['version'] == _version
