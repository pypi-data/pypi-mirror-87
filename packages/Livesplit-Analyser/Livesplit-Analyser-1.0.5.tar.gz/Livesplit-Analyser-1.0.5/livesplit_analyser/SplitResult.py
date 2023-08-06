import xml.etree.ElementTree as ET
import datetime
import numpy as np
import matplotlib.pyplot as plt

class SplitResult:
    def __init__(self, segmentName, segmentBest, segmentPB, runHistory):
        self.segmentName = segmentName
        self.segmentBest = segmentBest
        self.segmentPB = segmentPB
        self.runHistory = runHistory
    def __repr__(self):
        return '<SplitResult Segment Name: {} Segment Best: {} Segment PB: {} All: {}>'.format(self.segmentName, 
                                                                                                self.segmentBest,
                                                                                            self.segmentPB,
                                                                                            self.runHistory
                                                             )
    def __str__(self):
        return self.segmentName

    @property
    def pretty_metadata(self):
        """
        pretty_metadata is the prettified version of metadata
        """
        if self.meta:
            return ' | '.join(val for _, val in self.meta.items())
        return ''
    
class StatisticsResult:
    def __init__(self, segmentName, segmentBest, segmentWorst, segmentMean, segmentSTD,
                segmentMedian, segment10Per, segment90Per, segment99Per, averageDiff, length):
        self.segmentName = segmentName
        self.segmentBest = segmentBest
        self.segmentWorst = segmentWorst 
        self.segmentMean = segmentMean
        self.segmentSTD = segmentSTD
        self.segmentMedian = segmentMedian
        self.segment10Per = segment10Per
        self.segment90Per = segment90Per
        self.segment99Per = segment99Per
        self.averageDiff = averageDiff
        self.length = length
    
    def __repr__(self):
        return '<StatisticsResult Segment Name: {} Segment Best: {} Segment Worst: {} Segment Mean: {} Segment STD: {} Segment Median: {} Segment 10th percentile: {} Segment 90th percentile: {} Segment 99th percentile: {} Average to PB: {} Length: {}>'.format(self.segmentName, 
                                                                                            self.segmentBest,
                                                                                            self.segmentWorst,
                                                                                            self.segmentMean,
                                                                                            self.segmentSTD,
                                                                                            self.segmentMedian,
                                                                                            self.segment10Per,
                                                                                            self.segment90Per,
                                                                                            self.segment99Per,
                                                                                            self.averageDiff,
                                                                                            self.length
                                                                                    
                                                             )
    def __str__(self):
        return self.segmentName

    @property
    def pretty_metadata(self):
        """
        pretty_metadata is the prettified version of metadata
        """
        if self.meta:
            return ' | '.join(val for _, val in self.meta.items())
        return ''

class splitsParser:
    def __init__(self,filepath):    
        tree = ET.parse(filepath)
        self.root = tree.getroot()
        self.title = self.root.find('GameName').text + ' ' + self.root.find('CategoryName').text
        self.attempts = self.root.find('AttemptCount').text

    
    def getSegments(self):
        Split_Results = [
        SplitResult(
    
            segmentName = segment.find("Name").text,
    
            segmentBest = [segment.find("BestSegmentTime").find("RealTime").text 
                          if not segment.find("BestSegmentTime").find("RealTime").text == None
                          else segment.find("BestSegmentTime").find("GameTime").text ][0],
    
            segmentPB = [segment.find("SplitTimes").find("SplitTime").find("RealTime").text 
                     if not segment.find("SplitTimes").find("SplitTime").find("RealTime") == None 
                     else segment.find("SplitTimes").find("SplitTime").find("GameTime") ][0],
        
            runHistory = [history.find("RealTime").text if not 
                          history.find("RealTime") == None else
                          history.find("GameTime").text if not 
                          history.find("GameTime") == None else
                          0
                          for history in segment.find("SegmentHistory")]
        )
            for segment in self.root.find("Segments")]
        return Split_Results

    def getPlaytime(self):
        attemptRoot = self.root.find("AttemptHistory")
        vals = []
        for a in attemptRoot.findall("Attempt"):
            if a.get("started") == None:
                pass
            else:
                eY, eMon, eD, eH, eM, eS = self.getSecAndDate(a.get("ended"))
                dateEnd = datetime.datetime(int(eY), int(eMon), int(eD), int(eH), int(eM), int(eS))
                sY, sMon, sD, sH, sM, sS = self.getSecAndDate(a.get("started"))
                dateStart = datetime.datetime(int(sY), int(sMon), int(sD), int(sH), int(sM), int(sS))
                vals.append((dateEnd-dateStart).total_seconds())
        return(np.array(vals).sum() / 60**2)

    def sortSeconds(self):
        sortedRes = []
        Split_Results = self.getSegments()
        for s in Split_Results:
            sortedRes.append([s.segmentName,sorted(self.getSec(s.runHistory[1:],opt=True))])
        return sortedRes

    def getStatistics(self):
        Statistics_Result = [
            StatisticsResult(split[0],
                          np.array(split[1]).min(),
                          np.array(split[1]).max(), 
                          np.array(split[1]).mean(),
                          np.array(split[1]).std(),
                          np.percentile(np.array(split[1]),50),
                          np.percentile(np.array(split[1]),10),
                          np.percentile(np.array(split[1]),90),
                          np.percentile(np.array(split[1]),99),
                          np.array(split[1]).mean() - np.array(split[1]).min(),
                          len(split[1]))
                for split in self.sortSeconds()
        ]
        return Statistics_Result

    def getTimeSave(self):
        Split_Results = self.getSegments()
        base = 0 
        hmm = []
        for s in Split_Results:
            times = self.getSec([s.segmentPB,s.segmentBest], opt = True)
            
            hmm.append([s.segmentName, (times[0]-base)-times[1]])
            base = times[0]
        
        return(hmm)
    
    def getSOB(self):
        Split_Results = self.getSegments()
        times = [self.getSec([s.segmentBest],opt = True) for s in Split_Results]
        return(np.sum(times))
    
    def getGaps(self):
        '''Function that looks through all the attempts and returns the gaps since 
        last completed run. Returns a dictionary containing the gaps as well as the 
        completed time. To be used for easy preliminary graphs which are not related 
        to splits.'''
    
        gapsSinceLastCompleted = {"Difference" : [], "Completed Time": []}
        base = 0
        attemptRoot = self.root.find("AttemptHistory")
        for a in attemptRoot.findall("Attempt"):
            if a.find("RealTime") == None:
                pass
            else:
                gapsSinceLastCompleted["Difference"].append(int(a.get("id")) - int(base))
                gapsSinceLastCompleted["Completed Time"].append(a.find("RealTime").text)
                base = a.get("id")
            
        
        return gapsSinceLastCompleted
    
    def getSec(self,time_str, opt = False):
        runTime = []
        for time in time_str:
            """Get Seconds from time."""
            if time == 0:
                pass
            else:
                h, m, s = time.split(':')
                if opt == False:
                    runTime.append(int(h) * 3600 + int(m) * 60 + round(float(s),0))
                else:
                    runTime.append(float(h) * 3600 + float(m) * 60 + float(s))
        return runTime
    
    def getSecAndDate(self,time_str):
        dandh, m, s = time_str.split(':')
        month, day, year = dandh.split('/')
        year, hour = year.split(' ')
        return year, month, day, hour, m, s
    
    def plotInconsistency(self):
        gaps = self.getGaps()
        plt.plot(gaps["Difference"])
        plt.xlabel("Completed Runs")
        plt.ylabel("Number of resets in-between completed runs")
        plt.title("Inconsistency")
        plt.show()
        return 0
    
    def plotRuns(self,splits = None):
        if splits == None:
            mins = [float(seconds)/60 for seconds in self.getSec(self.getGaps()["Completed Time"])]
            plt.plot(mins)
            plt.xlabel("Completed Run")
            plt.ylabel("Time (mins)")
            plt.show()
        else:
            splits = self.getSec(splits)
            plt.plot(splits)
            plt.xlabel("Completed Run")
            plt.ylabel("Time (secs)")
            plt.show()
            return 0
        
        
    def boxPlot(self,outliers = False):
        seconds = []
        names = []
        values = self.sortSeconds()
        for s in values:
            names.append(s[0])
            seconds.append(s[1])
        if outliers == True:
            plt.boxplot(seconds)
            plt.xlabel("Segment")
            plt.ylabel("Time (sec)")
            plt.show()
        else:
            plt.boxplot(seconds, showfliers = False)
            plt.xlabel("Segment")
            plt.ylabel("Time (sec)")
            plt.show()
        return 0
