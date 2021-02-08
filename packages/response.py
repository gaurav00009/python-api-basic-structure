def parsejson(msg, response, status):
    data = {}
    data["error"] = 0
    data["data"] = {}
    data["msg"] = msg
    if status == 200:
        data["data"] = response if response else {}
    if status == 201:
        data['data'] = response if response else []
    elif status == 400:
        temp_list = []
        for key, item in msg.items():
            temp_list.append(key.title() + " : " + item[0])
        data["error"] = 1
        data["msg"] = ", ".join(temp_list)
    elif status == 403:
        data["error"] = 1
        data["msg"] = msg

    return data


def getdocs():
    _response_docs = {400: "List of Error Messages", 201: "Not Set"}
    return _response_docs
