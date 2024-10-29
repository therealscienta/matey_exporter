
# DEV
from pprint import pp

import sys
import yaml
from yaml.loader import SafeLoader
from pathlib import Path

from dotenv import load_dotenv
load_dotenv()

from requests.packages import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# TODO: make OS agnostic
try:
    with open(str(Path(__file__).parent.absolute()) + '\\config.yaml') as f:
        config = yaml.load(f, Loader=SafeLoader)
except Exception as e:
    sys.exit(f'Could not open config file: {e}')

if __name__ == '__main__':
    

    from utils import MateyHandler, load_submodules

    handler = MateyHandler()
    load_submodules(config, handler)

    from prometheus_client import start_http_server, Info
    import time

    i = Info('matey_build_version', 'Prometheus Matey Exporter build version')
    i.info({'version': '0.0.1', 'build': 'XXXXXXXX'})
    
    # from flask import Flask
    # from werkzeug.middleware.dispatcher import DispatcherMiddleware
    # from prometheus_client import make_wsgi_app

    # # Create my app
    # app = Flask(__name__)

    # # Add prometheus wsgi middleware to route /metrics requests
    # app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
    #     '/metrics': make_wsgi_app()
    # })
    
    # Start up the server to expose the metrics.
    start_http_server(8000)
    while True:
        for source in handler.sources:
            source.update()
            time.sleep(1)
