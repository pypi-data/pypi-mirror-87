from __future__ import absolute_import

from tornado import web

from ..utils import tasks
from ..views import BaseHandler
from ..api.tasks import BaseTaskHandler


class Timeline(BaseHandler):
    @web.authenticated
    def get(self):
        app = self.application
        events = app.events.state

        workers = sorted(events.workers.keys())
        tasks = sorted(self.capp.tasks.keys())

        self.render("timeline.html", workers=workers, tasks=tasks)


class TimelineListTasks(BaseTaskHandler):
    @web.authenticated
    def get(self):
        """
        List tasks

        **Example request**:

        .. sourcecode:: http

          GET /timeline/api/tasks HTTP/1.1
          Host: localhost:5555
          User-Agent: HTTPie/0.8.0

        **Example response**:

        .. sourcecode:: http

          HTTP/1.1 200 OK
          Content-Length: 1109
          Content-Type: application/json; charset=UTF-8
          Etag: "b2478118015c8b825f7b88ce6b660e5449746c37"
          Server: TornadoServer/3.1.1

          {
              "tasks": [{
                  "args": "[3, 4]",
                  "client": null,
                  "clock": 1079,
                  "eta": null,
                  "exception": null,
                  "exchange": null,
                  "expires": null,
                  "failed": null,
                  "kwargs": "{}",
                  "name": "tasks.add",
                  "received": 1398505411.107885,
                  "result": "'7'",
                  "retried": null,
                  "retries": 0,
                  "revoked": null,
                  "routing_key": null,
                  "runtime": 0.01610181899741292,
                  "sent": null,
                  "started": 1398505411.108985,
                  "state": "SUCCESS",
                  "succeeded": 1398505411.124802,
                  "timestamp": 1398505411.124802,
                  "traceback": null,
                  "uuid": "e42ceb2d-8730-47b5-8b4d-8e0d2a1ef7c9"
              },
              {
                  "args": "[1, 2]",
                  "client": null,
                  "clock": 1042,
                  "eta": null,
                  "exception": null,
                  "exchange": null,
                  "expires": null,
                  "failed": null,
                  "kwargs": "{}",
                  "name": "tasks.add",
                  "received": 1398505395.327208,
                  "result": "'3'",
                  "retried": null,
                  "retries": 0,
                  "revoked": null,
                  "routing_key": null,
                  "runtime": 0.012884548006695695,
                  "sent": null,
                  "started": 1398505395.3289,
                  "state": "SUCCESS",
                  "succeeded": 1398505395.341089,
                  "timestamp": 1398505395.341089,
                  "traceback": null,
                  "uuid": "f67ea225-ae9e-42a8-90b0-5de0b24507e0"
              }]
          }

        :query limit: maximum number of tasks
        :query workername: filter task by workername
        :query taskname: filter tasks by taskname
        :query state: filter tasks by state
        :query received_start: filter tasks by received date (must be greater than) format %Y-%m-%d %H:%M
        :query received_end: filter tasks by received date (must be less than) format %Y-%m-%d %H:%M
        :reqheader Authorization: optional OAuth token to authenticate
        :statuscode 200: no error
        :statuscode 401: unauthorized request
        """
        app = self.application
        limit = self.get_argument('limit', None)
        worker = self.get_argument('workername', None)
        type = self.get_argument('taskname', None)
        state = self.get_argument('state', None)
        received_start = self.get_argument('received_start', None)
        received_end = self.get_argument('received_end', None)

        limit = limit and int(limit)
        worker = worker if worker != 'All' else None
        type = type if type != 'All' else None
        state = state if state != 'All' else None

        result = []
        for task_id, task in tasks.iter_tasks(
                app.events, limit=limit, type=type,
                worker=worker, state=state,
                received_start=received_start,
                received_end=received_end):
            task = tasks.as_dict(task)

            worker = task['worker']
            task['worker'] = {
                'hostname': worker.hostname,
                'pid': worker.pid,
            }
            result.append(task)

        self.write({'tasks': result})
