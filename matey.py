
# DEV
from pprint import pp

import sys
import yaml
from yaml.loader import SafeLoader

try:
    with open('config.yaml') as f:
        configs = yaml.load(f, Loader=SafeLoader)
except Exception as e:
    sys.exit(f'Could not open config file: {e}')

from prometheus_matey_exporter.engine.handler import MateyHandler
from prometheus_matey_exporter.engine.processor import MateyDataProcessorSonarr

handler = MateyHandler()
controller = MateyDataProcessorSonarr()

if 'sonarr' in configs['arr'].keys():
    from prometheus_matey_exporter.arr import sonarr
    for i in configs['arr']['sonarr']:
        handler.add_source(sonarr.matey_sonarr(i['url'], i['api_key'], i['instance_name']))
 
#import os   
#from dotenv import load_dotenv
#load_dotenv()


from prometheus_client import start_http_server, Info
import time

i = Info('matey_build_version', 'Prometheus Matey Exporter build version')
i.info({'version': '0.0.1', 'buildhost': 'foo@bar'})

if __name__ == '__main__':
    
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
            controller.get_data(source)
            time.sleep(1)
