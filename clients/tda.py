import requests
import os


class TDAClient:

    def __init__(self, client_id):
        # need to initialize with client_id found in developer account settings
        self.client_id = client_id
        self.access_token = None
        self.url = "https://api.tdameritrade.com/v1/"

    def get_access_token(self):
        # implement refresh token method for getting access token
        # will need to implement method for refreshing refresh token (90 day expiration)
        # reliant on a tokeninfo.txt containing the refresh token to exist in on-da-dip/tdaclient within the server

        cwd = os.getcwd()
        dir = os.path.dirname(cwd)
        refresh_token_file = open(dir + "/tokeninfo.txt", "r")
        refresh_token = refresh_token_file.readline()
        refresh_token_file.close()

        endpoint = self.url + "oauth2/token"
        grant_type = "refresh_token"
        access_type = "offline"

        data = {
            "grant_type": grant_type,
            "access_type": access_type,
            "refresh_token": refresh_token,
            "client_id": self.client_id
        }

        result = requests.post(url=endpoint, data=data)

        if result.status_code == 200:
            result_body = result.json()
            self.access_token = result_body["access_token"]

            cwd = os.getcwd()
            dir = os.path.dirname(cwd)
            refresh_token_file = open(dir + "/tokeninfo.txt", "wt")
            # need to update token file with latest refresh token
            refresh_token_file.write(result_body["refresh_token"])
            refresh_token_file.close()

        elif result.status_code == 401:
            print("Invalid credentials.")
        elif result.status_code == 403:
            print("User doesn't have access to this account and/or permissions.")
        elif result.status_code == 400:
            print("Validation unsuccessful.  Check that client id and refresh tokens are correct.")
        elif result.status_code == 500:
            print("Server error, try again later.")
        else:
            print("Unknown error.")

    def get_quote(self, symbol):
        endpoint = self.url + "marketdata/" + symbol + "/quotes"

        headers = {
            "Authorization": "Bearer " + self.access_token
        }

        data = {
            "apikey": self.client_id
        }

        result = requests.get(url=endpoint, data=data, headers=headers)
        return result

