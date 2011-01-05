from mock import Mock
from cushion.api import RequestFactory

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

def test_retrieve_a_document_with_document_id():
    """Test that it can retrieve a document using document id"""
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

def test_retrieve_a_document_with_document_id_and_revision_number():
    """Test that it can retrieve a document with document id and rev number"""
    factory = create_request_factory(
        'username', 'password', 'base_uri'
    )
    request = factory.build(
        [
            "get",
            "database"
        ],
        dict(
            id='some_doc_id',
            rev='946B7D1C'
        )
    )
    request()
    request.http_client.request.assert_called_with(
        "base_uri/database/some_doc_id?rev=946B7D1C",
        "GET"
    )