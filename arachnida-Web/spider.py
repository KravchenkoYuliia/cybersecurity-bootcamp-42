import os
import sys
import requests
from termcolor import colored
from bs4 import BeautifulSoup as BS
from urllib.parse import urljoin
from urllib.parse import urlparse

visited = set()
base_domain = ""
options = {

    "recursive": False,
    "depth": 5,
    "path": "./data/"

}
MAX_IMAGES_PER_LINK = 5
MAX_LINKS = 5

def get_html_from_url( url, headers, count_depth ):

    try:
        response = requests.get( url, headers=headers )
        print( f"Code: {response.status_code}\n")
        if ( response.status_code == 403 ):
            return None
        elif ( response.status_code != 200 ):
            return None
    
    except requests.exceptions.RequestException:
        print( f"Error: invalid URL or inaccesible site [{url}]" )
        return None

    
    return response.text


def download_img_from_url( url, headers, count_depth ):

    global visited, options, base_domain

    if url in visited:
        return
    visited.add( url )
    
    if count_depth != 0:
        print( f"Found a valid link" )
    
  

    if count_depth == 0:
        base_domain = urlparse( url ).netloc

    print( f"\033[35mdepth is\033[0m {count_depth} \033[35msite is\033[0m {url}" )
    
    html = get_html_from_url(  url, headers, count_depth )
    if html == None:
        return 

    soup = BS( html, "html.parser" )
    print( f"\033[32mLooking for img tags on the site ...\033[0m" )
    count_images = 0
    img_tags = soup.find_all( 'img' )
    for img in img_tags:
        img_url = img.get( 'src' )
        if not img_url:
            continue
        
        allowed_extension = ( ".jpg", ".jpeg", ".png", "gif", ".bmp" )
        if not img_url.lower().endswith( allowed_extension ):
            continue
        
        if img_url:
            full_url = urljoin( url, img_url )
            img_name = img_url.split( '/' )[ -1 ]
            img_response = requests.get( full_url, headers=headers )            
            
            path = options[ "path" ] + img_name
            if count_images >= MAX_IMAGES_PER_LINK:
                break
            count_images += 1
            try:
                with open( path, "wb" ) as f:
                    print( f"\033[32mDownloading an image from the site ...\033[0m" )
                    f.write( img_response.content )

            except OSError as e:
                print( f"Error: invalid option -p, requires a valid path: {e}" )
                sys.exit(1)
    if options[ "recursive" ] == False:
        return
    if count_depth >= options["depth"]:
        return
    print( f"Start to getting links from the site {url}" )
    count_links = 0
    if options[ "recursive" ] == True:
        links = soup.find_all( 'a' )
        for link in links:
            href = link.get('href')
            if href and urlparse( href ).scheme in ( 'http', 'https' ) and href != url and urlparse( href ).netloc == base_domain:
                count_links += 1
                if count_links >= MAX_LINKS:
                    break
                download_img_from_url( href, headers, count_depth + 1 )
    
    print( f"No more links for depth {count_depth}" )
    

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
            if i + 1 >= len( args ) or not args[i + 1].isdigit() or int(args[i + 1]) < 1 or int(args[i + 1]) > 10:
                print( f"Error: invalid option -l, requires a valid depth (1-10)" )
                sys.exit(1)
            options[ "depth" ] = int(args[i + 1])
        elif arg == "-p":
            if i + 1 >= len( args ) or args[i + 1][-1] != '/':
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

    global options
    fill_options( args )
    headers = set_headers()
    os.makedirs( options[ "path" ], exist_ok=True )

    download_img_from_url( args[-1], headers, 0 )


if __name__=="__main__":
    main()