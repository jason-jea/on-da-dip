import requests

class tdaclient:

    def __init__(self, client_id):
        self.client_id = client_id
        self.access_token = None

    def get_access_token(self):
        refresh_token_file = open("tokeninfo.txt", "r")
        refresh_token = refresh_token_file.readline()
        refresh_token_file.close()
        endpoint = "https://api.tdameritrade.com/v1/oauth2/token"
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
        elif 401:
            print("Invalid credentials.")
        elif 403:
            print("User doesn't have access to this account and/or permissions.")
        elif 400:
            print("Validation unsuccessful.  Check that client id and refresh tokens are correct.")
        elif 500:
            print("Server error, try again later.")
        else:
            print("Unknown error.")

client = tdaclient("SZKIIQY0STUI4WGFAQCVLOBJANB61M0H")
client.get_access_token()
print(client.access_token)