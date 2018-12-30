#! python3
# quick_search - opens several search result links

import bs4
import pyperclip
import requests
import sys
import webbrowser


def query_getter():
    if len(sys.argv) > 1:
        query = ' '.join(sys.argv[1:])

    else:
        query = pyperclip.paste()

    return query


# a dictionary with the url, redirect url and the HTML tag containing the search links
search_urls = {
    'google': ['https://google.com/search?q=', 'https://google.com', '.r a'],
    'amazon': ['https://www.amazon.com/s/ref=nb_sb_noss?url=search-alias%3Daps&field-keywords=', '',
               '.a-link-normal'],
    'bing': ['https://www.bing.com/search?q=', '', 'h2 > a']
}

# to just open one new window for the browser for all search requests
browser = webbrowser.get()

new_search = ''

while new_search != 'n':
    search_query = query_getter().strip()

    first_word = search_query.split(' ')[0]

    search_engine = search_urls.get(first_word)

    if search_engine is not None:
        search_page = search_engine
        search_page_name = first_word
        search_query = ' '.join(search_query.split(' ')[1:])

    else:
        # should later be able to use the default search engine
        search_page = search_urls.get('google')
        search_page_name = 'google'

    url = search_page[0] + search_query

    print(f'Searching {search_page_name}....')

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/54.0.2840.71 Safari/537.36 '
    }

    try:
        # since amazon is anti-scraping, header have to be used to avoid 503 error
        response = requests.get(url, headers=headers, timeout=5) if search_page_name == 'amazon' \
            else requests.get(url, timeout=5)
        response.raise_for_status()

    except Exception as derr:
        print(f'There was a problem opening the website: {derr}')
        print(derr)

    else:

        # to get all the html data from that page
        soup = bs4.BeautifulSoup(response.text, features="html.parser")

        # to load the result links
        link_elements = soup.select(search_page[2])  # css class named r with element a

        print(f'There are about {len(link_elements)} results on this page. How many should be opened? (default is 5)')
        number_of_links = input('Enter number of links to open: ')

        # to open a browser tab for each result
        if number_of_links == '':
            links_to_open = min(5, len(link_elements))

        else:
            links_to_open = int(number_of_links)

        browser.open_new(url)

        for i in range(links_to_open):
            browser.open(search_page[1] + link_elements[i].get('href'))

    print('Done')
    
    new_search = input('Do you want to perform another search?[y/n]')
