import httplib2


class Part(object):
    def __init__(
        self,
        parts,
        client
    ):
        self.parts = parts
        self.client = client
        
    def __call__(self, **kwargs):
        uri = '/'.join(self.parts)
        return self._request(uri, kwargs)

    def _request(self, uri, kwargs):
        (method, uri_part) = uri.split("/")
        url =  "/".join([self.client.base_uri, uri_part, kwargs['id']])
        resp, content = self.client.request(
            url,
            method.upper()
        )
        return content

    def __getattr__(self, name):
        return Part(
            self.parts + [name],
            self.client
        )

class Cushion(object):
    def __init__(
        self,
        base_uri,
        username,
        password
    ):
        self.base_uri = base_uri
        self.username = username
        self.password = password

    def _get_http_client(self):
        h = httplib2.Http()
        h.base_uri = self.base_uri
        return h

    def __getattr__(self, name):
        return Part(
            [name],
            self._get_http_client()
        )
