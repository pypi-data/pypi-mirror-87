import json
import logging
import os

from flask import request
from flask_restplus import Resource, Namespace

from langauge.core.service.main.database import mongo

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

env = os.environ

config_ns = Namespace('config', description='All configuration settings')


@config_ns.route('/saveConfig')
class SaveConfig(Resource):
    @config_ns.doc('download file')
    def post(self):
        tasks = request.form.get('task')
        models = request.form.get('model')
        if not os.path.isdir(env.get('CONFIG_FOLDER')):
            os.makedirs(env.get('CONFIG_FOLDER'))
        with open(os.path.join(env.get('CONFIG_FOLDER'), 'task.json'), 'w+') as outfile:
            json.dump(tasks, outfile)
        with open(os.path.join(env.get('CONFIG_FOLDER'), 'models.json'), 'w+') as outfile:
            json.dump(models, outfile)
        return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


@config_ns.route('/runConfig')  # this is a job for GET, not POST
class RunConfig(Resource):
    @config_ns.doc('download file')
    def post(self):
        data = {'task': {}, 'model': {}}
        config_dir = env.get('CONFIG_FOLDER')
        if os.path.isfile(config_dir + '/task.json'):
            with open(os.path.join(config_dir, 'task.json'), 'r+') as outfile:
                data['task'] = json.load(outfile)
            with open(os.path.join(config_dir, 'models.json'), 'r+') as outfile:
                data['model'] = json.load(outfile)
        return data, 200, {'ContentType': 'application/json'}


@config_ns.route('/models/<task>')
@config_ns.param('task', 'The task identifier')
class Models(Resource):
    @config_ns.doc('available models')
    def get(self, task):
        from bson.json_util import dumps
        documents = mongo.db.model.find_one({"task": task})
        return dumps(documents)


@config_ns.route('/task')
class Tasks(Resource):
    @config_ns.doc('available task')
    def get(self):
        from bson.json_util import dumps
        documents = mongo.db.task.find()
        return dumps(documents)


# config_app = Blueprint('config_bp', __name__, url_prefix='/config')
# config_api = Api(config_app, version='0.1')
# config_api.add_namespace(config_ns)
