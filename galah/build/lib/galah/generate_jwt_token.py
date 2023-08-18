import json
import argparse
import requests
import jwt
import time

# global to store current token info
token_obj = {}

def main():
    filepath, token_url, client_id, client_secret = parse_input()
    token_config = {"token_url": token_url, "client_id": client_id, "client_secret": client_secret}

    # read token JSON file
    read_token_file(filepath)

    # usage example of access token with a protected ala api
    api_example_request(token_config)

def parse_input():

    parser = argparse.ArgumentParser(description="This script uses (and re-generated if needed) a JSON Web Token (JWT) for requests to protected ALA services. A a JSON file containing the initially generated token, regeneration and expiry details is expected as an argument", add_help=True, allow_abbrev=True,)

    # required non-positional arguments for filepath
    parser.add_argument('--file', type=str, help="Path to the JSON file containing the jwt access token, expiry and re-generation details", required=True, nargs='?')
    parser.add_argument('--tokenUrl', type=str, help="URL for for the JWT token generation service e.g. https://auth.ala.org.au/cas/oidc/oidcAccessToken", required=True, nargs='?')
    parser.add_argument('--clientId', type=str, help="Client ID previously used  for JWT generation", required=True, nargs='?')
    parser.add_argument('--clientSecret', type=str, help="Client Secret previously used for JET generation", required=True, nargs='?')

    args = parser.parse_args()

    return args.file, args.tokenUrl, args.clientId, args.clientSecret

# read the JSON file and save to global token_obj
def read_token_file(filepath):
    with open(filepath) as f:
        file_obj = json.load(f)
        # add just required values from JSON file to global token_obj
        token_obj["access_token"] = file_obj["access_token"]
        token_obj["id_token"] = file_obj["id_token"]
        token_obj["refresh_token"] = file_obj["refresh_token"]
        token_obj["scope"] = file_obj["scope"]

def get_token(token_config):
    # if expired regenerate, else just return the access_token
    print(token_obj)
    print(token_obj["access_token"])
    decoded = jwt.decode(token_obj["access_token"], options={"verify_signature": False})
    # re-generate token when expired.
    if decoded["exp"] < int(time.time()) :
        # regenerate token and update token_obj
        print("Current token has expired. Refreshing token...")
        regenerate_token(token_config)
    return token_obj["access_token"]

# regenerate token, return new token and update token_obj
def regenerate_token(token_config):
    payload = {'refresh_token': token_obj["refresh_token"], 'grant_type': 'refresh_token', 'scope':token_obj["scope"]}
    # refreshing token
    r = requests.post(token_config["token_url"], data=payload, auth=(token_config["client_id"], token_config["client_secret"]))
    if r.ok:
        data = r.json()
        token_obj["access_token"] = data["access_token"]
        token_obj["id_token"] = data["id_token"]
        print("Token refreshed")
    else:
        print("Unable to refresh access token. ", r.status_code)


def api_example_request(token_config):
    url = "https://api.test.ala.org.au/surveys/ws/project/search?hub=ala&max=20&offset=0&isCitizenScience=false&isWorks=false&isBiologicalScience=false&isWorldWide=false&isUserPage=false&mobile=false&flimit=15"
    # get the JWT
    print("getting jwt")
    jwt = get_token(token_config)
    print("jwt: {}".format(jwt))
    headers = {'user-agent': 'token-refresh/0.1.1', 'Authorization': 'Bearer {0}'.format(jwt)}
    r = requests.get(url, headers=headers)
    if r.ok:
        print(r.status_code, r.text)
    else:
        print("Error encountered during request ", r.status_code)


if __name__ == '__main__':
    main()