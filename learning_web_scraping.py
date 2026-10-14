# Source: https://realpython.com/python-web-scraping-practical-introduction/

from urllib.request import urlopen
import re

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
    pass

# ------------------------------------ #

def main():
    # section_1()
    section_2()

main()
