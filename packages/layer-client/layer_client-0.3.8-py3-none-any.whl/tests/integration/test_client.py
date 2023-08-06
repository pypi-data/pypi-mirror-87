import logging
import os
import socket
import subprocess
import time
import uuid
from dataclasses import dataclass, replace
from pathlib import Path
from typing import Iterator, List, Tuple
from unittest import mock

import pandas as pd
import pytest
from pyspark import SparkConf
from pyspark.sql import SparkSession
from yarl import URL

from layer_client import (
    DataCatalogConfig,
    Dataset,
    Feature,
    Featureset,
    LayerClient,
    LayerClientConfig,
    ModelCatalogConfig,
    SortBy,
    SQLFeature,
)


logger = logging.getLogger(__name__)


def get_unused_port() -> int:
    """Return a port that is unused on the current host."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def start_kube_service_proxy(
    *,
    namespace: str,
    service: str,
    port: int,
    timeout_s: float = 30.0,
    scheme: str = "http",
) -> Tuple[URL, "subprocess.Popen[str]"]:
    logger.info("Starting the %s proxy process", service)

    local_port = get_unused_port()

    end_time = time.monotonic() + timeout_s
    while True:
        if end_time < time.monotonic():
            raise RuntimeError(f"Could not get the {service} URL")

        process = subprocess.Popen(
            [
                "kubectl",
                "-n",
                namespace,
                "port-forward",
                f"svc/{service}",
                f"{local_port}:{port}",
            ],
            universal_newlines=True,
        )

        try:
            process.wait(timeout=1.0)
        except subprocess.TimeoutExpired:
            pass

        if process.poll() is None:
            break
        time.sleep(1.0)
        process.kill()

    return URL(f"{scheme}://127.0.0.1:{local_port}"), process


@pytest.fixture(scope="session")
def data_catalog_server() -> Iterator[URL]:
    url, process = start_kube_service_proxy(
        namespace="layer", service="data-catalog", port=9000
    )
    yield url
    process.kill()


@pytest.fixture(scope="session")
def model_catalog_server() -> URL:
    # Return mock address since model catalog is not deployed into the minikube
    return URL("tcp://0.0.0.0:9999")


@pytest.fixture(scope="session")
def s3_server() -> Iterator[URL]:
    url, process = start_kube_service_proxy(
        namespace="minio", service="minio", port=9000
    )
    yield url
    process.kill()


@pytest.fixture(scope="session")
def s3_bucket_name() -> str:
    return os.environ.get("AWS_S3_BUCKET_NAME", "layer-development")


@pytest.fixture(scope="session")
def aws_access_key_id() -> str:
    return os.environ.get("AWS_ACCESS_KEY_ID", "myaccesskey")


@pytest.fixture(scope="session")
def aws_secret_access_key() -> str:
    return os.environ.get("AWS_SECRET_ACCESS_KEY", "mysecretkey")


@pytest.fixture()
def data_catalog_config(  # noqa: PT022
    data_catalog_server: URL, s3_bucket_name: str
) -> Iterator[DataCatalogConfig]:
    assert data_catalog_server.host
    assert data_catalog_server.port
    yield DataCatalogConfig(
        host=data_catalog_server.host,
        port=data_catalog_server.port,
        s3_bucket_name=s3_bucket_name,
    )


@pytest.fixture()
def model_catalog_config(  # noqa: PT022
    model_catalog_server: URL,
) -> Iterator[ModelCatalogConfig]:
    assert model_catalog_server.host
    assert model_catalog_server.port
    yield ModelCatalogConfig(
        host=model_catalog_server.host,
        port=model_catalog_server.port,
    )


@pytest.fixture()
def config(
    data_catalog_config: DataCatalogConfig, model_catalog_config: ModelCatalogConfig
) -> LayerClientConfig:
    return LayerClientConfig(
        organization_id=uuid.uuid4(),
        user_id=uuid.uuid4(),
        client_id=uuid.uuid4(),
        data_catalog=data_catalog_config,
        model_catalog=model_catalog_config,
    )


@pytest.fixture()
def spark_extra_class_path() -> str:
    return str(Path(__file__).parent.parent.parent.parent / "spark-jars" / "*")


@pytest.fixture()
def spark_conf(
    s3_server: URL,
    s3_bucket_name: str,
    spark_extra_class_path: str,
    aws_access_key_id: str,
    aws_secret_access_key: str,
) -> SparkConf:
    bucket = s3_bucket_name
    return (
        SparkConf()
        .set("spark.driver.userClassPathFirst", "true")
        .set("spark.driver.extraClassPath", spark_extra_class_path)
        .set("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
        .set("spark.hadoop.fs.s3a.access.key", aws_access_key_id)
        .set("spark.hadoop.fs.s3a.secret.key", aws_secret_access_key)
        .set(f"spark.hadoop.fs.s3a.bucket.{bucket}.endpoint", str(s3_server))
        .set(f"spark.hadoop.fs.s3a.bucket.{bucket}.connection.ssl.enabled", "false")
        .set(f"spark.hadoop.fs.s3a.bucket.{bucket}.connection.timeout", "5000")
        .set(f"spark.hadoop.fs.s3a.bucket.{bucket}.attempts.maximum", "3")
        .set(f"spark.hadoop.fs.s3a.bucket.{bucket}.path.style.access", "true")
    )


@pytest.fixture()
def spark_session(spark_conf: SparkConf) -> Iterator[SparkSession]:
    session = SparkSession.builder.config(conf=spark_conf).getOrCreate()
    yield session
    session.stop()


@pytest.fixture()
def client(
    config: LayerClientConfig, spark_session: SparkSession
) -> Iterator[LayerClient]:
    with LayerClient(config, logger, spark_session).init() as client:
        yield client


class TestLayerClient:
    def test_data_catalog_save_spark_df_load(
        self, client: LayerClient, spark_session: SparkSession
    ) -> None:
        orig_df = spark_session.range(10)
        build = client.data_catalog.save("spark_dataframe", orig_df)
        assert build.location.uri.startswith("s3a:")  # type: ignore
        df = client.data_catalog.load("spark_dataframe")
        assert sorted(df.toPandas()["id"].tolist()) == orig_df.toPandas()["id"].tolist()

    def test_data_catalog_save_pandas_df_load(
        self, client: LayerClient, spark_session: SparkSession
    ) -> None:
        orig_df = pd.DataFrame(range(10), columns=["id"])
        build = client.data_catalog.save("pandas_dataframe", orig_df)
        assert build.location.uri.startswith("s3a:")  # type: ignore
        df = client.data_catalog.load("pandas_dataframe").toPandas()
        assert sorted(df["id"].tolist()) == orig_df["id"].tolist()

    def test_data_catalog_save_version(
        self, client: LayerClient, spark_session: SparkSession
    ) -> None:
        orig_df = spark_session.range(10)
        build = client.data_catalog.save("spark_dataframe", orig_df, version="1")
        assert build.location.uri.startswith("s3a:")  # type: ignore
        df = client.data_catalog.load("spark_dataframe", version="1")
        assert sorted(df.toPandas()["id"].tolist()) == orig_df.toPandas()["id"].tolist()

    def test_data_catalog_add_dataset_get_dataset_by_id(
        self, client: LayerClient
    ) -> None:
        orig_dataset = Dataset(
            name=str(uuid.uuid4()), metadata={"format": "testformat"}
        )
        orig_dataset = client.data_catalog.add_dataset(orig_dataset)
        dataset = client.data_catalog.get_dataset_by_id(orig_dataset.id)
        assert orig_dataset == dataset

    def test_data_catalog_add_dataset_get_dataset_by_name(
        self, client: LayerClient
    ) -> None:
        orig_dataset = Dataset(
            name=str(uuid.uuid4()), metadata={"format": "testformat"}
        )
        expected_dataset = replace(orig_dataset, id=mock.ANY, version=mock.ANY)
        dataset = client.data_catalog.add_dataset(orig_dataset)
        assert expected_dataset == dataset
        dataset = client.data_catalog.get_dataset_by_name(orig_dataset.name)
        assert expected_dataset == dataset

    def test_data_catalog_add_featureset_no_features(self, client: LayerClient) -> None:
        orig_featureset = Featureset(name=str(uuid.uuid4()), features=[])
        # TODO: should be failing
        client.data_catalog.add_featureset(orig_featureset)

    def test_data_catalog_add_featureset_get_featureset_by_id(
        self, client: LayerClient
    ) -> None:
        orig_featureset = Featureset(
            name=str(uuid.uuid4()),
            features=sorted(
                [
                    SQLFeature(name=str(uuid.uuid4()), query="SELECT c1 FROM table"),
                    SQLFeature(name=str(uuid.uuid4()), query="SELECT c2 FROM table"),
                ],
                key=lambda f: f.name,
            ),
        )
        expected_featureset = replace(
            orig_featureset,
            id=mock.ANY,
            features=[
                replace(feature, id=mock.ANY) for feature in orig_featureset.features
            ],
        )
        featureset = client.data_catalog.add_featureset(orig_featureset)
        featureset = replace(
            featureset, features=sorted(featureset.features, key=lambda f: f.name)
        )
        assert expected_featureset == featureset
        featureset = client.data_catalog.get_featureset_by_id(featureset.id)
        featureset = replace(
            featureset, features=sorted(featureset.features, key=lambda f: f.name)
        )
        assert expected_featureset == featureset

    def test_data_catalog_add_featureset_unsupported_type(
        self, client: LayerClient
    ) -> None:
        @dataclass(frozen=True)
        class UnsupportedFeature(Feature):
            pass

        orig_featureset = Featureset(
            name=str(uuid.uuid4()),
            features=[
                UnsupportedFeature(name=str(uuid.uuid4())),
            ],
        )
        with pytest.raises(TypeError, match="Unsupported type: .+UnsupportedFeature"):
            client.data_catalog.add_featureset(orig_featureset)

    def test_data_catalog_add_featureset_get_featureset_by_name(
        self, client: LayerClient
    ) -> None:
        orig_featureset = Featureset(
            name=str(uuid.uuid4()),
            features=sorted(
                [
                    SQLFeature(name=str(uuid.uuid4()), query="SELECT c1 FROM table"),
                    SQLFeature(name=str(uuid.uuid4()), query="SELECT c2 FROM table"),
                ],
                key=lambda f: f.name,
            ),
        )
        expected_featureset = replace(
            orig_featureset,
            id=mock.ANY,
            features=[
                replace(feature, id=mock.ANY) for feature in orig_featureset.features
            ],
        )
        featureset = client.data_catalog.add_featureset(orig_featureset)
        featureset = replace(
            featureset, features=sorted(featureset.features, key=lambda f: f.name)
        )
        assert expected_featureset == featureset
        featureset = client.data_catalog.get_featureset_by_name(orig_featureset.name)
        featureset = replace(
            featureset, features=sorted(featureset.features, key=lambda f: f.name)
        )
        assert expected_featureset == featureset

    def test_data_catalog_list_datasets(self, client: LayerClient) -> None:
        orig_datasets = [
            Dataset(
                name=str(uuid.uuid4()),
                metadata={"format": "testformat"},
            )
            for _ in range(5)
        ]
        names: List[str] = []
        for orig_dataset in orig_datasets:
            names.append(orig_dataset.name)
            orig_dataset = client.data_catalog.add_dataset(orig_dataset)

        expected_datasets = [
            replace(dataset, id=mock.ANY, version=mock.ANY) for dataset in orig_datasets
        ]

        datasets = [
            dataset
            for dataset in client.data_catalog.list_datasets()
            if dataset.name in names
        ]
        assert expected_datasets == datasets

    def test_data_catalog_list_datasets_do_not_query_build(
        self, client: LayerClient
    ) -> None:
        orig_datasets = [
            Dataset(
                name=str(uuid.uuid4()),
                metadata={"format": "testformat"},
            )
            for _ in range(5)
        ]
        names: List[str] = []
        for orig_dataset in orig_datasets:
            names.append(orig_dataset.name)
            orig_dataset = client.data_catalog.add_dataset(orig_dataset)

        expected_datasets = [
            replace(dataset, id=mock.ANY, version=mock.ANY, schema="", metadata={})
            for dataset in orig_datasets
        ]

        datasets = [
            dataset
            for dataset in client.data_catalog.list_datasets(query_build=False)
            if dataset.name in names
        ]
        assert expected_datasets == datasets

    def test_data_catalog_list_datasets_sort_by_name_asc(
        self, client: LayerClient
    ) -> None:
        orig_datasets = [
            Dataset(
                name=str(uuid.uuid4()),
                metadata={"format": "testformat"},
            )
            for _ in range(5)
        ]
        names: List[str] = []
        for orig_dataset in orig_datasets:
            names.append(orig_dataset.name)
            orig_dataset = client.data_catalog.add_dataset(orig_dataset)

        expected_datasets = sorted(
            (
                replace(dataset, id=mock.ANY, version=mock.ANY, schema="", metadata={})
                for dataset in orig_datasets
            ),
            key=lambda d: d.name,
        )

        datasets = [
            dataset
            for dataset in client.data_catalog.list_datasets(
                sort_fields=[SortBy.NAME_ASC], query_build=False
            )
            if dataset.name in names
        ]
        assert expected_datasets == datasets

    def test_data_catalog_list_datasets_sort_by_name_desc(
        self, client: LayerClient
    ) -> None:
        orig_datasets = [
            Dataset(
                name=str(uuid.uuid4()),
                metadata={"format": "testformat"},
            )
            for _ in range(5)
        ]
        names: List[str] = []
        for orig_dataset in orig_datasets:
            names.append(orig_dataset.name)
            orig_dataset = client.data_catalog.add_dataset(orig_dataset)

        expected_datasets = sorted(
            (
                replace(
                    dataset,
                    id=mock.ANY,
                    version=mock.ANY,
                    schema="",
                    metadata={},
                )
                for dataset in orig_datasets
            ),
            key=lambda d: d.name,
            reverse=True,
        )

        datasets = [
            dataset
            for dataset in client.data_catalog.list_datasets(
                sort_fields=[SortBy.NAME_DESC], query_build=False
            )
            if dataset.name in names
        ]
        assert expected_datasets == datasets

    def test_data_catalog_list_featuresets(self, client: LayerClient) -> None:
        orig_featuresets = [
            Featureset(
                name=str(uuid.uuid4()),
                features=[
                    SQLFeature(name=str(uuid.uuid4()), query="SELECT c1 FROM table"),
                ],
            )
            for _ in range(5)
        ]

        names: List[str] = []
        for orig_featureset in orig_featuresets:
            names.append(orig_featureset.name)
            client.data_catalog.add_featureset(orig_featureset)

        expected_featuresets = sorted(
            (
                replace(
                    dataset,
                    id=mock.ANY,
                    features=[
                        replace(feature, id=mock.ANY) for feature in dataset.features
                    ],
                )
                for dataset in orig_featuresets
            ),
            key=lambda f: f.name,
        )

        featuresets = sorted(
            (
                featureset
                for featureset in client.data_catalog.list_featuresets()
                if featureset.name in names
            ),
            key=lambda f: f.name,
        )
        assert expected_featuresets == featuresets
