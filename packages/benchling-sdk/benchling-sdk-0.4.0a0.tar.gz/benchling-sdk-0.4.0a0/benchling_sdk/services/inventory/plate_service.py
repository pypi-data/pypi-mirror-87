from typing import Iterable, List, Optional

from benchling_api_client.api.plates import (
    archive_plates,
    bulk_get_plates,
    create_plate,
    get_plate,
    list_plates,
    unarchive_plates,
    update_plate,
)
from benchling_api_client.models.plate import Plate
from benchling_api_client.models.plate_archive_request import PlateArchiveRequest
from benchling_api_client.models.plate_archive_response import PlateArchiveResponse
from benchling_api_client.models.plate_create import PlateCreate
from benchling_api_client.models.plate_list import PlateList
from benchling_api_client.models.plate_patch import PlatePatch
from benchling_api_client.models.plate_unarchive_request import PlateUnarchiveRequest
from benchling_api_client.models.reason import Reason
from benchling_api_client.models.sort12 import Sort12
from benchling_api_client.types import Response

from benchling_sdk.helpers.decorators import api_method
from benchling_sdk.helpers.pagination_helpers import NextToken, PageIterator
from benchling_sdk.helpers.response_helpers import model_from_detailed
from benchling_sdk.helpers.serialization_helpers import optional_array_query_param
from benchling_sdk.services.base_service import BaseService


class PlateService(BaseService):
    @api_method
    def get_by_id(self, plate_id: str) -> Plate:
        response = get_plate.sync_detailed(client=self.client, plate_id=plate_id)
        return model_from_detailed(response)

    @api_method
    def plates_page(
        self,
        *,
        page_size: Optional[int] = 50,
        next_token: Optional[str] = None,
        sort: Optional[Sort12] = None,
        schema_id: Optional[str] = None,
        modified_at: Optional[str] = None,
        name: Optional[str] = None,
        ancestor_storage_id: Optional[str] = None,
        storage_contents_id: Optional[str] = None,
        storage_contents_ids: Optional[List[str]] = None,
        archive_reason: Optional[str] = None,
    ) -> Response[PlateList]:
        return list_plates.sync_detailed(  # type: ignore
            client=self.client,
            sort=sort,
            schema_id=schema_id,
            modified_at=modified_at,
            name=name,
            ancestor_storage_id=ancestor_storage_id,
            storage_contents_id=storage_contents_id,
            storage_contents_ids=storage_contents_ids,
            archive_reason=archive_reason,
            next_token=next_token,
            page_size=page_size,
        )

    def list(
        self,
        *,
        sort: Optional[Sort12] = None,
        schema_id: Optional[str] = None,
        modified_at: Optional[str] = None,
        name: Optional[str] = None,
        ancestor_storage_id: Optional[str] = None,
        storage_contents_id: Optional[str] = None,
        storage_contents_ids: Optional[List[str]] = None,
        archive_reason: Optional[str] = None,
        page_size: Optional[int] = None,
    ) -> PageIterator[Plate]:
        def api_call(next_token: NextToken) -> Response[PlateList]:
            return self.plates_page(
                sort=sort,
                schema_id=schema_id,
                modified_at=modified_at,
                name=name,
                ancestor_storage_id=ancestor_storage_id,
                storage_contents_id=storage_contents_id,
                storage_contents_ids=storage_contents_ids,
                archive_reason=archive_reason,
                next_token=next_token,
                page_size=page_size,
            )

        def results_extractor(body: PlateList) -> Optional[List[Plate]]:
            return body.plates

        return PageIterator(api_call, results_extractor)

    @api_method
    def bulk_get(
        self, *, plate_ids: Optional[Iterable[str]] = None, barcodes: Optional[Iterable[str]] = None
    ) -> Optional[List[Plate]]:
        plate_id_string = optional_array_query_param(plate_ids)
        barcode_string = optional_array_query_param(barcodes)
        response = bulk_get_plates.sync_detailed(
            client=self.client, plate_ids=plate_id_string, barcodes=barcode_string
        )
        plates_list = model_from_detailed(response)
        return plates_list.plates

    @api_method
    def create(self, plate: PlateCreate) -> Plate:
        response = create_plate.sync_detailed(client=self.client, json_body=plate)
        return model_from_detailed(response)

    @api_method
    def update(self, plate_id: str, plate: PlatePatch) -> Plate:
        response = update_plate.sync_detailed(client=self.client, plate_id=plate_id, json_body=plate)
        return model_from_detailed(response)

    @api_method
    def archive(
        self, plate_ids: Iterable[str], reason: Reason, should_remove_barcodes: bool
    ) -> PlateArchiveResponse:
        archive_request = PlateArchiveRequest(
            plate_ids=list(plate_ids), reason=reason, should_remove_barcodes=should_remove_barcodes
        )
        response = archive_plates.sync_detailed(client=self.client, json_body=archive_request)
        return model_from_detailed(response)

    @api_method
    def unarchive(self, plate_ids: Iterable[str]) -> PlateArchiveResponse:
        unarchive_request = PlateUnarchiveRequest(plate_ids=list(plate_ids))
        response = unarchive_plates.sync_detailed(client=self.client, json_body=unarchive_request)
        return model_from_detailed(response)
