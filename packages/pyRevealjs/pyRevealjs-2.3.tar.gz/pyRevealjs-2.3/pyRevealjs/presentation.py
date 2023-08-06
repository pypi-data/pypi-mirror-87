import os
import re
import sys
import logging
import pathlib
import tempfile
from bs4 import BeautifulSoup
from pyRevealjs.slide_catalog import SlideCatalog
from pyRevealjs.slide import Slide
from typing import List, Dict
import distutils.dir_util as dirutil
import distutils.file_util as fileutil
from pyRevealjs.presentation_settings import PresentationSettings


class Presentation:
    """
    The Presentation class writes on disk a presentation based on revealjs.
    It uses SlideCatalog class to retrieve the content to display in the presentation, 
    an ordered list of slide ids to create content in this given order. Optionaly it may use links to create 
    more complex presentatrion structure whe a slide ma points on multiple other slides via these links.
    Finally this presentation is versioned, it relies on the different slide versions.
    """

    def __init__(self, presName, catalog: SlideCatalog, settings: PresentationSettings = None):
        """
        prepare the presentation object with a Name and a path to write presentation on disk.
        ---
        Parameters:
        - presName: the filename of the presentation.
        - catalog: catalog of slide
        - settings: dictionary of general settings. If None, default are applied
        """
        self.presName = presName
        self.catalog = catalog
        self.settings = settings if settings else PresentationSettings()
        self.slide_ids = []
        self.links = None
        self.slide_order = None
        self.template = self._resource_path(
            os.path.join('assets', 'template.html'))
        self.html: Dict[BeautifulSoup] = {}
        self.temp_dir = None
        self.files = {}

    def addLinks(self, links):
        """
        add links to certain slides.
        ---
        Parameters:
        - links: dictionary with key = current slide_id and values = next self.slide_order to be linked to current slide_id
        """
        self.links = links

    def addSlideById(self, id: int):
        self.slide_ids.append(id)

    def addSlideByIds(self, ids: List[int]):
        self.slide_ids.extend(ids)

    def defineSlideOrder(self, slide_order):
        """
        define in which order slides will be displayed
        ---
        Parameters:
        - slide_order: ordered list of Slide id. 
        the slide ids contained in this list must be consistent with the provided slide ids supplied with addSlide(s)
        slide_order can shorten the displayed slides but obviously can't point on non-referenced slides
        """
        self.slide_order = slide_order

    def generate(self, version: float = 0.0):
        """
        generate the html presentation.
        ---
        Parameters:
        - version: version of the presentation (float) = version of the slides if available or previous version if not. Default value is 0.0
        """
        logging.info('generate presentation {}, version {} '.format(
            self.presName, version))

        with open(self.template) as template:
            self.html[version] = BeautifulSoup(template, 'html.parser')

        self._setGeneralSettings(self.html[version])

        # if defineSlideOrder has not been called, all slides supplied with addSlide(s) are sorted increasingly and all are used
        if not self.slide_order:
            self.slide_order = sorted(self.slide_ids)

        for slide_id in self.slide_order:
            self._writeMarkdownSection(slide_id, version)

        self.temp_dir = tempfile.TemporaryDirectory().name
        output = os.path.join(self.temp_dir, str(version))
        file = self._prepareOutput(output, version)
        self.files[version] = file

        with open(file, "w") as output:
            output.write(self.html[version].prettify())

    def save(self, output_folder=None, version: float = 0.0):
        """
        save presentation in outpurFolder
        ---
        Parameters:
        - output_folder: folder where the presentation will be saved. If None, the current working directory (folder from where the app is launched) is used
        """
        if version not in self.html:
            self.generate(version)

        output_folder = output_folder if output_folder else os.getcwd()
        source_folder = os.path.join(self.temp_dir, str(version))
        # TODO best if we don't recopy existing files...
        dirutil.copy_tree(source_folder, output_folder)
        return self.files[version]

    def _resource_path(self, relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(
            os.path.abspath(__file__)))
        return os.path.join(base_path, relative_path)

    def _prepareOutput(self, output_folder, version):
        pathlib.Path(output_folder).mkdir(parents=True, exist_ok=True)
        self._copyLibs(output_folder)
        self._copyImages(output_folder, version)
        return os.path.join(output_folder, "{}_v{}.html".format(self.presName, version))

    def _copyLibs(self, output_folder):
        logging.info('copying libs...')
        libs = self._resource_path(os.path.join('assets', 'revealjsdist4.1.0'))
        dirutil.copy_tree(libs, os.path.join(output_folder, 'libs'))

    def _copyImages(self, output_folder: str, version):
        logging.info('copying images...')
        output = os.path.join(output_folder, 'images')
        imageFolders = self.catalog.imageFolders
        self.catalog.getSlideImages(self.slide_ids, version)

        slide_images = self.catalog.getSlideImages(self.slide_ids, version)
        for slide in slide_images:
            filename = slide.filename
            new_file = self._copyImage(filename, output)
            slide.filename = new_file
        for folder in imageFolders:
            dirutil.copy_tree(folder, output, update=True)

    def _copyImage(self, filename, output):

        if output == os.path.dirname(filename):
            return filename

        if not os.path.exists(output):
            os.makedirs(output)

        newFile = os.path.join(output, os.path.basename(filename))
        fileutil.copy_file(filename, newFile, update=True)
        return newFile

    def _setGeneralSettings(self, html: BeautifulSoup):
        html.title.string = self.settings.title
        self._setTheme(html)

    def _setTheme(self, html: BeautifulSoup):
        theme_tag = html.find(id='theme')
        link = theme_tag['href']
        sep = r'/'
        split = link.rsplit(sep, 1)
        split[1] = self.settings.theme+'.css'
        link = sep.join(split)
        theme_tag['href'] = link

    def _writeMarkdownSection(self, slide_id, version):

        links = self._getMarkdownLinks(slide_id, version)
        slide_contents = self.catalog.getSlideContents(slide_id, version)
        showLinks = self.catalog.showLinks(slide_id, version)

        html: BeautifulSoup = self.html[version]
        slides = html.find(class_='slides')

        nb_of_part = len(slide_contents)
        if nb_of_part > 1:
            parent = html.new_tag("section")
            slides.append(parent)
        else:
            parent = slides

        for part, slide_content in enumerate(slide_contents):
            section = html.new_tag("section", id='id'+str(slide_id))
            section['data-markdown'] = ''
            text_area = html.new_tag("textarea")
            text_area['data-template'] = ''
            section.append(text_area)
            parent.append(section)

            if showLinks:
                line = self._getLinkLine(links, part, slide_contents)
                slide_content += line
            text_area.string = slide_content

    def _getLinkLine(self, links, part, slide_contents):

        if not links:
            return ''

        # add links only in the last part of the slide
        if part != len(slide_contents) - 1:
            return ''

        sep = '-'
        return "  \n"+sep.join(links)

    def _getMarkdownLinks(self, slide_id: int, version:float=None):
        """returns markdown links correponding to the given link ids. It transforms theses ids as html links in a Presentation."""
        if self.links is None:
            return None

        if slide_id not in self.links:
            return None

        mdLinks = []
        for id in self.links[slide_id]:
            href = '#/id'+str(id)
            text = self.catalog.getSlideTitle(id, version)
            mdLinks.append('['+text+']('+href+')')
        return mdLinks
