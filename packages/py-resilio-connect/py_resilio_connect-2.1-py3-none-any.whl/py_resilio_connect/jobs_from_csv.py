import csv
import time
import threading
import logging

from jobs import addSimpleSyncJob, getJobs, getJobsByAttrs, getJobRunID, getJobByID

class jobsFromCSV:
    def __init__(self, csvFileName, jobsMonitor, callbackFunction, concurrentJobsCount, monitorInterval):
        self.csvFileName = csvFileName
        self.jobsList = []
        self.jobDict = {}
        self.nextJob = 0
        self.jobsMonitor = jobsMonitor
        self.callbackFunction = callbackFunction
        self.concurrentJobsCount = concurrentJobsCount
        self.monitorInterval = monitorInterval

        # read the csv file
        self.readCSV()
        # check the current state of the system
        self.syncCurrentState()
        # start the job creation and monitoring process
        threading.Thread(target=self.jobCreationThread).start()

    def readCSV(self):
        with open(self.csvFileName, "r") as file:
            csvReader = csv.DictReader(file, skipinitialspace=True)
            i = 0
            for row in csvReader:
                self.jobsList.append(row)
                self.jobDict[row['jobName']] = i
                i += 1
            print(self.jobsList)

    def updateCSV(self):
        with open(self.csvFileName, 'w') as csvfile:  
            writer = csv.DictWriter(csvfile, self.jobsList[0].keys())
            writer.writeheader()
            writer.writerows(self.jobsList)  


    def addNextJob(self):
        if (self.nextJob < len(self.jobsList)):
            addSimpleSyncJob(
                self.jobsList[self.nextJob]['jobName'],
                self.jobsList[self.nextJob]['jobDescription'],
                self.jobCompletedCallback,
                self.jobsList[self.nextJob]['ip1'],
                self.jobsList[self.nextJob]['name1'],
                self.jobsList[self.nextJob]['permission1'],
                self.jobsList[self.nextJob]['folder1'],
                self.jobsList[self.nextJob]['ip2'],
                self.jobsList[self.nextJob]['name2'],
                self.jobsList[self.nextJob]['permission2'],
                self.jobsList[self.nextJob]['folder2'],
                self.jobsMonitor
                )
            self.nextJob += 1

    def handleExistingJob(self, jobExists):
        print("Job: '" + self.jobsList[self.nextJob]['jobName'] + "' was already running")
        logging.info("Job: '" + self.jobsList[self.nextJob]['jobName'] + "' was already running")
        jobRunID = getJobRunID(jobExists[0]['id'])
        self.jobsMonitor.addMonitoredJob(jobRunID['data'][0]['id'], self.jobCompletedCallback)

    def syncCurrentState(self):
        for index in range(len(self.jobsList)):
            jobExists = getJobsByAttrs("name", self.jobsList[index]['jobName'])
            if (jobExists):
                self.handleExistingJob(jobExists)

    def jobCompletedCallback(self, jobID, runID):
        # persist completion state
        finishedJob = getJobByID(jobID)
        self.jobsList[self.jobDict[finishedJob['name']]]['completed'] = 'y'
        self.updateCSV()
        self.callbackFunction(jobID, runID)

    def jobCreationThread(self):
        while (True):
            jobs = getJobs()
            while ((self.nextJob < len(self.jobsList)) and (len(jobs) < self.concurrentJobsCount)):
                jobExists = getJobsByAttrs("name", self.jobsList[self.nextJob]['jobName'])
                if self.jobsList[self.nextJob]['completed'] == 'y':
                    self.nextJob += 1
                elif (not jobExists):
                    self.addNextJob()
                    jobs = getJobs()
                else:
                    self.handleExistingJob(jobExists)
                    self.nextJob += 1
            time.sleep(self.monitorInterval)
