import httplib2
from urllib import urlencode

class RequestFactory(object):
    """
        RequestFactory is responsible for building
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
        document_request = DocumentRequest(
            self.http_client,
            uri_parts,
            options
        )
        return document_request


class DocumentRequest(object):
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
        """return the http method"""
        if(len(self.uri_parts)):
            return self.uri_parts[0].upper()

    @property
    def uri(self):
        """Create the URI with the parameters"""
        elements = []
        elements.append(self.http_client.base_uri)

        for part in self.uri_parts[1:]:
            elements.append(part)

        if not self.uri_parts[-1].endswith("all_docs"):
            elements.append(self.options.get('id', ''))
            del self.options['id']

        uri = "/".join(elements)
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
            self.method
        )


class Part(object):
    def __init__(
        self,
        parts,
        request_factory
    ):
        self.parts = parts
        self.request_factory = request_factory

    def __call__(self, **kwargs):
        return self._request(self.parts, kwargs)

    def _request(self, uri_parts, kwargs):
        request = self.request_factory.build(
            uri_parts,
            kwargs
        )
        response, content = request()
        return content

    def __getattr__(self, name):
        return Part(
            self.parts + [name],
            self.request_factory
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

    def _get_request_factory(self):
        return RequestFactory(
            self.username,
            self.password,
            self.base_uri
        )

    def __getattr__(self, name):
        return Part(
            [name],
            self._get_request_factory()
        )
