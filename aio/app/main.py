import asyncio
import threading
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from jinja2 import Environment, FileSystemLoader

from orchestrator import (
    deploy_all, stop_all, update_all, remove_all_containers,
    get_all_statuses, is_provisioned, STATE_FILE,
)

app = FastAPI(title="Odysseus AIO")

templates = Environment(loader=FileSystemLoader(Path(__file__).parent / "templates"))

deploy_in_progress = False
deploy_log = []
deploy_complete = False
deploy_result = None

stop_in_progress = False
stop_log = []
stop_complete = False

update_in_progress = False
update_log = []
update_complete = False

remove_in_progress = False
remove_log = []
remove_complete = False


def deploy_thread():
    global deploy_in_progress, deploy_log, deploy_complete, deploy_result
    deploy_log = []
    deploy_in_progress = True
    deploy_complete = False
    deploy_result = None

    def log(msg):
        deploy_log.append(msg)

    result = deploy_all(log_callback=log)
    deploy_result = result
    deploy_complete = True
    deploy_in_progress = False


def stop_thread():
    global stop_in_progress, stop_log, stop_complete
    stop_log = []
    stop_in_progress = True
    stop_complete = False

    def log(msg):
        stop_log.append(msg)

    stop_all(log_callback=log)
    stop_complete = True
    stop_in_progress = False


def update_thread():
    global update_in_progress, update_log, update_complete
    update_log = []
    update_in_progress = True
    update_complete = False

    def log(msg):
        update_log.append(msg)

    update_all(log_callback=log)
    update_complete = True
    update_in_progress = False


def remove_thread():
    global remove_in_progress, remove_log, remove_complete
    remove_log = []
    remove_in_progress = True
    remove_complete = False

    def log(msg):
        remove_log.append(msg)

    remove_all_containers(log_callback=log)
    remove_complete = True
    remove_in_progress = False


@app.on_event("startup")
async def startup():
    if not is_provisioned():
        t = threading.Thread(target=deploy_thread, daemon=True)
        t.start()


@app.get("/", response_class=HTMLResponse)
async def index():
    statuses = get_all_statuses()
    html = templates.get_template("index.html").render(
        statuses=statuses,
        deploy_in_progress=deploy_in_progress,
        deploy_log=deploy_log,
        deploy_complete=deploy_complete,
        deploy_result=deploy_result,
        stop_in_progress=stop_in_progress,
        stop_log=stop_log,
        stop_complete=stop_complete,
        update_in_progress=update_in_progress,
        update_log=update_log,
        update_complete=update_complete,
        remove_in_progress=remove_in_progress,
        remove_log=remove_log,
        remove_complete=remove_complete,
    )
    return html


@app.get("/api/status")
async def api_status():
    statuses = get_all_statuses()
    return {
        "containers": statuses,
        "provisioned": is_provisioned(),
        "deploy_in_progress": deploy_in_progress,
        "deploy_complete": deploy_complete,
        "deploy_result": deploy_result,
        "deploy_log": deploy_log,
        "stop_in_progress": stop_in_progress,
        "stop_complete": stop_complete,
        "stop_log": stop_log,
        "update_in_progress": update_in_progress,
        "update_complete": update_complete,
        "update_log": update_log,
        "remove_in_progress": remove_in_progress,
        "remove_complete": remove_complete,
        "remove_log": remove_log,
    }


@app.post("/api/deploy")
async def api_deploy():
    global deploy_in_progress, deploy_complete, deploy_result, deploy_log
    if deploy_in_progress:
        return JSONResponse({"error": "Deploy already in progress"}, status_code=409)
    t = threading.Thread(target=deploy_thread, daemon=True)
    t.start()
    return {"status": "started"}


@app.post("/api/stop")
async def api_stop():
    global stop_in_progress, stop_complete, stop_log
    if stop_in_progress:
        return JSONResponse({"error": "Stop already in progress"}, status_code=409)
    t = threading.Thread(target=stop_thread, daemon=True)
    t.start()
    return {"status": "started"}


@app.post("/api/update")
async def api_update():
    global update_in_progress, update_complete, update_log
    if update_in_progress:
        return JSONResponse({"error": "Update already in progress"}, status_code=409)
    t = threading.Thread(target=update_thread, daemon=True)
    t.start()
    return {"status": "started"}


@app.post("/api/remove")
async def api_remove():
    global remove_in_progress, remove_complete, remove_log
    if remove_in_progress:
        return JSONResponse({"error": "Remove already in progress"}, status_code=409)
    t = threading.Thread(target=remove_thread, daemon=True)
    t.start()
    return {"status": "started"}
