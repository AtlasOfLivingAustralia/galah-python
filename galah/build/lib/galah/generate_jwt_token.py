import json
import requests
#import jwt
import time
import os
#import python_jwt as genjwt
#import jwcrypto.jwk as jwk

# global to store current token info
token_obj = {}

def generate_token_config(client_id = None,
                          client_secret = None):

    # set filepath and token_url
    filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ALA_keys.json')
    token_url = "https://auth-secure.auth.ap-southeast-2.amazoncognito.com/oauth2/token"

    # generate token configuration
    token_config = {"token_url": token_url, "client_id": client_id, "client_secret": client_secret}

    # read token JSON file
    read_token_file(filepath)

    return token_config

'''
def parse_input():

    parser = argparse.ArgumentParser(description="This script uses (and re-generated if needed) a JSON Web Token (JWT) for requests to protected ALA services. A a JSON file containing the initially generated token, regeneration and expiry details is expected as an argument", add_help=True, allow_abbrev=True,)

    # required non-positional arguments for filepath
    parser.add_argument('--file', type=str, help="Path to the JSON file containing the jwt access token, expiry and re-generation details", required=True, nargs='?')
    parser.add_argument('--tokenUrl', type=str, help="URL for for the JWT token generation service e.g. https://auth.ala.org.au/cas/oidc/oidcAccessToken, https://auth-test.ala.org.au/cas/oidc/oidcAccessToken, or https://auth-secure.auth.ap-southeast-2.amazoncognito.com/oauth2/token", required=True, nargs='?')
    parser.add_argument('--clientId', type=str, help="Client ID previously used  for JWT generation", required=True, nargs='?')
    parser.add_argument('--clientSecret', type=str, help="Client Secret previously used for JET generation", required=False, nargs='?')

    args = parser.parse_args()

    return args.file, args.tokenUrl, args.clientId, args.clientSecret
'''

# read the JSON file and save to global token_obj
def read_token_file(filepath):
    with open(filepath) as f:
        file_obj = json.load(f)
        # add just required values from JSON file to global token_obj
        token_obj["access_token"] = file_obj["access_token"]
        token_obj["id_token"] = file_obj["id_token"]
        token_obj["refresh_token"] = file_obj["refresh_token"]
        token_obj["scope"] = file_obj["scope"]

def get_jwt_token(token_config):
    print(token_config)
    print(token_obj)
    # if expired regenerate, else just return the access_token
    decoded = jwt.decode(token_obj["access_token"], options={"verify_signature": False})
    # re-generate token when expired.
    if decoded["exp"] < int(time.time()) :
        # regenerate token and update token_obj
        print("Current token has expired. Refreshing token...")
        regenerate_token(token_config)
    return token_obj["access_token"]

# regenerate token, return new token and update token_obj
def regenerate_token(token_config):
    # for cognito auth system use the payload below
    payload = {'refresh_token': token_obj["refresh_token"], 'grant_type': 'refresh_token', 'scope':token_obj["scope"], 'client_id':token_config["client_id"]}

    # for CAS auth system use the payload below
    # payload = {'refresh_token': token_obj["refresh_token"], 'grant_type': 'refresh_token', 'scope':token_obj["scope"]}

    # for cognito auth system use the request below
    r = requests.post(token_config["token_url"], data=payload)

    # for CAS auth system use the payload below
    # r = requests.post(token_config["token_url"], data=payload, auth=(token_config["client_id"], token_config["client_secret"]))

    if r.ok:
        data = r.json()
        token_obj["access_token"] = data["access_token"]
        token_obj["id_token"] = data["id_token"]
        print("Token refreshed")
    else:
        print("Unable to refresh access token. ", r.status_code, r.content)

'''
def api_example_request(token_config):
    url = "https://api.test.ala.org.au/occurrences/config"
    # get the JWT
    jwt = get_jwt_token(token_config)
    headers = {'user-agent': 'token-refresh/0.1.1', 'Authorization': 'Bearer {0}'.format(jwt)}
    r = requests.get(url, headers=headers)
    if r.ok:
        print(r.status_code, r.text)
    else:
        print("Error encountered during request ", r.status_code)
'''