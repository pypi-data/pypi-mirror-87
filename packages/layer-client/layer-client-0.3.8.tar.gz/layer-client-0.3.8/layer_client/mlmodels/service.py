import importlib
import inspect
import sys
from logging import Logger
from typing import Any, Optional, Tuple

from mlflow.models.signature import infer_signature

from layer_client.exceptions import LayerClientException
from layer_client.mlmodels import ModelObject, flavors
from layer_client.mlmodels.flavors.model_definition import ModelDefinition

from ..api.entity.model_pb2 import Model  # pylint: disable=unused-import
from ..api.value.schema_column_pb2 import SchemaColumn
from ..api.value.schema_pb2 import Schema
from ..api.value.signature_pb2 import Signature
from .flavors import ModelFlavor


class MLModelService:
    """
    Handles ML model lifecycle within the application. Users of this service can
    store/load/delete ML models.
    """

    def __init__(self, logger: Logger):
        self.logger = logger

    def log_metric(self, notebook_id: str, key: str, value: float) -> None:
        pass

    # pytype: disable=annotation-type-mismatch # https://github.com/google/pytype/issues/640
    def store(
        self,
        model_definition: ModelDefinition,
        model_object: ModelObject,
        model_input: Any,
        model_output: Any,
        flavor: ModelFlavor,
    ) -> None:  # pytype: enable=annotation-type-mismatch
        """
        Stores given model object along with its definition to the backing storage.
        The metadata written to db and used later on whilst loading the ML model.

        Args:
            model_definition: Model metadata object which describes the model instance
            model_object: Model object to be stored
            model_input: Model input (training) data
            model_output: Model output (prediction) data
            flavor: Corresponding flavor information of the model object
        """
        self.logger.debug(
            f"Saving user model {model_definition.model_name}({model_object})"
        )
        try:
            self.logger.debug(f"Writing model {model_definition}")
            flavor.save(model_definition, model_object)
            self.logger.debug(
                f"User model {model_definition.model_name} saved successfully"
            )
        except Exception as ex:
            raise LayerClientException(f"Error while storing model, {ex}")

    def get_model_signature(self, model_input, model_output) -> Any:
        if model_input is None and model_output is not None:
            raise LayerClientException(
                "Model input not found! Model output can be assigned only if model input is assigned"
            )
        if model_input is not None:

            def map_signature_columns(cols):
                return list(
                    map(
                        lambda col: SchemaColumn(name=col.name, type=col.type.value),
                        cols,
                    )
                )

            signature = infer_signature(model_input, model_output)
            input_columns = map_signature_columns(signature.inputs.columns)
            output_columns = (
                map_signature_columns(signature.outputs.columns)
                if signature.outputs is not None
                else None
            )
            return Signature(
                input_schema=Schema(columns=input_columns),
                output_schema=Schema(columns=output_columns),
            )
        return None

    def retrieve(self, model_definition: ModelDefinition) -> ModelObject:
        """
        Retrieves the given model definition from the storage and returns the actual
        model object

        Args:
            model_definition: Model metadata object which describes the model instance
        Returns:
            Loaded model object

        """
        self.logger.debug(
            f"User requested to load model {model_definition.model_name} "
        )
        flavor: ModelFlavor = self.get_model_flavor_from_proto(
            model_definition.proto_flavor
        )

        self.logger.debug(f"Loading model {model_definition.model_name}")
        module = importlib.import_module(flavor.metadata.module_name)
        model_flavor_class = getattr(module, flavor.metadata.class_name)
        return model_flavor_class().load(model_definition=model_definition)

    def delete(self, model_definition: ModelDefinition) -> None:
        """
        Deletes the model along with its metadata from the storage

        Args:
            model_definition: Model metadata object which describes the model instance
        """
        self.logger.debug(
            f"User requested to delete model {model_definition.model_name}"
        )

    @staticmethod
    def get_model_flavor(
        model_object: ModelObject,
    ) -> Tuple["Model.ModelFlavor", ModelFlavor]:
        """
        Checks if given model objects has a known model flavor and returns
        the flavor if there is a match.

        Args:
            model_object: User supplied model object

        Returns:
            The corresponding model flavor if there is match

        Raises:
            LayerException if user provided object does not have a known flavor.

        """
        flavor = MLModelService.__check_and_get_flavor(model_object)
        if flavor is None:
            raise LayerClientException(f"Unexpected model type {type(model_object)}")
        return flavor

    @staticmethod
    def get_model_flavor_from_proto(proto_flavor: "Model.ModelFlavor") -> ModelFlavor:
        if proto_flavor not in flavors.PROTO_TO_PYTHON_OBJECT_FLAVORS:
            raise LayerClientException(f"Unexpected model flavor {type(proto_flavor)}")
        return flavors.PROTO_TO_PYTHON_OBJECT_FLAVORS[proto_flavor]

    @staticmethod
    def __check_and_get_flavor(
        model_object: ModelObject,
    ) -> Optional[Tuple["Model.ModelFlavor", ModelFlavor]]:
        module = MLModelService.__get_module_name(model_object)
        possible_flavor = flavors.MODULE_TO_PYTHON_FLAVORS[module]
        if possible_flavor is None:
            return None
        if not possible_flavor.can_interpret_object(model_object):
            return None
        flavor_name = type(possible_flavor).__name__
        proto_flavor = flavors.PYTHON_CLASS_NAME_TO_PROTO_FLAVORS[flavor_name]
        return proto_flavor, possible_flavor

    @staticmethod
    def __get_module_name(
        model_object: ModelObject,
    ) -> str:
        base_class = (
            model_object.__class__.__bases__[0]
            if model_object.__class__.__bases__[0].__name__ != "object"
            else model_object
        )
        module = inspect.getmodule(base_class)
        base, _sep, _stem = module.__name__.partition(".")
        # Special case for keras as it is lives inside the tensorflow package.
        if "keras" in _stem:
            base = "keras"
        return sys.modules[base].__name__
