import httplib2
from urllib import urlencode
import simplejson as json

class RequestBuilder(object):
    """
    RequestBuilder is responsible for building
    the http request based on the http method type
    and URL that is being accessed
    """
    def __init__(
        self,
        username,
        password,
        base_uri
    ):
        self.username = username
        self.password = password
        self.http_client = httplib2.Http()
        self.http_client.base_uri = base_uri

    def build(
        self,
        uri_parts,
        options
    ):
        """
        Build the request, returns callable which in turn
        returns the http response and the http content body
        """

        if(len(uri_parts)):
            method = uri_parts[0].upper()

        if method == "GET":
            document_request = ReadDocumentRequest(
                self.http_client,
                uri_parts,
                options
            )
            return document_request


class ReadDocumentRequest(object):
    def __init__(
        self,
        client,
        uri_parts,
        options=None
    ):
        self.http_client = client
        self.uri_parts = uri_parts
        self.options = dict()
        if options:
            self.options = options

    @property
    def method(self):
        return "GET"

    @property
    def uri(self):
        """Create the URI with the parameters"""
        elements = []

        for part in self.uri_parts[1:]:
            elements.append(part)

        #probably should check for all reserved words
        if not self.uri_parts[-1].endswith("_all_docs"):
            elements.append(self.options.get('id', ''))
            del self.options['id']

        uri = self.http_client.base_uri + "/" + "/".join(elements)
        #this is so going to break with pust/posts
        if len(self.options):
            if self.options.has_key('startkey'):
                #the start key has to be quoted
                self.options['startkey'] = \
                    "\"" + self.options['startkey'] + "\""
            uri = uri + '?%s' % urlencode(self.options)

        return uri

    def __call__(self):
            return self.http_client.request(
                self.uri,
                "GET"
            )


class Part(object):
    def __init__(
        self,
        parts,
        request_builder
    ):
        self.parts = parts
        self.request_builder = request_builder

    def __call__(self, **kwargs):
        return self._request(self.parts, kwargs)

    def _request(self, uri_parts, kwargs):
        request = self.request_builder.build(
            uri_parts,
            kwargs
        )
        response, content = request()
        return content

    def __getattr__(self, name):
        return Part(
            self.parts + [name],
            self.request_builder
        )


class Cushion(object):
    """
    Cushion is the primary interface to CouchDB
    """
    def __init__(
        self,
        base_uri,
        username,
        password
    ):
        self.base_uri = base_uri
        self.username = username
        self.password = password

    def _get_request_builder(self):
        return RequestBuilder(
            self.username,
            self.password,
            self.base_uri
        )

    def __getattr__(self, name):
        return Part(
            [name],
            self._get_request_builder()
        )
