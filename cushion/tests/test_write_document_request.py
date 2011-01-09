from mock import Mock
from cushion.api import RequestBuilder, WriteDocumentRequest

#test cases created using http://wiki.apache.org/couchdb/HTTP_Document_API

def test_request_can_create_a_new_document_with_a_document_id():
    """Test that request can create a document with a document id"""
    http_client = Mock()
    http_client.base_uri = "base_uri"
    uri_parts = [
        "PUT",
        "database"
    ]
    options = dict(
        id='some_doc_id',
        Body="I decided today that I like baseball.",
    )
    request = WriteDocumentRequest(
        http_client,
        "PUT",
        uri_parts,
        options
    )
    request()
    request.http_client.request.assert_called_with(
        "base_uri/database/some_doc_id",
        "PUT",
        body='{"Body": "I decided today that I like baseball."}',
        headers={'Content-Type': 'application/json'}
    )

def test_request_create_a_new_document_when_document_id_not_provided_using_post():
    """Test that request can create a document with out document id using post"""
    http_client = Mock()
    http_client.base_uri = "base_uri"
    uri_parts = [
        "POST",
        "database"
    ]
    options = dict(
        Body="I decided today that I like baseball.",
    )
    request = WriteDocumentRequest(
        http_client,
        "POST",
        uri_parts,
        options
    )
    request()
    request.http_client.request.assert_called_with(
        "base_uri/database",
        "POST",
        body='{"Body": "I decided today that I like baseball."}',
        headers={'Content-Type': 'application/json'}
    )
