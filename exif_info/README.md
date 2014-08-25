EXIF Info
==================

* Retrieve EXIF informations from pictures

##How to Use

1. Install the PIL (Python Imaging Library) libraries, please refer to http://pythonware.com/products/pil/ or your OS manual for instructions.
2. This plugin is an extension to the Gallery plugin, so first install it, and refer to its README for usage instructions.
3. Add 'exif_info' to the plugin list.

If you want, you can also specify in your configuration: 

	EXIF_INFO_DEFAULT = True/False

To set whether or not to retrieve by default the EXIF informations from your pictures. This setting can be overriden on a per article/album basis.

###Articles

Override on a per article/post basis the default behaviour by adding the following:

	exifinfo: "True"

or

	exifinfo: "False"

###Gallery Page

At this time the Gallery page is *not* supported.

##Examples

###article.html

    {% if article.album %}
        {% for image in article.galleryimages %}
             {% if article.galleryexif and article.galleryexif.get(image) %}
                <table>
                    {% if article.galleryexif.get(image).get("Model") %}
                    <tr><th colspan="4">{{article.galleryexif.get(image).get("Model")}}</th></tr>
                    {% endif %}
                    {% if article.galleryexif.get(image).get("LensModel") %}
                    <tr><th colspan="4">{{article.galleryexif.get(image).get("LensModel")}}</th></tr>
                    {% endif %}
                    <tr>
                    {% if article.galleryexif.get(image).get("ISOSpeedRatings") %}
                        <td>{{article.galleryexif.get(image).get("ISOSpeedRatings")}}</td>
                    {% endif %}
                    {% if article.galleryexif.get(image).get("FocalLength") %}
                        <td>{{article.galleryexif.get(image).get("FocalLength")}}mm</td>
                    {% endif %}
                    {% if article.galleryexif.get(image).get("FNumber") %}
                        <td>f/{{article.galleryexif.get(image).get("FNumber")}}</td>
                    {% endif %}
                    {% if article.galleryexif.get(image).get("ExposureTime") %}
                        <td>{{article.galleryexif.get(image).get("ExposureTime")}}</td>
                    {% endif %}
                    </tr>
                </table>
            {% endif %}
        {% endfor %}
    {% endif %}

##Reasoning

This was developped as an external plugin, instead of adapting the Gallery plugin because this relies on the PIL libraries to be installed, and working.

As this set of library may - or not - be available on a given platform, it seemed unreasonable to limit the Gallery plugin to the systems where it is.