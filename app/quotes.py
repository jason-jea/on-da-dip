import tdaclient.client as tda


def parse_quotes_response(result, symbol):
    if result.status_code == 200:
        response_body = result.json()

        if symbol in response_body.keys():
            response_body = response_body[symbol]
            asset_type = response_body["assetType"]
            description= response_body["description"]
            last_price = response_body["lastPrice"]
            msg = "Asset Type: " + asset_type + "\nDescription: " + description + "\nLast Price: " + str(last_price)
            print(msg)
        else:
            print("Invalid symbol.")


client = tda.TDAClient("SZKIIQY0STUI4WGFAQCVLOBJANB61M0H")
client.get_access_token()

symbol = "SPY"
quote_results = client.get_quote(symbol)

parse_quotes_response(quote_results, symbol)

