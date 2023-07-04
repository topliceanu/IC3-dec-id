import requests
import os
from dotenv import load_dotenv
import json
import sys

load_dotenv()

API_ENDPOINT = 'https://discord.com/api/v10'
CLIENT_ID = os.getenv('DISCORD_APPLICATION_ID')
CLIENT_SECRET = os.getenv('DISCORD_CLIENT_SECRET')
REDIRECT_URI = os.getenv('REDIRECT_URI')

def exchange_code(code):
  data = {
    'client_id': CLIENT_ID,
    'client_secret': CLIENT_SECRET,
    'grant_type': 'authorization_code',
    'code': code,
    'redirect_uri': REDIRECT_URI
  }
  headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
  }
  r = requests.post('%s/oauth2/token' % API_ENDPOINT, data=data, headers=headers)
  r.raise_for_status()
  return r.json()

def get_token():
    data = {
        'grant_type': 'client_credentials',
        'scope': 'identify guilds connections guilds.members.read'
    }

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    r = requests.post('%s/oauth2/token' % API_ENDPOINT, data=data, headers=headers, auth=(CLIENT_ID, CLIENT_SECRET))
    r.raise_for_status()
    return r.json()

def get_user_server_list(access_token):
  headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Authorization': f'Bearer {access_token}'
  }

  print("headers", headers)
  r = requests.get('%s/users/@me/guilds' % API_ENDPOINT, headers=headers)
  r.raise_for_status()
  return r.json()

auth_obj = exchange_code(sys.argv[1])
print("auth obj", auth_obj)
# print("access token", auth_obj['access_token'])

# auth_obj = get_token()
# server_list = get_user_server_list(auth_obj['access_token'])
#
# found = False
# for server in server_list:
#     if server['id'] == DISCORD_SERVER_ID:
#         print('user is a part of dec-id')
#         found = True
#
# if not found:
#     print('user is NOT a part of dec-id')
