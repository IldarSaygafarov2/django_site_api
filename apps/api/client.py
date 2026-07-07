base_url = 'http://127.0.0.1:8000/api'

import requests


def authenticate():
    username = 'fromapiuser'
    password = 'string321321'

    response = requests.post(f'{base_url}/auth/login/',
                             data={'username': username, 'password': password})
    response.raise_for_status()
    return response.json()['access']


def get_categories():
    access_token = authenticate()

    response = requests.get(f'{base_url}/categories/', headers={
        'Authorization': f'Bearer {access_token}'
    })
    # response.raise_for_status()
    print(response.json())

# get_categories()

token = authenticate()
print(token)
resp = requests.get(f'{base_url}/users/me/',
                    headers={
                        'Authorization': f'Bearer {token}'
                    })
resp.raise_for_status()
print(resp.json())
# print(token)
# resp = requests.post(f'{base_url}/posts/3/comments/create/', headers={
#     'Authorization': f'Bearer {token}'
# }, json={'content': 'test comment'})
# print(resp)