import re
import unicodedata

from ...api.entity.model_pb2 import Model
from ...api.value.aws_credentials_pb2 import AwsCredentials
from ...api.value.s3_path_pb2 import S3Path


class ModelDefinition:
    """Holds information regarding an ML model.

    This class holds structural information about an ML Model and is able to
    construct a path where you can find the model in the storage.
    """

    def __init__(
        self,
        model_name: str,
        credentials: AwsCredentials,
        s3_path: S3Path,
        proto_flavor=None,
    ):
        self.__model_name = slugify(model_name).replace("-", "")
        self.__s3_path = s3_path
        self.__credentials = credentials
        self.__proto_flavor = proto_flavor

    @property
    def model_name(self) -> str:
        """Returns the model name

        Returns:
            A string name
        """
        return self.__model_name

    @property
    def s3_path(self) -> S3Path:
        """Returns the s3 path where the model stored

        Returns:
            the s3 path where the model stored
        """
        return self.__s3_path

    @property
    def credentials(self) -> AwsCredentials:
        """Returns the credentials object for this model

        Returns:
            the credentials object for this model
        """
        return self.__credentials

    @property
    def proto_flavor(self) -> Model.ModelFlavor:
        """Returns the proto flavor

        Returns:
            A string - the proto flavor
        """
        return self.__proto_flavor

    def __repr__(self) -> str:
        return (
            f"ModelDefinition{{"
            f"model_name:{self.model_name}"
            f"s3_path:{self.s3_path}"
            f"proto_flavor:{self.proto_flavor}"
            f"}}"
        )


def slugify(value, allow_unicode=False):
    """
    Convert to ASCII if 'allow_unicode' is False. Convert spaces to hyphens.
    Remove characters that aren't alphanumerics, underscores, or hyphens.
    Convert to lowercase. Also strip leading and trailing whitespace.

    Taken unchanged from django/utils/text.py
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize("NFKC", value)
    else:
        value = (
            unicodedata.normalize("NFKD", value)
            .encode("ascii", "ignore")
            .decode("ascii")
        )
    value = re.sub(r"[^\w\s-]", "", value).strip().lower()
    return re.sub(r"[-\s]+", "-", value)
