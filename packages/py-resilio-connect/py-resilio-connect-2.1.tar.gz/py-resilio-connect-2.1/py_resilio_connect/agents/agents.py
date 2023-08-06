import sys
import json
import logging

sys.path.append("./")
from ..communication.communication import getAPIRequest  

def getAgentList():
    return getAPIRequest("/api/v2/agents")

def getAgentByAttrs(attr1Name, attr1Value, attr2Name = None, attr2Value = None):
    agents = getAgentList()
    if (attr1Value == "*"):
        # TO DO: properly handle regex
        obj = [obj for obj in agents if (obj[attr2Name]==attr2Value)]
    else:    
        obj = [obj for obj in agents if ((obj[attr1Name]==attr1Value) and ((attr2Name==None) or (obj[attr2Name]==attr2Value)))]
    if (len(obj) == 0):
        print("failed to find Agent where '" + attr1Name + "'='" + attr1Value + "' and '" + attr2Name + "'='" + attr2Value + "'")
        logging.error("failed to find Agent where '" + attr1Name + "'='" + attr1Value + "' and '" + attr2Name + "'='" + attr2Value + "'")
    return obj
