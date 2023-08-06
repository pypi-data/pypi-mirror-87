import re
from pathlib import Path
from typing import Dict, List

from setuptools import find_packages, setup


init_text = (Path(__file__).parent / "layer_client" / "__init__.py").read_text("utf-8")
try:
    version = re.findall(r'^__version__ = "([^"]+)"\r?$', init_text, re.M)[0]
except IndexError:
    raise RuntimeError("Unable to determine version.")

install_requires = (
    "boto3==1.16.24",
    "grpcio-tools==1.33.2",
    "pandas==1.1.2",
    "pyspark==3.0.1",
    "mlflow==1.12.1",
)

# TODO: leaving extras to conform to Layer `python-project`
extras_require: Dict[str, List[str]] = {
    "test": [],
}

setup(
    name="layer-client",
    version=version,
    description="The Layer Client",
    author="The Layer Team",
    author_email="python-client@layer.co",
    url="https://pypi.org/project/layer-client/",
    license="Apache 2",
    packages=find_packages(),
    python_requires=">=3.6",
    install_requires=install_requires,
    extras_require=extras_require,
)
