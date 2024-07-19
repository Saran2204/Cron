import logging

from flask import request, jsonify
from flask_restx import Namespace, Resource, fields, reqparse

from azure_connector import batch_client
from api.job_schedular import BatchJobSchedular

logger = logging.getLogger(__name__)

job_manager_api = Namespace('jobs', description='Job operations')

# Define request headers
tenant_id_arg = job_manager_api.parser().add_argument(
    'tenant-id', location='headers', required=True, help='The tenant ID'
)
app_id_arg = job_manager_api.parser().add_argument(
    'app-id', location='headers', required=True, help='The application ID'
)

job_schedule_model = job_manager_api.model('JobSchedule', {
    'do_not_run_until': fields.String(
        required=True, description='Do not run until time in ISO 8601 format'
    ),
    'do_not_run_after': fields.String(
        required=True, description='Do not run after time in ISO 8601 format'
    ),
    'cron_expression': fields.String(
        required=True, description='Cron expression for scheduling'
    ),
})

@job_manager_api.route('/create')
class JobScheduleList(Resource):
    @job_manager_api.doc('create_jobschedule')
    @job_manager_api.expect(tenant_id_arg, app_id_arg, job_schedule_model, validate=True)
    def post(self):
        """Create a new job schedule"""
        # Extract tenant-id and app-id from headers
        tenant_id = request.headers.get('tenant-id')
        app_id = request.headers.get('app-id')
        
        if not tenant_id or not app_id:
            return {'message': 'Missing tenant-id or app-id in headers'}, 400

        data = request.json
        logger.info('Received data: %s', data)
        
        try:
            job_schedule, job_schedule_id = BatchJobSchedular.create_job_schedule(data)
            # Add the job schedule to the Batch service
            batch_client.job_schedule.add(job_schedule)
            return {'message': 'Job schedule created successfully', 'job_schedule_id': job_schedule_id}, 201
        except Exception as e:
            logger.error('Error creating job schedule: %s', e)
            return {'message': 'Failed to create job schedule'}, 500

@job_manager_api.route('/list')
class JobList(Resource):
    @job_manager_api.doc('list_jobs')
    def get(self):
        """List job schedules or get a specific job schedule by ID"""
        try:
            job_schedule_id = request.args.get('job_schedule_id')

            if job_schedule_id:
                # Retrieve the specific job schedule by ID
                job_schedule = batch_client.job_schedule.get(job_schedule_id)
                job = {
                    'job_schedule_id': job_schedule.id,
                    'display_name': job_schedule.display_name
                }
                return jsonify({'job': job})
            else:
                # Retrieve the list of all job schedules
                job_schedules = batch_client.job_schedule.list()
                jobs = [
                    {'job_schedule_id': job.id, 'display_name': job.display_name}
                    for job in job_schedules
                ]
                return jsonify({'jobs': jobs})
        except Exception as e:
            logger.error('Error listing job schedules: %s', e)
            return jsonify({'error': str(e)}), 500
        
# Define a parser for the delete endpoint
delete_parser = reqparse.RequestParser()
delete_parser.add_argument('job_schedule_id', type=str, required=True, help='Job schedule ID is required')

@job_manager_api.route('/delete')
class DeleteJob(Resource):
    @job_manager_api.doc('delete_job')
    @job_manager_api.expect(delete_parser)
    def delete(self):   
        """Delete a job schedule by ID"""
        args = delete_parser.parse_args()
        job_schedule_id = args['job_schedule_id']
        
        try:
            batch_client.job_schedule.delete(job_schedule_id)
            return {'message': 'Job schedule deleted successfully'}, 200
        except Exception as e:
            logger.error('Error deleting job schedule: %s', e)
            return {'error': str(e)}, 500