from abc import ABCMeta, abstractmethod
from typing import Any, NamedTuple

from mlflow.utils.file_utils import TempDir

from .. import ModelObject
from .model_definition import ModelDefinition
from .s3 import S3Util


class ModelFlavorMetaData(NamedTuple):
    """NamedTuple containing flavor module and class names"""

    module_name: str
    class_name: str


class ModelFlavor(metaclass=ABCMeta):
    """Represents a machine learning model flavor for a specific framework.

    Implementations provide methods for checking for membership, saving and loading
    of machine learning models within their flavor.
    """

    @abstractmethod
    def model_class(self) -> type:
        """Defines the class that this Model Flavor uses to check for compatibility.

        Returns:
            type: A class reference of the model type to check for.
        """

    @abstractmethod
    def log_model_impl(self) -> Any:
        """Defines the method that this Model Flavor uses to log(/store) a model.

        Returns:
             A method reference of the model log implementation.
        """

    @abstractmethod
    def load_model_impl(self) -> Any:
        """Defines the method that this Model Flavor uses to load a model.

        Returns:
             A method reference of the model loader implementation.
        """

    def can_interpret_object(self, model_object: ModelObject) -> bool:
        """Checks whether supplied model object has flavor of this class.

        Args:
            model_object: A machine learning model which could be originated from any framework.

        Returns:
            bool: true if this ModelFlavor can interprete the given model instance.
        """
        return isinstance(model_object, self.model_class())

    def save(
        self,
        model_definition: ModelDefinition,
        model_object: ModelObject,
    ) -> None:
        """Stores the given machine learning model definition to the backing store.

        Args:
            model_definition: Model metadata object which describes the model instance
            model_object: A machine learning model which could be originated from any framework
        """
        model_impl = self.log_model_impl()
        with TempDir() as tmp:
            local_path = tmp.path("model")
            model_impl(model_object, path=local_path)
            S3Util.upload_folder(
                local_dir=local_path, model_definition=model_definition
            )

    def load(self, model_definition: ModelDefinition) -> ModelObject:
        """Loads the given machine learning model definition from the backing store and
        returns an instance of it

        Args:
            model_definition: Model metadata object which describes the model instance

        Returns:
            A machine learning model object
        """
        with TempDir() as tmp:
            local_path = tmp.path("model")
            S3Util.download_folder(
                local_dir=local_path, model_definition=model_definition
            )
            model_impl = self.load_model_impl()
            return model_impl(f"file://{local_path}")

    @property
    def metadata(self) -> ModelFlavorMetaData:
        """Returns metadata which contains flavor module and classname to be used when loading an instance of a flavor

        Returns:
            ModelFlavorMetaData: a metadata dict
        """
        return ModelFlavorMetaData(
            module_name=self.__module__, class_name=self.__class__.__qualname__
        )


class SparkMLModelFlavor(ModelFlavor):
    """Spark ML Model flavor implementation which handles persistence of ML models in `pyspark.ml` package."""

    def model_class(self) -> type:
        from pyspark.ml.util import MLWritable

        return MLWritable

    def log_model_impl(self) -> Any:
        import mlflow.spark

        return mlflow.spark.save_model

    def load_model_impl(self) -> Any:
        import mlflow.spark

        return mlflow.spark.load_model


class ScikitLearnModelFlavor(ModelFlavor):
    """An ML Model flavor implementation which handles persistence of Scikit Learn Models."""

    def model_class(self) -> type:
        from sklearn.base import BaseEstimator  # type: ignore

        return BaseEstimator

    def log_model_impl(self) -> Any:
        import mlflow.sklearn

        return mlflow.sklearn.save_model

    def load_model_impl(self) -> Any:
        import mlflow.sklearn

        return mlflow.sklearn.load_model


class PyTorchModelFlavor(ModelFlavor):
    """An ML Model flavor implementation which handles persistence of PyTorch Models."""

    def model_class(self) -> type:
        import torch  # type: ignore

        return torch.nn.Module

    def log_model_impl(self) -> Any:
        import mlflow.pytorch

        return mlflow.pytorch.save_model

    def load_model_impl(self) -> Any:
        import mlflow.pytorch

        return mlflow.pytorch.load_model


class XGBoostModelFlavor(ModelFlavor):
    """An ML Model flavor implementation which handles persistence of XGBoost Models.

    Uses XGBoost model (an instance of xgboost.Booster).

    """

    def model_class(self) -> type:
        import xgboost  # type: ignore

        return xgboost.Booster

    def log_model_impl(self) -> Any:
        import mlflow.xgboost

        return mlflow.xgboost.save_model

    def load_model_impl(self) -> Any:
        import mlflow.xgboost

        return mlflow.xgboost.load_model


class LightGBMModelFlavor(ModelFlavor):
    """An ML Model flavor implementation which handles persistence of LightGBM Models.
    Uses LightGBM model (an instance of lightgbm.Booster).

    """

    def model_class(self) -> type:
        import lightgbm  # type: ignore

        return lightgbm.Booster

    def log_model_impl(self) -> Any:
        import mlflow.lightgbm

        return mlflow.lightgbm.save_model

    def load_model_impl(self) -> Any:
        import mlflow.lightgbm

        return mlflow.lightgbm.load_model


class TensorFlowModelFlavor(ModelFlavor):
    """An ML Model flavor implementation which handles persistence of TensorFlow Models."""

    def save(
        self,
        model_definition: ModelDefinition,
        model_object: ModelObject,
    ) -> None:
        """See ModelFlavor.save()'s documentation.

        Due to peculiar arguments required for mlflow.tensorflow.save_model, we need to duplicate a lot of code here.

        TODO: Refactor this
        """
        import tensorflow  # type: ignore

        model_impl = self.log_model_impl()

        with TempDir() as tmp:
            local_path = tmp.path("model")
            tmp_save_path = tmp.path(model_definition.model_name)
            tensorflow.saved_model.save(model_object, tmp_save_path)
            model_impl(
                tf_saved_model_dir=tmp_save_path,
                tf_meta_graph_tags=None,
                tf_signature_def_key="serving_default",
                path=local_path,
            )
            S3Util.upload_folder(
                local_dir=local_path, model_definition=model_definition
            )

    def model_class(self) -> type:
        import tensorflow  # type: ignore

        return tensorflow.Module

    def log_model_impl(self) -> Any:
        import mlflow.tensorflow

        return mlflow.tensorflow.save_model

    def load_model_impl(self) -> Any:
        import mlflow.tensorflow

        return mlflow.tensorflow.load_model


class KerasModelFlavor(ModelFlavor):
    """An ML Model flavor implementation which handles persistence of Keras Models."""

    def model_class(self) -> type:
        import keras  # type: ignore

        return keras.models.Sequential

    def log_model_impl(self) -> Any:
        import mlflow.keras

        return mlflow.keras.save_model

    def load_model_impl(self) -> Any:
        import mlflow.keras

        return mlflow.keras.load_model
