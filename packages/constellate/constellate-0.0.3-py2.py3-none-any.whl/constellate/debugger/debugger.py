import sys
from typing import List


def debugger_setup(enabled=False, host="host.docker.internal", port=4444):
    if enabled is True:
        sys.path.append("pydevd-pycharm.egg")
        import pydevd_pycharm

        pydevd_pycharm.settrace(
            host, port=port, stdoutToServer=True, stderrToServer=True, suspend=False
        )


def debugger_setup_stage(stage: str = None, enabled_stages: List[str] = []):
    debugger_setup(enabled=stage in enabled_stages)
