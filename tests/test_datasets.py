from io import BytesIO


def register_and_login(client):
    client.post('/auth/register', json={'email': 'prov@example.com', 'username': 'prov', 'password': 'secret123'})
    r = client.post('/auth/login', json={'email': 'prov@example.com', 'password': 'secret123'})
    return r.json()['access_token']


def test_search_and_summary_initial(client):
    r = client.get('/datasets/search')
    assert r.status_code == 200
    data = r.json()
    assert data['total'] == 0

    r2 = client.get('/datasets/stats/summary')
    assert r2.status_code == 200
    s = r2.json()
    assert 'users' in s and 'datasets' in s and 'transactions' in s


def test_upload_and_search(client):
    token = register_and_login(client)
    csv_bytes = b"col1,col2\n1,2\n3,4\n"
    files = {
        'file': ('test.csv', BytesIO(csv_bytes), 'text/csv')
    }
    data = {
        'title': 'Test Dataset',
        'description': 'Sample',
        'price': '9.99'
    }
    r = client.post('/datasets/upload', headers={'Authorization': f'Bearer {token}'}, files=files, data=data)
    assert r.status_code == 200
    ds = r.json()
    assert ds['title'] == 'Test Dataset'

    r2 = client.get('/datasets/search', params={'q': 'Test'})
    assert r2.status_code == 200
    items = r2.json()['items']
    assert any(i['title'] == 'Test Dataset' for i in items)


