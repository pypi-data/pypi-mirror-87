import logging
import os.path as path
import re
from pyRevealjs.slide import Slide


class SlideGenerator:
    """
    The SlideGenerator class tries to extract and returns needed information from files (markdown or images) to build a Slide object.
    It also checks that all necessary pieces of information are available to build this object.
    """

    def fromImage(self, file):
        """
        extract information from an image file name and returns a dictionary with the following key/value pairs:
        - title: arbitrary title
        - id: a unique integer. 2 slides can't have the same id, except if it is split.
        - part: [optional] float number. A Slide may be split in multiple parts. In this case, they have the same id but a different part number. If not set, 0.0 is the default value.
        - version: [optional] float number. A slide may have different versions, then a history may be managed (version 0 is older than version 1). If not set, 0.0 is the default value
        """
        details = self._fromFilename(file)
        return self._getSlide(details, file, isImage=True)

    def fromFilename(self, file):
        """
        extract information from the file name and returns a dictionary with the following key/value pairs:
        - title: arbitrary title
        - id: a unique integer. 2 slides can't have the same id, except if it is split.
        - part: [optional] float number. A Slide may be split in multiple parts. In this case, they have the same id but a different part number. If not set, 0.0 is the default value.
        - version: [optional] float number. A slide may have different versions, then a history may be managed (version 0 is older than version 1). If not set, 0.0 is the default value
        """
        details = self._fromFilename(file)
        return self._getSlide(details, file)

    def _fromFilename(self, file):
        filename = path.basename(file)
        patterns = re.search(r'([0-9]+)_([^_]+)_?([^_]*)_?(.*)\.',
                             filename, re.IGNORECASE)
        if not patterns or len(patterns.groups()) < 2:
            logging.warning(
                'filename {} does not comply with expected pattern: id_title[_part][_version]'.format(filename))
            return None

        details = dict()
        details['id'] = patterns.group(1)

        details['title'] = patterns.group(2)

        details['part'] = patterns.group(3) if len(
            patterns.group(3)) > 0 and patterns.group(3) else 0.0

        details['version'] = float(patterns.group(4)) if len(
            patterns.group(4)) > 0 and patterns.group(4) else 0.0

        return details

    def fromHeader(self, file):
        """
        extract information from header section in a file and returns a dictionary with the following key/value pairs:
        - title: arbitrary title
        - id: a unique integer. 2 slides can't have the same id, except if it is split.
        - part: [optional] float number. A Slide may be split in multiple parts. In this case, they have the same id but a different part number. If not set, 0.0 is the default value.
        - version: [optional] float number. A slide may have different versions, then a history may be managed (version 0 is older than version 1). If not set, 0.0 is the default value
        """
        with open(file) as f:
            data = f.read()

        contents = re.split('---+', data)

        if len(contents) < 2:
            return

        details = dict()
        header = contents[1]
        headerLines = header.splitlines()
        for line in headerLines:
            splitLine = line.split(':', 1)
            if len(splitLine) < 2:
                continue
            headerTag = splitLine[0].strip()
            details[headerTag] = splitLine[1].strip()

        return self._getSlide(details, file)

    def _getSlide(self, details, file, isImage=False):
        if not self._formatAndCheck(details):
            return None

        slide = Slide(details['id'], details['title'],
                      details['part'], details['version'], isImage=isImage)
        slide.associateFile(file)
        return slide

    def _formatAndCheck(self, details: dict):
        """
        checks is the given details are sufficient to define a slide.
        It also defines default values for part and version if not present in details
        ---
        Parameters:
        - details: a dictionary containing information on slides.
        The check is ok if this dictionary contains at least the keys 'title' and 'id'
        and if the value associated with the id key is an integer value
        """

        if not details:
            return False

        keys = ['title', 'id']
        for key in keys:
            if key not in details:
                return False

        if 'part' not in details:
            details['part'] = 0.0
        if 'version' not in details:
            details['version'] = 0.0

        try:
            details['id'] = int(details['id'])
            details['part'] = float(details['part'])
            details['version'] = float(details['version'])
        except ValueError:
            return False

        return True
