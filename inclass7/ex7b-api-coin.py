# Instructions. Implement the eth_latest_price function using the API from coinmarketcap.com
#
# Details: https://coinmarketcap.com/api/
#

def eth_latest_price():
    """
    Returns the latest Ethereum (ETH) price in USD using CoinMarketCap API.
    """
    import requests
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
    
    parameters = {
        'symbol': 'ETH',
        'convert': 'USD'
    }
    
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': '82925fe51e424632a8e4335f45824da1',
    }
    
    try:
        response = requests.get(url, headers=headers, params=parameters)
        response.raise_for_status()  # Raise error for bad status codes
        
        data = response.json()
        
        # Check for API-level errors
        if data['status']['error_code'] != 0:
            error_msg = data['status']['error_message']
            raise Exception(f"CoinMarketCap API error: {error_msg}")
        
        # Extract ETH price in USD
        price = data['data']['ETH']['quote']['USD']['price']
        
        return round(price, 2)  # Return price rounded to 2 decimal places
        
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {e}")
    except (KeyError, TypeError) as e:
        raise Exception(f"Failed to parse API response: {e}")


# Test the function
print(eth_latest_price())


print(eth_latest_price())


