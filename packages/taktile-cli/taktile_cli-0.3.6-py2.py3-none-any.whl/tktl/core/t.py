from typing import Union

from tktl.core import ExtendedEnum
from tktl.core.schemas.repository import Endpoint, Repository, RepositoryDeployment


class UserRepoConfigFileNameT(str, ExtendedEnum):
    YAML = "tktl.yaml"
    YML = "tktl.yml"


class UserProjectFileT(str, ExtendedEnum):
    FILE = "file"
    DIRECTORY = "dir"


class RequiredUserProjectPathsT(str, ExtendedEnum):
    SRC = "src"
    TKTL_YML = "tktl.yml"
    TKTL_YAML = "tktl.yaml"
    DOCKERFILE = ".buildfile"
    REQS = "requirements.txt"

    @classmethod
    def strictly_required_files(cls):
        return {cls.DOCKERFILE.value, cls.REQS.value}

    @classmethod
    def strictly_required_dirs(cls):
        return {cls.SRC.value}


class DeploymentStatesT(str, ExtendedEnum):
    PRE_ORION_UNKNOWN_ERROR = "errored"
    TEST_FAILED = "test_failed"
    IMAGE_BUILD_FAILED = "image_build_failed"
    DEPLOYMENT_FAILED = "deployment_failed"
    CANCELED = "canceled"
    SUCCEEDED = "succeeded"
    TEST_RUNNING = "test_running"
    IMAGE_BUILDING = "image_building"
    DEPLOYING = "deploying"
    MARKED_FOR_DELETION = "marked_for_deletion"
    DELETION_FAILED = "deletion_failed"


class ProjectAssetT(str, ExtendedEnum):
    DATA = "data"
    MODEL = "model"


class ProjectAssetSourceT(str, ExtendedEnum):
    S3 = "s3"
    LOCAL = "local"
    LFS = "lfs"


class InstanceTypeT(str, ExtendedEnum):
    GP_SMALL = "gp.small"
    GP_MEDIUM = "gp.medium"
    GP_LARGE = "gp.large"
    GP_XLARGE = "gp.xlarge"
    GP_2XLARGE = "gp.2xlarge"


class ServiceT(str, ExtendedEnum):
    REST = "rest"
    GRPC = "grpc"


class EndpointKinds(str, ExtendedEnum):
    CUSTOM = "custom"
    TABULAR = "tabular"
    BINARY = "binary"
    REGRESSION = "regression"
    MULTICLASS = "multiclass"


class RestSchemaTypes(ExtendedEnum):
    DICT = "Dict"
    SEQUENCE = "Sequence"
    ARRAY = "Array"
    FLAT_ARRAY = "FlatArray"
    SERIES = "Series"
    DATAFRAME = "DataFrame"
    SINGLE_VALUE = "SingleValue"
    CUSTOM_MODEL = "CustomModel"


Resources = Union[Repository, RepositoryDeployment, Endpoint]
