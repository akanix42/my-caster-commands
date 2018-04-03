import json
import urllib2

from dragonfly import Function, ActionBase, ActionError


def send_command(command):
    req = urllib2.Request('http://localhost:8089/action')
    req.add_header('Content-Type', 'application/json')
    res = urllib2.urlopen(req, json.dumps({'action': command}))


class IdeaAction(ActionBase):
    def __init__(self, action_id):
        ActionBase.__init__(self)
        self.action_id = action_id

    def _execute(self, data = None):
        try:
            send_command(self.action_id)
        except Exception, e:
            self._log.exception("Exception sending command %s:" % self.action_id)
            raise ActionError("%s: %s" % (self, e))


def intellijAction(command):
    def on_called():
        send_command(command)

    return on_called
