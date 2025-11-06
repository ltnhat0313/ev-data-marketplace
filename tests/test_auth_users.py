def register(client, email="test@example.com", username="tester", password="secret123"):
    r = client.post('/auth/register', json={
        'email': email,
        'username': username,
        'password': password
    })
    assert r.status_code == 200
    return r.json()


def login(client, email="test@example.com", password="secret123", code=None):
    payload = {'email': email, 'password': password}
    if code:
        payload['code'] = code
    r = client.post('/auth/login', json=payload)
    assert r.status_code == 200
    data = r.json()
    assert 'access_token' in data
    return data['access_token']


def test_register_login_me(client):
    user = register(client)
    token = login(client)
    r = client.get('/users/me', headers={'Authorization': f'Bearer {token}'})
    assert r.status_code == 200
    me = r.json()
    assert me['email'] == 'test@example.com'


