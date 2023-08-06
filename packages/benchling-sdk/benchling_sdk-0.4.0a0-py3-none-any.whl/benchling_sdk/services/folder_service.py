from typing import Iterable, List, Optional

from benchling_api_client.api.folders import (
    archive_folders,
    create_folder,
    get_folder,
    list_folders,
    unarchive_folders,
)
from benchling_api_client.models.create_folder import CreateFolder
from benchling_api_client.models.folder import Folder
from benchling_api_client.models.folder_archival_change import FolderArchivalChange
from benchling_api_client.models.folder_archive_request import FolderArchiveRequest
from benchling_api_client.models.folder_list import FolderList
from benchling_api_client.models.folder_unarchive_request import FolderUnarchiveRequest
from benchling_api_client.models.reason1 import Reason1
from benchling_api_client.models.sort import Sort
from benchling_api_client.types import Response

from benchling_sdk.helpers.decorators import api_method
from benchling_sdk.helpers.pagination_helpers import NextToken, PageIterator
from benchling_sdk.helpers.response_helpers import model_from_detailed
from benchling_sdk.services.base_service import BaseService


class FolderService(BaseService):
    @api_method
    def get_by_id(self, folder_id: str) -> Folder:
        response = get_folder.sync_detailed(client=self.client, folder_id=folder_id)
        return model_from_detailed(response)

    @api_method
    def folders_page(
        self,
        *,
        sort: Optional[Sort] = Sort.NAME,
        archive_reason: Optional[str] = None,
        name_includes: Optional[str] = None,
        parent_folder_id: Optional[str] = None,
        project_id: Optional[str] = None,
        next_token: Optional[str] = None,
        page_size: Optional[int] = 50,
    ) -> Response[FolderList]:
        return list_folders.sync_detailed(
            client=self.client,
            sort=sort,
            archive_reason=archive_reason,
            name_includes=name_includes,
            parent_folder_id=parent_folder_id,
            project_id=project_id,
            next_token=next_token,
            page_size=page_size,
        )

    def list(
        self,
        *,
        sort: Optional[Sort] = None,
        archive_reason: Optional[str] = None,
        name_includes: Optional[str] = None,
        parent_folder_id: Optional[str] = None,
        project_id: Optional[str] = None,
        page_size: Optional[int] = 50,
    ) -> PageIterator[Folder]:
        def api_call(next_token: NextToken) -> Response[FolderList]:
            return self.folders_page(
                sort=sort,
                archive_reason=archive_reason,
                name_includes=name_includes,
                parent_folder_id=parent_folder_id,
                project_id=project_id,
                next_token=next_token,
                page_size=page_size,
            )

        def results_extractor(body: FolderList) -> Optional[List[Folder]]:
            return body.folders

        return PageIterator(api_call, results_extractor)

    @api_method
    def create(self, folder: CreateFolder) -> Folder:
        response = create_folder.sync_detailed(client=self.client, json_body=folder)
        return model_from_detailed(response)

    @api_method
    def archive(self, folder_ids: Iterable[str], reason: Reason1) -> FolderArchivalChange:
        archive_request = FolderArchiveRequest(folder_ids=list(folder_ids), reason=reason)
        response = archive_folders.sync_detailed(client=self.client, json_body=archive_request)
        return model_from_detailed(response)

    @api_method
    def unarchive(self, folder_ids: Iterable[str]) -> FolderArchivalChange:
        unarchive_request = FolderUnarchiveRequest(folder_ids=list(folder_ids))
        response = unarchive_folders.sync_detailed(client=self.client, json_body=unarchive_request)
        return model_from_detailed(response)
