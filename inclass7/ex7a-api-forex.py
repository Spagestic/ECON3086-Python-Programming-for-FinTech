# Instructions. Implement the convert_currency function using the API in RapidAPI.com
#
# Hints: use this API https://rapidapi.com/exchangerateapi/api/exchangerate-api

# Return the amount with real time rate


def convert_currency(amount, from_currency, to_currency):
    # This function takes in an amount, the currency of the amount (from_currency), and the currency to convert to (to_currency).
    # It returns the converted amount based on the real-time exchange rate.
    pass


print(convert_currency(10_000,"HKD","USD"))  # should give roughly 1278
print(convert_currency(1_000_000,"JPY","HKD"))  # should give roughly 52000