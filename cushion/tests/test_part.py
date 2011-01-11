from mock import Mock
from cushion.api import RequestBuilder, Part

def test_calling_part_raises_exception_on_300_status_code():
    """Test that Parts raises an exception with a 300 series error"""
    mock_request_builder = Mock()
    mock_request = Mock()
    mock_request_builder.build.return_value = mock_request
    mock_request.return_value = (dict(status='300'), dict())

    part = Part(
        [],
        mock_request_builder
    )

    try:
        part()
    except ValueError as error:
        assert str(error) == "Invalid return code. {'status': '300'}"


def test_calling_part_parses_response_on_200_series_status_code():
    """Test that Parts parses response with 200 series status code"""
    mock_request_builder = Mock()
    mock_request = Mock()
    mock_request_builder.build.return_value = mock_request
    mock_request.return_value = (
        dict(
            status='200'
        ),
        """{"_id":"some_doc_id","_rev":"1-7e1eac5717f7c7a26150ea486e80d1cf","name":"shey"}"""
    )

    part = Part(
        [],
        mock_request_builder
    )
    parsed_response = part()
    assert parsed_response['_id'] == "some_doc_id"
    assert parsed_response['_rev'] == "1-7e1eac5717f7c7a26150ea486e80d1cf"