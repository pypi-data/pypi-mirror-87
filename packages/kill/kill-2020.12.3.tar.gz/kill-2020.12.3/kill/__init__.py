__all__ = ['kill']


import subprocess
import values


def _kill_args(pid):
    return ["kill"] + list(map(str, values.get(pid)))


def kill(pid):
    """kill process by pid and return stderr"""
    if not pid:
        return
    args = _kill_args(pid)
    process = subprocess.Popen(
        args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = process.communicate()
    return err.decode().rstrip()
