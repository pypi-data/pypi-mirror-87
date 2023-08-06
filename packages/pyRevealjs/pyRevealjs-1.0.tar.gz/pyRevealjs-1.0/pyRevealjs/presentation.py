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
                self._writeMarkdownSection(output, slideId, slides, version, links)
            self._copyInOutput(output, asset2)

        return file

    def resource_path(self, relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(
            os.path.abspath(__file__)))
        return os.path.join(base_path, relative_path)

    def _copyLibs(self, outputFolder):
        logging.info('copying libs...')
        libs = self.resource_path(os.path.join('assets', 'revealjsdist4.1.0'))
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

    def _writeMarkdownSection(self, output, slideId, slides, version, slideLinks):

        links = slides.getMarkdownLinks(
            slideLinks[slideId], version) if slideLinks and slideId in slideLinks else None
        slideContents = slides.getSlideContents(slideId, version)
        showLinks = slides.showLinks(slideId, version)

        end = '\n</section>'
        closeContentSection = '\n</textarea>'
        if len(slideContents) == 1:
            content = ''
            openSection1 = '\n<section data-markdown id="'
            openSection2 = '">\n<textarea data-template>'
            closeSection = ''

        else:
            content = '<section>\n'
            openSection1 = '\n<section data-markdown id="'
            openSection2 = '">\n<textarea data-template>'
            closeSection = '</section>\n'
            end = '\n</section>'

        for index, slideContent in enumerate(slideContents):
            content += openSection1
            content += 'id'+str(slideId)
            content += openSection2
            content += slideContent

            if showLinks:
                print('showLinks')
                line = self._getLinkLine(links, index, slideContents)
                print(line)
                content += line

            content += closeContentSection
            content += closeSection

        content += end
        output.write(content)

    def _getLinkLine(self, links, index, slideContents):

        print('links', links)
        print('index', index)
        print('slideContents', len(slideContents))

        if not links:
            return ''

        if index != len(slideContents) - 1:
            return ''

        sep = '-'
        return "  \n"+sep.join(links)
