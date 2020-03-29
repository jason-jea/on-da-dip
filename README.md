# on-da-dip
rough idea: Create a web app that allows users access to better visualization tools than what they can find in typical trading platforms.  Potentially down the line allows users to sync their trading accounts with the app to get more information about returns and trends.  Additionally, a major inspiration for this project is figuring out a way to build intuition for trading options by providing more educational charts and tables, in addition to collecting historical option prices.  The primary datasource will be through the TDA api.

# Setup
For collaborators.  Make sure you have login credentials for a TDA developer account, and that you've cloned the repo. Then create an app within TDA (follow steps [here](https://developer.tdameritrade.com/content/getting-started)).  For those using my developer account, note that I've set the redirect URI to https://tolocalhost.com/.


# Authentication:
Follow steps to create a refresh token from the [TDA documentation](https://developer.tdameritrade.com/content/simple-auth-local-apps). Some notes:

- if you're using https://tolocalhost.com/ as a callback, make sure you don't check the "redirect to localhost" box so that you can actually copy and past the code within the redirect
- OAUTH flow leverages your primary TDA trading account info

After you've generated an initial access and refresh token, create a txt file in your main `on-da-dip/` directory called `tokeninfo.txt`.  Paste your _refresh token_ into this file and save!  We've added this file to .gitignore so this info will not get committed.  The app will rely on reading the credentials from this file in order to authenticate.
