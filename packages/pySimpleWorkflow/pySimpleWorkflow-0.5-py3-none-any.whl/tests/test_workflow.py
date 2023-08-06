import unittest
import logging
import sys
import pandas as pd
from pySimpleWorkflow.workflow import Workflow


class testWorkflow(unittest.TestCase):

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

    def test_wkf(self):
        workflow: Workflow = Workflow(pd.read_csv('tests/resources/workflow.csv'), 'myWorkflow')
        workflow.printStatusPerStep()

    