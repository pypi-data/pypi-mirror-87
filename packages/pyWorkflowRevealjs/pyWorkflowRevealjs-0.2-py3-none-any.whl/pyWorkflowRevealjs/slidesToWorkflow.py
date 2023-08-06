from pyRevealjs import Slides
from pandas import DataFrame


class SlidesToWorkflow:
    """
    The SlidesToWorkflow class builds a pandas workflow definition based on a linear sequence of slide ids.
    If the slide ids are ordered in a sequence such as [1, 2, 5, 9], then a workflow is created with this sequence.
    Each step has 1 next (1->2), (2->5), (5->9). The slide title defines the step title.
    """

    def create(self, slides: Slides):
        """
        create a pandas workflow definition from a Slides object
        ---Parameters:
        - slides: Slides object used to create a pandas workflow definition
        """
        slideIds = slides.getDefaultSlideOrder()

        titles = ["" for slideId in slides.slides]

        nexts = [slideIds[index+1]
                 for index, id in enumerate(slideIds) if index < len(slideIds)-1]
        nexts.append('')

        return DataFrame(
            {'stepId': slideIds, 'title': titles, 'nexts': nexts})
