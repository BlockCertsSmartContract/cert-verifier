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
from json import JSONDecodeError

from cert_core import to_certificate_model

from cert_verifier import connectors, config
from cert_verifier.checks import create_verification_steps
from cert_verifier.connectors import ContractConnection


def verify_certificate(certificate_model, options={}):
    if str(certificate_model.certificate_json["issuer"]["id"]).endswith(".eth"):
        validitysum = 0
        messages = []
        merkleverif = verify_hash(certificate_model.certificate_json["merkleRoot"])
        validitysum += merkleverif["validitycount"]
        messages.append(merkleverif["message"])

        targethashverif = verify_hash(certificate_model.certificate_json["targetHash"])
        validitysum += targethashverif["validitycount"]
        messages.append(targethashverif["message"])
        if validitysum == 2:
            messages.append("Validation not passed")
        return messages

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
        messages = []
        verification_steps.add_detailed_status(messages)
        for message in messages:
            print(message['name'] + ',' + str(message['status']))
    return messages


def verify_hash(hash_val):
    try:
        sc = ContractConnection("blockcertsonchaining")
    except (KeyError, JSONDecodeError):
        print("Could not load smart contract")
    '''Checks if the smart contract was issued and if it is on the revocation list'''
    cert_status = sc.functions.call("hashes", hash_val)

    if cert_status == 0:
        return {"validitycount": 0, "message": "> hash is not issued on " + config.config["current_chain"]}
    elif cert_status == 1:
        return {"validitycount": 1, "message": "> hash is valid on " + config.config["current_chain"]}
    elif cert_status == 2:
        return {"validitycount": 0, "message": "> hash is revoked on " + config.config["current_chain"]}


def verify_certificate_file(certificate_file_name, transaction_id=None, options={}):
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
            print(cert_file)
            result = verify_certificate_file(cert_file)
            print(result)
    else:
        result = verify_certificate_file('../tests/data/2.0/valid.json')
        print(result)
