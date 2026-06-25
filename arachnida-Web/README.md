# Introduction to web scraping and metadata

## Exercice 1 - Spider 

The spider program allow you to extract all the images from a website, recursively, by
providing an url as a parameter.
Web scraping is an automated method to extract large amounts of data from websites

Python is the most popular language for web scraping as it can handle most of the processes easily. It also has a variety of libraries that were created specifically for Web Scraping

Usage:
```
python3 spider.py URL
```
```
python3 spider.py -r -l 5 -p ./data/ URL
```
-r: recursively  
-l: max depth level of the recursion  
-p: directory name to store the downloaded images  

Extension of images: .jpg/jpeg, .png, .gif, .bmp 

##  Exercice 2 - Scorpion

Program receive image files as parameters and must be able to parse them for EXIF and other metadata

The Exchangeable Image File Format (EXIF) is a standard that specifies how metadata about a multimedia file can be embedded within the file. For example, an image might contain EXIF data describing the: pixel width, height, and density, shutter speed, aperture, ISO settings, capture date, etc.

usage:
```
./scorpion.py FILE1 [FILE2 ...]
```