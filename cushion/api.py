import httplib2
import simplejson as json
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

        # document ids are obtained programmatically and therefore
        # must be passed in as a parameter, other requests will likely
        # have a more generic interface
        if options.has_key('id'):
            document_request = DocumentRequest(
                self.http_client,
                uri_parts,
                options
            )
            return document_request
        else:
            placeholder_request = PlaceHolderRequest()
            return placeholder_request

class PlaceHolderRequest(object):
    def __init__(self, *args):
        pass
    def __call__(self, *args):
        return ('a', 'b')


class DocumentRequest(object):
    def __init__(
        self,
        client,
        uri_parts,
        options
    ):
        self.http_client = client
        self.uri_parts = uri_parts
        self.options = options

    def __call__(self):
        (method_part, uri_part) = self.uri_parts[1], self.uri_parts[0]
        body = None
        uri =  "/".join(
            [
                self.http_client.base_uri,
                uri_part,
                self.options['id']
            ]
        )
        if method_part.upper() == "GET":
            uri = uri + '?%s' % urlencode({
                'revs': 'true'
            })
        elif method_part.upper() == "PUT":
            del self.options['id']
            body = self.options

        return self.http_client.request(
            uri,
            headers={'Content-Type': 'application/json'},
            method=method_part.upper(),
            body=json.dumps(body)
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
