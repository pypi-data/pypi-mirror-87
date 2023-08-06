import json
import requests

mcURL = ""
mcPort = -1
mcToken = ""
mcVerifySSL = True

def initializeMCParams(url, port, token, verifySSL):
    global mcURL
    global mcPort
    global mcToken
    global mcVerifySSL
    mcURL = url
    mcPort = port
    mcToken = "Token " + token
    mcVerifySSL = verifySSL 

def getAPIRequest(APIReq) -> json:
    URL = mcURL + ":" + str(mcPort) + APIReq
    headersData = {
        "Authorization": mcToken
    }
    req = requests.get(URL, headers=headersData, verify=mcVerifySSL)
    return json.loads(req.content)

def postAPIRequest(APIReq, bodyData) -> json:
    URL = mcURL + ":" + str(mcPort) + APIReq
    bodyData = json.dumps(bodyData)
    headersData = {
        "Authorization": mcToken,
        "Content-Type": "application/json",
        "Content-Length": str(len(bodyData))
    }
    req = requests.post(URL, headers=headersData, data=bodyData, verify=mcVerifySSL)
    return json.loads(req.content)

def deleteAPIRequest(APIReq) -> bool:
    URL = mcURL + ":" + str(mcPort) + APIReq
    headersData = {
        "Authorization": mcToken,
        "Content-Type": "application/json"
    }
    req = requests.delete(URL, headers=headersData, verify=mcVerifySSL)
    return (req.status_code == 204)
