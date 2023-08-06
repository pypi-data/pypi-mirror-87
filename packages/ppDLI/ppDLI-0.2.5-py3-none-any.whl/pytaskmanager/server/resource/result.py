# -*- coding: utf-8 -*-
"""
Resources below '/<api_base>/result'
"""
import logging

from flask import g, request, url_for
from flask_restful import Resource, abort
from requests import codes as rqc # todo remove and use HTTPStatus
from http import HTTPStatus
from . import parse_datetime
from . import with_user_or_node, with_node, only_for
from ._schema import *
from flasgger import swag_from
from http import HTTPStatus
from pathlib import Path

from pytaskmanager.server import db, socketio, api

module_name = __name__.split('.')[-1]
log = logging.getLogger(module_name)


def setup(api, api_base):

    path = "/".join([api_base, module_name])
    log.info('Setting up "{}" and subdirectories'.format(path))
    
    api.add_resource(
        Result,
        path,
        endpoint='result_without_id',
        methods=('GET',)
    )
    api.add_resource(
        Result,
        path + '/<int:id>',
        endpoint='result_with_id',
        methods=('GET', 'PATCH')
    )


# Schemas
result_schema = ResultSchema()
result_inc_schema = ResultTaskIncludedSchema()


# ------------------------------------------------------------------------------
# Resources / API's
# ------------------------------------------------------------------------------
class Result(Resource):
    """Resource for /api/task"""

    @only_for(['node', 'user', 'container'])
    @swag_from(str(Path(r"swagger/get_result_with_id.yaml")),endpoint="result_with_id")
    @swag_from(str(Path(r"swagger/get_result_without_id.yaml")), endpoint="result_without_id")
    def get(self, id=None):
        if id:
            t = db.TaskResult.get(id)
        else:
            session = db.Session()
            q = session.query(db.TaskResult)

            if request.args.get('state') == 'open':
                q = q.filter(db.TaskResult.finished_at == None)

            if request.args.get('node_id'):
                q = q.filter_by(node_id=request.args.get('node_id'))
            
            if request.args.get('task_id'):
                q = q.filter_by(task_id=request.args.get('task_id'))

            t = q.all()

        if request.args.get('include') == 'task':
            s = result_inc_schema
        else:
            s = result_schema

        return s.dump(t, many=not bool(id)), HTTPStatus.OK

    @with_node
    @swag_from(str(Path(r"swagger/patch_result_with_id.yaml")), endpoint="result_with_id")
    def patch(self, id):
        """Update a Result."""
        data = request.get_json()
        result = db.TaskResult.get(id)

        if result.node_id != g.node.id:
            return {"msg": "This is not your result to PATCH!"}, HTTPStatus.UNAUTHORIZED

        if result.finished_at is not None:
            return {"msg": "Cannot update an already finished result!"}, HTTPStatus.BAD_REQUEST

        
        # notify collaboration nodes/users that the task has an update
        socketio.emit(
            "status_update", 
            {'result_id': id}, 
            room='collaboration_'+str(result.task.collaboration.id),
            namespace='/tasks',
        )

        url = url_for('result_with_id', id=id)
        log.debug(f'result [{url}] was updated.')

        result.started_at = parse_datetime(data.get("started_at"), result.started_at)
        result.finished_at = parse_datetime(data.get("finished_at"))
        result.result = data.get("result")
        result.log = data.get("log")

        result.save()

        return result
