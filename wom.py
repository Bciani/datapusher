from prefect import flow, get_run_logger
from prefect.deployments import Deployment
from prefect.server.schemas.schedules import CronSchedule

from prefect.infrastructure import DockerContainer

@flow(name="pooSkiller")
def data_flow():
    logger = get_run_logger()
    logger.warning("Test Sent")

# This is needed to signal the main/start of the job
if __name__ == "__main__":
    data_flow()

# Needed for deployment -- changes here will override the info on the server BE CAREFUL!
Deployment.build_from_flow(
    flow=data_flow,
    name="data-Schedule",
    apply=False,
    version=1,
    tags=["poo"],
    work_pool_name="default-pool",
    work_queue_name="default",
    #storage=BitBucketRepository.load("bb-repo"), swap to githubsetup
    infrastructure= DockerContainer.load("standard-img"),
    infra_overrides=dict(env={"PREFECT_LOGGING_LEVEL":"DEBUG"}),
    path="",
    entrypoint="pooPusher/wom.py:data_flow"
    # every 30m, starting at 5am - 7pm, m-f
   # schedule=(CronSchedule(cron="*/30 5-19 * * 1-5", timezone="America/Chicago"))
)
