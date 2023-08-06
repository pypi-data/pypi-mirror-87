from enum import Enum
from io import BytesIO
from typing import Optional

import os

import pandas as pd
import pandavro

from maquette_lib.__client import Client
from maquette_lib.__user_config import UserConfiguration

client = Client.from_config(UserConfiguration('/home'))


class EAuthorizationType(str, Enum):
    USER = "user"
    ROLE = "role"
    WILDCARD = "*"


class EProjectPrivilege(str, Enum):
    MEMBER = "member"
    PRODUCER = "producer"
    CONSUMER = "consumer"
    ADMIN = "admin"


class EDatasetPrivilege(str, Enum):
    PRODUCER = "producer"
    CONSUMER = "consumer"
    ADMIN = "admin"


class EDataClassification(str, Enum):
    PUBLIC = "public"
    INTERNAL = "internal"
    CONFIDENTIAL = "confidential"
    RESTRICTED = "restricted"


class EDataVisibility(str, Enum):
    PUBLIC = "public"
    PRIVATE = "private"


class EPersonalInformation(str, Enum):
    NONE = "none"
    PERSONAL_INFORMATION = "pi"
    SENSITIVE_PERSONAL_INFORMATION = "spi"


class Administration:

    def __init__(self):
        pass

    @staticmethod
    def delete_token(name: str, for_user: str = None) -> str:
        status, resp = client.command(cmd='user token delete', args={
            'name': name,
            'for-user': for_user
        })
        if status == 200:
            return resp['output']
        else:
            raise RuntimeError('Ups! Something went wrong (ⓧ_ⓧ)\n'
                               'status code: ' + str(status) + ', content:\n' + resp)

    @staticmethod
    def renew_token(name: str, for_user: str = None) -> str:
        status, resp = client.command(cmd='user token renew', args={
            'name': name,
            'for-user': for_user
        })
        if status == 200:
            return resp['output']
        else:
            raise RuntimeError('Ups! Something went wrong (ⓧ_ⓧ)\n'
                               'status code: ' + str(status) + ', content:\n' + resp)

    @staticmethod
    def register_token(name: str, for_user: str = None) -> str:
        status, resp = client.command(cmd='user token register', args={
            'name': name,
            'for-user': for_user
        })
        if status == 200:
            return resp['output']
        else:
            raise RuntimeError('Ups! Something went wrong (ⓧ_ⓧ)\n'
                               'status code: ' + str(status) + ', content:\n' + resp)

    @staticmethod
    def tokens() -> pd.DataFrame:
        status, resp = client.command('user tokens')
        if status == 200:
            table_df = pd.json_normalize(resp)
            return table_df
        else:
            raise RuntimeError('Ups! Something went wrong (ⓧ_ⓧ)\n'
                               'status code: ' + str(status) + ', content:\n' + resp)


class DatasetVersion:
    __project: str = None

    __dataset: str = None

    __version: str = None

    def __init__(self, dataset: str, version: str = "", project: str = None):
        self.__project = project
        self.__dataset = dataset
        self.__version = version

    def get(self) -> pd.DataFrame:
        ds = self.__dataset
        version = self.__version

        resp = client.get('data/datasets/' + ds + '/' + version)
        return pandavro.from_avro(BytesIO(resp.content))


class Dataset:
    __project: str = None

    __name: str = None

    def __init__(self, dataset_name: str, title: str = None, summary: str = "Lorem Impsum",
                 visibility: str = EDataVisibility.PUBLIC,
                 classification: str = EDataClassification.PUBLIC,
                 personal_information: str = EPersonalInformation.NONE,
                 project_name: str = None):

        self.__name = dataset_name
        if title:
            self.__title = title
        else:
            self.__title = dataset_name

        self.__summary = summary
        self.__visibility = visibility
        self.__classification = classification
        self.__personal_information = personal_information
        self.__project = project_name

    def create(self) -> 'Dataset':
        client.command(cmd='datasets create',
                       args={'name': self.__name, 'title': self.__title, 'summary': self.__summary,
                             'visibility': self.__visibility, 'classification': self.__classification,
                             'personalInformation': self.__personal_information},
                       headers={'x-project': self.__project})
        return self


    def grant(self, grant: EDatasetPrivilege, to_auth: EAuthorizationType, to_name: str = None) -> 'Dataset':
        client.command(cmd='dataset grant', args={
            'dataset': self.__name,
            'project': self.__project,
            'privilege': grant.value,
            'authorization': to_auth.value,
            'to': to_name
        })

        return self

    def revoke(self, revoke: EDatasetPrivilege, auth: EAuthorizationType, from_name: str = None) -> 'Dataset':
        client.command(cmd='dataset revoke', args={
            'dataset': self.__name,
            'project': self.__project,
            'privilege': revoke.value,
            'authorization': auth.value,
            'from': from_name
        })

        return self

    def print(self):
        resp = client.command(cmd='datasets get', args={'dataset': self.__name, 'project': self.__project})
        print(resp[1])
        return self

    def put(self, data: pd.DataFrame, short_description: str) -> DatasetVersion:
        ds: str = self.__name

        file: BytesIO = BytesIO()
        pandavro.to_avro(file, data)
        file.seek(0)

        resp = client.post('data/datasets/' + ds, files={
            'message': short_description,
            'file': (short_description, file, 'avro/binary', {'Content-Type': 'avro/binary'})
        }, headers={'Accept': 'application/csv', 'x-project': self.__project})

        return self.version(resp.json())

    def revisions(self, to_csv=False) -> pd.DataFrame:
        if to_csv:
            resp = client.command(cmd='datasets revisions list',
                                  args={'dataset': self.__name, 'project': self.__project},
                                  headers={'Accept': 'application/csv'})
        else:
            resp = client.command(cmd='datasets revisions list',
                                  args={'dataset': self.__name, 'project': self.__project})
        return resp[1]

    def version(self, version: Optional[str] = ""):
        return DatasetVersion(self.__name, version, self.__project)

    def __str__(self):
        resp = client.command(cmd='datasets get', args={'dataset': self.__name, 'project': self.__project})
        return resp[1]

    def __repr__(self):
        return self.__str__()


class Project:
    __name: str = None
    __title: str = None

    def __init__(self, name: str, title: str = None):
        # TODO:  self.__name = generate_unique_name(title)
        self.__name = name
        if title:
            self.__title = title
        else:
            self.__title = name

    def create(self) -> 'Project':
        client.command(cmd='projects create', args={'title': self.__title, 'name': self.__name})
        return self

    def datasets(self) -> pd.DataFrame:
        resp = client.command(cmd='project datasets', args={'project': self.__name})
        return resp['data'][0]

    def dataset(self, dataset_name: str = None, dataset_title: str = None, summary: str = None,
                visibility: str = None, classification: str = None, personal_information: str = None) -> Dataset:
        args = [arg for arg in
                [dataset_name, dataset_title, summary, visibility, classification, personal_information] if
                arg]
        return Dataset(project_name=self.__name, *args, )

    def grant(self, grant: EProjectPrivilege, to_auth: EAuthorizationType, to_name: str = None) -> 'Project':
        client.command(cmd='project grant', args={
            'project': self.__name,
            'privilege': grant.value,
            'authorization': to_auth.value,
            'to': to_name
        })

        return self

    def revoke(self, grant: EProjectPrivilege, to_auth: EAuthorizationType, to_name: str = None) -> 'Project':
        client.command(cmd='project revoke', args={
            'project': self.__name,
            'privilege': grant.value,
            'authorization': to_auth.value,
            'from': to_name
        })

        return self

    def print(self) -> 'Project':
        resp = client.command(cmd='project get', args={'project': self.__name}, headers={'Accept': 'text/plain'})
        print(resp)
        return self

    def __str__(self):
        resp = client.command(cmd='project get', args={'project': self.__name}, headers={'Accept': 'text/plain'})
        return resp

    def __repr__(self):
        return self.__str__()


def admin() -> Administration:
    return Administration()


def project(name: str) -> Project:
    return Project(name=name)

def dataset(dataset_name: str = None, dataset_title: str = None, summary: str = None,
                visibility: str = None, classification: str = None, personal_information: str = None) -> Dataset:
    args = [arg for arg in
                [dataset_title, summary, visibility, classification, personal_information] if
                arg]
    return Dataset(dataset_name=dataset_name, project_name=os.environ.get('MQ_PROJECT_NAME', 'Project_42'), *args)

def datasets(name: str, to_csv=False) -> pd.DataFrame:
    if to_csv:
        resp = client.command(cmd='datasets list', args={'project': name}, headers={'Accept': 'application/csv'})
    else:
        resp = client.command(cmd='datasets list', args={'project': name})
    return resp[1]


def projects(to_csv=False) -> pd.DataFrame:
    if to_csv:
        resp = client.command(cmd='datasets list', headers={'Accept': 'application/csv'})
    else:
        resp = client.command(cmd='projects list')
    return resp[1]
