import requests

client_id = '51690111'
client_secret = '5630063b5630063b5630063b375524bc44556305630063b32aa9a6d437d173a85b896c0'
redirect_uri = 'https://api.vk.com/blank.html&display=page&response_type=token'

url = 'https://oauth.vk.com/access_token'
params = {
    'client_id': client_id,
    'client_secret': client_secret,
    'edirect_uri': redirect_uri,
    'grant_type': 'client_credentials'
}

response = requests.post(url, params=params)

if response.status_code == 200:
    access_token = response.json()['access_token']
    print('Access Token:', access_token)
else:
    print('Error:', response.text)