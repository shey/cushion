import httplib2
import base64
import simplejson as json
from urllib import urlencode


class Cushion(object):
    """
    Cushion is the primary interface to CouchDB
    """
    def __init__(
        self,
        base_uri,
        username=None,
        password=None
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
        self.http_client.auth_header = self.create_auth_header()

    def create_auth_header(self):
        #don't know why add_credentials is failing but it's
        #always a good idea to force auth headers with httplib2
        if self.username and self.password:
            print "shouldn't be here"
            base64string = base64.b64encode('%s:%s' % (self.username, self.password))
            header = "Basic %s" %(base64string,)
            return dict(Authorization=header)
        else:
            return dict()

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
            return ReadDocumentRequest(
                self.http_client,
                method,
                uri_parts[1:],
                options
            )
        else:
            return WriteDocumentRequest(
                self.http_client,
                method,
                uri_parts[1:],
                options
            )


class WriteDocumentRequest(object):
    def __init__(
        self,
        client,
        method,
        uri_parts,
        options=None
    ):
        self.http_client = client
        self.uri_parts = uri_parts
        self.method = method
        self.options = dict()
        if options:
            self.options = options

    @property
    def uri(self):
        elements = []
        for part in self.uri_parts:
            elements.append(part)

        if self.method == "PUT":
            elements.append(self.options.get('id', ''))
        return self.http_client.base_uri + "/" + "/".join(elements)

    def __call__(self):
        #id is part of uri, should not be in body
        if self.method == "PUT":
            body = dict(
                [
                    (k,v) for k,v in  self.options.iteritems() if  k != 'id'
                ]
            )
        else:
            body = self.options

        #headers
        headers = {'Content-Type': 'application/json'}
        headers.update(self.http_client.auth_header)

        return self.http_client.request(
            self.uri,
            self.method,
            headers=headers,
            body=json.dumps(body)
        )


class ReadDocumentRequest(object):
    def __init__(
        self,
        client,
        method,
        uri_parts,
        options=None
    ):
        self.http_client = client
        self.method = method
        self.uri_parts = uri_parts
        self.options = dict()
        if options:
            self.options = options

    @property
    def uri(self):
        """Create the URI with the parameters"""
        elements = []

        for part in self.uri_parts:
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
        headers = {"Accept": "application/json"}
        headers.update(self.http_client.auth_header)
        return self.http_client.request(
            self.uri,
            "GET",
            headers=headers
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
        request = self.request_builder.build(
            self.parts,
            kwargs
        )
        response, content = request()
        status = int(response['status'])
        #couchdb returns a content body for 400 series errors
        if status < 200 or status >= 300:
            raise ValueError, "Invalid return code. %s" % (str(response),)
        else:
            return json.loads(content)

    def __getattr__(self, name):
        return Part(
            self.parts + [name],
            self.request_builder
        )

