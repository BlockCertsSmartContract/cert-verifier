"""
Verify blockchain certificates (http://www.blockcerts.org/)

Overview of verification steps
- Check integrity: TODO: json-ld normalizatio
- Check signature (pre-v2)
- Check whether revoked
- Check whether expired
- Check authenticity

"""
import json
import sys

from cert_core import to_certificate_model

from cert_verifier import connectors, printer
from cert_verifier.checks import create_verification_steps


def verify_certificate(certificate_model, options=None):
    if options is None:
        options = {}
    try:
        is_issued_on_smartcontract = certificate_model.certificate_json["signature"]["anchors"][0]["type"] == "ETHSmartContract"
    except (TypeError, KeyError):
        is_issued_on_smartcontract = False
    messages = []
    if is_issued_on_smartcontract:
        verification_steps = create_verification_steps(certificate_model, is_issued_on_smartcontract=is_issued_on_smartcontract)
        verification_steps.execute()
        verification_steps.add_detailed_status(messages)
    else:
        # lookup issuer-hosted information
        issuer_info = connectors.get_issuer_info(certificate_model)

        # lookup transaction information
        connector = connectors.createTransactionLookupConnector(certificate_model.chain, options)
        transaction_info = connector.lookup_tx(certificate_model.txid)

        # create verification plan
        verification_steps = create_verification_steps(certificate_model, transaction_info, issuer_info,
                                                       certificate_model.chain)

        verification_steps.execute()
        verification_steps.add_detailed_status(messages)
    printer.print_issuer_information(certificate_model.certificate_json)
    printer.print_verification_information(messages)
    return messages


def verify_certificate_file(certificate_file_name, transaction_id=None, options={}):
    printer.print_certfile_information(certificate_file_name)
    with open(certificate_file_name, 'rb') as cert_fp:
        certificate_bytes = cert_fp.read()
        certificate_json = json.loads(certificate_bytes.decode('utf-8'))
        certificate_model = to_certificate_model(certificate_json=certificate_json,
                                                 txid=transaction_id,
                                                 certificate_bytes=certificate_bytes)
        result = verify_certificate(certificate_model, options)

    return result


if __name__ == "__main__":
    if len(sys.argv) > 1:
        for cert_file in sys.argv[1:]:
            verify_certificate_file(cert_file)
    else:
        default_certfile = '../tests/data/2.0/valid.json'
        verify_certificate_file(default_certfile)
