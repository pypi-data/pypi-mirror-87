import sys
import time
from PyQt5.QtWidgets import * 
from PyQt5 import QtCore, QtGui 
from PyQt5.QtGui import * 
from PyQt5.QtCore import * 
import sys 
import inspect
from livesplit_analyser.ScrollLabel import *
from livesplit_analyser.SplitResult import *

class Worker(QThread):
    #Worker to run commands on another thread, allowing the GUI not to lock up. Theoretically, any function should be able to be passed to this Worker.
    signal = QtCore.pyqtSignal(int)

    def __init__(self, fn, *args, **kwargs):
        QtCore.QThread.__init__(self)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs

    @QtCore.pyqtSlot()
    def run(self):
        self.fn(*self.args, **self.kwargs, signal=self.signal)
        
class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(50,50,400,400)
        self.setWindowTitle("Splits Analyser")
        
        self.splitsPage()
        
    def splitsPage(self):
        self.downloadDir = QLineEdit()
        self.downloadBrowse = QPushButton('Browse')
        self.conf = QPushButton('Ok')
        self.mname = QLabel('Methods :')
        self.oname = QLabel('Segments :')
        self.methods = QComboBox()
        self.options = QComboBox()
        self.run = QPushButton('Run')
        self.downloadDir.setPlaceholderText('File Path: ')
        self.attempts = QLabel('Attempts :')
        self.playtime = QLabel('Total Playtime :')
        self.execute = QPushButton('Execute')
        self.outputLabel = QLabel('Output :')
        self.Output = QLineEdit()
        self.scroll = QScrollArea() 
        
        
        layout = QVBoxLayout()
        
        central_widget = QWidget()
        central_widget.setLayout(layout)
        
        horizontalLayout = QHBoxLayout()
        horizontalLayout.addWidget(self.attempts)
        horizontalLayout.addWidget(self.playtime)
        layout.addLayout(horizontalLayout)
        
        horizontalLayout = QHBoxLayout()
        horizontalLayout.addWidget(self.downloadDir)
        horizontalLayout.addWidget(self.downloadBrowse)
        horizontalLayout.addWidget(self.conf)
        layout.addLayout(horizontalLayout)
        
        horizontalLayout = QHBoxLayout()
        horizontalLayout.addWidget(self.mname)
        horizontalLayout.addWidget(self.methods)
        horizontalLayout.addWidget(self.oname)
        horizontalLayout.addWidget(self.options)
        layout.addLayout(horizontalLayout)
        
        horizontalLayout.addWidget(self.execute)
        layout.addLayout(horizontalLayout)
        
        layout.addWidget(self.outputLabel)
    
        self.label = ScrollLabel()
        
        self.label.setText("No output")
        layout.addWidget(self.label)
        
        self.setCentralWidget(central_widget)
        self.downloadBrowse.clicked.connect(self.openFileDialog)
        self.conf.clicked.connect(self.initialiseSplits)
        self.execute.clicked.connect(self.runMethod)
        
        self.show()
        

        
        
    def openFileDialog(self):
        '''
        Opens the window selector for users to select what folder they want to download to.
        '''
        filename = QFileDialog.getOpenFileName(self, 'Open File', 'c:\\','Livesplit (*.lss)')
        filename = filename[0]
        self.downloadDir.setText(str(filename))

    
    def initialiseSplits(self):
        self.Analyser = splitsParser(self.downloadDir.text())
        self.setWindowTitle(self.Analyser.title)
        totalAttempts = self.Analyser.attempts
        time = self.Analyser.getPlaytime()
        self.attempts.setText(f'Attempts : {totalAttempts}')
        self.playtime.setText(f'Total Playtime : {time}')
        self.populateBoxes()
        
    def populateBoxes(self):
        self.titlesAndFuns = inspect.getmembers(self.Analyser, predicate = inspect.ismethod)

        self.d = {'Box Plot' : self.titlesAndFuns[1][1],
         'Sum of Best' : self.titlesAndFuns[4][1],
         'Segments' : self.titlesAndFuns[7][1],
         'Statistics' : self.titlesAndFuns[8][1],
         'Time Save' : self.titlesAndFuns[9][1],
         'Failed Runs until Completed' : self.titlesAndFuns[10][1],
         'Plot Splits' : self.titlesAndFuns[11][1]
            }
        
        self.options.clear()
        self.segments = self.Analyser.getSegments()
        self.options.addItem('All')
        for s in self.segments:
            self.options.addItem(s.segmentName)
            
        for name, fun in self.d.items():
            self.methods.addItem(name)
    
    def runMethod(self):
        meth = self.methods.currentText()
        index = self.options.currentIndex()-1
        onlyForAll = ['Failed Runs until Completed', 'Box Plot','Sum of Best']
        if meth in onlyForAll:
            self.label.setText(str(self.d[meth]()))
        else:
            if index < 0:
                specials = ['Statistics','Segments']
                if meth in specials:
                    text = f""
                    for i in range(1,self.options.count()):
                        
                        text += self.formatResultAtIndex(self.d[meth]()[i-1])
                    self.label.setText(text)
                else:
                    self.label.setText(str(self.d[meth]()))
                
                
            else:
                specials = ['Statistics','Segments']
                if meth in specials:
                    text = self.formatResultAtIndex(self.d[meth]()[index])
                    self.label.setText(text)
                
                elif meth == 'Time Save':
                    self.label.setText(str(self.d[meth]()[index]))
                
                else:
                    self.d[meth](self.Analyser.getSegments()[-2].runHistory)
                    
    def formatResultAtIndex(self,index):
        
        if str(type(index))=="<class 'livesplit_analyser.SplitResult.StatisticsResult'>":
            name = index.segmentName
            segbest = index.segmentBest
            segworst = index.segmentWorst
            mean = index.segmentMean
            std = index.segmentSTD
            median = index.segmentMedian
            tenpercentile = index.segment10Per
            nintypercentile = index.segment90Per
            nintyninepercentile = index.segment99Per
            averageDiff = index.averageDiff
            length = index.length
            
            formatString = f'''Segment Name: {name} \n
                             Best Segment Time: {segbest} \n
                             Worst Segment Time: {segworst} \n
                             Mean: {mean} \n
                             Standard Deviation: {std} \n
                             Median: {median} \n
                             10th Percentile: {tenpercentile} \n
                             90th Percentile: {nintypercentile} \n
                             99th Percentile: {nintyninepercentile} \n
                             Average difference: {averageDiff} \n
                             Length: {length} \n
                             \n \n \n'''
            return formatString
            
        else:
            
            name = index.segmentName
            best = index.segmentBest
            pb = index.segmentPB
            history = index.runHistory
            
            formatString = f'''Segment Name: {name} \n
                             Best Segment Time: {best} \n
                             Time at Personal Best: {pb} \n
                             History: {history} \n
                             \n \n \n'''
            return formatString

def main():
    application = QApplication(sys.argv)
    GUI = Window()
    sys.exit(application.exec_()) 
