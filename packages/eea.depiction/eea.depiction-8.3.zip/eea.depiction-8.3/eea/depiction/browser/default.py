"""Views registered for default thumbnail sizes for all ITraversable content.

The problem is that there is some code that tries to do something like:
    obj.restrictedTraverse('image_preview')

This will return None because the code in Traversable.py only tries to look

for a view and doesn't try to use the DefaultPublishTraverse hook that
v.i uses as traverser.
"""

from eea.depiction.traverse import ScaleTraverser
from zope.component import getMultiAdapter
from zope.publisher.interfaces.browser import IBrowserPublisher


class Base(object):
    """ Base
    """
    name = None

    def __call__(self):
        adapter = getMultiAdapter((
            self.context, self.request), IBrowserPublisher)

        # this code handles archetypes image fields
        scale = adapter.publishTraverse(self.request, self.name)
        index_html = getattr(scale, 'index_html', None)

        if index_html:
            return scale.index_html(self.request, self.request.response)

        # this code is meant to handle plone.namedfile scales
        traverser = ScaleTraverser(self.context, self.request)
        scale = traverser.fallback(self.request, self.name)
        index_html = getattr(scale, 'index_html', None)

        if index_html:
            return scale.index_html()
        else:
            return ""

    def absolute_url(self):
        """ URL
        """

        return self.context.absolute_url() + '/' + self.name


#
# EEA Custom Image scales
#
class ImagePrint(Base):
    """ Print
    """
    name = "image_print"


class ImagePanoramic(Base):
    """ Panoramic
    """
    name = "image_panoramic"


class ImageLandscape(Base):
    """ Landscape
    """
    name = "image_landscape"


class ImagePortrait(Base):
    """ Portrait
    """
    name = "image_portrait"


class ImageXlarge(Base):
    """ XLarge
    """
    name = "image_xlarge"


class ImageWide(Base):
    """ Wide
    """
    name = "image_wide"


#
# Plone default image scales
#
class ImageLarge(Base):
    """ Large
    """
    name = "image_large"


class ImagePreview(Base):
    """ Preview
    """
    name = "image_preview"


class ImageMini(Base):
    """ Mini
    """
    name = "image_mini"


class ImageThumb(Base):
    """ Thumb
    """
    name = "image_thumb"


class ImageTile(Base):
    """ Title
    """
    name = "image_tile"


class ImageIcon(Base):
    """ Icon
    """
    name = "image_icon"


class ImageListing(Base):
    """ Listing
    """
    name = "image_listing"
