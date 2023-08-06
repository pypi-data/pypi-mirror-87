from time import sleep, time

from benchling_api_client.api.tasks import get_task
from benchling_api_client.models.async_task import AsyncTask
from benchling_api_client.models.status1 import Status1

from benchling_sdk.helpers.decorators import api_method
from benchling_sdk.helpers.response_helpers import model_from_detailed
from benchling_sdk.services.base_service import BaseService


class TaskService(BaseService):
    @api_method
    def get_by_id(self, task_id: str) -> AsyncTask:
        response = get_task.sync_detailed(client=self.client, task_id=task_id)
        return model_from_detailed(response)

    @api_method
    def wait_for_task(
        self, task_id: str, interval_wait_seconds: int = 1, max_wait_seconds: int = 30
    ) -> AsyncTask:
        start_time = time()
        while (
            response := self.get_by_id(task_id)
        ).status == Status1.RUNNING and time() - start_time <= max_wait_seconds:
            sleep(interval_wait_seconds)
        return response
