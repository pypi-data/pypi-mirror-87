# ~*~ coding: utf-8 ~*~

import datetime
import json
from collections import defaultdict

from ansible import constants
from ansible.plugins.callback.default import CallbackModule
from ansible.plugins.callback.minimal import CallbackModule as CMDCallBackModule

class CallbackMixin:
    def __init__(self, display=None):

        self.results_raw = dict(
            ok=defaultdict(dict),
            failed=defaultdict(dict),
            unreachable=defaultdict(dict),
            skippe=defaultdict(dict),
        )
        self.results_summary = dict(
            contacted=defaultdict(dict),
            dark=defaultdict(dict),
            success=True
        )
        self.results = {
            'raw': self.results_raw,
            'summary': self.results_summary,
        }
        super().__init__()
        if display:
            self._display = display
        self._display.columns = 79

    def display(self, msg):
        self._display.display(msg)

    def gather_result(self, t, result):
        self._clean_results(result._result, result._task.action)
        host = result._host.get_name()
        task_name = result.task_name
        task_result = result._result

        self.results_raw[t][host][task_name] = task_result
        self.clean_result(t, host, task_name, task_result)


class AdHocResultCallback(CallbackMixin, CallbackModule, CMDCallBackModule):
    """
    Task result Callback
    """

    def clean_result(self, t, host, task_name, task_result):
        contacted = self.results_summary["contacted"]
        dark = self.results_summary["dark"]

        if task_result.get('rc') is not None:
            cmd = task_result.get('cmd')
            if isinstance(cmd, list):
                cmd = " ".join(cmd)
            else:
                cmd = str(cmd)
            detail = {
                'cmd': cmd,
                'stderr': task_result.get('stderr'),
                'stdout': task_result.get('stdout'),
                'rc': task_result.get('rc'),
                'delta': task_result.get('delta'),
                'msg': task_result.get('msg', '')
            }
        else:
            detail = {
                "changed": task_result.get('changed', False),
                "msg": task_result.get('msg', '')
            }

        if t in ("ok", "skipped"):
            contacted[host][task_name] = detail
        else:
            dark[host][task_name] = detail

    def v2_runner_on_failed(self, result, ignore_errors=False):
        self.results_summary['success'] = False
        self.gather_result("failed", result)

        if result._task.action in constants.MODULE_NO_JSON:
            CMDCallBackModule.v2_runner_on_failed(self,
                                                  result, ignore_errors=ignore_errors
                                                  )
        else:
            super().v2_runner_on_failed(
                result, ignore_errors=ignore_errors
            )

    def v2_runner_on_ok(self, result):

        self.gather_result("ok", result)
        if result._task.action in constants.MODULE_NO_JSON:
            CMDCallBackModule.v2_runner_on_ok(self, result)
        else:
            super().v2_runner_on_ok(result)

    def v2_runner_on_skipped(self, result):
        self.gather_result("skipped", result)
        super().v2_runner_on_skipped(result)

    def v2_runner_on_unreachable(self, result):
        self.results_summary['success'] = False
        self.gather_result("unreachable", result)
        super().v2_runner_on_unreachable(result)

    def display_skipped_hosts(self):
        pass

    def display_ok_hosts(self):
        pass

    def display_failed_stderr(self):
        pass


class CommandResultCallback(AdHocResultCallback):
    """
    Command result callback

    results_command: {
      "cmd": "",
      "stderr": "",
      "stdout": "",
      "rc": 0,
      "delta": 0:0:0.123
    }
    """

    def __init__(self, display=None, **kwargs):

        self.results_command = dict()
        self.log = []

        super().__init__(display)

        # print('self.foo',self.foo)

    def gather_result(self, t, res):
        super().gather_result(t, res)
        self.gather_cmd(t, res)

    def v2_playbook_on_play_start(self, play):
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        msg = '$ {} ({})'.format(play.name, now)
        self._play = play
        self._display.banner(msg)
        self.log.append("%s\r\n" % msg)

        # print('self._play.name', self._play.name)

    def v2_runner_on_ok(self, result):
        print('v2_runner_item_on_ok')
        self.results_summary['success'] = True


        ret = "%s | CHANGED | rc=%s => \r\n%s\r\n" % (
            result._host.get_name(), result._result.get("rc"), result._result.get("stdout",'').replace('\n', '\r\n'))

        self._display.display(ret)

        self.log.append(ret)


    def v2_runner_on_unreachable(self, result):
        self.results_summary['success'] = False
        self.gather_result("unreachable", result)
        msg = result._result.get("msg")

        if not msg:
            msg = json.dumps(result._result, indent=4)

        ret = "%s | FAILED! => \r\n%s\r\n" % (result._host.get_name(), msg,)

        self._display.display(ret, color=constants.COLOR_ERROR)

        self.log.append(ret)


    def v2_runner_on_failed(self, result, ignore_errors=False):
        self.results_summary['success'] = False
        self.gather_result("failed", result)
        msg = result._result.get("msg", '')
        stderr = result._result.get("stderr")
        if stderr:
            msg += '\n' + stderr
        module_stdout = result._result.get("module_stdout")
        if module_stdout:
            msg += '\n' + module_stdout
        if not msg:
            msg = json.dumps(result._result, indent=4)

        ret = "%s | FAILED! => \r\n%s\r\n" % (result._host.get_name(), msg,)

        self._display.display(ret, color=constants.COLOR_ERROR)

        self.log.append(ret)



    def _print_task_banner(self, task):
        pass

    def gather_cmd(self, t, res):
        host = res._host.get_name()
        cmd = {}
        if t == "ok":
            cmd['cmd'] = res._result.get('cmd')
            cmd['stderr'] = res._result.get('stderr')
            cmd['stdout'] = res._result.get('stdout')
            cmd['rc'] = res._result.get('rc')
            cmd['delta'] = res._result.get('delta')
        else:
            cmd['err'] = "Error: {}".format(res)

        self.results_command[host] = cmd


class CmdRedisResultCallback(CommandResultCallback):

    def v2_playbook_on_play_start(self, play):
        super().v2_playbook_on_play_start(play)

    def v2_runner_on_unreachable(self, result):
        super().v2_runner_on_unreachable(result)

    def v2_runner_on_failed(self, result, ignore_errors=False):
        super().v2_runner_on_failed(result, ignore_errors=ignore_errors)


class PlaybookResultCallBack(CMDCallBackModule):
    pass
