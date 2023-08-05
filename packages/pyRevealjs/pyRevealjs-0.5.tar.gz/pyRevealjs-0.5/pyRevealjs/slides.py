from pathlib import Path
import logging
import sys
import bisect as bs
from pyRevealjs.slide import Slide
from pyRevealjs.slideGenerator import SlideGenerator


class Slides:
    """
    The Slides class manages a catalog of Slide that may be used by the Presentation object.

    The slides may be retrieved from a disk location if the markdown files defining the slide content respect one of the following rules:
    - the markdown file owns a header section composed of a "---" sequence defining the start and end of the header. It should be at the very beginning of the file.
    In this header at least 2 keys must be defined :
        - title: arbitrary title
        - id: a unique integer. 2 slides can't have the same id, except if it is split.
        - part: [optional] float number. A Slide may be split in multiple parts. In this case, they have the same id but a different part number. If not set, 0.0 is the default value.
        - version: [optional] float number. A slide may have different versions, then a history may be managed (version 0 is older than version 1). If not set, 0.0 is the default value
    - the markdown file name is built as follow: id_title[_part][_version]. The fields are the same than in the header definition
    The slides can also be added by passing Slide objects.
    The slides may be built thanks to images. Image names should comply with the same rule given for markdown file names.
    """

    def __init__(self, displayTitles=False):
        """builds the object"""
        self.slides = dict()
        """self.slides is a dictionary with key = slide id and value is the version dictionary.
        The version dictionary is defined by key = slide version and value is the part dictionary
        The part dictionary is defined by key = slide part number and value = Slide object"""
        self.versions = [0]
        """references in a sorted list the different available versions. Some version may be only available for one or more slides."""
        self.displayTitles = displayTitles
        """if True, the slide title is displayedin slides"""
        self.imageFolders = []

    def catalog(self, folder: str, images=False):
        """
        references slides by the files contained in the given folder if they comply with the rules defined in the class definition
        ---
        Parameters:
        - folder: folder where files to produce slides may be found
        - images: indicates if files are image files if True
        """
        logging.info('search for files to create slides...')

        if images:
            self.declareResources(folder)

        path = Path(folder).rglob('*.*')
        files = [x for x in path if x.is_file()]
        counter = 0
        for file in files:
            slide = None
            if images:
                slide = SlideGenerator().fromImage(file)
            else:
                slide = SlideGenerator().fromHeader(file)
                if not slide:
                    slide = SlideGenerator().fromFilename(file)
            if not slide:
                logging.warning(
                    'can\'t retrieve useful information from file {}, slide is not created.'.format(file))
                continue
            self.addSlide(slide)
            counter += 1
        if counter > 0:
            logging.info('{} slides created'.format(counter))
        else:
            logging.warning(
                'no file found to define slides in {}'.format(folder))

    def declareResources(self, imageFolder):
        self.imageFolders.append(imageFolder)

    def addSlide(self, slide: Slide):
        """add a predefined Slide object"""
        version = slide.version
        if slide.id not in self.slides:
            self.slides[slide.id] = dict()
        if version not in self.slides[slide.id]:
            bs.insort(self.versions, version)
            self.slides[slide.id][version] = dict()
        self.slides[slide.id][version][slide.part] = slide

    def createMissingSlides(self, slideIds):
        """create missing slides according to the given slide ids. Slides are created with slide title="slide id" where id is the slide id.
        The slide is saved in the slideFolder with the markdown rules details in the class definition"""

        for slideId in slideIds:
            if self.getSlide(slideId, self.getHighestVersion()):
                continue
            title = 'slide {}'.format(slideId)
            slide = Slide(slideId, title)
            slide.setContent('# '+title)
            self.addSlide(slide)
            logging.info('slide {} {} created'.format(slideId, title))

    def getDefaultSlideOrder(self):
        return sorted(list(self.slides.keys()))

    def getFileName(self, title, id, version=0, part=0):
        """returns the slide filename"""
        return '{1}{0}{2}{0}{3}{0}{4}{5}'.format('_', id, title, version, part, '.md')

    def getHighestVersion(self):
        """returns the highest version value fourn for at least 1 slide in the collection"""
        return self.versions[-1]

    def getSlide(self, slideId, version=0):
        """returns a dictionary with key = part number and value = Slide object corresponding to the slide id and its version. 
        If no version is provided, version 0.0 is returned."""
        version = float(version)
        slideId = int(slideId)

        if slideId not in self.slides:
            logging.warning('slide {} not found'.format(slideId))
            return None

        try:
            index = self.versions.index(version)
        except ValueError:
            index = len(self.versions) - 1

        while version not in self.slides[slideId] and index >= 0:
            index -= 1
            version = self.versions[index]

        if index < 0:
            return self.slides[slideId][next(iter(self.slides[slideId]))]

        return self.slides[slideId][version]

    def _getSlidePart(self, slideId, part, version=0):
        """returns a slide part corresponding to the slide id, version and part. If no version is provided, version 0.0 is returned."""

        slide = self.getSlide(slideId, version)

        if not slide:

            return None

        # try:
        return slide[float(part)]
        # except KeyError:
        #     error("part {} not found for slide {}".format(part, slideId))

        # return self.slides[version][slideId][part]

    def getSlideTitle(self, slideId, version=0):
        """return the slide title by getting the slide title of its first part"""
        return self.getSlide(slideId, version)[next(iter(self.getSlide(slideId, version)))].title

    def getSlideContents(self, slideId, version=0):
        """returns slide contents, ie a list of markdown contents. Each item of the sorted list correspond to a slide part.If no version is provided, version 0.0 is returned."""
        contents = []
        slide = self.getSlide(slideId, version)
        if slide is None:
            contents.append('slide {} is missing.'.format(slideId))
            return contents
        parts = list(slide.keys())
        parts.sort()

        for part in parts:
            slidePart = self._getSlidePart(slideId, part, version)
            if slide is None:
                contents.append(
                    'slide {} part {} is missing.'.format(slideId, part))
            contents.append(slidePart.getContent(self.displayTitles))
        return contents

    def getMarkdownLinks(self, links, version=0):
        """returns markdown links correponding to the given link ids. It transforms theses ids as html links in a Presentation."""
        if links is None:
            return None
        mdLinks = ["  \n"]
        for slideId in links:
            href = '#/'+str(links[slideId])
            text = self.getSlideTitle(slideId, version)
            mdLinks.append('['+text+']('+href+')')
        return mdLinks
