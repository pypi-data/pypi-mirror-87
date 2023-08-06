# Workflow module

## Description

The Workflow module manages a sequence, ie a list of steps which are linked together in a sequential way.  
To define such a sequence, create a table in excel or csv file with columns named:
- stepId
- title
- nexts

**stepId** is the unique step identifier,  
**title** is an arbitrary name of the step,  
**nexts** is a list of stepIds that follows the step. The list is given by stepIds separated with '-' .

Here is an example:  

|stepId|title|nexts|
|---|:---:|---:|
|1|my first step|2-3|
|2|my second step|4|
|3|step 3!|12|
|4|step4||
|9|step9|12-4|
|12|step12||
  
In this example, steps 1 and 9 are the first steps in the workflow because the don't have any previous step.  
Steps 4 and 12 are the last steps because they don't have any next step.  
- Step 1 points to 2 next steps: steps 2 and 3,
- Step 2 points to step 4, ...  


As we can see, there is no need to define a continuous suite fo stepIds and the identifiers don't need to be sorted. 

## Basic call example
```python
import pandas as pd
from pycroaktools.workflow.workflow import Workflow
workflow = Workflow(pd.read_csv('workflow.csv'), 'myWorkflow') #read_csv may be replaced by read_excel
paths = workflow.getAllPaths()
for path in paths:
    for step in path:
        print(step.stepId)
```