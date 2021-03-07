from python_lambda_helpers import execution_error


def test_default_error():
    response = execution_error()
    assert response.get('body') == 'Bad Request'


def test_custom_error():
    response = execution_error('Invalid request')
    assert response.get('body') == 'Invalid request'
