from dateutil import parser
from enum import Enum
from string import Template
from typing import Any, List

from sktmls import MLSClient, MLSENV, MLSRuntimeENV, MLSResponse

SPARK_QUERY_FOR_LABLE_DATA = Template(
    """
SELECT sha2(source.svc_mgmt_num, 256) AS svc_mgmt_num, source.period AS period
FROM (
    ${source_query}
) AS source
"""
)


class ProblemType(Enum):
    """
    AutoML 데이터셋의 문제 타입입니다.

    - SCORE: 스코어 기반 고객 타겟팅
    - CLASSIFICATION: 분류
    - REGRESSION: 회귀
    """

    SCORE = "score"
    CLASSIFICATION = "classification"
    REGRESSION = "regression"


class DatasetError(Exception):
    def __init__(self, *args, **kwargs):
        """
        AutoML 데이터셋 에러.
        """
        super().__init__(*args, **kwargs)


class FeatureStoreConf:
    def __init__(self, enabled: bool, feature_group_id_list: List[int] = None, n_label_ratio: float = 1.0):
        """
        AutoML 데이터셋의 피쳐 스토어 설정입니다.

        ## Args

        - enabled: (bool) 피쳐 스토어 사용 유무
        - feature_group_id_list: (optional) (list(int)) 사용하고자 하는 피쳐 그룹의 ID 리스트
        - n_label_ratio: (optional) (float) N 레이블 샘플링 비율 (스코어 기반 고객 타겟팅 문제만 지원, 기본값: 1.0)

        ## Example

        ```python
        config = FeatureStoreConf(enabled=True, feature_group_id_list=[1, 2, 3], n_label_ratio=1.5)
        ```
        """
        self.enabled = enabled
        self.feature_group_id_list = feature_group_id_list
        self.n_label_ratio = n_label_ratio

    def __str__(self) -> str:
        return str(self.__dict__)


class LabelDataConf:
    def __init__(self, source_type: str, source_path: str):
        """
        AutoML 데이터셋의 레이블 데이터 설정입니다.

        ## Args

        - source_type: (str) 레이블 데이터 타입 (`csv` | `edd2` | `ye`).
        - source_path: (str) 레이블 데이터의 이름 또는 테이블 경로.
          - csv: 파일 이름 (ex. test.csv)
          - edd2: EDD -> MLS 로 전달된 BigQuery 테이블의 Full 경로 (ex. sktaic-datahub.mls_edd2_sync.test)
          - ye: YE -> MLS 로 전달된 데이터의 이름 (ex. test)

        ## Example

        ```python
        config = LabelDataConf(source_type="ye", source_path="my_test_table")
        ```
        """
        self.source_type = source_type
        self.source_path = source_path

    def __str__(self) -> str:
        return str(self.__dict__)


class Dataset:
    def __init__(self, **kwargs):
        """
        AutoML 학습 데이터셋 클래스.

        ## Attributes

        - id: (int) 데이터셋 ID
        - name: (str) 데이터셋 이름
        - status: (str) 데이터셋 상태
        - problem_type: (`sktmls.datasets.ProblemType`) 문제 타입
        - feature_store_conf: (`sktmls.datasets.FeatureStoreConf`) 피쳐 스토어 설정값
        - label_data_conf: (`sktmls.datasets.LabelDataConf`) 레이블 데이터 설정값
        - created_at: (datetime.datetime) 데이터셋 생성 시점
        - updated_at: (datetime.datetime) 데이터셋 생성 완료 또는 갱신 시점
        """
        self.id = kwargs.get("id")
        self.name = kwargs.get("name")
        self.status = kwargs.get("status")
        self.problem_type = ProblemType(kwargs.get("data_type"))

        base_feature_conf = kwargs.get("setup_conf", {}).get("base_feature_conf", {})
        self.feature_store_conf = FeatureStoreConf(
            enabled=base_feature_conf.get("enabled"),
            feature_group_id_list=base_feature_conf.get("feature_group_id_list"),
            n_label_ratio=base_feature_conf.get("n_label_ratio"),
        )

        label_data_conf = kwargs.get("setup_conf", {}).get("label_data_conf", {})
        self.label_data_conf = LabelDataConf(
            source_type=label_data_conf.get("source_type"),
            source_path=label_data_conf.get("source_path"),
        )

        try:
            self.created_at = parser.parse(kwargs.get("created_at"))
        except TypeError:
            self.created_at = None

        try:
            self.updated_at = parser.parse(kwargs.get("updated_at"))
        except TypeError:
            self.updated_at = None

    def __str__(self) -> str:
        return self.name


class DatasetClient(MLSClient):
    def __init__(
        self, env: MLSENV = None, runtime_env: MLSRuntimeENV = None, username: str = None, password: str = None
    ):
        """
        AutoML 데이터셋 관련 기능을 제공하는 클라이언트 클래스입니다.

        ## Args

        - env: (`sktmls.MLSENV`) 접근할 MLS 환경 (`sktmls.MLSENV.DEV`|`sktmls.MLSENV.STG`|`sktmls.MLSENV.PRD`) (기본값: `sktmls.MLSENV.STG`)
        - runtime_env: (`sktmls.MLSRuntimeENV`) 클라이언트가 실행되는 환경 (`sktmls.MLSRuntimeENV.YE`|`sktmls.MLSRuntimeENV.EDD`|`sktmls.MLSRuntimeENV.LOCAL`) (기본값: `sktmls.MLSRuntimeENV.LOCAL`)
        - username: (str) MLS 계정명 (기본값: $MLS_USERNAME)
        - password: (str) MLS 계정 비밀번호 (기본값: $MLS_PASSWORD)

        ## Returns
        `sktmls.datasets.DatasetClient`

        ## Example

        ```python
        client = DatasetClient(env=MLSENV.STG, runtime_env=MLSRuntimeENV.YE, username="mls_account", password="mls_password")
        ```
        """
        super().__init__(env=env, runtime_env=runtime_env, username=username, password=password)

    def create_dataset(
        self, name: str, problem_type: ProblemType, feature_store_conf: FeatureStoreConf, label_data_conf: LabelDataConf
    ) -> MLSResponse:
        """
        새 AutoML 데이터셋을 생성합니다.

        ## Args

        - name: (str) 데이터셋 이름
        - problem_type: (`sktmls.datasets.ProblemType`) 문제 타입
        - feature_store_conf: (`sktmls.datasets.FeatureStoreConf`) 피쳐 스토어 설정
        - label_data_conf: (`sktmls.datasets.LabelDataConf`) 레이블 데이터 설정

        ## Returns
        `sktmls.datasets.DatasetClient`

        ## Example

        ```python
        client = DatasetClient()
        client.create_dataset(
            name="my_dataset",
            problem_type=ProblemType.SCORE,
            feature_store_conf=FeatureStoreConf(enabled=True, feature_group_id_list=[1, 2, 3], n_label_ratio=1.5),
            label_data_conf=LabelDataConf(source_type="ye", source_path="my_test_table"),
        )
        ```
        """
        data = {
            "name": name,
            "type": problem_type.value,
            "base_feature_conf": feature_store_conf.__dict__,
            "label_data_conf": label_data_conf.__dict__,
        }
        return self._request(method="POST", url="api/v1/datasets", data=data)

    def list_datasets(self, **kwargs) -> List[Dataset]:
        """
        AutoML 데이터셋 리스트를 가져옵니다.

        ## Args

        - kwargs: (optional) (dict) 필터 조건
            - id: (int) 데이터셋 ID
            - name: (str) 데이터셋 이름
            - query: (str) 검색 문자
            - page: (int) 페이지 번호

        ## Returns
        list(`sktmls.datasets.Dataset`)
        """
        response = self._request(method="GET", url="api/v1/datasets", params=kwargs)

        if response.code != 0:
            raise DatasetError(f"Fail to search datasets: {response.error}")

        return [Dataset(**dataset) for dataset in response.results]

    def get_dataset(self, name: str = None, id: int = None) -> Dataset:
        """
        해당하는 AutoML 데이텨셋을 가져옵니다.

        ## Args: `id` 또는 `name` 중 한 개 이상의 값이 반드시 전달되어야 합니다.

        - id: (int) 데이터셋 ID
        - name: (str) 데이터셋 이름

        ## Returns
        `sktmls.datasets.Dataset`
        """
        assert id is not None or name, "One of id or name must be provided"

        datasets = self.list_datasets(name=name, id=id)

        if len(datasets) == 0:
            raise DatasetError("Dataset does not exists")

        return datasets[0]

    def delete_dataset(self, name: str = None, id: int = None) -> None:
        """
        해당하는 AutoML 데이터셋을 삭제합니다

        ## Args: `id` 또는 `name` 중 한 개 이상의 값이 반드시 전달되어야 합니다.

        - id: (int) 데이터셋 ID
        - name: (str) 데이터셋 이름

        """
        dataset = self.get_dataset(name=name, id=id)
        response = self._request(method="DELETE", url=f"api/v1/datasets/{dataset.id}")

        if response.code != 0:
            raise DatasetError(f"Fail to delete a dataset: {response.error}")

    def upload_label_data_from_ye(self, spark_session: Any, output_name: str, source_query: str) -> None:
        """
        YE 환경에서 레이블 데이터를 업로드합니다. 전달하려는 데이터의 원천 데이터는 Spark Query로 조회 가능해야 합니다.

        ## Args

        - spark_session: (SparkSession) `skt` 패키지의 skt.ye.get_spark() 함수를 통해 얻어지는 `SparkSession` 객체.
        - output_name: (str) 출력하고자 하는 데이터 이름.
        - source_query: (str) 업로드하고자 하는 데이터를 조회하기 위한 Spark Query(`svc_mgmt_num`, `period` 컬럼이 필수로 포함되어야 함).

        ## Example

        ```python
        source_query = '''
        SELECT svc_mgmt_num, '202001' AS period
        FROM test_db.test_table
        LIMIT 10000
        '''

        client = DatasetClient()
        client.upload_label_data_from_ye(spark_session=skt.ye.get_spark(), output_name="ye_test.csv", source_query=source_query)
        ```
        """
        assert type(spark_session).__name__ == "SparkSession", "Invalid type of spark_session"
        assert type(output_name) == str, "Invalid type of output_name"
        assert type(source_query) == str, "Invalid type of source_query"

        if not self.config.MLS_RUNTIME_ENV == "YE":
            raise DatasetError("upload_label_data_from_ye() is only supported over the YE environment.")

        query = SPARK_QUERY_FOR_LABLE_DATA.substitute(source_query=source_query)
        target_path = f"gs://sktmls-automl-{self.get_env().value}/{self.get_username()}/label_data_ye/{output_name}"
        spark_session.sql(query).write.mode("overwrite").csv(target_path, header=True)
        spark_session.stop()

    def upload_label_data_from_ye_bq(
        self,
        bigquery_client: Any,
        source_dataset: str,
        source_table: str,
        output_name: str = None,
    ) -> None:
        """
        YE 환경에서 BigQuery에 존재하는 테이블을 본인 MLS계정에 레이블 데이터로 업로드합니다.

        ## Args

        - bigquery_client: (google.cloud.bigquery.client.Client) `skt` 패키지의 skt.gcp.get_bigquery_client() 함수를 통해 얻어지는 `google.cloud.bigquery.client.Client` 객체.
        - source_dataset: (str) 업로드하고자 하는 BigQuery 데이터셋 이름.
        - source_table: (str) 업로드하고자 하는 BigQuery 테이블 이름 (`svc_mgmt_num`, `period` 컬럼이 필수로 포함되어야 함).
        - output_name: (optional) (str) 출력하고자 하는 데이터 이름. (기본값 : `source_table`)

        ## Example

        ```python
        client = DatasetClient()
        client.upload_label_data_from_ye_bq(bigquery_client=skt.gcp.get_bigquery_client(), source_dataset="my_dataset", source_table="my_table")
        ```
        """
        assert (
            str(type(bigquery_client)) == "<class 'google.cloud.bigquery.client.Client'>"
        ), "Invalid type of bigquery_client"
        assert type(source_dataset) == str, "Invalid type of source_dataset"
        assert type(source_table) == str, "Invalid type of source_table"
        if output_name is not None:
            type(output_name) == str, "Invalid type of otuput_name"

        if not output_name:
            output_name = source_table

        if not self.config.MLS_RUNTIME_ENV == "YE":
            raise DatasetError("upload_label_data_from_ye() is only supported over the YE environment.")

        try:
            bigquery_table = bigquery_client.get_table(f"sktaic-datahub.{source_dataset}.{source_table}")
        except Exception as e:
            raise DatasetError(str(e))

        try:
            extract_job = bigquery_client.extract_table(
                source=bigquery_table,
                destination_uris=f"gs://sktmls-automl-{self.get_env().value}/{self.get_username()}/label_data_ye/{output_name}/part-{output_name}",
            )
            extract_job.result()
        except Exception as e:
            raise DatasetError(str(e))
