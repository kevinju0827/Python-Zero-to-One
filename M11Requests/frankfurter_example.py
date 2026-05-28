# =============================================================================
# M11 - Practice 2: Fetching Live Data from a Public REST API
# =============================================================================
# Service : Frankfurter (https://www.frankfurter.app/)
# API Base: https://api.frankfurter.app
#
# Frankfurter is a free, open-source currency exchange rate API.
# It requires NO API key and NO registration — perfect for learning.
#
# Scenario: Build a simple currency converter that fetches live exchange
# rates and lets the user convert an amount from USD to other currencies.
# =============================================================================

import requests

BASE_URL = 'https://api.frankfurter.app'
DIVIDER = '-' * 50


# =============================================================================
# STEP 1: Fetch live exchange rates with query parameters
# =============================================================================
# Endpoint: GET /latest
# Parameters:
#   from = the base currency (we use USD)
#   to   = a comma-separated list of target currencies
#
# We only request 3 currencies to keep the response focused.
# The 'params' dictionary is the clean, correct way to build query strings.
# =============================================================================

print('STEP 1: Requesting exchange rates from the API...')
print(DIVIDER)

params = {
    'from': 'USD',
    'to': 'EUR,JPY,TWD'
}

try:
    response = requests.get(f'{BASE_URL}/latest', params=params)

    # raise_for_status() will immediately raise an exception if the server
    # returned a 4xx (client error) or 5xx (server error) status code.
    # If the status is 2xx (success), it does nothing and we continue.
    response.raise_for_status()

except requests.exceptions.ConnectionError:
    print('ERROR: Could not connect to the server.')
    print('Please check your internet connection and try again.')
    exit()  # Stop the script — there is nothing useful we can do without data

except requests.exceptions.HTTPError as err:
    print(f'ERROR: The server returned an error: {err}')
    exit()

# If we reach this line, the request was successful.
data = response.json()

print(f'Status Code : {response.status_code}')
print(f'Raw response: {data}')
print()


# =============================================================================
# STEP 2: Parse and display a formatted report
# =============================================================================
# The response JSON looks like this:
# {
#     "amount": 1.0,
#     "base": "USD",
#     "date": "2025-01-15",
#     "rates": {
#         "EUR": 0.9234,
#         "JPY": 155.21,
#         "TWD": 32.85
#     }
# }
#
# We extract the parts we need and display them cleanly.
# =============================================================================

print('STEP 2: Formatted exchange rate report')
print(DIVIDER)

base_currency = data['base']
rate_date = data['date']
rates = data['rates']   # This is a nested dictionary: {"EUR": 0.9234, ...}

print(f'Exchange rates from {base_currency} (as of {rate_date}):')
for currency, rate in rates.items():
    # f-string formatting:
    #   {currency:<5} — left-align in a field of 5 characters
    #   {rate:>10.4f} — right-align, display as a float with 4 decimal places
    print(f'  {currency:<5} : {rate:>10.4f}')

print()


# =============================================================================
# STEP 3: Interactive currency converter
# =============================================================================
# We ask the user to enter an amount in USD, then calculate and display
# the equivalent value in each of the three target currencies.
# =============================================================================

print('STEP 3: Currency Converter')
print(DIVIDER)

# input() always returns a string — we must convert it to a number.
# We use float() so the user can enter decimal amounts like 99.99.
try:
    amount_str = input('Enter an amount in USD to convert: $ ')
    amount_usd = float(amount_str)
except ValueError:
    # The user typed something that cannot be converted to a float (e.g., "abc")
    print('ERROR: Please enter a valid number.')
    exit()

print()
print(f'$ {amount_usd:.2f} USD is equivalent to:')
print(DIVIDER)

for currency, rate in rates.items():
    converted = amount_usd * rate

    # We apply different formatting rules depending on the currency.
    # JPY has no decimal places by convention; others typically show 2.
    if currency == 'JPY':
        print(f'  {currency}: {converted:>12,.0f}')
    else:
        print(f'  {currency}: {converted:>12,.2f}')

print()
print(f'(Rates sourced from Frankfurter API, dated {rate_date})')
