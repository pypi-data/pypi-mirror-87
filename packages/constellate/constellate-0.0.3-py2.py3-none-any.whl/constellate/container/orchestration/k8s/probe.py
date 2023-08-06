from pathlib import Path


def readiness(ready: bool = False, file_path: str = "/tmp/app.ready"):
    _file_proble(enabled=ready, file_path=file_path)


def liveness(live: bool = False, file_path="/tmp/app.live"):
    _file_proble(enabled=live, file_path=file_path)


def _file_proble(enabled: bool = False, file_path="/tmp/foobar"):
    p = Path(file_path)
    if enabled:
        p.touch()
    else:
        p.unlink(missing_ok=True)
