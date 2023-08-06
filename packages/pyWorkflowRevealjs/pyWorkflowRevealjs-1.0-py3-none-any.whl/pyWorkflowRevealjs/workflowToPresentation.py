from pyRevealjs import Presentation, SlideCatalog, PresentationSettings
from pySimpleWorkflow import Workflow


class WorkflowToPresentation:
    """
    The WorkflowToPresentation class builds a bridge between a defined workflow and a presentation.
    It generates presentations starting from this workflow and by matching Workflow data and Slides data.
    These presentations are versioned. The content evolve easily by requesting slide versions corresponding 
    to the expected presentation version.

    To do so, 2 functions are available : 
    - createLinearPresentations : each possible path defined by the workflow generates an individual presentation. 
    Then Each slide has only one next slide. This is a linear sequence from first to last slide.

    - createWorkflowPresentation: a unique presentation is generated to represent the workflow. Each slide may has multiple next slides. 
    Then links give choices to follow a path or another in the workflow

    """

    def __init__(self, workflow: Workflow, catalog: SlideCatalog, outputFolder):
        """
        Builds the object
        ---
        Parameters:
        - workflow: workflow definition
        - catalog: catalog of slides that should match the workflow
        - outputFolder: folder where the presentations are saved

        """
        self.workflow = workflow
        self.catalog = catalog
        self.outputFolder = outputFolder

    def _getPresNames(self, paths, version):
        presNames = []
        for path in paths:
            presName = self.workflow.name+'_v'+str(version)+'_'
            for step in path:
                presName += str(step.stepId)+'-'
            presNames.append(presName[:-1]+'.html')
        return presNames

    def createLinearPresentations(self, version, settings:PresentationSettings):
        """
        Each possible path defined by the workflow generates an individual presentation. 
        Then Each slide has only one next slide. This is a linear sequence from first to last slide.
        ---
        Parameters:
        - version: expected version of the presentation. Then this version of the slides is searched and if not
        found the previous one is used.
        """
        paths = self.workflow.getAllPaths()
        presNames = self._getPresNames(paths, version)

        for index, path in enumerate(paths):
            slideIds = [step.stepId for step in path]
            presentation = Presentation(presNames[index], self.catalog, settings)
            presentation.addSlideByIds(slideIds)
            file =presentation.save(self.outputFolder, version)

        return file

    def createWorkflowPresentation(self, version, settings: PresentationSettings):
        """
        A unique presentation is generated to represent the workflow. Each slide may has multiple next slides. 
        Then links give choices to follow a path or another in the workflow
        ---
        Parameters:
        - version: expected version of the presentation. Then this version of the slides is searched and if not
        found the previous one is used.
        """
        presName = self.workflow.name + '_v' + str(version)+'.html'
        links = self.workflow.getLinksPerSteps()

        pres = Presentation(presName, self.catalog, settings)
        pres.addSlideByIds(self.catalog.getAllIds())
        pres.addLinks(links)
        file = pres.save(self.outputFolder, version)
        return file
