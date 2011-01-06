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
    """Test that a request can get a document using document id"""
    http_client = Mock()
    http_client.base_uri = "base_uri"
    uri_parts = [
        "get",
        "database"
    ]
    options = dict(
        id='some_doc_id'
    )

    request = DocumentRequest(
        http_client,
        uri_parts,
        options
    )

    request()
    request.http_client.request.assert_called_with(
        "base_uri/database/some_doc_id",
        "GET"
    )

def test_request_can_get_a_document_using_document_id_and_rev_number():
    """Test that request can get a document using document id and rev number"""
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

def test_request_can_get_all_documents():
    """Test that a request can get all documents from a database"""
    http_client = Mock()
    http_client.base_uri = "base_uri"
    uri_parts = [
        "get",
        "database",
        "_all_docs"
    ]
    request = DocumentRequest(
        http_client,
        uri_parts
    )
    request()
    request.http_client.request.assert_called_with(
        "base_uri/database/_all_docs",
        "GET"
    )

def test_request_for_all_documents_includes_options():
    """Test that request for all documents includes filtering options"""
    http_client = Mock()
    http_client.base_uri = "base_uri"
    uri_parts = [
        "get",
        "database",
        "_all_docs"
    ]
    options = dict(
        limit=2,
        startkey="doc2",
        descending='true',
    )
    request = DocumentRequest(
        http_client,
        uri_parts,
        options
    )
    request()
    request.http_client.request.assert_called_with(
        "base_uri/database/_all_docs?startkey=%22doc2%22&descending=true&limit=2",
        "GET"
    )