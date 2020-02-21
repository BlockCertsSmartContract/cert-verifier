def print_issuer_information(cert_json):
    print("Issuer information from cert")
    #1.1
    try:
        issuer = cert_json['certificate']['issuer']
        print("Issuer        | {}".format(issuer['name']))
        print("Issuer URL    | {}".format(issuer['url']))
        print("Issuer E-Mail | {}".format(issuer['email']))
    except:
        pass
    # 1.2
    try:
        issuer = cert_json['document']['certificate']['issuer']
        print("Issuer        | {}".format(issuer['name']))
        print("Issuer URL    | {}".format(issuer['url']))
        print("Issuer E-Mail | {}".format(issuer['email']))
    except:
        pass
    # 2.0
    try:
        issuer = cert_json['badge']['issuer']
        print("Issuer        | {}".format(issuer['name']))
        print("Issuer URL    | {}".format(issuer['url']))
        print("Issuer E-Mail | {}".format(issuer['email']))
    except:
        pass
    # ENS
    try:
        if cert_json["signature"]["anchors"][0]["type"] == "ETHSmartContract":
            print("Issuer ENS    | {}".format(cert_json["signature"]["anchors"][0]["ens_name"]))
    except:
        pass


def print_certfile_information(cert_file):
    print("Verifying certificate = {}".format(cert_file))


def print_verification_information(messages):
    max_length_name = max(len(message["name"]) for message in messages)
    max_length_status = max(len(message["status"]) for message in messages)
    header_line_len = print_headers_verification_information(max_length_name=max_length_name, max_length_status=max_length_status)
    for message in messages:
        if message['name'] == "Validation":
            print("-"*header_line_len)
        diff = max_length_name - len(message["name"])
        print("{}{}{}{}".format(message['name'], " "*diff, ' | ', message['status']))
    print()


def print_headers_verification_information(max_length_name, max_length_status):
    header_name = "Verification step"
    header_status = "Status"

    diff = max_length_name - len(header_name)
    header_len_max = len(header_name + " " * diff + ' | ') + max_length_status

    header_line = header_name + " " * diff + ' | ' + header_status

    print()
    print(header_line)
    print("-"*header_len_max)

    return header_len_max
