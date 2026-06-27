# Introduction to web scraping and metadata

## Exercice 1 - Spider 

The spider program allow you to extract all the images from a website, recursively, by
providing an url as a parameter.
Web scraping is an automated method to extract large amounts of data from websites

Python is the most popular language for web scraping as it can handle most of the processes easily. It also has a variety of libraries that were created specifically for Web Scraping

Usage:
```
python3 spider.py -r -l <number from 1 to 10> -p <path> <URL>
```
Example:
```
python3 spider.py https://cats.com
python3 spider.py -r -l 2 -p ./images/ https://www.nationalgeographic.com/
```
-r: recursively  
-l: max depth level of the recursion  
-p: directory name to store the downloaded images  

Extension of images: .jpg/jpeg, .png, .gif, .bmp 

##  Exercice 2 - Scorpion

Program receive image files as parameters and must be able to parse them for EXIF and other metadata

The Exchangeable Image File Format (EXIF) is a standard that specifies how metadata about a multimedia file can be embedded within the file. For example, an image might contain EXIF data describing the: pixel width, height, and density, shutter speed, aperture, ISO settings, capture date, etc.

Usage:
```
python3 scorpion.py <image1> <image2> ...
```

Example:
```
python3 scorpion.py assets/robot.jpeg assets/palm-tree.jpg assets/speed-1.jpg
```

## Bonus part

Add options to modify or delete EXIF information
-m to modify
-d to delete

Usage
```
python3 scorpion_bonus.py <image> -m <TAG> <new value>
python3 scorpion_bonus.py <image> -d <TAG>
```
Example:
```
python3 scorpion_bonus.py assets/robot.jpeg -m "Model" "iPhone 14"
python3 scorpion_bonus.py assets/robot.jpeg -d "Model"
```
- double quotes are mandatory for key and value after the option