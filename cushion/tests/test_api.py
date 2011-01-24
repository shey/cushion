from cushion.api import Cushion


def test_create_client_with_server_uri_only():
    """Test Create Client with server uri only"""
    c = Cushion("http://localhost:5984")
    assert c.base_uri == "http://localhost:5984"
    assert c.password == None
    assert c.username == None
    assert c.timeout == None

def test_create_client_with_server_uri_username_and_password():
    """Test create client with server_uri, username and password"""
    c = Cushion(
        "http://localhost:5984",
        password="admin1",
        username="admin"
    )
    assert c.base_uri == "http://localhost:5984"
    assert c.password == "admin1"
    assert c.username == "admin"
    assert c.timeout == None

def test_create_client_with_server_uri_and_timeout():
    """Create client with server_uri and tiemout"""
    c = Cushion(
        "http://localhost:5984",
        timeout=5
    )
    assert c.base_uri == "http://localhost:5984"
    assert c.password == None
    assert c.username == None
    assert c.timeout == 5

def test_create_client_with_all_options():
    """Create client with server_uri, username, password and timeout"""
    c = Cushion(
        "http://localhost:5984",
        username="admin",
        password="admin1",
        timeout=5
    )
    assert c.base_uri == "http://localhost:5984"
    assert c.password == "admin1"
    assert c.username == "admin"
    assert c.timeout == 5