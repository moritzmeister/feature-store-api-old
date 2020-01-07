import os
import requests

class Client: 

    TOKEN_FILE = "token.jwt"
    ENV_REST_ENDPOINT = "REST_ENDPOINT"
    ENV_VERIFY = "REQUEST_VERIFY"
    DOMAIN_CA_TRUSTSTORE_PEM = "DOMAIN_CA_TRUSTSTORE_PEM"

    def __init__(): 
        self._host = _get_host()
        # TODO(Fabio) : Have a thread that refreshes the token
        self._token = _read_jwt()
        self._verify = _get_verify()
        self._session = request.session() 


    def get_feature_group(self, feature_store_id, feature_group_name, version):
        


    def _get_verify(self):
        """
        Get verification method for sending HTTP requests to Hopsworks.
        Credit to https://gist.github.com/gdamjan/55a8b9eec6cf7b771f92021d93b87b2c
        Returns:
            if env var HOPS_UTIL_VERIFY is not false
                then if hopsworks certificate is self-signed, return the path to the truststore (PEM)
                else if hopsworks is not self-signed, return true
            return false
        """
        if ENV_VERIFY in os.environ and os.environ[ENV_VERIFY] == 'true':

            hostname_idna = idna.encode(hostname)
            sock = socket.socket()

            sock.connect((hostname, int(port)))
            ctx = SSL.Context(SSL.SSLv23_METHOD)
            ctx.check_hostname = False
            ctx.verify_mode = SSL.VERIFY_NONE

            sock_ssl = SSL.Connection(ctx, sock)
            sock_ssl.set_connect_state()
            sock_ssl.set_tlsext_host_name(hostname_idna)
            sock_ssl.do_handshake()
            cert = sock_ssl.get_peer_certificate()
            crypto_cert = cert.to_cryptography()
            sock_ssl.close()
            sock.close()

            try:
                commonname = crypto_cert.subject.get_attributes_for_oid(NameOID.COMMON_NAME)[0].value
                issuer = crypto_cert.issuer.get_attributes_for_oid(NameOID.COMMON_NAME)[0].value
                if commonname == issuer and DOMAIN_CA_TRUSTSTORE_PEM_ENV_VAR in os.environ:
                    return os.environ[DOMAIN_CA_TRUSTSTORE_PEM_ENV_VAR]
                else:
                    return True
            except x509.ExtensionNotFound:
                return True

        return False


    def _get_host(self):
        """
        Returns:
            The hopsworks REST endpoint for making requests to the REST API

        """
        return os.environ[REST_ENDPOINT]


    def _read_jwt(self):
        """
        Retrieves jwt from local container.

        Returns:
            Content of jwt.token file in local container.
        """
        with open(TOKEN_FILE, "r") as jwt:
            return jwt.read()


    def _send_request(self, method, path_param, query_param, headers, data):
        path_param.insert(0, self._host)
        url = str.join("/", path_param)

        headers['Authorization'] = "Bearer " + self._token

        request = requests.Request(method, url=url, headers=headers, params=params) 
        prepped = self._session.prepare_request(request)
        response = self._session.send(prepped, verify=self._verify)

        if response.status_code // 100 != 2:
            error_object = response.json()
            raise RestAPIError("Metadata operation error: (url: {}). Server response: \n" \
                    "HTTP code: {}, HTTP reason: {}, error code: {}, error msg: {}, user msg: {}".format(
                        url,
                        response.status_code,
                        response.reason,
                        error_object.get('errorCode', ""),
                        error_object.get('errorMsg', ""),
                        error_object.get('usrMsg', "")
                    )
        else
            return response.json()



class RestAPIError(Exception)