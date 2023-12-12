import os
import pytest
from PIL import Image
from app.ocr_sys_v2.ocr_read import read_text

@pytest.fixture
def image_path():
    # Provide the path to a sample image for testing
    return os.path.join(os.path.dirname(__file__), '/ocr_sys_v2/test_images/test_ddi.jpg')

def test_read_text_success(image_path, mocker):
    # Mock the Azure Form Recognizer API call to return a predefined result
    mocker.patch('azure.ai.formrecognizer.DocumentAnalysisClient.begin_analyze_document')
    mock_result = mocker.MagicMock()
    mock_result.result.return_value = {'mock_key': 'mock_value'}
    azure_mock = mocker.patch('app.your_module.DocumentAnalysisClient', return_value=mock_result)

    response = read_text(image_path)

    assert response == b'{"message": "Success!"}\n'
    azure_mock.assert_called_once_with(os.getenv("VISION_ENDPOINT"), mocker.ANY)

def test_read_text_failure(image_path, mocker):
    # Mock the Azure Form Recognizer API call to raise an exception
    mocker.patch('azure.ai.formrecognizer.DocumentAnalysisClient.begin_analyze_document', side_effect=Exception('Mocked exception'))
    
    response = read_text(image_path)

    assert response == b'{"message": "Error!"}\n'