import os, sys
sys.path.append(os.path.dirname( \
os.path.dirname(os.path.realpath(__file__))))

from pyngrok import ngrok
import datetime
from .code import ImCode

def port_forward(port, force=False):
    active_tunnels = ngrok.get_tunnels()
    for tunnel in active_tunnels:
        used_port = int(tunnel.data['config']['addr'].rsplit(":")[-1])
        public_url = tunnel.public_url
        if used_port == port:
            if force:
                ngrok.disconnect(public_url)
            else:
                message = "port already used {} -> localhost:{}".format(public_url, port)
                print("[{}] {}  {}".format(datetime.datetime.utcnow().isoformat()[:-3] + "Z", "error", message))
                return

    return ngrok.connect(addr=port, options={"bind_tls": True})