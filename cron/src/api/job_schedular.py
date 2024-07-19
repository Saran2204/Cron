import uuid

from azure.batch import models as batchmodels
from utils.cron_parser import parse_cron_expression
from utils.recurrance_parser import convert_cron_to_iso8601
from utils.time_utils import convert_to_utc


class BatchJobSchedular:
    @staticmethod
    def create_job_schedule(data):
        """
        Create a job schedule based on the provided data.

        Args:
            data (dict): A dictionary containing the job schedule parameters.

        Returns:
            tuple: A tuple containing the JobScheduleAddParameter object and the job schedule ID.
        """
        job_schedule_id = BatchJobSchedular.generate_job_schedule_id()
        do_not_run_until = convert_to_utc(data['do_not_run_until'])
        do_not_run_after = convert_to_utc(data['do_not_run_after'])
        cron_expression = data['cron_expression']

        # Parse the cron expression
        parsed_cron = parse_cron_expression(cron_expression)
        recurrence_interval = convert_cron_to_iso8601(parsed_cron)

        # Define the recurrence schedule
        recurrence = batchmodels.Schedule(
            do_not_run_until=do_not_run_until,
            do_not_run_after=do_not_run_after,
            recurrence_interval=recurrence_interval
        )

        # Define the job manager task
        job_manager_task = batchmodels.JobManagerTask(
            id='JobManagerTask',
            command_line='your_command_line_here',
            display_name='your_display_name_here'
        )

        # Define the job specification
        job_spec = batchmodels.JobSpecification(
            priority=0,  # Default priority
            pool_info=batchmodels.PoolInformation(pool_id='mypool'),
            job_manager_task=job_manager_task
        )

        # Define the job schedule
        job_schedule = batchmodels.JobScheduleAddParameter(
            id=job_schedule_id,
            schedule=recurrence,
            job_specification=job_spec
        )
        
        return job_schedule, job_schedule_id

    @staticmethod
    def generate_job_schedule_id():
        """
        Generate a unique job schedule ID.

        Returns:
            str: A unique job schedule ID.
        """
        return str(uuid.uuid4())
