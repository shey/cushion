from mock import Mock
from cushion.api import RequestBuilder, WriteDocumentRequest

#test cases created using http://wiki.apache.org/couchdb/HTTP_Document_API

def test_request_can_create_a_new_document_with_a_document_id():
    """Test that request can create a document with a document id"""
    http_client = Mock()
    uri_parts = [
        'base_uri',
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
    request.requestor.assert_called_with(
        "base_uri/database/some_doc_id",
        "PUT",
        body='{"Body": "I decided today that I like baseball."}'
    )

def test_request_create_a_new_document_when_document_id_not_provided_using_post():
    """Test that request can create a document with out document id using post"""
    http_client = Mock()
    base_uri = ""
    uri_parts = [
        'base_uri',
        'database'
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
    request.requestor.assert_called_with(
        "base_uri/database",
        "POST",
        body='{"Body": "I decided today that I like baseball."}'
    )

def test_request_delete_a_document_with_id_and_revsion_number():
    """Test that Write request can delete a document using the id and rev number"""
    http_client = Mock()
    base_uri = ""
    uri_parts = [
        'base_uri',
        'database'
    ]
    options = dict(
        id='some_doc_id',
        rev='1582603387'
    )

    request = WriteDocumentRequest(
        http_client,
        "DELETE",
        uri_parts,
        options
    )

    request()
    #todo: fix this, sending to much data, but couchdb is ok with it
    request.requestor.assert_called_with(
        "base_uri/database/some_doc_id?rev=1582603387&id=some_doc_id",
        "DELETE",
        body='{"rev": "1582603387"}'
    )