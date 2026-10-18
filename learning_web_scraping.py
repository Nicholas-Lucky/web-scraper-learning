# Note to self: I needed to be in Python 3.9 for BeautifulSoup/bs4 to work and not have a ModuleNotFoundError that might be a me problem for now though
# I don't know if this also applies to MechanicalSoup ^^

# Source: https://realpython.com/python-web-scraping-practical-introduction/

from urllib.request import urlopen
import re
from bs4 import BeautifulSoup
import mechanicalsoup
import time

# --------- Helper Functions --------- #
def get_html_from_url(url: str):
    page = urlopen(url)

    # Get the HTML content of the page
    html_bytes = page.read()
    html = html_bytes.decode("utf-8")
    # print(html)

    return html

def get_title_hardcoded(html):
    # Get the title of the page (the text in the <title> tag)
    start_tag = "<title>"
    end_tag = "</title>"

    title = html[html.find(start_tag) + len(start_tag):html.find(end_tag)]

    return title

def print_all_found_patterns(regex: str, text: str, flag=0):
    found_patterns = re.findall(regex, text, flag)
    print(f"Found Patterns for: | regex = {regex} | text = {text}")
    print(f"{found_patterns}\n")

# ------------------------------------ #

# ---------- Code Sections ----------- #
def section_1():
    """
    Introduction to Opening URLs, Parsing HTML, and Regular Expressions
    """

    # Open the page with the specified url (Aphrodite page)
    url = "http://olympus.realpython.org/profiles/aphrodite"
    html = get_html_from_url(url)

    # Get the title of the page (the text in the <title> tag)
    title = get_title_hardcoded(html)
    # print(title)

    # (Poseidon page)
    url = "http://olympus.realpython.org/profiles/poseidon"
    html = get_html_from_url(url)

    # vv this doesn't work because the Poseidon page uses <title > instead of <title>
    # so hardcoding a find("<title>") would result in -1 instead of the actual starting
    # index of the title, basically this is a reason for more reliable text extraction
    title = get_title_hardcoded(html)
    # print(title)

    # Regular expressions
    print_all_found_patterns("ab*c", "ac")
    print_all_found_patterns("ab*c", "abcac")
    print_all_found_patterns("ab*c", "abdc")
    print_all_found_patterns("ab*c", "ABC")
    print_all_found_patterns("ab*c", "ABC", re.IGNORECASE)
    print_all_found_patterns("a.c", "ac")
    print_all_found_patterns("a.c", "acc")
    print_all_found_patterns("a.c", "accccc")
    print_all_found_patterns("a.*c", "accccc")
    print_all_found_patterns("a.*c", "abbbbbc")

    # vv calling .group() on the result of re.search will give the first and most inclusive result
    # .group() is usually the result we want I guess
    match_result = re.search("ab*c", "ABC", re.IGNORECASE)
    print(match_result.group())

    # vv Python finds the LONGEST match bc it's greedy so the match goes from the < before replaced to the > after tags
    string = "Everything is <replaced> if it's in <tags>."
    string = re.sub("<.*>", "ELEPHANTS", string)
    print(string)

    # ? does 3 things
    # 1. Alone it means 0 or 1 of the preceding character/group
    # 2. After a * like *? this changes the * to be non-greedy and will take the SHORTEST instead of the longest pattern
    # 3. Grouping variations so (?: means non-capturing, (?= means positive lookahead, (?! means negative lookahead, and (?<= means positive lookbehind
    string = "Everything is <replaced> if it's in <tags>."
    string = re.sub("<.*?>", "ELEPHANTS", string)
    print(string)

    # Fun fact ^^ the greedy version the .* actually goes past the > and then has to back up to the most recent > it passed
    # bc the goal for it is to find the longest match, while the non greedy version the .*? doesn't need to back up
    # it just stops at the first > it sees bc it wants the shortest match

def section_2():
    """
    More involved HTML parsing (involving .find() and regex)
    """

    # My solution (gets all of the titles for multiple title tags)
    url = "http://olympus.realpython.org/profiles/poseidon"
    html = get_html_from_url(url)

    # Use regular expressions to parse the title
    starting_tag_regex = "<\\s?title\\s?>"
    ending_tag_regex = "</\\s?title\\s?>"

    match_results = re.findall(f"{starting_tag_regex}.*{ending_tag_regex}", html)

    titles = []
    for match in match_results:
        parsed_title = re.sub("<.*?>", "", match)
        titles.append(parsed_title)

    # print(titles)

    # Real Python's solution
    url = "http://olympus.realpython.org/profiles/dionysus"
    page = urlopen(url)
    html = page.read().decode("utf-8")

    pattern = "<title.*?>.*?</title.*?>"
    match_results = re.search(pattern, html, re.IGNORECASE)
    title = match_results.group()
    title = re.sub("<.*?>", "", title) # Remove HTML tags

    # print(title)

    # My answer for the "Check Your Understanding"
    # I mean I don't know if this works, but it doesn't use .find()?
    url = "http://olympus.realpython.org/profiles/dionysus"
    html = get_html_from_url(url)

    pattern = "Name:\\s.*</"
    match_results = re.search(pattern, html, re.IGNORECASE)
    name = match_results.group()
    name = re.sub("Name:\\s", "", name)
    name = re.sub("</", "", name)

    pattern = "Favorite Color:\\s.*"
    match_results = re.search(pattern, html, re.IGNORECASE)
    favorite_color = match_results.group()
    favorite_color = re.sub("Favorite Color:\\s", "", favorite_color)
    favorite_color = re.sub("</", "", favorite_color)

    print(name)
    print(favorite_color)

    # Intended solution for the "Check Your Understanding"
    url = "http://olympus.realpython.org/profiles/dionysus"
    html_page = urlopen(url)
    html_text = html_page.read().decode("utf-8")

    for string in ["Name: ", "Favorite Color:"]:
        string_start_idx = html_text.find(string)
        text_start_idx = string_start_idx + len(string)

        next_html_tag_offset = html_text[text_start_idx:].find("<")
        text_end_idx = text_start_idx + next_html_tag_offset

        raw_text = html_text[text_start_idx : text_end_idx]
        clean_text = raw_text.strip(" \r\n\t")
        print(clean_text)

def section_3():
    """
    Opening and parsing HTML using BeautifulSoup
    """

    # Opening a page with BeautifulSoup
    url = "http://olympus.realpython.org/profiles/dionysus"
    page = urlopen(url)
    html = page.read().decode("utf-8")

    # "html.parser" is the chosen parser for now and is Python's built-in HTML parser
    soup = BeautifulSoup(html, "html.parser")

    # I guess this can be run in the interactive window but I haven't been able to run the interactice window as of right now
    text = soup.get_text()

    # Remove newlines with .replace()
    # text = text.replace("\n\n", "\n")

    # Remove newlines with regular expressions
    # + in regex means one or more I think
    # text = re.sub("(\\n)+", "\\n", text)

    # print(text)

    # Get all URLs from the <img> tags
    img_tags = soup.find_all("img")
    # print(img_tags)

    # Each element in ^^ img_tags is a Tag object
    image1, image2 = soup.find_all("img")
    # print(image1.name)

    # Specifying the value of the HTML attribute
    specific_img_src = soup.find_all("img", src="/static/dionysus.jpg")
    # print(specific_img_src)
    
    # We can access HTML attributes like key-value pairs in a dictionary
    # print(image1["src"])
    # print(image2["src"])

    # Title tag in a document
    # print(soup.title)
    # print(soup.title.string)

    # My answer for the "Check Your Understanding"
    # I see my issue is I didn't concatenate the hrefs with the base URL!
    url = "http://olympus.realpython.org/profiles"
    page = urlopen(url)
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")

    a_tags = soup.find_all("a")
    for a_tag in a_tags:
        print(a_tag["href"])
    
    # Intended solution for the "Check Your Understanding"
    base_url = "http://olympus.realpython.org"
    html_page = urlopen(base_url + "/profiles")
    html_text = html_page.read().decode("utf-8")
    soup = BeautifulSoup(html_text, "html.parser")

    for link in soup.find_all("a"):
        link_url = base_url + link["href"]
        print(link_url)

def section_4():
    """
    Browsing through a web page using MechanicalSoup
    """

    # vv this can be used to browse through a page through code??? 
    browser = mechanicalsoup.Browser()

    url = "http://olympus.realpython.org/login"
    page = browser.get(url)

    # page is a Response object
    # 200 status code = successful
    # 404 status code = URL doesn't exist
    # 500 status code = server error
    # print(page)

    # MechanicalSoup uses BeautifulSoup
    # (does that mean we need BeautifulSoup installed to use MechanicalSoup?)
    # print(type(page.soup))

    html = page.soup
    # print(html)

    # Submit a form with MechanicalSoup
    # 1. Load a MechanicalSoup browser and open the login page
    browser = mechanicalsoup.Browser()
    url = "http://olympus.realpython.org/login"
    login_page = browser.get(url)
    login_html = login_page.soup

    # 2. Select the form element and input the credentials into the input fields
    form = login_html.select("form")[0]
    form.select("input")[0]["value"] = "zeus"
    form.select("input")[1]["value"] = "ThunderDude"

    # 3. Submit the form to the login page's URL?
    profiles_page = browser.submit(form, login_page.url)

    # If the loging was successful, the url should be "http://olympus.realpython.org/profiles"
    # If it didn't work, the url would still be "http://olympus.realpython.org/login"
    # print(profiles_page.url)

    # Get each profile link from the profiles page
    links = profiles_page.soup.select("a")

    base_url = "http://olympus.realpython.org"
    for link in links:
        address = base_url + link["href"]
        text = link.text
        # print(f"{text}: {address}")

    # My answer for the "Check Your Understanding"
    browser = mechanicalsoup.Browser()
    url = "http://olympus.realpython.org/login"
    page = browser.get(url)
    html = page.soup

    username = "zeus"
    password = "ThunderDude"

    form = html.select("form")[0]
    form.select("input")[0]["value"] = username
    form.select("input")[1]["value"] = password

    profiles_page = browser.submit(form, page.url)
    profiles_page_html = profiles_page.soup
    print(profiles_page_html.title)
    
    # Intended solution for the "Check Your Understanding"
    browser = mechanicalsoup.Browser()

    login_url = "http://olympus.realpython.org/login"
    login_page = browser.get(login_url)
    login_html = login_page.soup

    form = login_html.form
    form.select("input")[0]["value"] = "zeus"
    form.select("input")[1]["value"] = "ThunderDude"

    profiles_page = browser.submit(form, login_page.url)
    print(profiles_page.soup.title)

def section_5():
    """
    Calling web pages in real-time
    """

    browser = mechanicalsoup.Browser()

    # Print the result of the dice 4 times after 10 seconds (rerolls the dice each time the page is loaded)
    for i in range(4):
        url = "http://olympus.realpython.org/dice"
        page = browser.get(url)
        html = page.soup

        tag = html.select("#result")[0]
        print(tag.text)

        if i < 3:
            time.sleep(10)

# ------------------------------------ #

def main():
    # section_1()
    # section_2()
    # section_3()
    # section_4()
    # section_5()

    pass

main()
