# Instructions. Implement the convert_currency function using the API in RapidAPI.com
#
# Hints: use this API https://rapidapi.com/exchangerateapi/api/exchangerate-api

# Return the amount with real time rate


def convert_currency(amount, from_currency, to_currency):
    """
    Converts amount from from_currency to to_currency using real-time rates
    via the ExchangeRate-API on RapidAPI.
    """
    import requests
    if from_currency.upper() == to_currency.upper():
        return float(amount)
    
    url = f"https://exchangerate-api.p.rapidapi.com/rapid/latest/{from_currency.upper()}"
    
    headers = {
        'X-RapidAPI-Key': '0d7f1fe33fmsh26df5caf453a834p160688jsndee3bb1a8411',
        'X-RapidAPI-Host': 'exchangerate-api.p.rapidapi.com'
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"API request failed: {response.status_code} - {response.text}")
    
    data = response.json()
    
    if data.get('result') != 'success':
        error = data.get('error', 'Unknown error')
        raise Exception(f"API error: {error}")
    
    rates = data.get('rates', {})
    to_currency = to_currency.upper()
    
    if to_currency not in rates:
        raise Exception(f"Target currency '{to_currency}' not supported")
    
    rate = rates[to_currency]
    return round(amount * rate, 2)  # Return rounded to 2 decimal places


print(convert_currency(10_000,"HKD","USD"))  # should give roughly 1278
print(convert_currency(1_000_000,"JPY","HKD"))  # should give roughly 52000