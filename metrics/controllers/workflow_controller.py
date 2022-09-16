import json
import logging

from metrics.utils.config import Config
from metrics.utils.security import validate_secret
from metrics.views.workflow_view import WorkflowView
from metrics.models.workflow_job_model import WorkflowJobModel

logger = logging.getLogger(__name__)


class WorkflowController(object):
    def __init__(self, config: Config, event: dict, model: WorkflowJobModel = None, view: WorkflowView = None):
        self.model = model
        self.view = view
        self.config = config
        self.event = event

    def process_workflow_job_event(self) -> WorkflowView:
        # Basic structure validation
        event_body: str = self.event['body']
        try:
            json.loads(event_body)
        except ValueError:
            logger.error("Failed to decode json", stack_info=True)
            return WorkflowView(status_code=500, body={"error": "json decode failure"})

        # Secret decoding with HMAC and signature verification
        signature = self.event['headers'].get('x-hub-signature-256')
        if not validate_secret(signature, event_body, self.config.webhook_secret):
            return WorkflowView(status_code=403, body={"error": "invalid signature"})

        # Workflow jobs have 3 different stages
        if self.event['body']['action'] == "queued":
            self.__insert_workflow_job()
        elif self.event['body']['action'] == "in_progress":
            self.__set_workflow_job_to_in_progress()
        elif self.event['body']['action'] == "completed":
            self.__set_workflow_job_to_completed()

        return WorkflowView(status_code=200, body={"message": "Valid message"})

    def __insert_workflow_job(self):
        self.model.job.insert_job()
        return True

    def __set_workflow_job_in_progress(self):
        self.model.job.update_in_progress()
        return True

    def __set_workflow_job_completed(self):
        self.model.job.update_completed()
        return True
