# -*- coding: utf-8 -*-
import base64
import hashlib
import logging
import re
import textwrap

import requests

logging.basicConfig(level=logging.INFO)
_logger = logging.getLogger(__name__)


def clean_xml(xml: str) -> str:
    """Clean a XML string to be used in SAT request.

    Removes all the spaces and new line characters between tags.

    Args:
        xml (str): XML to be cleaned.

    Returns:
        str: XML clean.
    """
    return re.sub(r"\s+(?=[<>])", "", xml).strip()


def remove_namespaces(xml):
    return re.sub(r"[souh]:", "", xml)


def prepare_template(template: str, data: dict) -> str:  # TODO simplify
    """Takes a XML template and fill the `variable` (data betwen {}) fields.

    Args:
        template (str): Template to be processed.
        data (dict): Variables to be replaced.

    Returns:
        str: Template with variables replaced.
    """
    template_clean = clean_xml(template)
    final_template = template_clean.format(**data)
    if "signature" in data.keys() and not data.get("signature"):
        data["signature"] = "{signature}"
        template_signature_to_replace = template_clean.format(**data)
        return (final_template, template_signature_to_replace)
    return final_template


def binary_to_utf8(binary: bytes) -> str:
    """Takes a bytes object an returns the string represents it.

    Args:
        binary (bytes): Raw binary to be process.

    Returns:
        str: binary in base64 in utf-8.
    """
    return base64.encodebytes(binary).decode("UTF-8")


def digest(data: str) -> str:
    return binary_to_utf8(hashlib.sha1(data.encode("UTF-8")).digest())


def der_to_pem(der_data: str, type: str) -> str:
    """Convert DER data into PEM.

    Args:
        der_data (str): DER data to be convert.
        type (str): Type of certificate to be created (`ENCRYPTED PRIVATE KEY`, `CERTIFICATE`, etc).

    Returns:
        str: Certificate converted.
    """
    wrapped = "\n".join(textwrap.wrap(der_data, 64))
    pem = f"-----BEGIN {type}-----\n{wrapped}\n-----END {type}-----\n"
    return pem


def consume(soap_action, uri, body, token=None):
    headers = {
        "Content-type": 'text/xml; charset="utf-8"',
        "Accept": "text/xml",
        "Cache-Control": "no-cache",
        "SOAPAction": soap_action,
    }
    if token:
        headers["Authorization"] = f'WRAP access_token="{token}"'
    response = requests.post(uri, body, headers=headers)
    return response
