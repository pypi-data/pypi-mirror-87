""" This is main module web browser Akasia. """

import sys
import requests
import html2text


# pylint settings:
# pylint: disable=E1101


def get_request(url: str) -> str:
    """

    This function receives a request from the site.

    Args:
        url (str): A variable that stores the URL that will open in the browser Akasia.

    Returns:
        site_content (str): The variable contains the content of the site in html format.
        request_get (str): This variable stores the request from the site.

    """

    try:
        request_get = requests.get(url)
    except requests.exceptions.MissingSchema:
        choosing_the_right_url = input(
            f"Invalid URL '{url}': No schema supplied. Perhaps you meant http://{url}? (y/n) ")
        if choosing_the_right_url.lower() == 'y' or choosing_the_right_url.lower() == 'yes':
            request_get = requests.get(f'http://{url}')
        else:
            sys.exit()

    try:
        site_content = str(request_get.content, 'utf-8')
    except UnicodeDecodeError:
        site_content = str(request_get.content, 'latin-1')
    return site_content, request_get


def print_site(site_content: str, request_get: str) -> str:
    """

    This function prints the site in format markdown.

    Args:
        site_content (str): The variable contains the content of the site in html format.
        request_get (str): This variable stores the request from the site.
    Returns:
        site (str): The variable stores the text of the site in markdown format.
    """
    if len(site_content) == 0:

        if request_get.status_code == requests.codes.ok:
            site = (html2text.html2text(site_content))
        if request_get.status_code == 404:
            site = ('Error 404, Not Found!')
        if request_get.status_code == 500:
            site = ('Error 500, Internal server error!')

        site = (html2text.html2text(site_content))

    # If non-empty content is detected, print it.
    # This is to allow customised html error messages.

    site = (html2text.html2text(site_content))
    return site


def save_site_in_html(site_content: str, path: str) -> None:
    """

    This function is needed to save the site in html format.

    Args:
        site_content (str): This variable stores the site in html format.
        path (str): This variable stores path which will saved site in format html.

    Returns:
        None: The function returns nothing.

    """


    file = open(path, 'w')
    file.write(site_content)
    file.close()

def save_site_in_markdown(site_content: str, path: str) -> None:
    """

    This function is needed to save the site in markdown format.

    Args:
        site_content (str): This variable stores the site in html format.
        path (str): This variable stores path which will saved site in format html.

    Returns:
        None: The function returns nothing.

    """
    file = open(path, 'w')
    file.write(html2text.html2text(site_content))
    file.close()

def main() -> None:
    """ This is main function, what initializing web browser Akasia. """

    print('''
          d8888 888                        d8b          
         d88888 888                        Y8P          
        d88P888 888                                     
       d88P 888 888  888  8888b.  .d8888b  888  8888b.  
      d88P  888 888 .88P     "88b 88K      888     "88b 
     d88P   888 888888K  .d888888 "Y8888b. 888 .d888888 
    d8888888888 888 "88b 888  888      X88 888 888  888 
   d88P     888 888  888 "Y888888  88888P' 888 "Y888888\n\n\n''')
    print('Akasia - A fork tiny python text-based web browser Asiakas.\n'.center(58))
    print('Type "quit" or "q" to shut down the browser.'.center(58))
    print('Type "google" or "g" to search information in Google.'.center(58))
    print('Type "save_html" or "sh" to save site in format html.'.center(58))
    print('Type "save_markdown" or "smd" to save site in format html.'.center(58))

    while True:
        link = input('URL: ')
        if link.lower() == 'quit' or link.lower() == 'q':
            break
        if link.lower() == 'google' or link.lower() == 'g':
            request = input('Request: ')
            link = ('https://google.com/search?q=' + request.replace(' ', '+'))
            cont, req_get = get_request(link)
            print(print_site(cont, req_get))
        elif link.lower() == 'save_html' or link.lower() == 'sh':
            link = input('URL: ')
            path = input('Path: ')
            cont, req_get = get_request(link)
            save_site_in_html(cont, path)
        elif link.lower() == 'save_markdown' or link.lower() == 'smd':
            link = input('URL: ')
            path = input('Path: ')
            cont, req_get = get_request(link)
            save_site_in_markdown(cont, path)
        else:
            cont, req_get = get_request(link)
            print(print_site(cont, req_get))


main()
