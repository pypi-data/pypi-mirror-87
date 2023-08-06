import unittest
import tempfile
import logging
import sys
from pyWorkflowRevealjs import Generator


class TestGenerator(unittest.TestCase):

    def setUp(self):
        root = logging.getLogger()
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(filename)s - %(lineno)d - %(message)s')
        root.setLevel(logging.DEBUG)

        # console
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(formatter)
        root.addHandler(console_handler)

        logging.info('logger initialised')
    def test_generator(self):

        with tempfile.TemporaryDirectory() as temp_dir:
            settings = {'workflowFile': 'tests/resources/workflow.csv', 'imageFolder': 'tests/resources/images', 'outputFolder': 'temp_dir',
                        'slideFolder': 'tests/resources/slides', 'versions': [0, 1], 'createLinearPresentations': True, 'createWorkflowPresentation': True, 'theme': 'white'}

            Generator(settings)
