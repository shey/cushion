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

def test_retrieve_a_document_with_document_id():
    """Test Retrieve a document using with document id"""
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
    assert request.method == "GET"
    assert request.uri == "base_uri/database/some_doc_id"

def test_retrieve_a_document_with_document_id_and_revision_number():
    """Test Retrieve a document with a document id and revision number"""
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
    assert request.method == "GET"
    assert request.uri == "base_uri/database/some_doc_id?rev=946B7D1C"