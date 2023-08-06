from datetime import datetime
from typing import Dict, List, Optional, Union

import certifi
from beautifultable import BeautifulTable
from pydantic import UUID4, BaseModel

from tktl.core import ExtendedEnum
from tktl.core.utils import flatten


class AccessKind(str, ExtendedEnum):

    # see also corresponding AccessKind on t-api
    OWNER = "owner"
    VIEWER = "viewer"


class TablePrintableBaseModelMixin:
    def table_repr(self, subset: List[str] = None) -> Dict:
        ...


class Endpoint(BaseModel):
    id: Optional[UUID4] = None
    name: Optional[str] = None
    deployment_id: Optional[UUID4] = None

    def table_repr(self, subset=None):
        as_dict = self.dict()
        as_dict["Name"] = as_dict.pop("name")
        as_dict["Deployment ID"] = str(as_dict.pop("deployment_id"))
        return as_dict


class RepositoryDeployment(BaseModel, TablePrintableBaseModelMixin):
    id: UUID4
    created_at: datetime
    status: str
    public_docs_url: Optional[str]
    service_type: Optional[str]
    instance_type: Optional[str]
    replicas: Optional[int]
    branch_name: str
    major_version: int
    minor_version: int
    commit_hash: str
    endpoints: List[Endpoint]

    def table_repr(self, subset=None):
        endpoint_names = [e.name for e in self.endpoints]
        as_dict = self.dict(exclude={"service_type", "endpoints"})
        as_dict[
            "Branch @ Commit"
        ] = f"{as_dict.pop('branch_name')} @ {as_dict.pop('commit_hash')[0:7]}"
        as_dict["Status"] = as_dict.pop("status")
        as_dict["Endpoints"] = ", ".join(endpoint_names)
        as_dict["Created At"] = str(as_dict.pop("created_at"))
        as_dict[
            "Version"
        ] = f"{as_dict.pop('major_version')}.{as_dict.pop('minor_version')}"
        as_dict["Instance Type"] = as_dict.pop("instance_type")
        as_dict["Replicas"] = as_dict.pop("replicas")
        as_dict["REST Docs URL"] = _format_http_url(as_dict.pop("public_docs_url"))
        if subset:
            return {k: v for k, v in as_dict.items() if k in subset}
        return as_dict


class Repository(BaseModel, TablePrintableBaseModelMixin):
    id: UUID4
    ref_id: int
    repository_name: str
    repository_owner: str
    repository_description: Optional[str] = None
    access: AccessKind
    deployments: List[RepositoryDeployment]

    def table_repr(self, subset=None):
        deployment_ids = [str(e.id) for e in self.deployments]
        as_dict = self.dict(exclude={"ref_id", "deployments"})
        as_dict["Deployments"] = "\n".join(deployment_ids)
        as_dict["Access"] = f"{as_dict.pop('access').value}"
        as_dict[
            "Name"
        ] = f"{as_dict.pop('repository_owner')}/{as_dict.pop('repository_name')}"
        desc = as_dict.pop("repository_description")
        as_dict["Description"] = f"{desc[0:20] + '...' if desc else '-'}"
        if subset:
            return {k: v for k, v in as_dict.items() if k in subset}
        return as_dict


class RepositoryList(BaseModel):
    __root__: List[Repository]

    def get_repositories(self) -> List[Repository]:
        return flatten(
            [
                sum(
                    [
                        len(e.endpoints) if len(e.endpoints) > 0 else 1
                        for e in r.deployments
                    ]
                )
                * [r]
                for r in self.__root__
            ]
        )

    def get_endpoints(self) -> List[Endpoint]:
        return flatten(
            [
                flatten(
                    [
                        [e for e in d.endpoints] if d.endpoints else [Endpoint()]
                        for d in r.deployments
                    ]
                )
                for r in self.__root__
            ]
        )

    def get_deployments(self) -> List[RepositoryDeployment]:
        return flatten(
            flatten(
                [
                    (len(d.endpoints) if len(d.endpoints) > 0 else 1) * [d]
                    for d in r.deployments
                ]
                for r in self.__root__
            )
        )

    def __str__(self):
        table = BeautifulTable(maxwidth=250)
        rows = self.total_rows()
        table.columns.header = [
            "Repository",
            "Branch @ Commit",
            "Deployment Status",
            "REST Docs URL",
            "Version",
            "Created At",
            "Endpoint Name",
            "Endpoint ID",
        ]
        table.rows.header = [str(i) for i in range(rows)]
        table.columns[0] = [
            f"{r.repository_owner}/{r.repository_name}" for r in self.get_repositories()
        ]
        table.columns[1] = [
            f"{d.branch_name} @ {d.commit_hash}" for d in self.get_deployments()
        ]
        table.columns[2] = [f"{d.status}" for d in self.get_deployments()]
        table.columns[3] = [
            f"{_format_http_url(d.public_docs_url)}" for d in self.get_deployments()
        ]
        table.columns[4] = [
            f"{d.major_version}.{d.minor_version}" for d in self.get_deployments()
        ]
        table.columns[5] = [f"{d.created_at}" for d in self.get_deployments()]
        table.columns[6] = [e.name if e.name else "" for e in self.get_endpoints()]
        table.columns[7] = [e.id if e.id else "" for e in self.get_endpoints()]
        return table.__str__()

    def total_rows(self):
        return sum(
            [len([len(d.endpoints) for d in r.deployments]) for r in self.__root__]
        )


class ReportResponse(BaseModel):
    deployment_id: UUID4
    endpoint_name: str
    report_type: str
    chart_name: Optional[str] = None
    variable_name: Optional[str] = None
    value: Union[List, Dict]


def _format_http_url(url):
    return f"https://{url}" if (url and url != "UNAVAILABLE") else "UNAVAILABLE"


def _format_grpc_url(url):
    return f"grpc+tls://{url}:5005" if (url and url != "UNAVAILABLE") else "UNAVAILABLE"


def load_certs():
    with open(certifi.where(), "r") as cert:
        return cert.read()
