# Source: https://realpython.com/python-web-scraping-practical-introduction/

from urllib.request import urlopen

# Open the page with the specified url (Aphrodite page)
url = "http://olympus.realpython.org/profiles/aphrodite"
page = urlopen(url)

# Get the HTML content of the page
html_bytes = page.read()
html = html_bytes.decode("utf-8")
print(html)

# Get the title of the page (the text in the <title> tag)
start_tag = "<title>"
end_tag = "</title>"

title = html[html.find(start_tag) + len(start_tag):html.find(end_tag)]
print(title)

# (Poseidon page)
pass

