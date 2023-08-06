import os
import sys
import logging
from webbrowser import open as webopen
from pandas import read_csv
import distutils.dir_util as dirutil
import pyBaseApp.applauncher as launcher
from pyRevealjs import SlideCatalog
from pyRevealjs import PresentationSettings
from pySimpleWorkflow import Workflow
from pyWorkflowRevealjs.slidesToWorkflow import SlidesToWorkflow
from pyWorkflowRevealjs.workflowToPresentation import WorkflowToPresentation


class Generator(launcher.Settings):
    """
    The Generator class generates presentations either based on a workflow, on a list of images, a list of markdown slides or all together.
    It inherits from pyWorkflowRevealjs.applauncher.settings.Settings that manages the settings.
    """

    def __init__(self, settings: dict):
        """
        builds the class according to the settings dictionary.
        Parameters
        ----------
        settings : dictionary that may contain the following key and values

        - slideFolder: folder that contains markdown files. 
        These files define either a slide thanks to their name or thanks to their header.
        See class Slides to get more details about the header.

        - imageFolder: folder that contains images. These images define either their own slide if the image name complies 
        with the slide definition (see class Slides) or may be called by a markdown file.

        - outputFolder: folder where the presentation is created. If none is provided, the current working directory
        (from where the app is launched) is used.

        - workflowFile: csv file defining the workflow. See class Workflow for a description of this csv file

        - createFlowchart: if True, a graphical representation of the workflow is generated

        - createLinearPresentations: if True, each possible path defined by the workflow generates an individual presentation. 
        Then Each slide has only one next slide. This is a linear sequence from first to last slide.

        - createWorkflowPresentation: if True, a unique presentation is generated to represent the workflow. 
        Each slide may have multiple next slides. Then links give choices to follow a path or another in the workflow

        - displayTitles: if true, each slide displays its title
        """

        self.slideFolder = None
        self.imageFolder = None
        self.outputFolder = os.getcwd()
        self.workflowFile = None
        self.versions = [0.]
        self.createFlowchart = False
        self.createLinearPresentations = False
        self.createWorkflowPresentation = True
        self.displayTitles = False
        self.theme = None
        self.title = None
        self.setProperties(settings)

        self._build()

    def _build(self):
        slides = self._manageSlides()
        self._manageImages(slides)
        workflow = self._manageWorkflow(slides)
        self._manageMissingSlides(slides, workflow)
        pres = self._generate(workflow, slides, self._generateGeneralSettings())
        self.open(pres)

    def open(self, filename):
        if not filename:
            return
        new = 2
        logging.info('presentation available at {}'.format(filename))
        url = "file:///"+os.path.realpath(filename)
        logging.info('opening presentation at url {}'.format(url))
        webopen(url, new=new)

    def _generateGeneralSettings(self):
        settings = PresentationSettings()
        if self.title:
            settings.title = self.title 
        if self.theme:
            settings.theme = self.theme
        return settings

    def _manageImages(self, catalog: SlideCatalog):
        if not self.imageFolder:
            return
        catalog.catalog(self.imageFolder, images=True)

    def _manageSlides(self):
        catalog = SlideCatalog()
        if self.slideFolder:
            catalog.catalog(self.slideFolder)
        else:
            self.slideFolder = os.path.join(self.outputFolder, 'slides')

        return catalog

    def _manageWorkflow(self, catalog: SlideCatalog):
        if self.workflowFile:
            try:
                return Workflow(read_csv(
                    self.workflowFile), os.path.basename(self.workflowFile)[:-4])
            except FileNotFoundError:
                launcher.error('file {} not found'.format(self.workflowFile))

        if not catalog.getDefaultSlideOrder():
            launcher.error('no workflow or slide found')

        return Workflow(SlidesToWorkflow().create(catalog), 'presentation')

    def _manageMissingSlides(self, catalog: SlideCatalog, workflow: Workflow):
        catalog.createMissingSlides(
            [step.stepId for step in workflow.getSteps()])

    def _generate(self, workflow: Workflow, catalog: SlideCatalog, settings: PresentationSettings):
        toPres = WorkflowToPresentation(
            workflow, catalog, self.outputFolder)

        presentation = None
        for version in self.versions:
            logging.info('version {} ...'.format(version))
            if self.createLinearPresentations:
                presentation = toPres.createLinearPresentations(version, settings)
            if self.createWorkflowPresentation:
                presentation = toPres.createWorkflowPresentation(version, settings)
        return presentation
