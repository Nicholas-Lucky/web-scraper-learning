from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
from gzip import decompress

def main():
    url = "https://www.sec.gov/data-research/sec-markets-data/form-13f-data-sets"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive",
        "Host": "www.sec.gov"
    }

    request = Request(url, headers=headers)
    page = urlopen(request)

    # In headers we set "Accept-Encoding" to gzip, so we need to decompress the gzip that we get back I think
    html = decompress(page.read())
    
    soup = BeautifulSoup(html, "html.parser")

    text = soup.get_text()
    print(text)

main()
