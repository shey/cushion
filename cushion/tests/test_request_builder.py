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

#test cases created using http://wiki.apache.org/couchdb/HTTP_Document_API

def test_builder_returns_read_document_request_for_get():
    """Test that the document request is callable"""
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

