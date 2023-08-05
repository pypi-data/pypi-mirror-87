import re, sys, logging
import os.path as path

class Slide:
    """
    The Slide class defines a Slide used in a Presentation.  
    A slide is defined by its id, filename and title, and optionally a part number and a version number.
    The filenames points on a disk location where the slide content can be retrieved in a markdown format.
    The other arguments are:
    - title: arbitrary title
    - id: a unique integer. 2 slides can't have the same id, except if it is split.
    - part: [optional] float number. A Slide may be split in multiple parts. In this case, they have the same id but a different part number. If not set, 0.0 is the default value.
    - version: [optional] float number. A slide may have different versions, then a history may be managed (version 0 is older than version 1). If not set, 0.0 is the default value
    """

    def __init__(self, id: int, title: str, part=0, version=0, isImage=False):
        """builds the object"""
        self.filename = None
        self.content = None
        self.isImage = isImage
        self.id = id
        self.title = title
        self.part = float(part)
        self.version = float(version)

    def associateFile(self, filename: str):
        """
        associates a file to this slide to retrieve the content.
        A header may be defined in the markdown file. See The Slides object for more information.
        """
        self.filename = filename

    def setContent(self, text: str):
        """
        sets the content of the slide
        ---
        Parameters:
        - text: a markdown formated text
        """
        self.content = text

    def _getFileContent(self):
        """
        get markdown file content. 
        """
        with open(self.filename) as file:
            data = file.read()

        groups = re.split('---+', data)

        if len(groups) < 2:
            return data

        content = ''
        for group in groups[2:]:
            content += group
        return content

    def _getImageContent(self):
        # def createImageSlideContent(self, slides, outputFolder, image):
        imageLink = path.basename(path.dirname(
            self.filename))+'/'+path.basename(self.filename)
        content = '![{0}]({1})'.format(
            self.title, re.sub(r'\s+', '%20', imageLink))
        return content

    def getContent(self, addTitle=False):
        """ get slide content"""
        content = self.content
        if self.filename:
            if self.isImage:
                content = self._getImageContent()
            else:
                content = self._getFileContent()

        if addTitle or not content:
            content = self._addTitle(content)

        return content

    def _addTitle(self, content):
        if not content:
            content = ''
        return '## '+self.title+'\n'+content
