from typing import Iterable, List, Optional

from benchling_api_client.api.assay_runs import (
    bulk_get_assay_runs,
    create_assay_runs,
    get_assay_run,
    list_assay_runs,
    list_automation_input_generators,
    list_automation_output_processors,
    update_assay_run,
)
from benchling_api_client.models.assay_run import AssayRun
from benchling_api_client.models.assay_run_bulk_create import AssayRunBulkCreate
from benchling_api_client.models.assay_run_create import AssayRunCreate
from benchling_api_client.models.assay_run_list import AssayRunList
from benchling_api_client.models.assay_run_patch import AssayRunPatch
from benchling_api_client.models.assay_run_post_response import AssayRunPostResponse
from benchling_api_client.models.automation_file_input_list import AutomationFileInputList
from benchling_api_client.models.automation_file_output_list import AutomationFileOutputList
from benchling_api_client.models.automation_input_generator import AutomationInputGenerator
from benchling_api_client.models.automation_output_processor import AutomationOutputProcessor
from benchling_api_client.types import Response

from benchling_sdk.helpers.decorators import api_method
from benchling_sdk.helpers.pagination_helpers import NextToken, PageIterator
from benchling_sdk.helpers.response_helpers import model_from_detailed
from benchling_sdk.services.base_service import BaseService


class AssayRunService(BaseService):
    @api_method
    def get_by_id(self, assay_run_id: str) -> AssayRun:
        response = get_assay_run.sync_detailed(client=self.client, assay_run_id=assay_run_id)
        return model_from_detailed(response)

    @api_method
    def assay_runs_page(
        self,
        schema_id: str,
        min_created_time: Optional[int] = None,
        max_created_time: Optional[int] = None,
        next_token: NextToken = None,
        page_size: Optional[int] = None,
    ) -> Response[AssayRunList]:
        return list_assay_runs.sync_detailed(
            client=self.client,
            schema_id=schema_id,
            min_created_time=min_created_time,
            max_created_time=max_created_time,
            next_token=next_token,
            page_size=page_size,
        )

    def list(
        self,
        schema_id: str,
        min_created_time: Optional[int] = None,
        max_created_time: Optional[int] = None,
        page_size: Optional[int] = None,
    ) -> PageIterator[AssayRun]:
        def api_call(next_token: NextToken) -> Response[AssayRunList]:
            return self.assay_runs_page(
                schema_id=schema_id,
                min_created_time=min_created_time,
                max_created_time=max_created_time,
                next_token=next_token,
                page_size=page_size,
            )

        def results_extractor(body: AssayRunList) -> Optional[List[AssayRun]]:
            return body.assay_runs

        return PageIterator(api_call, results_extractor)

    @api_method
    def bulk_get(self, assay_run_ids: Iterable[str]) -> Optional[List[AssayRun]]:
        response = bulk_get_assay_runs.sync_detailed(client=self.client, assay_run_ids=list(assay_run_ids))
        runs_list = model_from_detailed(response)
        return runs_list.assay_runs

    @api_method
    def create(self, assay_runs: Iterable[AssayRunCreate]) -> AssayRunPostResponse:
        create_runs = AssayRunBulkCreate(assay_runs=list(assay_runs))
        response = create_assay_runs.sync_detailed(client=self.client, json_body=create_runs)
        return model_from_detailed(response)

    @api_method
    def update(self, assay_run_id: str, assay_run: AssayRunPatch) -> AssayRun:
        response = update_assay_run.sync_detailed(
            client=self.client, assay_run_id=assay_run_id, json_body=assay_run
        )
        return model_from_detailed(response)

    @api_method
    def automation_input_generators_page(
        self, assay_run_id: str, next_token: NextToken = None,
    ) -> Response[AutomationFileInputList]:
        return list_automation_input_generators.sync_detailed(  # type: ignore
            client=self.client, assay_run_id=assay_run_id, next_token=next_token,
        )

    def automation_input_generators(self, assay_run_id: str) -> PageIterator[AutomationInputGenerator]:
        def api_call(next_token: NextToken) -> Response[AutomationFileInputList]:
            return self.automation_input_generators_page(assay_run_id=assay_run_id, next_token=next_token)

        def results_extractor(body: AutomationFileInputList) -> List[AutomationInputGenerator]:
            return body.automation_input_generators

        return PageIterator(api_call, results_extractor)

    @api_method
    def automation_output_processors_page(
        self, assay_run_id: str, next_token: NextToken = None,
    ) -> Response[AutomationFileOutputList]:
        return list_automation_output_processors.sync_detailed(  # type: ignore
            client=self.client, assay_run_id=assay_run_id, next_token=next_token,
        )

    def automation_output_processors(self, assay_run_id: str) -> PageIterator[AutomationOutputProcessor]:
        def api_call(next_token: NextToken) -> Response[AutomationFileOutputList]:
            return self.automation_output_processors_page(assay_run_id=assay_run_id, next_token=next_token)

        def results_extractor(body: AutomationFileOutputList) -> List[AutomationOutputProcessor]:
            return body.automation_output_processors

        return PageIterator(api_call, results_extractor)
