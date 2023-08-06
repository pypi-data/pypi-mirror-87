import sys
import json
import time
import threading

#sys.path.append("./")
from communication import getAPIRequest, postAPIRequest, deleteAPIRequest
from agents import getAgentByAttrs

def appendToJobAgentList(list, id, permission, path) -> json: 
    list.append({
        "id": id,
        "permission": permission,
        "path": {"linux": path, "win": path, "osx": path, "android": path, "xbox": path }
    })
    return list

def addJob(name, desc, type, agents) -> json:
    jobInfo = {
        "name": name,
        "description": desc,
        "type": type,
        "agents": agents
    }
    return postAPIRequest("/api/v2/jobs", jobInfo)

def startJob(jobID) -> json:
    jobInfo = {
        "job_id": jobID
    }
    return postAPIRequest("/api/v2/runs", jobInfo)

def getJobs() -> json:
    return getAPIRequest("/api/v2/jobs")

def getJobByID(jobID) -> json:
    return getAPIRequest("/api/v2/jobs/" + str(jobID))

def getJobsByAttrs(attr1Name, attr1Value, attr2Name = None, attr2Value = None):
    jobs = getAPIRequest("/api/v2/jobs")
    return [obj for obj in jobs if ((obj[attr1Name]==attr1Value) and ((attr2Name==None) or (obj[attr2Name]==attr2Value)))]

def getJobRunID(jobID) -> json:
    return getAPIRequest("/api/v2/runs?job_id=" + str(jobID))

def getJobRunStatus(runID) -> json:
    return getAPIRequest("/api/v2/runs/" + str(runID))

def deleteJob(jobID) -> json:
    return deleteAPIRequest("/api/v2/jobs/" + str(jobID))

def addSimpleSyncJob(jobName, jobDescription, callbackfunction,
                    agent1IP, agent1Name, agent1Permission, agent1Folder,
                    agent2IP, agent2Name, agent2Permission, agent2Folder,
                    myJobsMonitor):
    jobAgentList = []
    jobAgentList = appendToJobAgentList(jobAgentList, getAgentByAttrs("ip", agent1IP, "name", agent1Name)[0]['id'], agent1Permission, agent1Folder)   
    jobAgentList = appendToJobAgentList(jobAgentList, getAgentByAttrs("ip", agent2IP, "name", agent2Name)[0]['id'], agent2Permission, agent2Folder)   
    newJob = addJob(jobName, jobDescription, "sync", jobAgentList)
    newJobRunID = getJobRunID(newJob['id'])
    myJobsMonitor.addMonitoredJob(newJobRunID['data'][0]['id'], callbackfunction)

class jobRunMonitor:
    def __init__(self, runID, finishedCallbackFunction):
        self.monitorJobID = 0
        self.monitorRunID = runID
        self.monitorJobStatus = ""
        self.monitorErrCode = 200
        self.monitorCallback = finishedCallbackFunction

    def getJobStatus(self) -> str:
        return self.monitorJobStatus
    
    def getErrCode(self) -> int:
        return self.monitorErrCode

    def updateJobRunStatus(self):
        runStatus = getJobRunStatus(self.monitorRunID)
        self.monitorJobID = runStatus["job_id"]
        self.monitorJobStatus = runStatus["status"]
        try:
            self.monitorErrCode = runStatus["code"]
        except:
            self.monitorErrCode = 0
        if (self.monitorJobStatus == "finished"):
            self.monitorCallback(self.monitorJobID, self.monitorRunID)

class jobsMonitor:
    def __init__(self, monitorInterval):
        self.monitorInterval = monitorInterval
        self.jobRuns = {}
        self.jobRunsLock = threading.Lock()
        threading.Thread(target=self.jobMonitorThread).start()  # , daemon=True

    def addMonitoredJob(self, runID, finishedCallbackFunction):
        with self.jobRunsLock:
            if (not runID in self.jobRuns):
                # new job run to monitor
                self.jobRuns[runID] = jobRunMonitor(runID, finishedCallbackFunction)

    def jobMonitorThread(self):
        while (True):
            with self.jobRunsLock:
                ids = list(self.jobRuns.keys())
                for runID in ids:
                    if ((self.jobRuns[runID].getJobStatus() != "finished") and (self.jobRuns[runID].getErrCode != 404)):        
                        self.jobRuns[runID].updateJobRunStatus()
                    else: 
                        self.jobRuns.pop(runID, None)
            time.sleep(self.monitorInterval)
        
