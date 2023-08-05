# PyRevealjs module

**Note** Before using this module, have a look to the [pyWorkflowRevealjs](https://github.com/20centcroak/pyWorkflowRevealjs) module. It may be easier to use despite it requires more libraries (including this module).

## Description

The PyRevealjs module allows the easy creation of revealjs presentations from text, markdown or image files defining the slides.  
It is also possible to define slides direcly in code.

The goal is to be able to generate presentations with volatile content. 
Suppose you need to document a software thanks to screenshots and additional texts, you will need to update this presentation many times, but most often just in changing a screenshot.

The module not only recreates fastly a new presentation when the content changes but it can also manages different versions. 
Then you could have different versions of presentations if you need to document different versions of software.

The module also manages slide parts, then a slide may be decomposed in vertical parts and revealjs allows the vertical (slide parts) and horizontal (different slides) browsing in the presentation.

Finally the module manages links in presentation, then it is possible to jump from one slide to another thanks to these links. This option is easier managed with the easyPresentation module.

## Basic call examples

### The easy way: only using images
Image names should comply with this pattern *ID_title[_part][_version]* where :
- ID is a unique identifier (integer), ID may be not unique when part or version number differs
- title is an arbitrary title for the slide,
- part is an optional part number (to display slide parts vertically)
- version is an optional version number (to create presentation versions relative to slide or image versions)

Suppose that you have an image folder names *C:/temp/images* with the following images inside:
- 0_First image.jpg
- 1_First image.jpg
- 2_First image.jpg
- ... 

```python
from pyRevealjs import Slides, Presentation

#get slides from images
slides = Slides()
slides.catalog('C:/temp/images',images=True)

#Create Presentation based on Slides in the current working directory
Presentation().createPresentation('presentation.html', slides)
```

### A more complete example
```python
from pyRevealjs import Slide, Slides, SlideGenerator, Presentation

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

```