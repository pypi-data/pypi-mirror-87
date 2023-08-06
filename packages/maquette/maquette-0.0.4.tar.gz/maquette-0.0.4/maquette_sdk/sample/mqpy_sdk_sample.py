from maquette_sdk.__mq import EProjectPrivilege, EDatasetPrivilege, EAuthorizationType, EDataClassification, EDataVisibility, EPersonalInformation
import maquette_sdk
import pandas as pd

# Create Project
#maquette_sdk.Project('sample-project2').create()
#print(maquette_sdk.projects())

# add a dataset to a project
# maquette_sdk.dataset('another-dataset').create()

# upload data to the dataset
testdf = pd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})
dsv = maquette_sdk.dataset('another-dataset').put(testdf, "muahahaha")
# show a list of all datasets of a project
#print(maquette_sdk.datasets('sample-project',True))

# show a list of all revisions of a dataset
# print(maquette_sdk.project('sample-project').dataset('another-dataset').revisions(True))

#initialize a DatasetVersion from a Dataset
df = maquette_sdk.dataset('another-dataset').version().get()
print(df)
#

# get a dataset from a project
# df = maquette_sdk.project("sample-project").dataset('some-dataset').version("latest").get()
# print(df)
# remove a dataset from a project


### Access rights
#TODO integrate later