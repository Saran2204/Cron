from flask import Flask
from flask_restx import Api
from api.job_manager import job_manager_api


app = Flask(__name__)
api = Api(app, version='1.0', doc='/swagger', title='Job Scheduler API', description='A simple job scheduler API')

# Register API namespaces
api.add_namespace(job_manager_api)

if __name__ == '__main__':
    app.run(debug=True)
