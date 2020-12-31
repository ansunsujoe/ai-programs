import requests
import sys

if len(sys.argv) < 6:
  print('Usage: python quotes.py <apikey> <token> <symbol> <period_type> <period_value> <freq_type> <freq_value>')
  print('Period type : day, month, year, ytd')
  print('Freqcy type : minute, daily, weekly, monthly')
  sys.exit(1)

apikey       = sys.argv[1]
token        = sys.argv[2]
symbol       = sys.argv[3]
period_type  = sys.argv[4]
period_value = sys.argv[5]
freq_type    = sys.argv[6]
freq_value   = sys.argv[7]

auth_url = r'https://api.tdameritrade.com/v1/oauth2/token'

# define headers
auth_headers = {
   'Content-Type':'application/x-www-form-urlencoded'
}
auth_payload = {
   'grant_type':'refresh_token',
   'refresh_token':token,
   'client_id':apikey,
   'redirect_uri':'https://localhost/test'
}

def auth_token():
    # post the data to get the token
    authReply = requests.post(auth_url, headers=auth_headers, data=auth_payload)

    # convert json to dictionary
    decoded_content = authReply.json()

    # grab the access token
    access_token = decoded_content["access_token"]
    response_auth_headers = {'Authorization':'Bearer {}'.format(access_token)}

    return response_auth_headers

auth_ret = auth_token()

auth_token = auth_ret['Authorization']

# define headers
request_headers = {
   'Content-Type':'application/x-www-form-urlencoded'
}
request_payload = {
   'Authorization':auth_token,
}

quote_url = f'https://api.tdameritrade.com/v1/marketdata/{symbol}/pricehistory?apikey={apikey}&periodType={period_type}&period={period_value}&frequencyType={freq_type}&frequency={freq_value}'

def get_quotes():
    # post the data to get the response
    response = requests.request("GET", quote_url, headers=request_headers, data=request_payload)
    
    # convert json to dictionary
    decoded_content = response.json()

    return decoded_content

quotes = get_quotes()

print(quotes)
