from pyRevealjs import Slide, Slides, SlideGenerator, Presentation
import unittest
import tempfile


class testPresentation(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.temp_dir = tempfile.TemporaryDirectory()
        print('temp dir: %s', cls.temp_dir.name)

    @classmethod
    def tearDownClass(cls):
        cls.temp_dir.cleanup()

    def test_simple(self):
        # get slides from images
        slides = Slides()
        slides.catalog('tests/resources/onlyimages', images=True)
        # Create Presentation based on Slides in the current working directory
        Presentation().createPresentation('presentation.html',
                                          slides, outputFolder=self.temp_dir.name)

    def test_full(self):
        # Create a slide with id=1. Part and version numbers are let to defaut values (0.0)
        # Content is given as a string
        slide1 = Slide(1, "slide 1")
        slide1.setContent(
            '# Slide1\nThis slide has only 1 version (0.0) and one part (0.0)')

        # Create slide 2
        # Content is given as an external markdown file with header where id=2. Part and version numbers are let to defaut values (0.0)
        slide2part0 = SlideGenerator().fromHeader('tests/resources/full/slide2.md')

        # Create a slide with the same id than slide 2 because it is a second part (part number 1.1) of the same slide
        # Parts of a same slide will be displayed vertically in the presentation while different ids are displayed horizontally
        slide2part1 = Slide(2, 'slide2-1', 1.1)
        slide2part1.setContent('This part is 1.1')

        # The content is not defined, it will be automatically generated using the title of the slide
        # content is not defined for this slide, it will automatically generated based on its title
        slide3version0_1 = Slide(3, 'slide3', version=0.1)

        slide3version1 = Slide(3, 'slide3', version=1)
        slide3version1.setContent('This is version1 of Slide3')

        # Add slides to Slides
        slides = Slides()
        slides.addSlide(slide1)
        slides.addSlide(slide2part0)
        slides.addSlide(slide2part1)
        slides.addSlide(slide3version0_1)
        slides.addSlide(slide3version1)

        # if slides embed images from imageFolder in their markdown content, the following line is required:
        # slides.declareResources(imageFolder):

        # Define versions of presentation to create
        # slides does not need to all have the same version. The presentation will find the closest version of slide less than the requested version if not found
        versions = [0, 0.1, 1]

        # Create Presentation based on Slides in the current working directory
        presentation = Presentation()
        for version in versions:
            presentation.createPresentation('presentation_v{}.html'.format(
                version), slides, version=version, outputFolder=self.temp_dir.name)

