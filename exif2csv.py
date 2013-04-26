import glob
import PIL
from PIL import Image
from PIL.ExifTags import TAGS
import csv

def convert_to_degress(value):
    """Helper function to convert the GPS coordinates stored in the EXIF to degress in float format. Forked from github.com/erans/983821"""
    d0 = value[0][0]
    d1 = value[0][1]
    d = float(d0) / float(d1)
 
    m0 = value[1][0]
    m1 = value[1][1]
    m = float(m0) / float(m1)
 
    s0 = value[2][0]
    s1 = value[2][1]
    s = float(s0) / float(s1)
 
    return d + (m / 60.0) + (s / 3600.0)

photos = glob.glob('*.jpg')
file = open('exifdata.csv', 'wb')
table = csv.writer(file)
table.writerow(['Photo', 'DateTime', 'Make', 'Model', 'Cutline', 'Photographer', 'Latitude', 'Longitude'])

for photo in photos:
    img = Image.open(photo)
    exif = {
        PIL.ExifTags.TAGS[k]: v
        for k, v in img._getexif().items()
        if k in PIL.ExifTags.TAGS 
    }
    datetime = exif['DateTime']
    make = exif['Make']
    model = exif['Model']
    cutline = exif['ImageDescription']
    try:
        photog = cutline[cutline.find("(")+1:cutline.find("/")]
    except:
        print "No photographer in cutline."
          
    lat = convert_to_degress(exif['GPSInfo'][2])
    lon = convert_to_degress(exif['GPSInfo'][4])
    
    if exif['GPSInfo'][3] == 'W':
        lon = lon * -1
    
    table.writerow([photo, datetime, make, model, cutline, photog, lat, lon])
    print 'Extracting data for photo %s' % photo
    
file.close()
