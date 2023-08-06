""" Multimedia
"""
import os.path
import OFS.Image
import PIL.Image
from StringIO import StringIO
from zope.component import getUtility
from zope.interface import implements
from zope.publisher.interfaces import NotFound
from Products.CMFCore.interfaces import IPropertiesTool
from Products.Five.browser import BrowserView
from p4a.video.interfaces import IVideo
from eea.depiction.browser.interfaces import IImageView
from eea.depiction.cache import ramcache


class MultimediaImageView(BrowserView):
    """ Adapts a p4a video object and returns its album art image.
        This makes it possible to enter a URL like my_vid_file/image_thumb
         and have it return the p4a album art - no need for p4a's long and
         weird looking video art URLs.
    """
    implements(IImageView)
    _img = False

    @property
    def img(self):
        """ img
        """
        if self._img is False:
            self._img = IVideo(self.context).video_image
        return self._img

    @ramcache(lambda *args: "button", lifetime=31536000)
    def button(self):
        """ Media play button
        """
        path = os.path.dirname(__file__)
        path = os.path.join(path, 'images', 'play-button.png')
        with open(path) as ofile:
            return ofile.read()

    @ramcache(lambda *args: "sizes", lifetime=86400)
    def sizes(self):
        """ Sizes
        """
        _sizes = {}
        props = getUtility(IPropertiesTool).imaging_properties
        sizes = props.getProperty('allowed_sizes')
        for size in sizes:
            name, info = size.split(' ')
            w, h = info.split(':')
            _sizes[name] = (int(w), int(h))
        return _sizes

    def display(self, scalename='thumb'):
        """ Display
        """
        if not self.img:
            return False
        return scalename in self.sizes()

    def __call__(self, scalename='thumb', fieldname='image'):
        #This scaling should be done once and then cached
        if not self.display(scalename):
            raise NotFound(self.request, scalename)

        orig = PIL.Image.open(StringIO(self.img.data))
        button = PIL.Image.open(StringIO(self.button()))
        thumb = thumbnail(orig, button, self.sizes()[scalename])

        destfile = StringIO()
        thumb.save(destfile, 'PNG')
        destfile.seek(0)

        dest = OFS.Image.Image('tmp-video-thumb', 'tmp-video-thumb', destfile)
        dest.width = thumb.size[0]
        dest.height = thumb.size[1]

        return dest.__of__(self.context)


def thumbnail(orig, button, size):
    """ Thumbnails
    """
    # Create an image with the requested size
    bg = PIL.Image.new('RGB', size, color=(0, 0, 0))

    # Investigate the dimensions of the resulting image depending on if we
    # scale the width or the height
    scale = float(size[0]) / orig.size[0]
    scaled_height = int(scale * orig.size[1])

    scale = float(size[1]) / orig.size[1]
    scaled_width = int(scale * orig.size[0])

    # If there's less than 10 px between the scaled version and the resulting
    # size, we clamp the image (hope no-one will see the difference!). This
    # is to avoid tiny black borders
    if (size[0] - scaled_width) < 10:
        scaled_width = size[0]
    if (size[1] - scaled_height) < 10:
        scaled_height = size[1]

    # Scale in the direction that results in least black borders
    if (scaled_height - size[1]) < (scaled_width - size[0]):
        thumb_size = (size[0], scaled_height)
    else:
        thumb_size = (scaled_width, size[1])
    thumb = orig.resize(thumb_size, PIL.Image.ANTIALIAS)

    # Paste it onto the background (centered)
    x = (bg.size[0]/2) - (thumb.size[0]/2)
    y = (bg.size[1]/2) - (thumb.size[1]/2)
    w = x + thumb.size[0]
    h = y + thumb.size[1]
    bg.paste(thumb, (x, y, w, h))

    # Apply the play button (centered)
    scale = float(thumb_size[1]) / button.size[1]
    new_button_size = (int(button.size[0]*scale), int(button.size[1]*scale))
    button = button.resize(new_button_size, PIL.Image.ANTIALIAS)
    x = (bg.size[0]/2) - (button.size[0]/2)
    y = (bg.size[1]/2) - (button.size[1]/2)
    bg.paste(button, (x, y), button)

    return bg
