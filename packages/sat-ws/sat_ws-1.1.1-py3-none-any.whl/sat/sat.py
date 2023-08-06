# -*- coding: utf-8 -*-
import base64
import logging
import time
from datetime import datetime, timedelta
from importlib import resources
from uuid import uuid1

import xmltodict
from OpenSSL import crypto

from . import templates
from . import utils
import urllib

logging.basicConfig(level=logging.INFO)
_logger = logging.getLogger(__name__)


TEMPLATES = {
    "Envelope": resources.read_text(templates.common, "Envelope.xml"),
    "KeyInfo": resources.read_text(templates.common, "KeyInfo.xml"),
    "Signature": resources.read_text(templates.common, "Signature.xml"),
    "SignedInfo": resources.read_text(templates.common, "SignedInfo.xml"),
    "Timestamp": resources.read_text(templates.login, "Timestamp.xml"),
    "LoginEnvelope": resources.read_text(templates.login, "Envelope.xml"),
    "SolicitaDescarga": resources.read_text(templates.query, "SolicitaDescarga.xml"),
    "VerificaSolicitudDescarga": resources.read_text(
        templates.verify, "VerificaSolicitudDescarga.xml"
    ),
    "PeticionDescargaMasivaTercerosEntrada": resources.read_text(
        templates.download, "PeticionDescargaMasivaTercerosEntrada.xml"
    ),
}


def ensure_login(f):
    def wrapper(*args, **kwargs):
        self = args[0]
        self.login()
        res = f(*args, **kwargs)
        return res

    return wrapper


class SAT:
    """Class to make a connection to the SAT"""

    class DownloadType:
        """Helper to select the download type"""

        ISSUED = "RfcEmisor"
        RECEIVED = "RfcReceptor"

    class RequestType:
        """Helper to select the request type"""

        CFDI = "CFDI"
        METADATA = "Metadata"

    class NoRFCException(Exception):
        """If not valid RFC founded in the certificate"""

    class NoIssuerException(Exception):
        """If not valid Issuer founded in the certificate"""

    class RequestException(Exception):
        """If there is a problem in the request"""

    class QueryException(Exception):
        """If not valid query"""

    cert = None
    key = None
    password = None
    key_pem = None
    cert_pem = None
    certificate = None
    rfc = None
    token = None
    token_expires = None

    def __init__(self, cert: bytes, key: bytes, password: str) -> None:
        """Loads the certificate, key file and password to stablish the connection to the SAT

        Creates a object to manage the SAT connection.

        Args:
            cert (bytes): DER Certificate in raw binary
            key (bytes): DER Key Certificate in raw binary
            password (str): Key password in plain text (utf-8)
        """
        self.cert = utils.binary_to_utf8(cert)
        self.key = utils.binary_to_utf8(key)
        self.password = password
        self._load_certs()
        self._compute_data_from_cert()
        _logger.info("Data correctly loaded")

    def _load_certs(self):
        """Loads the PEM version of the certificate and key file, also loads the crypto certificate

        Convert the `cert` and `key` from DER to PEM and creates the real certificate (X509)
        """
        self.key_pem = utils.der_to_pem(self.key, type="ENCRYPTED PRIVATE KEY")
        self.cert_pem = utils.der_to_pem(self.cert, type="CERTIFICATE")
        self.certificate = crypto.load_certificate(crypto.FILETYPE_PEM, self.cert_pem)

    def _compute_data_from_cert(self):
        """Gets the RFC and Issuer directly from the certificate"""
        self._get_rfc_from_cert()
        self._get_issuer_from_cert()

    def _get_rfc_from_cert(self):
        """Gets the RFC from the certificate

        Raises:
            NoRFCException: If not RFC founded
        """
        subject_components = self.certificate.get_subject().get_components()
        for c in subject_components:
            if c[0] == b"x500UniqueIdentifier":
                self.rfc = c[1].decode("UTF-8").split(" ")[0]
                _logger.debug(f"RFC {self.rfc} loaded")
                break
        else:
            raise self.NoRFCException()

    def _get_issuer_from_cert(self):
        """Gets the Issuer from the certificate

        Raises:
            NoIssuerException: If not Issuer founded
        """
        self.certificate.issuer = ",".join(
            [
                f'{c[0].decode("UTF-8")}={urllib.parse.quote(c[1].decode("UTF-8"))}'
                for c in self.certificate.get_issuer().get_components()
            ]
        )
        if not self.certificate.issuer:
            raise self.NoIssuerException()
        _logger.debug(f"Issuer {self.certificate.issuer} loaded")

    def _token_expired(self) -> bool:
        """Checks if the token expiration date is yet to come

        Returns:
            bool: True if not token or if is expired
        """
        if not self.token or not self.token_expires:
            _logger.debug("Token expired")
            return True
        return self.token_expires > datetime.utcnow()

    def _create_common_envelope(self, template: str, data: dict) -> str:
        _logger.debug("Creating Envelope")
        _logger.debug(f"{template}")
        _logger.debug(f"{data}")
        query_data, query_data_signature = utils.prepare_template(template, data)
        digest_value = utils.digest(query_data)
        signed_info = utils.prepare_template(
            TEMPLATES["SignedInfo"],
            {
                "uri": "",
                "digest_value": digest_value,
            },
        )
        key_info = utils.prepare_template(
            TEMPLATES["KeyInfo"],
            {
                "issuer_name": self.certificate.issuer,
                "serial_number": self.certificate.get_serial_number(),
                "certificate": self.cert,
            },
        )
        signature_value = self.sign(signed_info)
        signature = utils.prepare_template(
            TEMPLATES["Signature"],
            {
                "signed_info": signed_info,
                "signature_value": signature_value,
                "key_info": key_info,
            },
        )
        envelope_content = utils.prepare_template(
            query_data_signature,
            {
                "signature": signature,
            },
        )
        envelope = utils.prepare_template(
            TEMPLATES["Envelope"],
            {
                "content": envelope_content,
            },
        )
        _logger.debug("Final Envelope")
        _logger.debug(f"{envelope}")
        return envelope

    def sign(self, data) -> str:
        """Signs the `data` using SHA1 with the `key_pem` content"""
        _logger.debug(f"Signing {data}")
        private_key = crypto.load_privatekey(
            crypto.FILETYPE_PEM, self.key_pem, passphrase=self.password
        )
        signed_data = utils.binary_to_utf8(crypto.sign(private_key, data, "sha1"))
        return signed_data

    def login(self, created: datetime = None, expires: datetime = None, uuid: str = None):
        created = created or datetime.utcnow()
        expires = expires or created + timedelta(minutes=5)
        uuid = uuid or f"uuid-{uuid1()}-1"
        """If the current token is invalid, tries to login

        Args:
            created (datetime, optional): Creation date to be used in the session. Defaults to datetime.utcnow().
            expires (datetime, optional): Expiration date to be used in the session. Defaults to datetime.utcnow()+timedelta(minutes=5).
            uuid (str, optional): UUID date to be used in the session. Defaults to f'uuid-{uuid1()}-1'.
        """
        if self._token_expired():
            _logger.debug("Token expired, creating a new one")
            self.token_expires = expires
            self._login(created, expires, uuid)
            _logger.debug("New token created")

    def _login(self, created: datetime, expires: datetime, uuid: str):
        """Send login request to the SAT

        Args:
            created (datetime): Creation date to be used in the session
            expires (datetime): Expiration date to be used in the session
            uuid (str): UUID date to be used in the session

        Raises:
            RequestException: If there was an error in the request
        """
        request_content = self._get_login_soap_body(created, expires, uuid)
        response = utils.consume(
            "http://DescargaMasivaTerceros.gob.mx/IAutenticacion/Autentica",
            "https://cfdidescargamasivasolicitud.clouda.sat.gob.mx/Autenticacion/Autenticacion.svc",
            request_content,
        )
        if response.status_code != 200:
            raise self.RequestException(response.status_code, response.reason, request_content)
        else:
            self._get_login_data(utils.remove_namespaces(response.content.decode("UTF-8")))

    def _get_login_soap_body(
        self, created_object: datetime, expires_object: datetime, uuid: str
    ) -> str:
        """Creates the request body to be used in login

        Args:
            created_object (datetime): Creation date to be used in the session
            expires_object (datetime): Expiration date to be used in the session
            uuid (str): UUID date to be used in the session

        Returns:
            str: Content body
        """
        created = created_object.isoformat()
        expires = expires_object.isoformat()
        timestamp = utils.prepare_template(
            TEMPLATES["Timestamp"],
            {
                "created": created,
                "expires": expires,
            },
        )
        digest_value = utils.digest(timestamp)
        signed_info = utils.prepare_template(
            TEMPLATES["SignedInfo"],
            {
                "uri": "#_0",
                "digest_value": digest_value,
            },
        )
        signature_value = self.sign(signed_info)
        _logger.debug(
            f"""Creating Login Envelope with the next data
            "created": {created},
            "expires": {expires},
            "uuid": {uuid},
        """
        )
        envelope = utils.prepare_template(
            TEMPLATES["LoginEnvelope"],
            {
                "binary_security_token": self.cert,
                "created": created,
                "digest_value": digest_value,
                "expires": expires,
                "signature_value": signature_value,
                "uuid": uuid,
            },
        )
        return envelope

    def _get_login_data(self, response: str) -> str:
        """Gets the token from the raw response"""
        response_dict = xmltodict.parse(response)
        self.token = response_dict["Envelope"]["Body"]["AutenticaResponse"]["AutenticaResult"]

    @ensure_login
    def query(self, start: datetime, end: datetime, download_type: str, request_type: str) -> str:
        """Creates a Query in the SAT system"""
        request_content = self._get_query_soap_body(start, end, download_type, request_type)
        response = utils.consume(
            "http://DescargaMasivaTerceros.sat.gob.mx/ISolicitaDescargaService/SolicitaDescarga",
            "https://cfdidescargamasivasolicitud.clouda.sat.gob.mx/SolicitaDescargaService.svc",
            request_content,
            token=self.token,
        )
        if response.status_code != 200:
            raise self.RequestException(response.status_code, response.reason, request_content)
        else:
            id = self._get_query_id(utils.remove_namespaces(response.content.decode("UTF-8")))
            return id

    def _get_query_soap_body(
        self, start: datetime, end: datetime, download_type: str, request_type: str
    ):
        """Creates the SOAP body to the query request"""
        start = start.isoformat()
        end = end.isoformat()
        data = {
            "start": start,
            "end": end,
            "rfc": self.rfc,
            "download_type": download_type,
            "request_type": request_type,
            "signature": "",
        }
        envelope = self._create_common_envelope(TEMPLATES["SolicitaDescarga"], data)
        return envelope

    def _get_query_id(self, response: str) -> str:
        """Gets the Query ID from the raw response"""
        response_dict = xmltodict.parse(response)
        result = response_dict["Envelope"]["Body"]["SolicitaDescargaResponse"][
            "SolicitaDescargaResult"
        ]
        status_code = int(result.get("@CodEstatus", -1))
        if status_code == 5000:
            id = result["@IdSolicitud"]
            return id
        return None

    @ensure_login
    def verify(self, query_id: str) -> dict:
        """Checks the status of a Query"""
        request_content = self._get_verify_soap_body(query_id)
        response = utils.consume(
            "http://DescargaMasivaTerceros.sat.gob.mx/IVerificaSolicitudDescargaService/VerificaSolicitudDescarga",
            "https://cfdidescargamasivasolicitud.clouda.sat.gob.mx/VerificaSolicitudDescargaService.svc",
            request_content,
            token=self.token,
        )
        if response.status_code != 200:
            raise self.RequestException(response.status_code, response.reason, request_content)
        else:
            data = self._get_verify_data(utils.remove_namespaces(response.content.decode("UTF-8")))
            return data

    def _get_verify_soap_body(self, query_id: str) -> str:
        """Creates the SOAP body to check the query status"""
        data = {
            "rfc": self.rfc,
            "query_id": query_id,
            "signature": "",
        }
        envelope = self._create_common_envelope(TEMPLATES["VerificaSolicitudDescarga"], data)
        return envelope

    def _get_verify_data(self, response: str) -> dict:
        """Gets the Query ID from the raw response"""
        response_dict = xmltodict.parse(response)
        result = response_dict["Envelope"]["Body"]["VerificaSolicitudDescargaResponse"][
            "VerificaSolicitudDescargaResult"
        ]
        data = {
            "EstadoSolicitud": result["@EstadoSolicitud"],
            "CodEstatus": result["@CodEstatus"],
            "Mensaje": result["@Mensaje"],
            "CodigoEstadoSolicitud": result["@CodigoEstadoSolicitud"],
            "NumeroCFDIs": result["@NumeroCFDIs"],
            "IdsPaquetes": [result["IdsPaquetes"]]
            if result["@EstadoSolicitud"] == "3"
            else "",  # TODO Check what happens when multiple ids
        }
        return data

    @ensure_login
    def download(self, package_ids: (list, str)) -> dict:
        """Checks the status of a Query"""
        if type(package_ids) == str:
            package_ids = [package_ids]
        downloads = {}
        for package_id in package_ids:
            request_content = self._get_download_soap_body(package_id)
            response = utils.consume(
                "http://DescargaMasivaTerceros.sat.gob.mx/IDescargaMasivaTercerosService/Descargar",
                "https://cfdidescargamasiva.clouda.sat.gob.mx/DescargaMasivaService.svc",
                request_content,
                token=self.token,
            )
            if response.status_code != 200:
                raise self.RequestException(response.status_code, response.reason, request_content)
            else:
                downloads[package_id] = self._get_download_data(
                    utils.remove_namespaces(response.content.decode("UTF-8"))
                )
        return downloads

    def _get_download_soap_body(self, package_id: str) -> dict:
        """Creates the SOAP body to check the query status"""
        data = {
            "rfc": self.rfc,
            "package_id": package_id,
            "signature": "",
        }
        envelope = self._create_common_envelope(
            TEMPLATES["PeticionDescargaMasivaTercerosEntrada"], data
        )
        return envelope

    def _get_download_data(self, response: str) -> bytes:
        """Gets the Download data from the raw response"""
        response_dict = xmltodict.parse(response)
        package = response_dict["Envelope"]["Body"]["RespuestaDescargaMasivaTercerosSalida"][
            "Paquete"
        ]
        return package and base64.b64decode(package)

    def wait_query(self, query_id: str, retries: int = 10, wait_seconds: int = 2) -> list:
        for _ in range(retries):
            verification = self.verify(query_id)
            if verification["EstadoSolicitud"] == "3":
                return verification["IdsPaquetes"]
            time.sleep(wait_seconds)
        else:
            raise TimeoutError("The query is not yet resolved")
