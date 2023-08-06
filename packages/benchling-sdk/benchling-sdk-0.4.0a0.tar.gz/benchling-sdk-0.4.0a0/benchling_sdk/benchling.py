import re
from typing import Optional
import urllib.parse

from benchling_api_client.benchling_client import BenchlingApiClient
from benchling_api_client.client import Client

from benchling_sdk.helpers.retry_helpers import RetryStrategy
from benchling_sdk.services.aa_sequence_service import AaSequenceService
from benchling_sdk.services.assay_result_service import AssayResultService
from benchling_sdk.services.assay_run_service import AssayRunService
from benchling_sdk.services.blob_service import BlobService
from benchling_sdk.services.custom_entity_service import CustomEntityService
from benchling_sdk.services.dna_sequence_service import DnaSequenceService
from benchling_sdk.services.folder_service import FolderService
from benchling_sdk.services.inventory_service import InventoryService
from benchling_sdk.services.lab_automation_service import LabAutomationService
from benchling_sdk.services.oligo_service import OligoService
from benchling_sdk.services.project_service import ProjectService
from benchling_sdk.services.registry_service import RegistryService
from benchling_sdk.services.request_service import RequestService
from benchling_sdk.services.schema_service import SchemaService
from benchling_sdk.services.task_service import TaskService


class Benchling(object):

    _client: Client
    _registry_service: RegistryService
    _task_service: TaskService
    _custom_entity_service: CustomEntityService
    _aa_sequence_service: AaSequenceService
    _dna_sequence_service: DnaSequenceService
    _request_service: RequestService
    _assay_run_service: AssayRunService
    _folder_service: FolderService
    _lab_automation_service: LabAutomationService
    _project_service: ProjectService
    _schema_service: SchemaService
    _inventory_service: InventoryService
    _assay_result_service: AssayResultService
    _oligo_service: OligoService
    _blob_service: BlobService

    def __init__(
        self,
        url: str,
        api_key: str,
        base_path: Optional[str] = "/api/v2",
        retry_strategy: Optional[RetryStrategy] = RetryStrategy(),
    ):
        """
        :param url: A server URL (host and optional port) including scheme such as https://benchling.com
        :param api_key: A valid Benchling API token for authentication and authorization
        :param base_path: If provided, will append to the host. Otherwise, assumes the V2 API. This is
                          a workaround until the generated client supports the servers block. See BNCH-15422
        :param retry_strategy: An optional retry strategy for retrying HTTP calls on failure. Setting to None
                               will disable retries
        """
        full_url = self._format_url(url, base_path)
        client = BenchlingApiClient(base_url=full_url, token=api_key)
        if retry_strategy is None:
            retry_strategy = RetryStrategy.no_retries()
        self._client = client
        self._registry_service = RegistryService(client, retry_strategy=retry_strategy)
        self._task_service = TaskService(client, retry_strategy=retry_strategy)
        self._custom_entity_service = CustomEntityService(client, retry_strategy=retry_strategy)
        self._request_service = RequestService(client, retry_strategy=retry_strategy)
        self._assay_run_service = AssayRunService(client, retry_strategy=retry_strategy)
        self._folder_service = FolderService(client, retry_strategy=retry_strategy)
        self._project_service = ProjectService(client, retry_strategy=retry_strategy)
        self._aa_sequence_service = AaSequenceService(client, retry_strategy=retry_strategy)
        self._dna_sequence_service = DnaSequenceService(client, retry_strategy=retry_strategy)
        self._schema_service = SchemaService(client, retry_strategy=retry_strategy)
        self._inventory_service = InventoryService(client, retry_strategy=retry_strategy)
        self._assay_result_service = AssayResultService(client, retry_strategy=retry_strategy)
        self._blob_service = BlobService(client, retry_strategy=retry_strategy)
        self._oligo_service = OligoService(client, retry_strategy=retry_strategy)
        self._lab_automation_service = LabAutomationService(client, retry_strategy=retry_strategy)

    @property
    def client(self) -> Client:
        return self._client

    @property
    def aa_sequences(self) -> AaSequenceService:
        return self._aa_sequence_service

    @property
    def assay_results(self) -> AssayResultService:
        return self._assay_result_service

    @property
    def assay_runs(self) -> AssayRunService:
        return self._assay_run_service

    @property
    def blobs(self) -> BlobService:
        return self._blob_service

    @property
    def custom_entities(self) -> CustomEntityService:
        return self._custom_entity_service

    @property
    def dna_sequences(self) -> DnaSequenceService:
        return self._dna_sequence_service

    @property
    def folders(self) -> FolderService:
        return self._folder_service

    @property
    def inventory(self) -> InventoryService:
        return self._inventory_service

    @property
    def lab_automation(self) -> LabAutomationService:
        return self._lab_automation_service

    @property
    def oligos(self) -> OligoService:
        return self._oligo_service

    @property
    def projects(self) -> ProjectService:
        return self._project_service

    @property
    def registry(self) -> RegistryService:
        return self._registry_service

    @property
    def requests(self) -> RequestService:
        return self._request_service

    @property
    def schemas(self) -> SchemaService:
        return self._schema_service

    @property
    def tasks(self) -> TaskService:
        return self._task_service

    @staticmethod
    def _format_url(url: str, base_path: Optional[str]) -> str:
        if base_path:
            joined_url = urllib.parse.urljoin(url, base_path)
            # Strip any trailing slashes, the API client will lead with them
            joined_url = re.sub(r"/+$", "", joined_url)
            return joined_url
        return url
