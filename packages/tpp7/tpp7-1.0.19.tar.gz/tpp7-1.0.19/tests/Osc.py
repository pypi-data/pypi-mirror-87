#!/usr/bin/env python
# coding: utf-8
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import sys, uuid, time, getopt
import traceback

from matplotlib import pyplot as plt
from Oscillo import Oscillo
import numpy, scipy.io, pandas

forHelp = False
forHardcopy = False
forData = False
forGraph = False
fromBash = False

dataTransfered = False
splash = True
win = None
app = None
hc = None
outputDir = '/tmp'
devList = None
devNum = 0

def doHelp():
  print('TDS.py -hHDGN')
  print('-h, --help        print this help')
  print('-H, --hardcopy    get hardcopy of the scope')
  print('-D, --data        get data of each channel of the scope')
  print('-b, --bash       when used from bash script')
  print('-G, --graph       reproduce a graph as the scope screen')
  print('-d dir, --dir=dir specifies the directory where files are written')
  print('-N, --nosplash    dont open a splash screen')


class OscSignals(QObject):
  finished = pyqtSignal()
  error = pyqtSignal(tuple)
  result = pyqtSignal(object)
  progress = pyqtSignal(int)


class Osc(QRunnable):
  def __init__(self, fn, *args, **kwargs):
    super(Osc, self).__init__()

    # Store constructor arguments (re-used for processing)
    self.fn = fn
    self.args = args
    self.kwargs = kwargs
    self.signals = OscSignals()    

    # Add the callback to our kwargs
    self.kwargs['progress_callback'] = self.signals.progress

  @pyqtSlot()
  def run(self):        
    # Retrieve args/kwargs here; and fire processing using them
    try:
      result = self.fn(*self.args, **self.kwargs)
    except:
      traceback.print_exc()
      exctype, value = sys.exc_info()[:2]
      self.signals.error.emit((exctype, value, traceback.format_exc()))
    else:
      self.signals.result.emit(result)  # Return the result of the processing
    finally:
      self.signals.finished.emit()  # Done
        
class MainWindow(QMainWindow):
  def __init__(self, *args, **kwargs):
    super(MainWindow, self).__init__(*args, **kwargs)

    self.devNum = devNum
    
    if not splash:
      self.doStart()
      return

    layout = QVBoxLayout()
    
    self.pbar = QProgressBar(self)
    self.pbar.setGeometry(0, 0, 300, 25)
    self.pbar.setMaximum(0)
    
    self.l = QLabel(self)
    # self.l.setText(type(self.osc).__name__)
    self.l.setText("Prêt ?")
    self.l.move(0,30)

    self.cb = QComboBox()
    self.cb.addItems(["{} - {}".format(dev.manufacturer, dev.product) for dev in devList])
    self.cb.setCurrentIndex(self.devNum)
    self.cb.currentIndexChanged.connect(self.selectionChange)

    self.forGraph = QCheckBox("Graphique")
    self.forGraph.setChecked(forGraph)
    # self.forGraph.stateChanged.connect(lambda:self.btnstate(self.forGraph))
    layout.addWidget(self.forGraph)
  
    self.forHardcopy = QCheckBox("Hardcopy")
    self.forHardcopy.setChecked(forHardcopy)
    # self.forHardcopy.stateChanged.connect(lambda:self.btnstate(self.forHardcopy))
    layout.addWidget(self.forHardcopy)

    self.forData = QCheckBox("Data")
    self.forData.setChecked(forData)
    # self.forData.stateChanged.connect(lambda:self.btnstate(self.forData))
    layout.addWidget(self.forData)


    self.b = QPushButton("Commencer !")
    self.b.pressed.connect(self.doStart)

    layout.addWidget(self.cb)
    layout.addWidget(self.l)    
    layout.addWidget(self.pbar)
    self.pbar.setVisible(False)
    layout.addWidget(self.b)

    w = QWidget()
    w.setLayout(layout)

    self.setCentralWidget(w)
    self.show()
    self.threadpool = QThreadPool()
  
    self.timer = QTimer()
    self.timer.setInterval(1000)
    self.timer.timeout.connect(self.recurring_timer)
    self.timer.start()
    return

  def selectionChange(self, i):
    self.devNum = i
    return

  def progress_fn(self, n):
    return

#retrieve data from the oscilloscope
  def getData(self):
    global dataTransfered, data
    if dataTransfered:
      return
    if splash:
      self.l.setText("Transfert des données")
    activeChannelList = self.osc.getActiveChannelList()
    data = self.osc.getChannelListData(activeChannelList)
    dataTransfered = True

  def doGraph(self):
    self.getData()
    return

  def doHardcopy(self):
    global hc
    if outputDir == "/tmp":
      fileName = outputDir+'/'+str(uuid.uuid1())+".png"
    else:
      fileName = outputDir+"/hardcopy.png"
    print(fileName)
    
    if splash:
      self.l.setText("Transfert de hardcopy")
    hc = self.osc.getHardcopy()
    plt.imsave(fileName, hc)
    if splash:
      self.l.setText("doHardcopy Fait !")
    return

  def doData(self):
    if outputDir == "/tmp":
      fileName = outputDir+'/'+str(uuid.uuid1())+".txt"
    else:
      fileName = outputDir+"/data.txt"
  
    self.getData()
    if splash:
      self.l.setText("Writing csv File")
    df = pandas.DataFrame(data)
    df.to_csv(fileName)
        
    if splash:
      self.l.setText("Writing mat File")
    scipy.io.savemat( outputDir+'/data.mat', mdict={'data': data})    
    print(fileName)
    sys.stdout.flush()
    if splash:
      self.l.setText("doData Fait !")
    return

  def doTruc(self):
    if splash:
      self.pbar.setVisible(True)
    if forGraph:
        self.doGraph()
    if forHardcopy:
        self.doHardcopy()
    if forData:
        self.doData()
    if forGraph:
        self.doGraph()
    if splash:
      self.pbar.setVisible(False)     
    return

  def execute_this_fn(self, progress_callback):
    global forGraph, forData, forHardcopy

    forGraph = self.forGraph.isChecked()
    forHardcopy = self.forHardcopy.isChecked()
    forData = self.forData.isChecked()

    self.doTruc()

    return "Done."

  def print_output(self, s):
    return

  def thread_complete(self):
    self.close()
    return

  def doStart(self):
    # Pass the function to execute
    if splash:
      self.pbar.setVisible(True)
      self.b.setVisible(False)

    self.osc = Oscillo.openDevice(devList[self.devNum])

    if not splash:
      self.doTruc()
      return

    osc = Osc(self.execute_this_fn) # Any other args, kwargs are passed to the run function
    osc.signals.result.connect(self.print_output)
    osc.signals.finished.connect(self.thread_complete)
    osc.signals.progress.connect(self.progress_fn)
    
    # Execute
    self.threadpool.start(osc)
    
      
  def recurring_timer(self):
    return

def doFromBash():
  global fromBash
  
  fromBash = True


def doNoSplash():
  global splash
  splash = False

def startSplash():
  global splash, app, win
  app = QApplication([])
  win = MainWindow()
  return

def endSplash():
  return

def init():
  if splash:
    app.exec_()    
  return


def main(argv):
  global outputDir, forHelp, forHardcopy, forData, forGraph, devList, devNum, hc
  
  try:
    opts, args = getopt.getopt(argv,"hbHDGNd:", ["help", "bash", "hardcopy","data", "graph","nosplash","dir=","dev="])
  except getopt.GetoptError:
    doHelp()
    sys.exit(2)

  for opt, arg in opts:
    if opt in ('-h','--help'):
      forHelp = True
    elif opt in ('-b','--bash'):
      doFromBash()
    elif opt in ('-N','--nosplash'):
      doNoSplash()
    elif opt in ('-H','--hardcopy'):          
      forHardcopy = True
    elif opt in ("-D", "--data"):
      forData = True
    elif opt in ("-G", "--graph"):
      forGraph = True
    elif opt in ("-d", "--dir"):
      outputDir = arg
    elif opt in ("--dev"):
      devNum = int(arg)
 
  if forHelp:
    doHelp()
    exit(0)

  devList = Oscillo.getDeviceList()
  startSplash()

  init()
  
  if not fromBash:
    if forHardcopy:
      fig, ax = plt.subplots()
      plt.imshow(hc)
      ax.axis('off')

    if forGraph:
      win.osc.plotData(data)

    if forHardcopy or forGraph:  
      plt.show() 

  endSplash()

main(sys.argv[1:])
