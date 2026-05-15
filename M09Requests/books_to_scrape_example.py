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
#
# NOTE: In this practice, we only FETCH the HTML. We do NOT parse it.
# Parsing HTML to extract specific data (like titles and prices) requires
# a library called BeautifulSoup — that is the topic of M10.
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
# STEP 5: Reflection — why do we need BeautifulSoup?
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

    # Show 200 characters of context around it — notice how messy the HTML tags are
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
# REFLECTION (read this comment block carefully):
#
# Q: Why would it be difficult to extract just the list of book titles
#    using only string methods like .find() or .split()?
#
# A: HTML is a deeply nested, tag-based format. Even though we *found*
#    the title text, it is buried inside layers of tags like:
#
#      <article class="product_pod">
#        <h3><a href="..." title="Tipping the Velvet">Tipping the ...</a></h3>
#        ...
#      </article>
#
#    To extract *all* titles, we would need to:
#      - Handle inconsistent whitespace and newlines
#      - Navigate through parent and sibling tags
#      - Deal with truncated text (the <a> tag shows a short version)
#      - Handle any edge cases in the HTML structure
#
#    String methods become brittle and hard to maintain very quickly.
#    A proper HTML parser like BeautifulSoup understands the tree structure
#    of the document and lets us say things like:
#
#      soup.find_all('article', class_='product_pod')
#
#    ...which is precise, readable, and robust. That is exactly what M10
#    will teach you.
# =============================================================================

print('Reflection printed in the source code as a comment block.')
print('Open this .py file and read the comment at the bottom of Step 5.')
