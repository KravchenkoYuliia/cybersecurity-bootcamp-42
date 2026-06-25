import sys
import os
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS

BOLD = "\033[1m"
UNDERLINE = "\033[4m"
YELLOW ="\033[33m"
RESET = "\033[0m"


def fill_dictionary( image ):
    info_dict = {
        "Filename": image.filename,
        "Image Size": image.size,
        "Image Height": image.height,
        "Image Width": image.width,
        "Image Format": image.format,
        "Image Mode": image.mode,
        "Image is Animated": getattr(image, "is_animated", False),
        "Frames in Image": getattr(image, "n_frames", 1)
    }

    return info_dict


def get_args():

    args = sys.argv[1:]
    if len( args ) < 1 or len( args ) > 1000:
        print( f"Error: put arguments from 1 to 1000" )
        sys.exit()
    
    for arg in args:
        if not os.path.isfile( arg ):
            print( f"Error: invalid file" )
            sys.exit()
        try:
            Image.open( arg ).verify()
        except Exception:
            print( f"Error: file must be an image" )
            sys.exit()
    
    return args

def dms_to_decimal(dms, ref):
            degrees, minutes, seconds = dms
            decimal = float(degrees) + float(minutes)/60 + float(seconds)/3600
            if ref in ['S', 'W']:
                decimal = -decimal
            return decimal

def main():
    args  = get_args()
    
    for i, arg in enumerate( args ):

        print( f"{BOLD}{UNDERLINE}{YELLOW}Image {i + 1}{RESET}" )
        image = Image.open( arg )
        
        info_dict = fill_dictionary( image )
        for label,value in info_dict.items():
            print(f"{label:25}: {value}")
        
        exifdata = image.getexif()
        if exifdata:

            gps_info = exifdata.get_ifd( 0x8825 ) #0x8825 - gsp info tag
            for tag_id in exifdata:
                # get the tag name, instead of human unreadable tag id
                tag = TAGS.get( tag_id, tag_id )
                data = exifdata.get( tag_id )
                # decode bytes
                if isinstance( data, bytes ):
                    data = data.decode()
                print( f"{tag:25}: {data}" )

            for tag_id, value in gps_info.items():
                tag = GPSTAGS.get(tag_id, tag_id)
                print(f"{tag:25}: {value}")
            
            lat = dms_to_decimal(gps_info.get(2), gps_info.get(1))
            lon = dms_to_decimal(gps_info.get(4), gps_info.get(3))
            print(f"Location: {lat}, {lon}")
        
        print( f"\n" )

    
    

if __name__=="__main__":
    main()