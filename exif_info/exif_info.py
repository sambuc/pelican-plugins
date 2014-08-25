import os
import re
from pelican import signals
from PIL import Image
from PIL.ExifTags import TAGS
 
def get_exif_data(fname):
    """Get embedded EXIF data from an image file."""
    exif = {}
    ret = {}
    try:
        img = Image.open(fname)
        if hasattr( img, '_getexif' ):
            exifinfo = img._getexif()
            if exifinfo != None:
                for tag, value in exifinfo.items():
                    decoded = TAGS.get(tag, tag)
                    ret[decoded] = value
    except IOError:
        print 'IOERROR ' + fname

    #print ret
    # Keep and format the most interesting fields
    for tag in ret:
        if tag == "DateTimeOriginal":
            exif[tag] = ret[tag]
        if tag == "Model":
            exif[tag] = ret[tag]
        if tag == "LensModel":
            exif[tag] = ret[tag]
        if tag == "ISOSpeedRatings":
            exif[tag] = ret[tag]
        if tag == "FocalLength":
            exif[tag] = "{:2.1f}".format(float(ret[tag][0]) / float(ret[tag][1]))
        if tag == "FNumber":
            exif[tag] = "{:2.1f}".format(float(ret[tag][0]) / float(ret[tag][1]))
        if tag == "ExposureTime":
            exif[tag] = str(ret[tag][0]) + "/" + str(ret[tag][1])

    return exif


def add_exif_post(generator):
    get_exif = generator.settings.get('EXIF_INFO_DEFAULT')
    if get_exif == None:
        get_exif = True;

    contentpath = generator.settings.get('PATH')
    gallerycontentpath = os.path.join(contentpath,'images/gallery')

    for article in generator.articles:
        if 'exifinfo' in article.metadata.keys():
            if article.metadata.get('exifinfo'):
                # Ignore anything which is not a capitalization variation of
                # true/false
                if article.metadata.get('exifinfo').lower() == "true":
                    get_exif = True;
                if article.metadata.get('exifinfo').lower() == "false":
                    get_exif = False;

        if get_exif:
            if 'gallery' in article.metadata.keys():
                album = article.metadata.get('gallery')
                galleryexif = dict()

                articlegallerypath=os.path.join(gallerycontentpath, album)

                # If the gallery has not yet been generated generate one
                if article.metadata.get('galleryimages'):
                    galleryimages = article.metadata.get('galleryimages');
                else:
                    galleryimages = []
                    if(os.path.isdir(articlegallerypath)):
                        for i in os.listdir(articlegallerypath):
                            if os.path.isfile(os.path.join(os.path.join(gallerycontentpath, album), i)):
                                galleryimages.append(i)

                # Retrieve the EXIF informations for all the images
                for img in galleryimages:
                    galleryexif[img] = get_exif_data(articlegallerypath + "/" + img)

                article.galleryexif = galleryexif


def register():
    signals.article_generator_finalized.connect(add_exif_post)