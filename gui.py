# -*- coding: utf-8 -*-  
# 
# Developer
# Ismail AKBUDAK
# ismailakbudak.com
# Election algorithm on graph
  
from PyQt4 import QtCore, QtGui
from graph import *

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s
try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

# Application UI
class Ui_MainWindow():
     
    def __init__(self):
        self.graph = Graph()  
        self.graph.traceGrowth = False
        self.graph.traceLog = True
        self.graph.traceElection = True
        self.graph.traceElectionVisual = True
        self.graph.readFiles()
        
    def setupUi(self, MainWindow): 
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(400, 400)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        MainWindow.setWindowTitle(_translate("MainWindow", "Election algorithm on graph - Ismail AKBUDAK", None))
        font = QtGui.QFont()
        font.setStrikeOut(False)
        font.setPointSize(13)
        MainWindow.setFont(font) 

        # Tabs initialized
        self.tabWidget = QtGui.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 2000, 2000))
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))        
        # Tab main initialized
        self.tabMain = QtGui.QWidget()
        self.tabMain.setObjectName(_fromUtf8("tabMain")) 

        # Main - Nodes count label title
        self.labelNodesCount = QtGui.QLabel(self.tabMain)
        self.labelNodesCount.setGeometry(QtCore.QRect(85, 10, 350, 30)) 
        self.labelNodesCount.setObjectName(_fromUtf8("labelNodesCount"))
        self.labelNodesCount.setText(_translate("MainWindow", "Number of Nodes : ", None)) 

        # Main - Draw Graph  button
        self.pushButtonDraw = QtGui.QPushButton(self.tabMain)
        self.pushButtonDraw.setGeometry(QtCore.QRect(85, 90, 200, 30)) 
        self.pushButtonDraw.setObjectName(_fromUtf8("pushButtonDraw"))
        self.pushButtonDraw.setText(_translate("MainWindow", "Draw Graph", None))
        self.pushButtonDraw.clicked.connect(self.draw)

        # Main - Read Files  button
        self.pushButtonReadFiles = QtGui.QPushButton(self.tabMain)
        self.pushButtonReadFiles.setGeometry(QtCore.QRect(85, 130, 200, 30)) 
        self.pushButtonReadFiles.setObjectName(_fromUtf8("pushButtonReadFiles"))
        self.pushButtonReadFiles.setText(_translate("MainWindow", "Read Files", None))
        self.pushButtonReadFiles.clicked.connect(self.readFiles)
        
        # Main - Close figure  button
        self.pushButtonClearGraph = QtGui.QPushButton(self.tabMain)
        self.pushButtonClearGraph.setGeometry(QtCore.QRect(85, 170, 200, 30)) 
        self.pushButtonClearGraph.setObjectName(_fromUtf8("pushButtonClearGraph"))
        self.pushButtonClearGraph.setText(_translate("MainWindow", "Clear Graph", None))
        self.pushButtonClearGraph.clicked.connect(self.clearGraph)
  
        # Main - Start election algorithm button
        self.pushButtonStartElection = QtGui.QPushButton(self.tabMain)
        self.pushButtonStartElection.setGeometry(QtCore.QRect(85, 210, 200, 30)) 
        self.pushButtonStartElection.setObjectName(_fromUtf8("pushButtonStartElection"))
        self.pushButtonStartElection.setText(_translate("MainWindow", "Start Election Algorithm", None))
        self.pushButtonStartElection.clicked.connect(self.startElection)
 
        # Tab settings initialized
        self.tabSettings = QtGui.QWidget()
        self.tabSettings.setObjectName(_fromUtf8("tabSettings"))   
         
        settingUp = 30
        settingSpace = 30 
        # settings - traceGrowth
        self.checkBoxUseRandomCapacity = QtGui.QCheckBox(self.tabSettings)
        self.checkBoxUseRandomCapacity.setGeometry(QtCore.QRect(85, settingUp, 300, 30))
        self.checkBoxUseRandomCapacity.setObjectName(_fromUtf8("checkBoxUseRandomCapacity"))
        self.checkBoxUseRandomCapacity.setText(_translate("MainWindow", "Use Random Capacity", None))
        self.checkBoxUseRandomCapacity.setChecked(False)

        # settings - traceLog
        self.checkBoxTraceLog = QtGui.QCheckBox(self.tabSettings)
        self.checkBoxTraceLog.setGeometry(QtCore.QRect(85, settingUp + settingSpace, 300 , 30))
        self.checkBoxTraceLog.setObjectName(_fromUtf8("checkBoxTraceLog"))
        self.checkBoxTraceLog.setText(_translate("MainWindow", "Graph Log", None))
        self.checkBoxTraceLog.setChecked(False)
        # settings - traceElection
        self.checkBoxTraceElection = QtGui.QCheckBox(self.tabSettings)
        self.checkBoxTraceElection.setGeometry(QtCore.QRect(85, settingUp + 2*settingSpace, 300, 30))
        self.checkBoxTraceElection.setObjectName(_fromUtf8("checkBoxTraceElection"))
        self.checkBoxTraceElection.setText(_translate("MainWindow", "Election Log", None))
        self.checkBoxTraceElection.setChecked(False)
        # settings - traceElectionVisual
        self.checkBoxTraceElectionVisual = QtGui.QCheckBox(self.tabSettings)
        self.checkBoxTraceElectionVisual.setGeometry(QtCore.QRect(85, settingUp + 3*settingSpace, 300, 30))
        self.checkBoxTraceElectionVisual.setObjectName(_fromUtf8("checkBoxTraceElectionVisual"))
        self.checkBoxTraceElectionVisual.setText(_translate("MainWindow", "Election Result Display", None))
        self.checkBoxTraceElectionVisual.setChecked(False) 

        # Tab main initialized
        self.tabNode = QtGui.QWidget()
        self.tabNode.setObjectName(_fromUtf8("tabNode"))

        # Main window
        # Because of dialog exception 
        # MainWindow.setCentralWidget(self.centralwidget)  
        self.tabWidget.setCurrentIndex(0)
        self.tabWidget.addTab(self.tabMain, _fromUtf8(""))
        self.tabWidget.addTab(self.tabSettings, _fromUtf8("")) 
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabMain), _translate("MainWindow", "Main Menu", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabSettings), _translate("MainWindow", "Settings ", None)) 
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # Fill with data
        self.fill_fields()
        self.set_check_box()

    def startElection(self):
        self.set_graph_trace() 
        self.graph.findCoordinates()    

    def draw(self):
        self.set_graph_trace()
        self.graph.draw()

    def clearGraph(self):
        self.set_graph_trace() 
        self.graph.removeAll()
        self.fill_fields()      
        
    def readFiles(self):
        self.set_graph_trace() 
        self.graph.removeAll()
        self.graph.readFiles()
        self.fill_fields()
        self.graph.findCoordinates()     
        
    def fill_fields(self): 
        self.set_labels()
    
    def set_labels(self):
        num = len(self.graph.nodes.keys())
        self.labelNodesCount.setText(  "Number of Nodes : %s" % ( str(num) ) ) 
    
    def set_graph_trace(self):
        if self.checkBoxTraceLog.isChecked():
            self.graph.traceLog = True
        else:
            self.graph.traceLog = False

        if self.checkBoxUseRandomCapacity.isChecked():
            self.graph.useRandomCapacity = True
        else:
            self.graph.useRandomCapacity = False
            
        if self.checkBoxTraceElection.isChecked():
            self.graph.traceElection = True
        else:
            self.graph.traceElection = False
             
        if self.checkBoxTraceElectionVisual.isChecked():
            self.graph.traceElectionVisual = True
        else:
            self.graph.traceElectionVisual = False
            
    def set_check_box(self):
        if self.graph.traceLog:
            self.checkBoxTraceLog.setChecked(True)
        else:
            self.checkBoxTraceLog.setChecked(False)

        if self.graph.useRandomCapacity:
            self.checkBoxUseRandomCapacity.setChecked(True)
        else:
            self.checkBoxUseRandomCapacity.setChecked(False)

        if self.graph.traceElection:
            self.checkBoxTraceElection.setChecked(True)
        else:
            self.checkBoxTraceElection.setChecked(False)
 
        if self.graph.traceElectionVisual:
            self.checkBoxTraceElectionVisual.setChecked(True)
        else:
            self.checkBoxTraceElectionVisual.setChecked(False)
  
class Win(QtGui.QDialog,Ui_MainWindow):
    def __init__(self):
        Ui_MainWindow.__init__(self)
        QtGui.QDialog.__init__(self)
        self.setupUi(self)

# Main application
if __name__ == "__main__":
    import sys 
    app = QtGui.QApplication(sys.argv) 
    MWindow = Win()
    MWindow.show()
    sys.exit(app.exec_())
