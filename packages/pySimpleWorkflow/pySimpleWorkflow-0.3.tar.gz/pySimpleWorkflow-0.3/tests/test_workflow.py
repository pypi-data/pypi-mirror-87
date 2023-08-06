import unittest
import pandas as pd
from pySimpleWorkflow.workflow import Workflow


class testWorkflow(unittest.TestCase):

    def test_wkf(self):
        workflow = Workflow(pd.read_csv('tests/resources/workflow.csv'), 'myWorkflow')
        paths = workflow.getAllPaths()
        for path in paths:
            for step in path:
                print(step.stepId)