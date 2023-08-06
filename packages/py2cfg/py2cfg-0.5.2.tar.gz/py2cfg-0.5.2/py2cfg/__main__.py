import argparse
import os
import pty
import sys
import logging
from logging.handlers import DatagramHandler
from pudb.debugger import Debugger
from pudb.run import main as pudb_main

# Relative and absolute version of the same thing for interpreter tolerance
sys.path.append("..")
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

parser = argparse.ArgumentParser(
    description="Generate control flow graphs on debugger step"
)
parser.add_argument(
    "file",
    help="Path to main file",
    type=str,
)
parser.add_argument(
    "-p",
    "--port",
    help="Serve control flow graphs locally at port",
    type=int,
    default=8000,
)
parser.add_argument(
    "--wsport",
    help="Websocket port",
    type=int,
)
parser.add_argument(
    "--directory",
    help="Serve control flow graphs here",
    default=os.environ["HOME"],
)
parser.add_argument(
    "-l",
    "--level",
    help="Logging level",
    type=str,
    default="WARN",
    choices=[
        "DEBUG",
        "INFO",
        "CRITICAL",
        "ERROR",
    ]
)
parser.add_argument(
    "--logger-port",
    type=int,
    help="Bind socket logger at port",
    default=None,
)
parser.add_argument(
    "--logger-output",
    type=str,
    help="logging destination",
    default="/dev/null"
)
parser.add_argument(
    "--browser",
    type=str,
    help="Render graphs in browser",
    default="xdg-open",
)

optarg = parser.parse_args()
if not os.path.exists(optarg.file):
    raise OSError(f"{optarg.file} not found")
elif os.path.isdir(optarg.file):
    raise OSError(f"{optarg.file} is a directory")

os.environ["PY2CFG_SERVER_PORT"] = str(optarg.port)
os.environ["PY2CFG_SOCKET_PORT"] = str(
    optarg.port + 1 if optarg.wsport is None else optarg.wsport
)
if not os.path.exists(optarg.directory):
    raise OSError(f"{optarg.directory} does not exist")
elif os.path.exists(directory := os.path.join(optarg.directory, ".py2cfg")):
    raise OSError(f"{directory} exists")

os.environ["PY2CFG_SERVE_AT"] = optarg.directory
os.environ["PY2CFG_LOGGER_OUT"] = optarg.logger_output
os.environ["PY2CFG_BROWSER"] = optarg.browser
os.environ["PY2CFG_LOGLEVEL"] = optarg.level

logger = logging.getLogger()
logger.setLevel(getattr(logging, optarg.level))
sock_handler = DatagramHandler(
    "",
    optarg.port + 2 if optarg.logger_port is None else optarg.logger_port
)
sock_handler.setFormatter(logging.Formatter("%(process)s - %(message)s"))

logger.addHandler(sock_handler)
if os.path.isfile(optarg.logger_output):
    filehandler = logging.FileHandler(optarg.logger_output)
    filehandler.setFormatter(logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    ))
    logger.addHandler(filehandler)
else: # TODO redirect to atty
    pass

if (child := pty.fork()[0]) == 0:
    from py2cfg._serve import serve
    serve(optarg.port) # start http server
else:
    from py2cfg._debug_hooks import debug_init
    from py2cfg._serve import set_pid
    set_pid(child) # child is deleted from globals by pudb
    debug_init(Debugger, optarg.file, optarg.port)
    pudb_main()
    
    # pudb wipes globals so reimport
    from os import kill
    from signal import SIGINT
    from py2cfg._serve import get_pid
    kill(get_pid(), SIGINT)
