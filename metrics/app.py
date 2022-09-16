import os
from metrics.controllers.workflow_controller import WorkflowController
from metrics.utils.config import Config


def lambda_handler(event, context):
    app_config = Config(db_host=os.environ['DB_HOST'], db_user=os.environ['DB_USER'],
                        db_password=os.environ['DB_PASSWORD'], webhook_secret=os.environ['WEBHOOK_SECRET'])
    wf_ctl = WorkflowController(config=app_config, event=event)
    view = wf_ctl.process_workflow_job_event()
    return view.render()
