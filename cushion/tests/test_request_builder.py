from mock import Mock
from cushion.api import RequestBuilder

def create_request_builder(username, password, base_uri):
    builder = RequestBuilder(
        username,
        password,
        base_uri
    )
    builder.http_client = Mock()
    builder.http_client.base_uri = base_uri
    return builder

def test_builder_returns_read_document_request_for_get():
    """Test that get request returns  ReadDocumentRequest"""
    builder = create_request_builder(
        'username', 'password', 'base_uri'
    )
    request = builder.build(
        [
            "get",
            "database"
        ],
        dict(
            id='some_doc_id'
        )
    )
    assert request.__class__.__name__ == "ReadDocumentRequest"
    assert request.method == "GET"
    assert callable(request)

def test_builder_returns_write_document_request_for_put():
    """Test that put request returns WriteDocumentRequest"""
    builder = create_request_builder(
        'username', 'password', 'base_uri'
    )
    request = builder.build(
        [
            "PUT",
            "database"
        ],
        dict()
    )
    assert request.__class__.__name__ == "WriteDocumentRequest"
    assert request.method == "PUT"
    assert callable(request)

def test_builder_returns_write_document_request_for_post():
    """Test that post request returns WriteDocumentRequest"""
    builder = create_request_builder(
        'username', 'password', 'base_uri'
    )
    request = builder.build(
        [
            "POST",
            "database"
        ],
        dict()
    )
    assert request.__class__.__name__ == "WriteDocumentRequest"
    assert request.method == "POST"
    assert callable(request)