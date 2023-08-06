import config as cfg
import requests
import json

"""
USAGE:
First you have to init factory with base settings
factory = RequestFactory(stage=${STAGE}, version=${VERSION}, api_key=${API_KEY})

Then need to create request instance depend on the type of the request you want to send
metrics_request = factory.create_request("Metrics")

Pass the data to set_data function
metrics_request.set_data(
    agent_version,
    overview,
    plugins
)

Then send it to the BackEnd and receive the response
response = metrics_request.send()
"""


class RequestFactory:
    requests = {}
    stage = None
    version = None
    api_key = None

    def __init__(self, stage, version, api_key):
        self.stage = stage
        self.version = version
        self.api_key = api_key

    def create_request(self, request_type):
        if request_type not in RequestFactory.requests:
            RequestFactory.requests[request_type] = eval(request_type + '.Factory(self.stage, self.version, self.api_key)')
        return RequestFactory.requests[request_type].create()


class Request(object):
    stage = None
    version = None
    api_key = None
    prefix = None
    api_base = None

    def __init__(self, stage, version, api_key):
        self.stage = stage
        self.version = version
        self.api_key = api_key
        self.prefix = ""
        if self.stage == 'staging':
            self.prefix = "-staging"
        self.api_base = "https://api{}.cloudvisor.io".format(self.prefix)

    def send(self):
        res = requests.post(
            self.build_url(),
            data=json.dumps(self.message, separators=(',', ':'))
        )
        return self.Response(res)


class Metrics(Request):
    message = {}

    def build_url(self):
        return '{}{}'.format(self.api_base, cfg.post_metrics_ep)

    def set_data(self, agent_version, overview, plugins):
        self.message = {
            "agent": {
                "version": agent_version
            },
            "overview": overview,
            "plugins": plugins
        }

    class Response:
        raw_data: str = None
        status_code = None

        def __init__(self, res):
            self.status_code = res.status_code
            self.raw_data = res.json()
            for k, v in self.raw_data.items():
                exec('self.' + k + '=v')

    class Factory:
        stage = None
        version = None
        api_key = None

        def __init__(self, stage, version, api_key):
            self.stage = stage
            self.version = version
            self.api_key = api_key

        def create(self): return Metrics(stage=self.stage, version=self.version, api_key=self.api_key)


class FsResizeAllowed(Request):
    message = {}

    def build_url(self):
        return '{}{}'.format(self.api_base, cfg.fs_resize_allowed_ep)

    def set_data(self, filesystems, action_id, instance, fs):
        self.message = {
            "filesystems": filesystems,
            "action_id": action_id,
            "instance": instance,
            "fs_to_resize": fs
        }

    class Response:
        raw_data = None
        status_code = None
        message = None
        ready = False
        device = None
        action = None

        def __init__(self, res):
            self.status_code = res.status_code
            self.raw_data = res.json()
            self.message = self.raw_data.get('message')
            self.ready = self.raw_data.get('Ready')
            self.device = self.raw_data.get('device')
            self.action = self.raw_data.get('action')

    class Factory:
        stage = None
        version = None
        api_key = None

        def __init__(self, stage, version, api_key):
            self.stage = stage
            self.version = version
            self.api_key = api_key

        def create(self): return FsResizeAllowed(stage=self.stage, version=self.version, api_key=self.api_key)


class FsResizeCompleted(Request):
    message = {}

    def build_url(self):
        return '{}{}'.format(self.api_base, cfg.fs_resize_completed_ep)

    def set_data(self, dev_path, filesystems, action_id, exit_code, resize_output):
        self.message = {
            "dev_path": dev_path,
            "filesystems": filesystems,
            "action_id": action_id,
            "exit_code": exit_code,
            "resize_output": resize_output
        }

    class Response:
        raw_data = None
        status_code = None
        success = None
        message = None

        def __init__(self, res):
            self.status_code = res.status_code
            self.raw_data = res.json()
            self.success = self.raw_data.get('Success')
            self.message = self.raw_data.get('message')

    class Factory:
        stage = None
        version = None
        api_key = None

        def __init__(self, stage, version, api_key):
            self.stage = stage
            self.version = version
            self.api_key = api_key

        def create(self): return FsResizeCompleted(stage=self.stage, version=self.version, api_key=self.api_key)


class FsResizeFailed(Request):
    message = {}

    def build_url(self):
        return '{}{}'.format(self.api_base, cfg.resize_failed_ep)

    def set_data(self, dev_path, filesystems, action_id, exit_code, resize_output, error, resize_steps):
        self.message = {
            "dev_path": dev_path,
            "filesystems": filesystems,
            "action_id": action_id,
            "exit_code": exit_code,
            "resize_output": resize_output,
            "error": error,
            "resize_steps": resize_steps
        }

    class Response:
        raw_data = None
        status_code = None
        success = None
        message = None

        def __init__(self, res):
            self.status_code = res.status_code
            self.raw_data = res.json()
            self.success = self.raw_data.get('Success')
            self.message = self.raw_data.get('message')

    class Factory:
        stage = None
        version = None
        api_key = None

        def __init__(self, stage, version, api_key):
            self.stage = stage
            self.version = version
            self.api_key = api_key

        def create(self): return FsResizeFailed(stage=self.stage, version=self.version, api_key=self.api_key)
