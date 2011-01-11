from mock import Mock
from cushion.api import RequestBuilder, ReadDocumentRequest


#test cases created using http://wiki.apache.org/couchdb/HTTP_Document_API

def test_request_can_get_a_document_using_document():
    """Test that a request can get a document using document id"""
    http_client = Mock()
    uri_parts = [
        "database"
    ]
    options = dict(
        id='some_doc_id'
    )

    request = ReadDocumentRequest(
        http_client,
        "base_uri",
        "GET",
        uri_parts,
        options
    )

    request()
    request.requestor.assert_called_with(
        "base_uri/database/some_doc_id",
        "GET"
    )

def test_request_can_get_a_document_using_document_id_and_rev_number():
    """Test that request can get a document using document id and rev number"""
    http_client = Mock()
    uri_parts = [
        "database"
    ]
    options = dict(
        id='some_doc_id',
        rev='946B7D1C'
    )
    request = ReadDocumentRequest(
        http_client,
        "base_uri",
        "GET",
        uri_parts,
        options
    )
    request()
    request.requestor.assert_called_with(
        "base_uri/database/some_doc_id?rev=946B7D1C",
        "GET"
    )

def test_request_can_get_all_documents():
    """Test that a request can get all documents from a database"""
    http_client = Mock()
    http_client.auth_header = dict()
    http_client.base_uri = "base_uri"
    uri_parts = [
        "database",
        "_all_docs"
    ]

    request = ReadDocumentRequest(
        http_client,
        "base_uri",
        "GET",
        uri_parts
    )
    request()
    request.requestor.assert_called_with(
        "base_uri/database/_all_docs",
        "GET"
    )

def test_request_for_all_documents_includes_options():
    """Test that request for all documents includes filtering options"""
    http_client = Mock()
    uri_parts = [
        "database",
        "_all_docs"
    ]
    options = dict(
        limit=2,
        startkey="doc2",
        descending='true',
    )

    request = ReadDocumentRequest(
        http_client,
        "base_uri",
        "GET",
        uri_parts,
        options
    )
    request()
    request.requestor.assert_called_with(
        "base_uri/database/_all_docs?startkey=%22doc2%22&descending=true&limit=2",
        "GET"
    )