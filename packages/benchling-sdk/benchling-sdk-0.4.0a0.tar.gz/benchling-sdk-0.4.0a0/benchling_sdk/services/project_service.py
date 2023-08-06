from typing import Iterable, List, Optional

from benchling_api_client.api.projects import archive_projects, get_project, list_projects, unarchive_projects
from benchling_api_client.models.project import Project
from benchling_api_client.models.project_archival_change import ProjectArchivalChange
from benchling_api_client.models.project_archive_request import ProjectArchiveRequest
from benchling_api_client.models.project_list import ProjectList
from benchling_api_client.models.project_unarchive_request import ProjectUnarchiveRequest
from benchling_api_client.models.reason1 import Reason1
from benchling_api_client.models.sort import Sort
from benchling_api_client.types import Response

from benchling_sdk.helpers.decorators import api_method
from benchling_sdk.helpers.pagination_helpers import NextToken, PageIterator
from benchling_sdk.helpers.response_helpers import model_from_detailed
from benchling_sdk.services.base_service import BaseService


class ProjectService(BaseService):
    @api_method
    def get_by_id(self, project_id: str) -> Project:
        response = get_project.sync_detailed(client=self.client, project_id=project_id)
        return model_from_detailed(response)

    @api_method
    def projects_page(
        self,
        *,
        sort: Optional[Sort] = Sort.NAME,
        archive_reason: Optional[str] = None,
        next_token: Optional[str] = None,
        page_size: Optional[int] = 50,
    ) -> Response[ProjectList]:
        return list_projects.sync_detailed(
            client=self.client,
            sort=sort,
            archive_reason=archive_reason,
            next_token=next_token,
            page_size=page_size,
        )

    def list(
        self,
        *,
        sort: Optional[Sort] = None,
        archive_reason: Optional[str] = None,
        page_size: Optional[int] = 50,
    ) -> PageIterator[Project]:
        def api_call(next_token: NextToken) -> Response[ProjectList]:
            return self.projects_page(
                sort=sort, archive_reason=archive_reason, next_token=next_token, page_size=page_size,
            )

        def results_extractor(body: ProjectList) -> Optional[List[Project]]:
            return body.projects

        return PageIterator(api_call, results_extractor)

    @api_method
    def archive(self, project_ids: Iterable[str], reason: Reason1) -> ProjectArchivalChange:
        archive_request = ProjectArchiveRequest(project_ids=list(project_ids), reason=reason)
        response = archive_projects.sync_detailed(client=self.client, json_body=archive_request)
        return model_from_detailed(response)

    @api_method
    def unarchive(self, project_ids: Iterable[str]) -> ProjectArchivalChange:
        unarchive_request = ProjectUnarchiveRequest(project_ids=list(project_ids))
        response = unarchive_projects.sync_detailed(client=self.client, json_body=unarchive_request)
        return model_from_detailed(response)
