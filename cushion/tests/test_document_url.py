from mock import Mock
from cushion.api import RequestFactory, DocumentRequest

def create_request_factory(username, password, base_uri):
    factory = RequestFactory(
        username,
        password,
        base_uri
    )
    factory.http_client = Mock()
    factory.http_client.base_uri = base_uri
    return factory

#test cases created using http://wiki.apache.org/couchdb/HTTP_Document_API

def test_request_returned_by_factory_is_callable():
    """Test that the document request is callable"""
    factory = create_request_factory(
        'username', 'password', 'base_uri'
    )
    request = factory.build(
        [
            "get",
            "database"
        ],
        dict(
            id='some_doc_id'
        )
    )
    assert request.__class__.__name__ == "DocumentRequest"
    assert callable(request)

def test_request_can_get_a_document_using_document():
    """Test request can get a document using document id"""
    factory = create_request_factory(
        'username', 'password', 'base_uri'
    )
    request = factory.build(
        [
            "get",
            "database"
        ],
        dict(
            id='some_doc_id'
        )
    )
    request()
    request.http_client.request.assert_called_with(
        "base_uri/database/some_doc_id",
        "GET"
    )

def test_request_can_get_a_document_using_document_id_and_rev_number():
    """Test request can get a document using document id and rev number"""
    http_client = Mock()
    http_client.base_uri = "base_uri"
    uri_parts = [
        "get",
        "database"
    ]
    options = dict(
        id='some_doc_id',
        rev='946B7D1C'
    )
    request = DocumentRequest(
        http_client,
        uri_parts,
        options
    )
    request()
    request.http_client.request.assert_called_with(
        "base_uri/database/some_doc_id?rev=946B7D1C",
        "GET"
    )