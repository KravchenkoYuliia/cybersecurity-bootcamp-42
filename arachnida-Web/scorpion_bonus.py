import sys
import os
import argparse
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
from scorpion import print_exif

BOLD = "\033[1m"
UNDERLINE = "\033[4m"
YELLOW = "\033[33m"
MAGENTA= "\033[35m"
RESET = "\033[0m"

exif_dictionary = {}
image = None

def print_properties():

    global exif_dictionary, image
    exif_dictionary = {
        "Filename": image.filename,
        "Image Size": image.size,
        "Image Height": image.height,
        "Image Width": image.width,
        "Image Format": image.format,
        "Image Mode": image.mode,
        "Image is Animated": getattr(image, "is_animated", False),
        "Frames in Image": getattr(image, "n_frames", 1)
    }

    print( f"{UNDERLINE}Image properties:{RESET}" )
    for label,value in exif_dictionary.items():
        print( f"{label:25}: {value}" )


def dms_to_decimal(dms, ref):
   
    degrees, minutes, seconds = dms
    decimal = float(degrees) + float(minutes)/60 + float(seconds)/3600
    if ref in ['S', 'W']:
        decimal = -decimal
    
    return decimal


def get_args():

    args_parser = argparse.ArgumentParser()
    args_parser.add_argument(
        "image",
        help="image file"
    )

    group = args_parser.add_mutually_exclusive_group()
    group.add_argument( "-m", nargs=2, help="modify EXIF data: -m key value" )
    group.add_argument( "-d", nargs=1, help="delete EXIF data: -d key" )

    args = args_parser.parse_args()
    
    return args


def print_general_exif( exif_data, key, new_value, action ):
    
    for tag_id in list( exif_data ):

        # get the tag name, instead of human unreadable tag id
        tag = TAGS.get( tag_id, tag_id )
        data = exif_data.get( tag_id )
        # decode bytes
        if isinstance( data, bytes ):
            data = data.decode()

        if tag == key:
            try:
                if action == "m":
                    exif_data[ tag_id ] = new_value
                elif action == "d":
                    exif_data.pop( tag_id, None )
            except Exception as e:
                print( f"Error: can't modify value {e}" )
                sys.exit(1)
            data = new_value

        print( f"{tag:25}: {data}" )
    


def print_gps_exif( exif_data, key, new_value, action ):
    
    global exif_dictionary
    gps_info = exif_data.get_ifd( 0x8825 ) # IFD 0x8825 is the GPS IFD
    for tag_id, value in list( gps_info.items() ):
        tag = GPSTAGS.get( tag_id, tag_id )
        if tag == key:
            try:
                if action == "m":
                    gps_info[ tag_id ] = new_value
                elif action == "d":
                    exif_data.pop( tag_id, None )
            except Exception as e:
                print( f"Error: can't modify value {e}" )
                sys.exit(1)


            value = new_value
        print( f"{tag:25}: {value}" )

    if gps_info:
        latitude = dms_to_decimal( gps_info.get(2), gps_info.get(1) )
        longitude = dms_to_decimal( gps_info.get(4), gps_info.get(3) )
        location = ( latitude, longitude )
        print( f"{'Location':25}: {location}" )


def change_and_print_data( image_name, key, new_value, action ):

    global image
    
    exif_data = image.getexif()
    if exif_data:
        
        print( f"{UNDERLINE}EXIF:{RESET}" )
        try:
            print_general_exif( exif_data, key, new_value, action )
            print_gps_exif( exif_data, key, new_value, action )
            image.save( image_name, exif=exif_data)
        except Exception as e:
            print( f"Error: can't save the modification {e}" )
            sys.exit(1)


def modify_exif( image_name, key, new_value ):
    change_and_print_data( image_name, key, new_value, "m" )


def delete_exif( image_name, key ):
    change_and_print_data( image_name, key, None, "d" )


def main():
    args = get_args()
    if args.m == None and args.d == None:
        print_exif( args.image )
        return 

    global image
    try:
        image = Image.open( args.image )
        print_properties()
    except Exception as e:
        print( f"Error: {e}" )
        sys.exit(1)


    if args.m != None:
        modify_exif( args.image, args.m[0], args.m[1] )
    

    elif args.d != None:
        delete_exif( args.image, args.d[0] )
    


if __name__=="__main__":
    main()