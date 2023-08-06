from pathlib import Path
from typing import List
import logging
import sys
import bisect as bs
from pyRevealjs.slide import Slide
from pyRevealjs.slide_generator import SlideGenerator


class SlideCatalog:
    """
    The SlideCatalog class manages a catalog of Slide that may be used by the Presentation object.

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

    def __init__(self):
        """builds the object"""
        self.slides = dict()
        """self.slides is a dictionary with key = slide id and value is the version dictionary.
        The version dictionary is defined by key = slide version and value is the part dictionary
        The part dictionary is defined by key = slide part number and value = Slide object"""
        self.versions = []
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

    def createMissingSlides(self, slide_ids):
        """create missing slides according to the given slide ids. SlideCatalog are created with slide title="slide id" where id is the slide id.
        The slide is saved in the slideFolder with the markdown rules details in the class definition"""

        for slide_id in slide_ids:
            if self.getslide_parts(slide_id, self.getHighestVersion()):
                continue
            title = 'slide {}'.format(slide_id)
            slide = Slide(slide_id, title)
            slide.setContent('# '+title)
            self.addSlide(slide)
            logging.info('slide {} {} created'.format(slide_id, title))

    def getHighestVersion(self, slide_id=None):
        """returns the highest version value fourn for at least 1 slide in the collection"""
        if not self.versions:
            return None
        if not slide_id:
            return self.versions[-1]
        if slide_id not in self.slides:
            logging.error('no slide for id %s', slide_id)
            return None

        available_versions = sorted(list(self.slides[slide_id].keys()))

        return float(available_versions[-1])

    def showLinks(self, slide_id, version):
        slide_parts = self.getslide_parts(slide_id, version)
        show = True
        for part in slide_parts:
            show = show and slide_parts[part].showLinks
        return show

    def getslide_parts(self, slide_id, version=None):
        """returns a dictionary with key = part number and value = Slide object corresponding to the slide id and its version. 
        If no version is provided, latest version is used."""

        if not self.slides:
            logging.error("No slide in catalog")
            return None

        if slide_id not in self.slides:
            logging.error('slide {} not found'.format(slide_id))
            return None

        version = self._getSatisfyingVersion(slide_id, version)
        slide_id = int(slide_id)

        return self.slides[slide_id][version]

    def getslide_part(self, slide_id, part=None, version=None) -> Slide:
        """returns a slide part corresponding to the slide id, version and part. 
        If no part is provided, first part is used
        If no version is provided, lattest version is used."""

        slide_parts = self.getslide_parts(slide_id, version)
        if not slide_parts:
            return None

        part = float(part) if part else next(iter(slide_parts))

        return slide_parts[float(part)]

    def getSlideTitle(self, slide_id: int, version: float = None):
        """return the slide title by getting the slide title of its first part"""
        slide = self.getslide_part(slide_id, version=version)
        if not Slide:
            logging.error(
                'no slide for this id: %s / version: %s', slide_id, version)
        return slide.title

    def getSlideContents(self, slide_id: int, version: float = None)->List[str]:
        """returns slide contents, ie a list of markdown contents. Each item of the sorted list correspond to a slide part.If no version is provided, version 0.0 is returned."""
        contents = []
        slide_parts = self.getslide_parts(slide_id, version)
        if not slide_parts:
            contents.append('slide {} is missing.'.format(slide_id))
            return contents

        parts = sorted(list(slide_parts.keys()))

        for part in parts:
            slide_part:Slide = slide_parts[part]
            if slide_part is None:
                contents.append(
                    'slide {} part {} is missing.'.format(slide_id, part))
            contents.append(slide_part.getContent())

        return contents

    def getSlideImages(self, slide_ids: list = None, version: float = None) -> List[Slide]:
        """
        returns a list of filename of slides defined by an image
        Parameters:
        -----------
        slide_ids: [optional] ids of slide for which images should be retrieved, all will be retrieved if none is supplied
        version:  [optional] version of slides for which images should be retrieved. If None, the most recent version will be used.
        """
        if not slide_ids:
            slide_ids = self.getAllIds()

        slides = []
        for slide_id in slide_ids:

            version = self._getSatisfyingVersion(slide_id, version)

            for part in self.slides[slide_id][version]:
                slide = self.slides[slide_id][version][part]
                if slide.isImage:
                    slides.append(slide)

        return slides

    def getAllIds(self):
        return list(self.slides.keys())

    def _getSatisfyingVersion(self, slide_id: int, version:float)->float:

        if version is None:
            version = self.getHighestVersion(slide_id)
            index = self.versions.index(version)
            return version, index

        available_versions = sorted(list(self.slides[slide_id].keys()))
        satisfying_versions = list(
            filter(lambda i: i <= version, available_versions))

        if not satisfying_versions:
            satisfying_versions = [available_versions[0]]
            # TODO si aucune version plus petite ou égale à celle demandée, on prend la plus petite de la liste : ne devrait-on pas supprimer le slide ?
            # si on le supprime, alors la version slide et la version présentation sont cohérentes mais comment le gérer si le workflow et les liens y font appel ?

        version = float(satisfying_versions[-1])

        return version
