import httplib2
import simplejson as json
from urllib import urlencode
from functools import partial


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
        method_part,
        uri_part,
        options
    ):
        """
        Build the request, returns callable which in turn
        returns the http response and the http content body
        """
        body = None
        uri =  "/".join(
            [
                self.http_client.base_uri,
                uri_part,
                options['id']
            ]
        )
        if method_part.upper() == "GET":
            uri = uri + '?%s' % urlencode({
                'revs': 'true'
            })
        elif method_part.upper() == "PUT":
            del options['id']
            body = options

        return partial(
            self.http_client.request,
            uri,
            headers={'Content-Type': 'application/json'},
            method=method_part.upper(),
            body=json.dumps(body)
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

    def _request(self, method_parts, kwargs):
        (method_part, uri_part) = method_parts[0], method_parts[1]
        request = self.request_builder.build(
            uri_part,
            method_part,
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
