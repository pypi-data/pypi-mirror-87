
import json
from dwebsocket.decorators import accept_websocket
from django.http import HttpResponse
from celery.result import AsyncResult
import logging

log = logging.getLogger("django")


@accept_websocket
def async_result(request, task_id):
    def pm(body):
        try:
            if body['status'] in ['FAILURE', 'REVOKED']:
                body['result'] = unicode(body['result'])
            # print body
            request.websocket.send(('%s\r' % json.dumps(body)).encode('utf8'))
        except Exception, e:
            import traceback
            log.error("async_result dump json error, body: %s; error: %s", body, traceback.format_exc())

    rs = AsyncResult(task_id)
    if not request.is_websocket():
        body = {'status': rs.state, 'result': unicode(rs.result)}
        return HttpResponse(json.dumps(body))

    else:
        d = dict(
            task_id=rs.task_id,
            state=rs.state,
            status=rs.status,
            result=rs.status == 'FAILURE' and unicode(rs.result) or rs.result,
            traceback=rs.traceback
        )
        pm(d)
        try:
            r = rs.get(on_message=pm, propagate=False)
        except Exception, e:
            body = {'status': 'FAILURE', 'result': unicode(e)}
            request.websocket.send(('%s\r' % json.dumps(body)).encode('utf8'))
