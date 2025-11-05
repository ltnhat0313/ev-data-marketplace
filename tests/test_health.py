def test_health(client):
    r = client.get('/health')
    assert r.status_code == 200
    assert r.json().get('status') == 'ok'


def test_ready(client):
    r = client.get('/ready')
    assert r.status_code == 200
    assert r.json().get('ready') is True


def test_robots(client):
    r = client.get('/robots.txt')
    assert r.status_code == 200
    assert 'User-agent' in r.text


