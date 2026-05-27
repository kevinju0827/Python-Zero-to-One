# =============================================================================
# M09 - Practice 3: Fetching Content from a Regular Webpage
# =============================================================================
# Service: Books to Scrape (https://books.toscrape.com/)
#
# This is a legal, purpose-built website designed specifically for
# practising web scraping. It is safe and will never block your requests.
#
# IMPORTANT DISTINCTION:
#   - Practice 1 & 2 talked to REST APIs  → responses were JSON
#   - This practice fetches a real webpage → response is HTML
#
# The requests library works identically in both cases.
# What changes is what comes back and how we interpret it.
# =============================================================================

import requests

TARGET_URL = 'https://books.toscrape.com/'
DIVIDER = '-' * 50


# =============================================================================
# STEP 1: Send a GET request to the webpage
# =============================================================================
# From the requests library's point of view, fetching a webpage is identical
# to calling a JSON API. The difference is invisible until we look at the
# response.
# =============================================================================

print('STEP 1: Sending GET request to Books to Scrape...')
print(DIVIDER)

try:
    response = requests.get(TARGET_URL)
    response.raise_for_status()
    print(f'Request successful!')

except requests.exceptions.ConnectionError:
    print('ERROR: Could not connect. Please check your internet connection.')
    exit()

except requests.exceptions.HTTPError as err:
    print(f'ERROR: Server returned an error: {err}')
    exit()

print()


# =============================================================================
# STEP 2: Inspect the response metadata
# =============================================================================
# Before looking at the content itself, let's examine the headers.
# Headers tell us important things about what came back.
# =============================================================================

print('STEP 2: Inspecting the response')
print(DIVIDER)

print(f'Status Code  : {response.status_code}')

# The Content-Type header reveals the format of the response body.
# Compare what you see here to what you would see from a JSON API.
content_type = response.headers.get('Content-Type', 'Not specified')
print(f'Content-Type : {content_type}')

# The Content-Length header tells us the size of the response, in bytes.
# Not all servers include this — some use chunked transfer encoding instead.
content_length = response.headers.get('Content-Length', 'Not provided by server')
print(f'Content-Length: {content_length}')

# We can also check the final URL after any redirects.
print(f'Final URL    : {response.url}')
print()


# =============================================================================
# STEP 3: Inspect the raw response body (HTML)
# =============================================================================
# response.text contains the entire raw HTML of the page as one large string.
# We only print the first 500 characters to avoid flooding the terminal.
# =============================================================================

print('STEP 3: Preview of the raw HTML content (first 500 characters)')
print(DIVIDER)

preview = response.text[:500]
print(preview)
print()
print(f'... (total length: {len(response.text):,} characters)')
print()


# =============================================================================
# STEP 4: Contrast with a JSON API response
# =============================================================================
# Let's make a quick call to a JSON API for comparison.
# This side-by-side contrast highlights the core difference between
# fetching a webpage and calling a REST API.
# =============================================================================

print('STEP 4: Contrast — fetching a JSON API for comparison')
print(DIVIDER)

json_response = requests.get('https://jsonplaceholder.typicode.com/posts/1')

print('--- Webpage response (Books to Scrape) ---')
print(f'Content-Type : {response.headers.get("Content-Type")}')
print(f'Preview      : {response.text[:120].strip()}')
print()

print('--- JSON API response (JSONPlaceholder) ---')
print(f'Content-Type : {json_response.headers.get("Content-Type")}')
print(f'Preview      : {json_response.text[:120].strip()}')
print()


# =============================================================================
# STEP 5: The struggle of using plain string methods
# =============================================================================
# Try to find the word "Tipping the Velvet" (one of the book titles on the
# homepage) inside the raw HTML using a plain Python string method.
# =============================================================================

print('STEP 5: Attempting to find data using plain string methods')
print(DIVIDER)

search_term = 'Tipping the Velvet'
html = response.text

if search_term in html:
    # Find the character position of the title in the HTML string
    position = html.find(search_term)

    # Show 250 characters of context around it — notice how messy the HTML tags are
    surrounding_html = html[position - 100 : position + 150]
    print(f'Found "{search_term}" at character position {position}.')
    print()
    print('The raw HTML surrounding it looks like this:')
    print(DIVIDER)
    print(surrounding_html)
    print(DIVIDER)
else:
    print(f'Could not find "{search_term}" in the raw HTML.')

print()


# =============================================================================
# STEP 6: The Better Way — Using BeautifulSoup
# =============================================================================
# String methods break as soon as HTML structure changes or scales.
# A proper parser like BeautifulSoup understands the tree structure of the
# document, making data extraction precise and robust.
# =============================================================================

print('STEP 6: Extracting data with BeautifulSoup')
print(DIVIDER)

try:
    from bs4 import BeautifulSoup
except ImportError:
    print('BeautifulSoup is not installed. Please run: pip install beautifulsoup4')
    exit()

# 1. Parse the raw HTML string into a BeautifulSoup object
soup = BeautifulSoup(response.text, 'html.parser')

# 2. Find all <article> tags with the class 'product_pod'
articles = soup.find_all('article', class_='product_pod')

print(f'Found {len(articles)} books on the page using BeautifulSoup. Here are all the titles:\n')

# 3. Loop through the articles and extract the title attribute from the <a> tag
for index, article in enumerate(articles, start=1):
    # The structure is: <article> -> <h3> -> <a title="The Title">
    title = article.h3.a['title']
    print(f'{index:>2}. {title}')

print()