import clients.tda as tda
import pandas as pd
import plotnine as pn


def parse_historical_response(result, symbol):
    if result.status_code == 200:
        response_body = result.json()

        history = pd.DataFrame(response_body["candles"])
        return history


client = tda.TDAClient("SZKIIQY0STUI4WGFAQCVLOBJANB61M0H")
client.get_access_token()

symb = "SPY"
quote_results = client.get_quote_history(symb, startdate="2019-01-01")

spy_history = parse_historical_response(quote_results, symb)
spy_history["datetime"] = pd.to_datetime(spy_history["datetime"], unit="ms")
print(spy_history)

