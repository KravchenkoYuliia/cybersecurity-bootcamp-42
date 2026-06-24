import os
import sys
import requests
from bs4 import BeautifulSoup as BS
from urllib.parse import urljoin
from urllib.parse import urlparse

count_depth = -1
options = {

    "recursive": False,
    "depth": 5,
    "path": "./data/"

}


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
        print( f"Error: invalid URL or inaccesible site [{url}]" )
        sys.exit(1)
    
    return response.text


def download_img_from_url( url, headers ):

    global count_depth
    global options    

    count_depth += 1
    if count_depth > options["depth"]:
        return

    html = get_html_from_url(  url, headers )
    print( f"Depth: {count_depth}" )

    soup = BS( html, "html.parser" )
    img_tags = soup.find_all( 'img' )
    for img in img_tags:
        img_url = img.get( 'src' )
        allowed_extension = ( ".jpg", ".jpeg", ".png", "gif", ".bmp" )
        if not img_url.lower().endswith( allowed_extension ):
            continue
        if img_url:
            full_url = urljoin( url, img_url )
            img_name = img_url.split( '/' )[ -1 ]
            img_response = requests.get( full_url, headers=headers )
            
            dir_path = "./data/" + str( count_depth ) + "/"
            os.makedirs( dir_path, exist_ok=True )
            path = dir_path + img_name
            #print( f"Downloading from {url} to {dir_path}..." )
            
            try:
                with open( path, "wb" ) as f:
                    f.write( img_response.content )
            except OSError as e:
                print( f"Error: invalid option -p, requires a valid path: {e}" )
                return 1
    
    if options[ "recursive" ] == True:
        #more than 1 time
        links = soup.find_all( 'a' )
        for link in links:
            href = link.get('href')
            if href and urlparse( href ).scheme in ( 'http', 'https' ) and href != url:
                download_img_from_url( href, headers )



def set_headers():
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    return headers


def fill_options( args ):
    
    global options

    for i, arg in enumerate( args ):
        #if not arg[0] == '-':
        #    return
        #options_types = ("-r", "-l", "-p" )
        
        if arg == "-r":
            options[ "recursive" ] = True
        elif arg == "-l":
            if i + 1 >= len( args ) or not args[i + 1].isdigit() or int(args[i + 1]) > 100:
                print( f"Error: invalid option -l, requires a valid depth (0-100)" )
                sys.exit(1)
            options[ "depth" ] = int(args[i + 1])
        elif arg == "-p":
            if i + 1 >= len( args ):
                print( f"Error: invalid option -p, requires a valid path" )
                sys.exit(1)
            options["path"] = args[i + 1]



def get_args( argv ):
    
    args = argv[1:]
    if len(args) < 1:
        print( f"Error: give an URL" )
        sys.exit(1)

    if len(args) > 6:
        print( f"Error: too much arguments\nExample: spider.py -r -l -p URL" )
        sys.exit(1)

    if args[-1][0] == '-':
        print( f"Error: last argument must be an URL" )
        sys.exit(1)

    return args


def main():
    args = get_args( sys.argv )

    fill_options( args )
    headers = set_headers()
    os.makedirs( "./data/", exist_ok=True )

    download_img_from_url( args[-1], headers )


if __name__=="__main__":
    main()