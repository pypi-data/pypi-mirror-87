from typing import Optional

from pydantic import UUID4, BaseModel

from tktl.core.t import DeploymentStatesT


class DeploymentBase(BaseModel):
    id: Optional[UUID4] = None
    git_branch: str = None
    git_hash: str = None
    requester_id: UUID4 = None
    repository_id: UUID4 = None
    repo_ref_id: int
    status_id: UUID4 = None
    ecr_repo_url: str


# Properties to receive on item update
class DeploymentUpdate(DeploymentBase):
    status_name: DeploymentStatesT
