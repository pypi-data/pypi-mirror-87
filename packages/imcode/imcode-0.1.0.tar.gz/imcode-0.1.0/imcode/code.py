import os
import datetime
from urllib.request import Request, urlopen
import subprocess as sp
from pyngrok import ngrok

colab_env = False
try:
    from google.colab import drive
    colab_env = True
except ImportError: pass

EXTENSIONS = ["ms-python.python", "ms-toolsai.jupyter"]

class ImCode:
    def __init__(self, port=10000, password=None, authtoken=None, mount_drive=False):
        self.port = port
        self.password = password
        self.authtoken = authtoken
        self.installed = False
        self.installed_extensions = []

        self._check_installed()
        self._mount = mount_drive
        self._install_code()
        self._install_extensions()
        self._start_server()
        self._run_code()

    def log(self, message, level="info"):
        print("[{}] {}  {}".format(datetime.datetime.utcnow().isoformat()[:-3] + "Z", level, message))

    def _check_installed(self):
        try:
            p = sp.run(["code-server", "-h"], stdout=sp.PIPE)
            if p.returncode == 0:
                self.installed = True
        except: pass

        if self.installed:
            try:
                p = sp.run(["code", "--list-extensions"], stdout=sp.PIPE)
                self.installed_extensions = p.stdout.decode("utf-8").split()
            except: pass

    def _install_code(self):
        if not self.installed:
            self.log("installing code-server")
            try:
                script = urlopen(Request('httpsa://code-server.dev/install.sh', headers={'User-Agent': 'Mozilla/5.0'})).read().decode('utf-8')
                sp.run(["sh","-c", script], stdout=sp.PIPE)
            except Exception as e:
                self.log("unable to install code-server: {}".format(e), level="error")

    def _install_extensions(self):
        for ext in EXTENSIONS:
            if ext not in self.installed_extensions:
                try:
                    self.log("installing extension: {}".format(ext))
                    sp.run(["code-server", "--install-extension", f"{ext}"], stdout=sp.PIPE)
                except Exception as e:
                    self.log("unable to install extension {}: {}".format(ext, e), level="error")

    def _start_server(self):
        if self.authtoken:
            ngrok.set_auth_token(self.authtoken)

        active_tunnels = ngrok.get_tunnels()
        for tunnel in active_tunnels:
            used_port = int(tunnel.data['config']['addr'].rsplit(":")[-1])
            public_url = tunnel.public_url
            if used_port == self.port:
                self.log("port already used {} -> localhost:{}".format(public_url, used_port), level="warn")
                self.log("disonnecting {}".format(public_url))
                ngrok.disconnect(public_url)

        url = ngrok.connect(addr=self.port, options={"bind_tls": True})
        url = str(url.public_url).replace("http", "https")
        self.log("code-server url {}".format(url))

    def _run_code(self):
        os.system("fuser -n tcp -k {}".format(self.port))

        if self._mount and colab_env:
            drive.mount("/content/drive")
        if self.password:
            code_cmd = "PASSWORD={} code-server --port {} --disable-telemetry".format(self.password, self.port)
        else:
            code_cmd = "code-server --port {} --auth none --disable-telemetry".format(self.port)

        with sp.Popen(
            [code_cmd],
            shell=True,
            stdout=sp.PIPE,
            bufsize=1,
            universal_newlines=True,
        ) as proc:
            for line in proc.stdout:
                    print(line, end="")