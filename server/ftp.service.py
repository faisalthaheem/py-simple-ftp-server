"""
   Copyright 2019 Faisal Thaheem

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""

from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
from pyftpdlib.authorizers import DummyAuthorizer

import argparse
import pprint
import signal
import logging
import yaml
import os


#create logger
logger = logging.getLogger('ftp.service')
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
fh = logging.FileHandler('ftp.service.log')
fh.setLevel(logging.DEBUG)
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
# create formatter and add it to the handlers
formatter = logging.Formatter('[%(levelname)1.1s %(asctime)s] %(message)s',"%Y-%m-%d %H:%M:%S")
fh.setFormatter(formatter)
ch.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)

ap = argparse.ArgumentParser()
ap.add_argument("-cf", "--config.file", default='./config/ftp.service.yaml',
        help="Config file describing service parameters")
args = vars(ap.parse_args())

# ftp related
server = None
dispatcherThread = None

config = None

########## FTP Section
class MyHandler(FTPHandler):

    def on_connect(self):
        logger.info("%s:%s connected" % (self.remote_ip, self.remote_port))

    def on_disconnect(self):
        # do something when client disconnects
        pass

    def on_login(self, username):
        # do something when user login
        pass

    def on_logout(self, username):
        # do something when user logs out
        pass

    def on_file_sent(self, file):
        # do something when a file has been sent
        pass

    def on_file_received(self, file):
        try:
            file_name = os.path.basename(file)
                        
        except:
            logger.error("An error occurred: ", exc_info=True)
        pass
    
    def readFileContent(self, path):
        with open(path, 'rb') as content_file:
            return content_file.read()

    def on_incomplete_file_sent(self, file):
        # do something when a file is partially sent
        pass

    def on_incomplete_file_received(self, file):
        # remove partially uploaded files
        os.remove(file)


def main():

    global config
    global server
    try:

        with open(args["config.file"]) as stream:
            try:
                if os.getenv('PRODUCTION') is not None: 
                        config = yaml.safe_load(stream)['prod']
                else:
                        config = yaml.safe_load(stream)['dev']

                pprint.pprint(config)
            except yaml.YAMLError as err:
                logger.error("An error occurred: ", exc_info=True)

        authorizer = DummyAuthorizer()
        
        for acc in config['accounts']:
            #ensure the upload dir exists
            os.makedirs(acc['upload-path'],exist_ok=True)

            authorizer.add_user(acc['username'], acc['password'], homedir=acc['upload-path'], perm='elradfmwMT')
            
        handler = MyHandler
        handler.authorizer = authorizer

        server = FTPServer(('0.0.0.0', config['server_port']), handler)
        server.serve_forever()
    except:
        logger.error("An error occurred: ", exc_info=True)

def signal_handler(sig, frame):
    try:
        logger.info("Ctrl-c pressed, stopping")
        server.close_all()
    except:
        logger.error("An error occurred: ", exc_info=True)
    
#handle ctrl-c
signal.signal(signal.SIGINT, signal_handler)
main()
