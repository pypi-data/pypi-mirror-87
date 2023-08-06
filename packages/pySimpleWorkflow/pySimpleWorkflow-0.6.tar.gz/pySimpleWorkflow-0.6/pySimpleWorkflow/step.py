class Step:
    """
    The Step class defines a step in a workflow. 
    It may be seen as a node in a graph with oriented edges: previous and next steps.
    Since a workflow is an oriented graph, step may be defined as first (ie without previous step)
    or last (ie wihtout next step)
    """

    def __init__(self, stepId: int, title=None):
        """
        Builds the object.
        ---
        Parameters:
        - stepId: unique id for a step in a workflow
        """
        self.stepId = stepId
        """ id of the step"""
        self.nexts = dict()
        """dictionary with keys = id of next steps and values = next steps as Step object"""
        self.previouses = dict()
        """dictionary with keys = id of previous steps and values = previous steps as Step object"""
        self.title = title if title else 'step '+str(stepId)

    def getNexts(self):
        """
        get list of ids correponding to next steps
        """
        return list(self.nexts.values())

    def getPreviouses(self):
        """
        get list of ids correponding to previous steps
        """
        return list(self.previouses.values())

    def addNext(self, nextStep):
        """
        add a next step to the nexts dictionary. Doing that, it adds this step as previous to the given nextStep
        ---
        Parameters:
        - nextStep: next step as Step object
        """
        if nextStep.stepId not in self.nexts:
            self.nexts[nextStep.stepId] = nextStep
        if self.stepId not in nextStep.previouses:
            nextStep.previouses[self.stepId] = self

    def isFirst(self):
        """
        tells if this step is first in a workflow (returns True), it means that it does not have any previous step
        """
        return not self.previouses

    def isLast(self):
        """
        tells if this step is last in a workflow (returns True), it means that it does not have any next step
        """
        return not self.nexts
