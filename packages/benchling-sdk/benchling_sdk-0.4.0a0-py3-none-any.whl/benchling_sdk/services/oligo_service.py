from typing import Iterable, List, Optional

from benchling_api_client.api.oligos import (
    archive_oligos,
    bulk_create_oligos,
    bulk_get_oligos,
    create_oligo,
    get_oligo,
    list_oligos,
    unarchive_oligos,
    update_oligo,
)
from benchling_api_client.models.async_task_link import AsyncTaskLink
from benchling_api_client.models.oligo import Oligo
from benchling_api_client.models.oligo_archive_request import OligoArchiveRequest
from benchling_api_client.models.oligo_archive_response import OligoArchiveResponse
from benchling_api_client.models.oligo_bulk_create import OligoBulkCreate
from benchling_api_client.models.oligo_create import OligoCreate
from benchling_api_client.models.oligo_list import OligoList
from benchling_api_client.models.oligo_patch import OligoPatch
from benchling_api_client.models.oligo_unarchive_request import OligoUnarchiveRequest
from benchling_api_client.models.oligos_bulk_create import OligosBulkCreate
from benchling_api_client.models.reason import Reason
from benchling_api_client.models.sort import Sort
from benchling_api_client.types import Response

from benchling_sdk.helpers.decorators import api_method
from benchling_sdk.helpers.pagination_helpers import NextToken, PageIterator
from benchling_sdk.helpers.response_helpers import model_from_detailed
from benchling_sdk.services.base_service import BaseService


class OligoService(BaseService):
    @api_method
    def get_by_id(self, oligo_id: str) -> Oligo:
        response = get_oligo.sync_detailed(client=self.client, oligo_id=oligo_id)
        return model_from_detailed(response)

    @api_method
    def oligos_page(
        self,
        modified_at: Optional[str] = None,
        name: Optional[str] = None,
        bases: Optional[str] = None,
        folder_id: Optional[str] = None,
        mentioned_in: Optional[List[str]] = None,
        project_id: Optional[str] = None,
        registry_id: Optional[str] = None,
        schema_id: Optional[str] = None,
        archive_reason: Optional[str] = None,
        mentions: Optional[List[str]] = None,
        sort: Optional[Sort] = None,
        page_size: Optional[int] = None,
        next_token: NextToken = None,
    ) -> Response[OligoList]:
        return list_oligos.sync_detailed(  # type: ignore
            client=self.client,
            modified_at=modified_at,
            name=name,
            bases=bases,
            folder_id=folder_id,
            mentioned_in=mentioned_in,
            project_id=project_id,
            registry_id=registry_id,
            schema_id=schema_id,
            archive_reason=archive_reason,
            mentions=mentions,
            sort=sort,
            page_size=page_size,
            next_token=next_token,
        )

    def list(
        self,
        modified_at: Optional[str] = None,
        name: Optional[str] = None,
        bases: Optional[str] = None,
        folder_id: Optional[str] = None,
        mentioned_in: Optional[List[str]] = None,
        project_id: Optional[str] = None,
        registry_id: Optional[str] = None,
        schema_id: Optional[str] = None,
        archive_reason: Optional[str] = None,
        mentions: Optional[List[str]] = None,
        sort: Optional[Sort] = None,
        page_size: Optional[int] = None,
    ) -> PageIterator[Oligo]:
        def api_call(next_token: NextToken) -> Response[OligoList]:
            return self.oligos_page(
                modified_at=modified_at,
                name=name,
                bases=bases,
                folder_id=folder_id,
                mentioned_in=mentioned_in,
                project_id=project_id,
                registry_id=registry_id,
                schema_id=schema_id,
                archive_reason=archive_reason,
                mentions=mentions,
                sort=sort,
                page_size=page_size,
                next_token=next_token,
            )

        def results_extractor(body: OligoList) -> Optional[List[Oligo]]:
            return body.oligos

        return PageIterator(api_call, results_extractor)

    @api_method
    def create(self, oligo: OligoCreate) -> Oligo:
        response = create_oligo.sync_detailed(client=self.client, json_body=oligo)
        return model_from_detailed(response)

    @api_method
    def update(self, oligo_id: str, oligo: OligoPatch) -> Oligo:
        response = update_oligo.sync_detailed(client=self.client, oligo_id=oligo_id, json_body=oligo)
        return model_from_detailed(response)

    @api_method
    def archive(self, oligo_ids: Iterable[str], reason: Reason) -> OligoArchiveResponse:
        archive_request = OligoArchiveRequest(reason=reason, oligo_ids=list(oligo_ids))
        response = archive_oligos.sync_detailed(client=self.client, json_body=archive_request)
        return model_from_detailed(response)

    @api_method
    def unarchive(self, oligo_ids: Iterable[str]) -> OligoArchiveResponse:
        unarchive_request = OligoUnarchiveRequest(oligo_ids=list(oligo_ids))
        response = unarchive_oligos.sync_detailed(client=self.client, json_body=unarchive_request)
        return model_from_detailed(response)

    @api_method
    def bulk_get(self, oligo_ids: Iterable[str]) -> Optional[List[Oligo]]:
        oligo_id_string = ",".join(oligo_ids)
        response = bulk_get_oligos.sync_detailed(client=self.client, oligo_ids=oligo_id_string)
        oligos_results = model_from_detailed(response)
        return oligos_results.oligos

    @api_method
    def bulk_create(self, oligos: Iterable[OligoBulkCreate]) -> AsyncTaskLink:
        body = OligosBulkCreate(list(oligos))
        response = bulk_create_oligos.sync_detailed(client=self.client, json_body=body)
        return model_from_detailed(response)
