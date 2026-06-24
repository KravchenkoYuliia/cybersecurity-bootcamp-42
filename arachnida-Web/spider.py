import os
import sys
import requests
from bs4 import BeautifulSoup as BS
from urllib.parse import urljoin
from urllib.request import urlretrieve

def get_html_from_url( url, headers ):

    try:
        response = requests.get( url, headers=headers )
        if ( response.status_code == 403 ):
            print( f"Error 403: the website does not allow this request " )
            sys.exit(1)
        elif ( response.status_code != 200 ):
            print( f"Error {response.status_code}" )
            sys.exit(1)
        print( f"Code: {response.status_code}\n")#content: {response.text}" )
    
    except requests.exceptions.RequestException:
        print( f"Error: invalid URL or inaccesible site" )
        sys.exit(1)
    
    return response.text


def set_headers():
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    return headers


def get_args( argv ):
    
    args = argv[1:]
    if ( len(args) < 1 ):
        print(f"Error: give an URL")
        sys.exit(1)

    return args


def main():
    args = get_args( sys.argv )
    headers = set_headers()

    html = get_html_from_url(  args[0], headers )

    os.makedirs( "./data/", exist_ok=True )

    soup = BS( html, "html.parser" )
    img_tags = soup.find_all( 'img' )
    for img in img_tags:
        img_url = img.get( 'src' )
        allowed_extension = ( ".jpg", ".jpeg", ".png", "gif", ".bmp" )
        if not img_url.lower().endswith( allowed_extension ):
            continue
        if img_url:
            full_url = urljoin( args[0], img_url )
            img_name = img_url.split( '/' )[ -1 ]
            img_response = requests.get( full_url, headers=headers )
            path = "./data/" + img_name
            with open( path, "wb" ) as f:
                f.write( img_response.content )


if __name__=="__main__":
    main()