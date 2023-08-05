#!/usr/bin/env python
# coding: utf-8
# https://www.learnpyqt.com/examples/no2pads-simple-notepad-clone/
# https://stackoverflow.com/questions/38652324/issues-using-slots-and-signals-when-connecting-two-windows-in-qt-using-pyqt


import os

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import sys, uuid, time, getopt
import traceback

import matplotlib
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
winData = None
app = None
hc = None
outputDir = '/tmp'
devList = None
devNum = 0


matplotlib.use('Qt5Agg')

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

class DataWindow(QMainWindow):
  def __init__(self, dataStr, *args, **kwargs):
    super(QMainWindow, self).__init__(*args, **kwargs)
    self.buildLayout()

    w = QWidget()
    w.setLayout(self.layout)
    self.setCentralWidget(w)
    self.show()

  def buildLayout(self):
    self.file_path = None

    self.save_current_file_shortcut = QShortcut(QKeySequence('Ctrl+S'), self)
    self.save_current_file_shortcut.activated.connect(self.save_current_file)

    self.layout = QVBoxLayout()
    text = "Untitled File"
    self.title = QLabel(text)
    self.title.setWordWrap(True)
    self.title.setAlignment(Qt.AlignCenter)
    self.layout.addWidget(self.title)
  
    self.scrollable_text_area = QTextEdit()
    self.setTexte("Pour le moment il n'y a rien....", show=False)
    self.layout.addWidget(self.scrollable_text_area)

    file_toolbar = QToolBar("File")
    file_toolbar.setIconSize(QSize(14, 14))
    self.addToolBar(file_toolbar)
    file_menu = self.menuBar().addMenu("&File")

#    save_file_action = QAction(QIcon(os.path.join('..','images', 'disk.png')), "Save", self)
#    save_file_action.setStatusTip("Save current page")
#    save_file_action.triggered.connect(self.file_save)
#    file_menu.addAction(save_file_action)
#    file_toolbar.addAction(save_file_action)

    saveas_file_action = QAction(QIcon(os.path.join('..', 'images', 'disk--pencil.png')), "Enregistrer sous...", self)
    saveas_file_action.setStatusTip("Enregistrer le fichier courant ")
    saveas_file_action.triggered.connect(self.file_saveas)
    file_menu.addAction(saveas_file_action)
    file_toolbar.addAction(saveas_file_action)

  def file_save(self):
    if self.file_path is None:
      # If we do not have a path, we need to use Save As.
      return self.file_saveas()
    self._save_to_path(self.file_path)

  def file_saveas(self):
    path, _ = QFileDialog.getSaveFileName(self, "Enregister fichier CSV", "", "Documents CSV (*.csv); Documents textes (*.txt); All files (*.*)")

    if not path:
      # If dialog is cancelled, will return ''
      return

    self._save_to_path(path)

  def _save_to_path(self, path):
    text = self.scrollable_text_area.toPlainText()
    try:
      with open(path, 'w') as f:
        f.write(text)

    except Exception as e:
      self.dialog_critical(str(e))

    else:
      self.path = path
      self.title.setText(path)

  def setTexte(self, dataStr, show=True):
     self.scrollable_text_area.setText(dataStr)
     if show:
      self.show()

  def updateTexte(self, dataStr):
    self.scrollable_text_area.setText(dataStr)
    self.show()

  def save_current_file(self):
    if not self.file_path:
      new_file_path, filter_type = QFileDialog.getSaveFileName(
        self, 
        "Save this file as...",
        "data.csv", 
        "CSV Files (*.csv, *.txt, *.*)")
      if new_file_path:
        self.file_path = new_file_path
      else:
        return False
    file_contents = self.scrollable_text_area.toPlainText()
    with open(self.file_path, "w") as f:
      f.write(file_contents)
    self.title.setText(self.file_path)
  

class MainWindow(QMainWindow):
  textSaved = pyqtSignal(str)
  def __init__(self, *args, **kwargs):
    global winData
    super(MainWindow, self).__init__(*args, **kwargs)

    self.devNum = devNum
    
    if not splash:
      self.doStart()
      return

    w = QWidget()
    self.buildLayout()
    w.setLayout(self.layout)

    self.setCentralWidget(w)
    self.show()

    self.threadpool = QThreadPool()
  
    self.timer = QTimer()
    self.timer.setInterval(1000)
    self.timer.timeout.connect(self.recurring_timer)
    self.timer.start()


    winData = DataWindow("Elle n'y est pas pour rien celle là !")
    self.textSaved.connect(winData.updateTexte)
    return

  def buildLayout(self):
    self.layout = QVBoxLayout()

    self.pbar = QProgressBar(self)
    self.pbar.setGeometry(0, 0, 300, 25)
    self.pbar.setMaximum(0)
    
    self.l = QLabel(self)
    self.l.setText("Prêt ?")
    self.l.move(0,30)

    self.cb = QComboBox()
    self.cb.addItems(["{} - {}".format(dev.manufacturer, dev.product) for dev in devList])
    self.cb.setCurrentIndex(self.devNum)
    self.cb.currentIndexChanged.connect(self.selectionChange)

    self.forGraph = QCheckBox("Graphique")
    self.forGraph.setChecked(forGraph)
    self.layout.addWidget(self.forGraph)
  
    self.forHardcopy = QCheckBox("Hardcopy")
    self.forHardcopy.setChecked(forHardcopy)
    self.layout.addWidget(self.forHardcopy)

    self.forData = QCheckBox("Data")
    self.forData.setChecked(forData)
    self.layout.addWidget(self.forData)


    self.b = QPushButton("Commencer !")
    self.b.pressed.connect(self.doStart)

    self.layout.addWidget(self.cb)
    self.layout.addWidget(self.l)    
    self.layout.addWidget(self.pbar)
    self.pbar.setVisible(False)
    self.layout.addWidget(self.b)

  def pousseSetTexte(self, texte):
    self.textSaved.emit(texte)
    return

  def selectionChange(self, i):
    self.devNum = i
    return

  def progress_fn(self, n):
    return

  def send_signal(self):
    global winData
    if self.counter == 0:
      signal=self.__line.displayText()
      self.Window2=Window2(signal, self)
      self.Window2.show()
      self.textSaved.connect(self.Window2.showMessage)
      self.counter = 1
    else:
      signal = self.__line.displayText()
      self.textSaved.emit(signal)

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
    global winData

    if outputDir == "/tmp":
      fileName = outputDir+'/'+str(uuid.uuid1())+".txt"
    else:
      fileName = outputDir+"/data.txt"
  
    self.getData()
    if splash:
      self.l.setText("Writing csv File")
    df = pandas.DataFrame(data)
    df.to_csv(fileName)
    
    self.pousseSetTexte(df.to_csv())
    winData.show()

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
    if forData:
        self.doData()
    if forGraph:
        self.doGraph()
    if forHardcopy:
        self.doHardcopy()
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
    global outputDir, forHelp, forHardcopy, forData, forGraph, devList, devNum, hc
    if not fromBash:
      doNotFromBash()
      self.close() ####################### Si on veut fermer la fenêtre de contrôle une fois que tout est fait...
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

def doNotFromBash():
  global outputDir, forHelp, forHardcopy, forData, forGraph, devList, devNum, hc
  if forHardcopy:
    fig, ax = plt.subplots()
    plt.imshow(hc)
    ax.axis('off')

  if forGraph:
    win.osc.plotData(data)

  if forHardcopy or forGraph:  
    plt.show() 


def doFromBash():
  global fromBash
  fromBash = True


def doNoSplash():
  global splash
  splash = False

def startSplash():
  global splash, app, win, winData
  app = QApplication([])
  win = MainWindow()
  winData.hide()
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
  
  # if not fromBash:
    # doNotFromBash() #### Il faut revoir cette organisation qui n'est pas bonne...

  endSplash()

main(sys.argv[1:])
