from typing import List, Optional

from benchling_api_client.api.schemas import get_request_schema, list_request_schemas
from benchling_api_client.models.paginated_request_schema_list import PaginatedRequestSchemaList
from benchling_api_client.models.request_schema import RequestSchema
from benchling_api_client.types import Response

from benchling_sdk.helpers.decorators import api_method
from benchling_sdk.helpers.pagination_helpers import NextToken, PageIterator
from benchling_sdk.helpers.response_helpers import model_from_detailed
from benchling_sdk.services.base_service import BaseService


class RequestSchemaService(BaseService):
    @api_method
    def get_by_id(self, schema_id: str) -> RequestSchema:
        response = get_request_schema.sync_detailed(client=self.client, schema_id=schema_id)
        return model_from_detailed(response)

    @api_method
    def request_schemas_page(
        self, *, next_token: Optional[str] = None, page_size: Optional[int] = 50,
    ) -> Response[PaginatedRequestSchemaList]:
        return list_request_schemas.sync_detailed(  # type:ignore
            client=self.client, next_token=next_token, page_size=page_size,
        )

    def list(self, *, page_size: Optional[int] = 50,) -> PageIterator[RequestSchema]:
        def api_call(next_token: NextToken) -> Response[PaginatedRequestSchemaList]:
            return self.request_schemas_page(next_token=next_token, page_size=page_size,)

        def results_extractor(body: PaginatedRequestSchemaList) -> Optional[List[RequestSchema]]:
            return body.request_schemas

        return PageIterator(api_call, results_extractor)
