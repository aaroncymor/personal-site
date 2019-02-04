from django.shortcuts import get_object_or_404

from bs4 import BeautifulSoup


def parse_html_content(post_content):
    """[summary]
    
    Arguments:
        html_doc {[type]} -- [description]
    """
    soup = BeautifulSoup(post_content)
    return soup.get_text()
