from typing import Dict

from ...api.entity.model_pb2 import Model
from .flavor import (
    KerasModelFlavor,
    LightGBMModelFlavor,
    ModelFlavor,
    PyTorchModelFlavor,
    ScikitLearnModelFlavor,
    SparkMLModelFlavor,
    TensorFlowModelFlavor,
    XGBoostModelFlavor,
)


PROTO_TO_PYTHON_OBJECT_FLAVORS: Dict["Model.ModelFlavor", ModelFlavor] = {
    Model.ModelFlavor.Value("MODEL_FLAVOR_PYTORCH"): PyTorchModelFlavor(),
    Model.ModelFlavor.Value("MODEL_FLAVOR_SPARK"): SparkMLModelFlavor(),
    Model.ModelFlavor.Value("MODEL_FLAVOR_SKLEARN"): ScikitLearnModelFlavor(),
    Model.ModelFlavor.Value("MODEL_FLAVOR_XGBOOST"): XGBoostModelFlavor(),
    Model.ModelFlavor.Value("MODEL_FLAVOR_LIGHTGBM"): LightGBMModelFlavor(),
    Model.ModelFlavor.Value("MODEL_FLAVOR_KERAS"): KerasModelFlavor(),
    Model.ModelFlavor.Value("MODEL_FLAVOR_TENSORFLOW"): TensorFlowModelFlavor(),
}

PYTHON_CLASS_NAME_TO_PROTO_FLAVORS: Dict[str, "Model.ModelFlavor"] = {
    PyTorchModelFlavor.__name__: Model.ModelFlavor.Value("MODEL_FLAVOR_PYTORCH"),
    SparkMLModelFlavor.__name__: Model.ModelFlavor.Value("MODEL_FLAVOR_SPARK"),
    ScikitLearnModelFlavor.__name__: Model.ModelFlavor.Value("MODEL_FLAVOR_SKLEARN"),
    XGBoostModelFlavor.__name__: Model.ModelFlavor.Value("MODEL_FLAVOR_XGBOOST"),
    LightGBMModelFlavor.__name__: Model.ModelFlavor.Value("MODEL_FLAVOR_LIGHTGBM"),
    KerasModelFlavor.__name__: Model.ModelFlavor.Value("MODEL_FLAVOR_KERAS"),
    TensorFlowModelFlavor.__name__: Model.ModelFlavor.Value("MODEL_FLAVOR_TENSORFLOW"),
}

MODULE_TO_PYTHON_FLAVORS: Dict[str, ModelFlavor] = {
    "torch": PyTorchModelFlavor(),
    "pyspark": SparkMLModelFlavor(),
    "sklearn": ScikitLearnModelFlavor(),
    "xgboost": XGBoostModelFlavor(),
    "lightgbm": LightGBMModelFlavor(),
    "keras": KerasModelFlavor(),
    "tensorflow": TensorFlowModelFlavor(),
}
