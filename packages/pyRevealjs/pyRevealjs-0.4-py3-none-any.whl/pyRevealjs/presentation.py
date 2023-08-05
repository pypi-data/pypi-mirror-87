import os
import sys
import logging
import pathlib
from pyRevealjs.slides import Slides
import distutils.dir_util as dirutil
import distutils.file_util as fileutil


class Presentation:
    """
    The Presentation class writes on disk a presentation based on revealjs.
    It uses Slides class to retrieve the content to display in the presentation, 
    an ordered list of slide ids to create content in this given order. Optionaly it may use links to create 
    more complex presentatrion structure whe a slide ma points on multiple other slides via these links.
    Finally this presentation is versioned, it relies on the different slide versions.
    """

    def createPresentation(self, presName, slides: Slides, slideIds=None, outputFolder=None, links=None, version=0.0, imageFolder=None):
        """
        save a revealjs presentation in output folder.
        ---
        Parameters:
        - presName: the filename of the presentation.
        - slides: the slides to display in presentation
        - slideIds: ordered list of Slide id (See class Slide for more information). 
        Slide content will be retrieve and saved in the presentation from Slides object in this order
        - outputFolder: folder where the presentation will be saved. If None, the current working directory (folder from where the app is launched) is used
        - links: dictionary with key = current slideId and values = next slideIds to be linked to current slideId
        - version: version of the presentation (float) = version of the slides if available or previous version if not. Default value is 0.0
        - imageFolder: folder that contains images to add in the presentation
        """
        if not outputFolder:
            outputFolder = os.getcwd()

        pathlib.Path(outputFolder).mkdir(parents=True, exist_ok=True)

        logging.info('create presentation {} '.format(
            os.path.join(outputFolder, presName)))

        self._copyLibs(outputFolder)

        self._copyImages(slides, outputFolder)

        file = os.path.join(outputFolder, presName)

        asset1 = self.resource_path(os.path.join('assets', 'firstPart.txt'))
        asset2 = self.resource_path(os.path.join('assets', 'secondPart.txt'))

        if not slideIds:
            slideIds = slides.getDefaultSlideOrder()

        with open(file, mode='w') as output:
            self._copyInOutput(output, asset1)
            for slideId in slideIds:
                htmlLinks = slides.getMarkdownLinks(
                    links[slideId], version) if links else None
                self._writeMarkdownSection(output,
                                           slides.getSlideContents(slideId, version), htmlLinks)
            self._copyInOutput(output, asset2)

        return file

    def resource_path(self, relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(
            os.path.abspath(__file__)))
        return os.path.join(base_path, relative_path)

    def _copyLibs(self, outputFolder):
        logging.info('copying libs...')
        libs = self.resource_path(os.path.join('assets', 'reveal.js-3.9.2'))
        dirutil.copy_tree(libs, os.path.join(outputFolder, 'libs'))

    def _copyImages(self, slides: Slides, outputFolder: str):
        logging.info('copying images...')
        output = os.path.join(outputFolder, 'images')
        imageFolders = slides.imageFolders
        for slideId in slides.slides:
            for version in slides.slides[slideId]:
                for part in slides.slides[slideId][version]:
                    self._copyImage(
                        slides.slides[slideId][version][part], output)
        for folder in imageFolders:
            dirutil.copy_tree(folder, output, update=True)

    def _copyImage(self, slide, output):
        if not slide.isImage:
            return

        if output == os.path.dirname(slide.filename):
            return

        if not os.path.exists(output):
            os.makedirs(output)

        newFile = os.path.join(output, os.path.basename(slide.filename))
        fileutil.copy_file(slide.filename, newFile, update=True)
        slide.filename = newFile

    def _copyInOutput(self, output, content):
        with open(content, mode='r') as file:
            output.write(file.read())

    def _writeMarkdownSection(self, output, slideContents, links=None):

        end = '\n</section>'
        closeContentSection = '\n</textarea>'
        if len(slideContents) == 1:
            content = '<section data-markdown>\n<textarea data-template>'
            openSection = ''
            closeSection = ''

        else:
            content = '<section>\n'
            openSection = '\n<section data-markdown>\n<textarea data-template>'
            closeSection = '</section>\n'
            end = '\n</section>'

        for index, slideContent in enumerate(slideContents):
            content += openSection
            content += slideContent

            if index == len(slideContents) - 1 and links:
                sep = '-'
                link_line = sep.join(links)+'\n'
                content += link_line
#                 for link in links:
#                     content += link+'\n'
                    # content+='\n<div><a href="'+link['href']+'">'+link['text']+'</a></div>\n'

            content += closeContentSection
            content += closeSection

        content += end
        output.write(content)
