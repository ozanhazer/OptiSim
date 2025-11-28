from PyQt5 import QtWidgets, QtCore

class DataBaseWidget(QtWidgets.QWidget):
    '''
    class to display database 
    '''
    #create custom signal (not used) handle callback instead
    #DBIndexChanged = QtCore.pyqtSignal(str)

    def __init__(self, layer, database, callback):

        super(DataBaseWidget, self).__init__()
    
        self.layer = layer
        self.Materials = database
    
        self.callback = callback
    
        self.setupUi()
    
    def setupUi(self):
    
        VLayoutDB = QtWidgets.QVBoxLayout(self)
        self.DBList = QtWidgets.QListWidget()
        self.DBList.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.DBList.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        #self.DBList.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
    
        self.DBList.addItems(self.Materials)
        MaterialLabel = QtWidgets.QLabel('Material:')
        VLayoutDB.addWidget(MaterialLabel)
        VLayoutDB.addWidget(self.DBList)
    
        DBItem = self.DBList.findItems(self.layer.criDBName, QtCore.Qt.MatchFixedString)
        self.DBList.setCurrentItem(DBItem[0])
    
        self.DBList.currentItemChanged.connect(self.criDBChanged)

    def criDBChanged(self, Item):
        #self.DBIndexChanged.emit(Item.text())
        self.callback(Item.text())
    
    def criDBClicked(self):
        """
        origin of n and k values and displey criSourceWidget funktions
        """
        if self.criFromDB.isChecked():
            self.FileFrame.hide()
            self.ConstantFrame.hide()
            self.DBFrame.show()
 
    
    
class FromFileWidget(QtWidgets.QWidget):
    '''
    class to display widget 'from file' 
    '''
    def __init__(self, layer, callback):

        super(FromFileWidget, self).__init__()
    
        self.path = layer.criFile['path']        
        self.alpha = layer.criFile['alpha']        
        self.n = layer.criFile['n']
        self.callback = callback

        self.setupUi()


    def setupUi(self):
        VLayout = QtWidgets.QVBoxLayout(self)
        HLayoutFile = QtWidgets.QHBoxLayout()
        FileLabel = QtWidgets.QLabel('file:')
        self.FilePathName = QtWidgets.QLineEdit()
    
        self.criFilePathButton = QtWidgets.QPushButton('...')
    
        HLayoutFile.addWidget(FileLabel)
        HLayoutFile.addWidget(self.FilePathName)
        HLayoutFile.addWidget(self.criFilePathButton)
    
        self.alphaGroupBox = QtWidgets.QGroupBox()
        self.alphaGroupBox.setTitle("alpha only")
        self.alphaGroupBox.setCheckable(True)
        self.alphaGroupBox.setChecked(self.alpha)
        alphaLabel = QtWidgets.QLabel(self.alphaGroupBox)
        alphaLabel.setText('constant refractive index n:')
        self.spinBox = QtWidgets.QDoubleSpinBox(self.alphaGroupBox)
        self.spinBox.setProperty("value", self.n)
        self.spinBox.setSingleStep(0.1)
        HLayoutAlpha = QtWidgets.QHBoxLayout(self.alphaGroupBox)
        HLayoutAlpha.addWidget(alphaLabel)
        HLayoutAlpha.addWidget(self.spinBox)
    
        VLayout.addLayout(HLayoutFile)
        VLayout.addWidget(self.alphaGroupBox)
    
        if self.path:
            self.FilePathName.setText(self.path) 

        self.criFilePathButton.clicked.connect(self.selectCRIFilePath)
        self.alphaGroupBox.toggled.connect(self.updateAlpha)
        self.spinBox.valueChanged.connect(self.updateAlpha)
    
    def selectCRIFilePath(self):
        #TODO: make LineEdit editable for costum path input
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self)
        if fileName:
            self.path = fileName
            self.FilePathName.setText(fileName)
            criFile = dict( path = self.path,
                            alpha = self.alpha,
                            n = self.n) 
            self.callback(criFile)

    def updateAlpha(self):
        self.alpha = self.alphaGroupBox.isChecked()
        self.n = self.spinBox.value()
        criFile = dict( path = self.path,
                        alpha = self.alpha,
                        n = self.n)
        self.callback(criFile)

class ConstantWidget(QtWidgets.QWidget):
    '''
    class to display widget 'from file' 
    '''
    def __init__(self, layer, callback):

        super(ConstantWidget, self).__init__()
    
        self.n = layer.criConstant[0]
        self.k = layer.criConstant[1]
    
        self.callback = callback
    
        self.setupUi()

    def setupUi(self):
    
        GridLayoutConstant = QtWidgets.QGridLayout(self)
        nLabel = QtWidgets.QLabel('refractive index n:')
        kLabel = QtWidgets.QLabel('extinction coefiicient k:')
        self.ConstantnEdit = QtWidgets.QDoubleSpinBox()
        self.ConstantkEdit = QtWidgets.QDoubleSpinBox()
        # set locale to english for point instead of comma seperator
        self.ConstantnEdit.setLocale(QtCore.QLocale('C'))
        self.ConstantkEdit.setLocale(QtCore.QLocale('C'))
        GridLayoutConstant.addWidget(nLabel, 0, 0)
        GridLayoutConstant.addWidget(kLabel, 1, 0)
        GridLayoutConstant.addWidget(self.ConstantnEdit, 0, 1)
        GridLayoutConstant.addWidget(self.ConstantkEdit, 1, 1)
        #set values from layer properties
        self.ConstantnEdit.setProperty("value", self.n)
        self.ConstantkEdit.setProperty("value", self.k)

        self.ConstantnEdit.valueChanged.connect(self.updateConstant)
        self.ConstantkEdit.valueChanged.connect(self.updateConstant)
    
    
    def updateConstant(self):
        self.n = self.ConstantnEdit.value()
        self.k = self.ConstantkEdit.value()
    
        self.callback([self.n, self.k])
