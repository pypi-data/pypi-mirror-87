import base64
import json
import os
import time
import tempfile
import ssl
import jwt

from ..logging import ZdmLogger

logger = ZdmLogger().get_logger()

# Load zdevice.json file
def load_zdevice(root_zdevice, file="zdevice.json"):
    path = os.path.join(root_zdevice, file)
    logger.info("Reading credential file: '{}'".format(path))
    with open(path) as ff:
        content = json.load(ff)
        return content


def default_time_func():
    return int(time.time())


class Credentials():

    def __init__(self, root_zdevice):
        if isinstance(root_zdevice, dict):
            logger.debug("Reading zdevice.json from dict: {}".format(root_zdevice))
            nfo = root_zdevice
        else:
            try:
                nfo = load_zdevice(root_zdevice)
            except Exception as e:
                logger.error("Can't load device provisioning info. {}".format( e))
                raise e
        logger.debug("Credential file: {}'".format(nfo))
        self.device_id = nfo["devinfo"]["device_id"]
        self.mode = nfo["devinfo"]["mode"]
        self.secret = nfo["prvkey"]
        self.endpoint = nfo["endpoint"]["host"]
        self.port = nfo["endpoint"]["port"]
        self.key_id = nfo["devinfo"].get("key_id", 0)
        self.key_type = nfo["devinfo"].get("key_type", "sym")

        self.endpoint_mode = nfo["endpoint"].get("mode", "secure")
        logger.info("Credential type: '{}' Endpoint mode: '{}'".format(self.mode, self.endpoint_mode))

        if self.endpoint_mode == "secure":
            if self.mode == "device_token" or self.mode == "cloud_token":
                # Save ca_cert into temporary file
                cacert = nfo.get("cacert", "")
                if cacert != "":
                    self.caCertPath = self._save_to_tempfile(cacert)
                else:
                    raise Exception("Empty ca cert file")

            else:
                # Save cli_cert and prvkey into temporary files
                clicert = nfo.get("clicert", "")
                if clicert != "":
                    self.cliCertPath = self._save_to_tempfile(clicert)
                if self.secret != "":
                    self.prvKeyClientPath = self._save_to_tempfile(self.secret)



    def configure_mqtt_client(self, client):
        if self.endpoint_mode == "secure":
            if self.mode=="device_token" or self.mode=="cloud_token":
                logger.debug("Reading Ca cert path: {}".format(self.caCertPath))
                client.client.tls_set(
                    ca_certs=self.caCertPath,
                    cert_reqs=ssl.CERT_REQUIRED,
                    tls_version=ssl.PROTOCOL_TLSv1_2
                )
            else:
                logger.debug("Reading Ca Cert path: {}".format(self.caCertPath))
                logger.debug("Reading Client cert from path: {} ".format(self.cliCertPath))
                logger.debug("Reading Private Key cert from path: {} ".format(self.prvKeyClientPath))
                # options=ssl.CERT_REQUIRED | ssl.SERVER_AUT
                client.client.tls_set(
                    ca_certs=self.caCertPath,
                    cert_reqs=ssl.CERT_REQUIRED,
                    certfile=self.cliCertPath,
                    keyfile=self.prvKeyClientPath,
                    tls_version=ssl.PROTOCOL_TLSv1_2,
                )
        if self.mode == "cloud_token":
            client.set_username_pw(self.device_id, self.secret)
        elif self.mode == "device_token":
            token = self.generate_token()
            client.set_username_pw(self.device_id, token)
        else:
            logger.debug("Unsupported mode")
            raise Exception("Unsupported mode")

    def generate_token(self):
        # get current timestamp
        ts = default_time_func()
        payload = {"sub": self.device_id, "key": self.key_id, "exp": ts + 3600}
        # encode token
        secret = base64.b64decode(self.secret)
        token = jwt.encode(payload, secret, 'HS256' if self.key_type == "sym" else "ES256")
        logger.debug("Generated Jwt Token: '{}'".format(token))
        return token

    def _save_to_tempfile(self, content):
        path = os.path.join(tempfile.gettempdir(), os.urandom(24).hex())
        logger.debug("Saving '{}' to file path '{}'".format(content, path))
        with open(path, 'w') as fp:
            fp.write(content)
            fp.flush()
        return path

class Config():
    def __init__(self, keepalive=60):
        self.keepalive = keepalive
        # self.cycle_timeout=cycle_timeout
        # self.command_timeout=command_timeout
        self.sock_keepalive = [1, 10, 5]
        self.clean_session = True
        self.qos_publish = 0
        self.qos_subscribe = 1
