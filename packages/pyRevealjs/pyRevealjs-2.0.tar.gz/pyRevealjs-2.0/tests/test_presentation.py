from pyRevealjs import Slide, SlideCatalog, SlideGenerator, Presentation, PresentationSettings
import unittest
import tempfile
import logging


class testPresentation(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.temp_dir = tempfile.TemporaryDirectory()
        print('temp dir: ', cls.temp_dir.name)

    @classmethod
    def tearDownClass(cls):
        cls.temp_dir.cleanup()

    def test_simple(self):
        # get slides from images
        catalog = SlideCatalog()
        catalog.catalog('tests/resources/onlyimages', images=True)
        # Create Presentation based on Slides in the current working directory
        settings = {'title': 'simple presentation', 'theme': 'white'}
        pres = Presentation('simple presentation', catalog, PresentationSettings(settings))
        pres.addSlideByIds(catalog.getAllIds())
        pres.save('temp')

    def test_full(self):
        # Create a slide with id=1. Part and version numbers are let to defaut values (0.0)
        # Content is given as a string
        slide1 = Slide(1, "slide 1")
        slide1.setContent(
            '# Slide1  \nversion {} - part {}'.format(slide1.version, slide1.part))

        # Create slide 2
        # Content is given as an external markdown file with header where id=2. Part and version numbers are let to defaut values (0.0)
        slide2part0 = SlideGenerator().fromHeader('tests/resources/full/slide2.md')

        # Create a slide with the same id than slide 2 because it is a second part (part number 1.1) of the same slide
        # Parts of a same slide will be displayed vertically in the presentation while different ids are displayed horizontally
        slide2part1 = Slide(2, 'slide2-1', part=1.1)
        slide2part1.setContent(
            '# Slide2  \nversion {} - part {}'.format(slide2part1.version, slide2part1.part))

        # The content is not defined, it will be automatically generated using the title of the slide
        # content is not defined for this slide, it will automatically generated based on its title
        slide3version0_1 = Slide(3, 'slide3', version=0.1)
        slide3version0_1.setContent(
            '# Slide3  \nversion {} - part {}'.format(slide3version0_1.version, slide3version0_1.part))

        slide3version1 = Slide(3, 'slide3', version=1)
        slide3version1.setContent(
            '# Slide3  \nversion {} - part {}'.format(slide3version1.version, slide3version1.part))

        # Add slides to Slides
        catalog = SlideCatalog()
        catalog.addSlide(slide1)
        catalog.addSlide(slide2part0)
        catalog.addSlide(slide2part1)
        catalog.addSlide(slide3version0_1)
        catalog.addSlide(slide3version1)

        # slide2.md asks to not display links
        links = {1: [2, 3], 2: [3]}

        # if slides embed images from imageFolder in their markdown content, the following line is required:
        # slides.declareResources(imageFolder):

        # Define versions of presentation to create
        # slides does not need to all have the same version. The presentation will find the closest version of slide less than the requested version if not found
        versions = [0.0, 0.1, 1.0]

        # Create Presentation based on Slides in the current working directory
        pres = Presentation('presentation', catalog)
        pres.addSlideByIds(catalog.getAllIds())
        pres.addLinks(links)
        temp = self.temp_dir.name
        for version in versions:
            pres.save('temp', version)
