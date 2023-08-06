import json
import logging
import os

from flask import jsonify, send_file
from flask_restplus import Resource, Namespace

from langauge.core.service.main.database import mongo
from langauge.core.service.main.worker import celery

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

env = os.environ
celery_task_ns = Namespace('celery', description='All task related information')


@celery_task_ns.route('/<task_id>', endpoint='task_status')
@celery_task_ns.param('task_id', 'The status identifier')
class TaskStatus(Resource):
    @celery_task_ns.doc('check status')
    def get(self, task_id):
        task = celery.AsyncResult(task_id)
        if task.state == 'PENDING':
            # job did not start yet
            response = {
                'state': task.state,
                'current': 0,
                'total': 1,
                'status': 'Pending...'
            }
        elif task.state != 'FAILURE':
            response = {
                'state': task.state,
                'current': task.info.get('current', 0),
                'total': task.info.get('total', 1),
                'status': task.info.get('status', '')
            }
            response['id'] = task_id
            if 'preview' in task.info:
                response['preview'] = task.info['preview']
            if 'time' in task.info:
                response['time'] = task.info['time']
        else:
            # something went wrong in the background job
            response = {
                'state': task.state,
                'current': 1,
                'total': 1,
                'status': str(task.info),  # this is the exception raised
            }
        return jsonify(response)


@celery_task_ns.route('/fileDownload/<task_id>')
@celery_task_ns.param('task_id', 'The task_id identifier')
class DownloadFile(Resource):
    @celery_task_ns.doc('download file')
    def get(self, task_id):
        outputs = env.get('OUTPUT_FOLDER') + '/' + task_id + '-00000-of-00001'
        # print(outputs)
        return send_file(outputs,
                         mimetype='text/csv',
                         attachment_filename='results.txt',
                         as_attachment=True)


def task_already_running(channel):
    logger.info('task_already_running')
    i = celery.control.inspect()
    if i.active() is not None:
        for key, value in i.active().items():
            if len(value) >= 2:
                logger.log("there are already 2 task runing, Please submit after some time !!")
                return True
            # for task in value:
            #     if task.get('id') == channel:
            #         return True
        return False


@celery_task_ns.route('/history')
class TaskHistory(Resource):
    @celery_task_ns.doc('task history')
    def get(self):
        documents = mongo.db.celery_taskmeta.find()
        taskList = []
        for history in documents:
            history['id'] = history.pop('_id')
            result = json.loads(history.pop('result'))
            history['model'] = result.get('model', '')
            history['task'] = result.get('task', '')
            taskList.append(history)
        return taskList


# celery_task_app = Blueprint('celery_task_bp', __name__, url_prefix='/celery')
# celery_task_api = Api(celery_task_app, version='0.1')
# celery_task_api.add_namespace(celery_task_ns)