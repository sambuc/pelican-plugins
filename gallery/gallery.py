import os
import ast
from pelican import signals


def add_gallery_post(generator):

    contentpath = generator.settings.get('PATH')
    gallerycontentpath = os.path.join(contentpath,'images/gallery')

    for article in generator.articles:
        if 'gallery' in article.metadata.keys():
            album = article.metadata.get('gallery')
            galleryimages = []
            gallerycaptions = dict()
            gallerycomments = dict()

            articlegallerypath=os.path.join(gallerycontentpath, album)

            if(os.path.isdir(articlegallerypath)):
                for i in os.listdir(articlegallerypath):
                    if os.path.isfile(os.path.join(os.path.join(gallerycontentpath, album), i)):
                        galleryimages.append(i)

            if 'gallerycaptions' in article.metadata.keys():
                line = article.metadata.get('gallerycaptions').encode('ascii','xmlcharrefreplace')
                gallerycaptions = ast.literal_eval(line)

            if 'gallerycomments' in article.metadata.keys():
                line = article.metadata.get('gallerycomments').encode('ascii','xmlcharrefreplace')
                gallerycomments = ast.literal_eval(line)

            article.album = album
            article.galleryimages = sorted(galleryimages)
            article.gallerycaptions = gallerycaptions
            article.gallerycomments = gallerycomments


def generate_gallery_page(generator):

    contentpath = generator.settings.get('PATH')
    gallerycontentpath = os.path.join(contentpath,'images/gallery')

    for page in generator.pages:
        if page.metadata.get('template') == 'gallery':
            gallery = dict()

            for a in os.listdir(gallerycontentpath):
                if os.path.isdir(os.path.join(gallerycontentpath, a)):

                    for i in os.listdir(os.path.join(gallerycontentpath, a)):
                        if os.path.isfile(os.path.join(os.path.join(gallerycontentpath, a), i)):
                            gallery.setdefault(a, []).append(i)
                    gallery[a].sort()

            page.gallery=gallery


def register():
    signals.article_generator_finalized.connect(add_gallery_post)
    signals.page_generator_finalized.connect(generate_gallery_page)
