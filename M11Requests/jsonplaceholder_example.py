# =============================================================================
# M09 - Practice 1: Exploring a REST API with JSONPlaceholder
# =============================================================================
# JSONPlaceholder is a free, fake REST API perfect for learning.
# It simulates a real server without requiring any sign-up or API key.
# URL: https://jsonplaceholder.typicode.com
#
# In this script, we will walk through the complete CRUD cycle:
#   C - Create  (POST)
#   R - Read    (GET)
#   U - Update  (PUT / PATCH)
#   D - Delete  (DELETE)
# =============================================================================

import requests

BASE_URL = 'https://jsonplaceholder.typicode.com'

# A visual separator to make the terminal output easier to read
DIVIDER = '-' * 50


# =============================================================================
# STEP 1: Fetch a single post (GET one resource)
# =============================================================================
# We target /posts/1 — the post with ID 1.
# This is the most basic operation: "give me this one specific thing."
# =============================================================================

print('STEP 1: Fetch a single post')
print(DIVIDER)

response = requests.get(f'{BASE_URL}/posts/1')

# Always check the status code first.
# 200 means "OK" — the server found what we asked for and returned it.
print(f'Status Code: {response.status_code}')

# .json() converts the raw response text into a Python dictionary for us.
post = response.json()
print(f'Post ID    : {post["id"]}')
print(f'User ID    : {post["userId"]}')
print(f'Title      : {post["title"]}')
print(f'Body       : {post["body"][:80]}...')  # Only show the first 80 characters
print()


# =============================================================================
# STEP 2: Fetch all posts by a specific user (GET with query parameters)
# =============================================================================
# The /posts endpoint returns ALL 100 posts by default.
# We use the 'params' argument to filter — this is much cleaner than
# manually building a URL string like "?userId=1&_limit=3".
# =============================================================================

print('STEP 2: Fetch posts by userId=1 (limited to 3 results)')
print(DIVIDER)

params = {
    'userId': 1,
    '_limit': 3   # JSONPlaceholder supports this custom parameter to limit results
}
response = requests.get(f'{BASE_URL}/posts', params=params)

print(f'Status Code  : {response.status_code}')
print(f'Total results: {len(response.json())}')
print()

posts = response.json()
for p in posts:
    print(f'  ID {p["id"]:>3} | {p["title"]}')

print()


# =============================================================================
# STEP 3: Create a new post (POST)
# =============================================================================
# We send a Python dictionary as the request body using the 'json=' argument.
# The requests library will automatically:
#   1. Convert the dictionary to a JSON string
#   2. Set the 'Content-Type: application/json' header for us
# =============================================================================

print('STEP 3: Create a new post')
print(DIVIDER)

new_post = {
    'title': 'My First API Post',
    'body': 'This was created by sending a POST request from a Python script!',
    'userId': 1
}

response = requests.post(f'{BASE_URL}/posts', json=new_post)

# A successful creation typically returns status code 201 ("Created"),
# not 200 ("OK"). This is an important distinction in REST API design.
print(f'Status Code: {response.status_code}')  # Expect: 201

created_post = response.json()
print(f'Server assigned ID : {created_post["id"]}')
print(f'Title              : {created_post["title"]}')
print(f'Body               : {created_post["body"]}')
print()

# Save the new ID for the next steps.
# NOTE: JSONPlaceholder is a fake API — it doesn't actually store the data.
# In a real API, this ID would refer to a record that was genuinely saved.
new_post_id = created_post['id']


# =============================================================================
# STEP 4a: Replace the post entirely (PUT)
# =============================================================================
# PUT replaces the *entire* resource. We must send ALL fields.
# If we omit a field, the server may treat it as null/empty.
# =============================================================================

print('STEP 4a: Replace the post with PUT')
print(DIVIDER)

replacement = {
    'id': new_post_id,
    'title': 'Completely Replaced Title',
    'body': 'This is the new body. The entire resource has been replaced.',
    'userId': 1
}

response = requests.put(f'{BASE_URL}/posts/{new_post_id}', json=replacement)

print(f'Status Code : {response.status_code}')  # Expect: 200
print(f'Updated post: {response.json()}')
print()


# =============================================================================
# STEP 4b: Update only one field (PATCH)
# =============================================================================
# PATCH is more surgical — we only need to send the fields we want to change.
# The server is expected to leave all other fields untouched.
# =============================================================================

print('STEP 4b: Update only the title with PATCH')
print(DIVIDER)

partial_update = {
    'title': 'Only This Title Was Changed by PATCH'
}

response = requests.patch(f'{BASE_URL}/posts/{new_post_id}', json=partial_update)

print(f'Status Code : {response.status_code}')  # Expect: 200
updated = response.json()
# Notice: 'body' is still present even though we only sent 'title' in our request
print(f'Updated title: {updated["title"]}')
print(f'Body (unchanged): {updated.get("body", "(not returned — this is a fake API)")}')
print()


# =============================================================================
# STEP 5: Delete the post (DELETE)
# =============================================================================
# We target the specific resource by its ID in the URL path.
# A successful deletion usually returns 200 OK or 204 No Content.
# The response body is typically empty (or an empty JSON object {}).
# =============================================================================

print('STEP 5: Delete the post')
print(DIVIDER)

response = requests.delete(f'{BASE_URL}/posts/{new_post_id}')

print(f'Status Code    : {response.status_code}')  # Expect: 200
print(f'Response body  : {response.text}')          # Expect: {}
print()
print('Full CRUD cycle complete!')
