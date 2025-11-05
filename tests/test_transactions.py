from io import BytesIO


def register_and_login(client):
    client.post('/auth/register', json={'email': 'buyer@example.com', 'username': 'buyer', 'password': 'secret123'})
    r = client.post('/auth/login', json={'email': 'buyer@example.com', 'password': 'secret123'})
    return r.json()['access_token']


def create_dataset(client, token):
    csv_bytes = b"col1,col2\n1,2\n"
    files = { 'file': ('test.csv', BytesIO(csv_bytes), 'text/csv') }
    data = { 'title': 'Buyable', 'description': 'x', 'price': '1.0' }
    r = client.post('/datasets/upload', headers={'Authorization': f'Bearer {token}'}, files=files, data=data)
    assert r.status_code == 200
    return r.json()['id']


def test_purchase_flow(client):
    token = register_and_login(client)
    dataset_id = create_dataset(client, token)
    r = client.post('/transactions/purchase', headers={'Authorization': f'Bearer {token}'}, params={'dataset_id': dataset_id})
    assert r.status_code == 200
    body = r.json()
    assert body['ok'] is True and body['dataset_id'] == dataset_id


