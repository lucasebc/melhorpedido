import sys

from PySide2 import QtWidgets, QtGui, QtCore

from modelORM import ProviderORM, ProductORM, OrderORM

class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data

    def data(self, index, role):
        if role == QtCore.Qt.DisplayRole:
            # See below for the nested-list data structure.
            # .row() indexes into the outer list,
            # .column() indexes into the sub-list
            return self._data[index.row()][index.column()]

    def rowCount(self, index):
        # The length of the outer list.
        return len(self._data)

    # def columnCount(self, index):
    #     # The following takes the first sub-list, and returns
    #     # the length (only works if all rows are an equal length)
    #     return len(self._data[0])

class ProductsTable(QtWidgets.QTableWidget):
    def __init__(self, data):
        super(ProductsTable, self).__init__()
        self.product = {'barCode': None, 'description': None}

        self.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)

        self.setColumnCount(2)
        self.setHorizontalHeaderLabels(['Código de barras', 'Descrição'])

        self.setRowCount(len(data))

        self.horizontalHeader().setStretchLastSection(True) 
        self.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch) 

        self.itemSelectionChanged.connect(self.itemSelected)

        self.displayData(data)

    def displayData(self, data):
        for i, product in enumerate(data):
            self.setItem(i, 0, QtWidgets.QTableWidgetItem(str(product['barCode'])))
            self.setItem(i, 1, QtWidgets.QTableWidgetItem(product['description']))
    
    def itemSelected(self):
        self.product = ProductORM().searchProductByBarCode(int(self.selectedItems()[0].text()))
        self.parent().setWorkingObject(self.product)
        print(self.product)
            
class ProvidersTable(QtWidgets.QTableWidget):
    def __init__(self, data):
        super(ProvidersTable, self).__init__()
        self.provider = {'cnpj': None, 'unitPrice': None, 'minBatchSize': None, 'product': None}

        self.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)

        self.setColumnCount(5)
        self.setHorizontalHeaderLabels(['CNPJ', 'Preço unitário', 'Quantidade Mínima', 'Preço total(qtde. min.)', 'Produto'])

        self.setRowCount(len(data))

        self.horizontalHeader().setStretchLastSection(True) 
        self.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch) 

        self.itemSelectionChanged.connect(self.itemSelected)

        self.displayData(data)

    def displayData(self, data):
        for i, provider in enumerate(data):
            self.setItem(i, 0, QtWidgets.QTableWidgetItem(str(provider['cnpj'])))
            self.setItem(i, 1, QtWidgets.QTableWidgetItem(str(provider['unitPrice'])))
            self.setItem(i, 2, QtWidgets.QTableWidgetItem(str(provider['minBatchSize'])))
            self.setItem(i, 3, QtWidgets.QTableWidgetItem(str(provider['unitPrice'] * provider['minBatchSize'])))
            self.setItem(i, 4, QtWidgets.QTableWidgetItem(str(ProductORM().searchProductByBarCode(provider['product'])['description'])))

    def itemSelected(self):
        self.provider = ProviderORM().searchProviderByCNPJ(int(self.selectedItems()[0].text()))
        self.parent().setWorkingObject(self.provider)
        print(self.provider)

class customGroup(QtWidgets.QWidget):
    pass

class customActionGroup(QtWidgets.QWidget):
    def __init__(self, actFor, functions=[], parent=None):
        super(customActionGroup, self).__init__(parent)

        self.buttonNew       = QtWidgets.QPushButton('Novo ' + actFor)
        self.buttonSave      = QtWidgets.QPushButton('Salvar ' + actFor)
        self.buttonDelete    = QtWidgets.QPushButton('Excluir ' + actFor)

        self.layout = QtWidgets.QHBoxLayout()

        self.buttonSave.clicked.connect(functions[0])
        self.buttonDelete.clicked.connect(functions[1])
        self.buttonNew.clicked.connect(functions[2])

        self.layout.addWidget(self.buttonNew)
        self.layout.addWidget(self.buttonSave)
        self.layout.addWidget(self.buttonDelete)

        self.setLayout(self.layout)

class MainWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setWindowTitle('Melhor opção de compra')
        self.setWindowIcon(QtGui.QIcon('icon.ico'))

        self.masterLayout = QtWidgets.QHBoxLayout()

        self.menuLayout = QtWidgets.QVBoxLayout()
        self.menuLayout.setMargin(0)
        self.menuLayout.setContentsMargins(20,0,20,0)

        self.activeInputs = []

        self.mainLayout = QtWidgets.QVBoxLayout()
        self.mainLayout.addSpacerItem(QtWidgets.QSpacerItem(1,1,QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum))

        self.createMenu()

        self.masterLayout.addLayout(self.menuLayout)
        self.masterLayout.addLayout(self.mainLayout)
        self.setLayout(self.masterLayout)

        self.product    = None
        self.provider   = None

    def createMenu(self):
        self.buttonNewProduct   = QtWidgets.QPushButton('Novo produto')
        self.buttonNewProvider  = QtWidgets.QPushButton('Novo fornecedor')
        self.buttonNewOrder     = QtWidgets.QPushButton('Novo pedido')
        self.menuSpacer         = QtWidgets.QSpacerItem(1,1,QtWidgets.QSizePolicy.Minimum,QtWidgets.QSizePolicy.Expanding)

        self.buttonNewProduct.clicked.connect(self.createFormProduct)
        self.buttonNewProvider.clicked.connect(self.createFormProvider)
        self.buttonNewOrder.clicked.connect(self.createFormOrder)

        self.menuLayout.addWidget(self.buttonNewProduct)
        self.menuLayout.addWidget(self.buttonNewProvider)
        self.menuLayout.addWidget(self.buttonNewOrder)
        self.menuLayout.addSpacerItem(self.menuSpacer)

    def createFormProduct(self):
        self.removeComponents(self.mainLayout)

        self.products = ProductORM().getProducts()

        self.mainLayout     = QtWidgets.QFormLayout()

        buttonGroup = customActionGroup('produto', [self.saveProduct, self.removeProduct, self.newProduct])

        self.mainLayout.addWidget(buttonGroup)

        labelProdDesc       = QtWidgets.QLabel('Descrição: ')
        labelProdBarCode    = QtWidgets.QLabel('Código de barras: ')

        inputProdDesc       = QtWidgets.QLineEdit()
        inputProdBarCode    = QtWidgets.QLineEdit()

        self.activeInputs.append(inputProdBarCode)
        self.activeInputs.append(inputProdDesc)

        self.mainLayout.addRow(labelProdDesc, inputProdDesc)
        self.mainLayout.addRow(labelProdBarCode, inputProdBarCode)

        # groupProviders = QtWidgets.QGroupBox('Fornecedores')
        # groupProvLayout = QtWidgets.QGridLayout()
        # groupProviders.setLayout(groupProvLayout)
        # self.createProviderFields(groupProvLayout)
        # buttonAddProvider = QtWidgets.QPushButton('adicionar')
        # groupProvLayout.addWidget(buttonAddProvider)

        # tableProviders = QtWidgets.QTableWidget()
        # groupProvLayout.addWidget(tableProviders, 4, 0, 1, 2)

        # self.mainLayout.addRow(groupProviders)

        tableProducts       = ProductsTable(self.products)
        self.mainLayout.addRow(tableProducts)

        self.masterLayout.addLayout(self.mainLayout)

    def createFormProvider(self):
        self.removeComponents(self.mainLayout)

        self.providers = ProviderORM().getProviders()
        
        self.mainLayout = QtWidgets.QFormLayout()

        buttonGroup = customActionGroup('fornecedor', [self.saveProvider, self.removeProvider, self.newProvider])
        self.mainLayout.addWidget(buttonGroup)

        labelDesc       = QtWidgets.QLabel('Descrição: ')
        labelPrice      = QtWidgets.QLabel('Preço: ')
        labelAmount     = QtWidgets.QLabel('Quantidade: ')

        inputDesc       = QtWidgets.QLineEdit()
        inputPrice      = QtWidgets.QLineEdit()
        inputAmount     = QtWidgets.QLineEdit()

        self.activeInputs.append(inputDesc)
        self.activeInputs.append(inputPrice)
        self.activeInputs.append(inputAmount)

        self.mainLayout.addRow(labelDesc, inputDesc)
        self.mainLayout.addRow(labelPrice, inputPrice)
        self.mainLayout.addRow(labelAmount, inputAmount)

        tableProviders  = ProvidersTable(self.providers)
        self.mainLayout.addRow(tableProviders)

        self.masterLayout.addLayout(self.mainLayout)

    def createFormOrder(self):
        pass

    def createProductFields(self, layout):
        labelProdDesc       = QtWidgets.QLabel('Descrição: ')
        labelProdBarCode    = QtWidgets.QLabel('Código de barras: ')

        inputProdDesc       = QtWidgets.QLineEdit()
        inputProdBarCode    = QtWidgets.QLineEdit()

        layout.addRow(labelProdDesc, inputProdDesc)
        layout.addRow(labelProdBarCode, inputProdBarCode)

    def createProviderFields(self, layout):
        labelDesc       = QtWidgets.QLabel('Descrição: ')
        labelPrice      = QtWidgets.QLabel('Preço: ')
        labelAmount     = QtWidgets.QLabel('Quantidade: ')

        inputDesc       = QtWidgets.QLineEdit()
        inputPrice      = QtWidgets.QLineEdit()
        inputAmount     = QtWidgets.QLineEdit()

        layout.addWidget(labelDesc, 0, 0)
        layout.addWidget(inputDesc, 0, 1)
        layout.addWidget(labelPrice, 1, 0)
        layout.addWidget(inputPrice, 1, 1)
        layout.addWidget(labelAmount, 2, 0)
        layout.addWidget(inputAmount, 2, 1)
        
    def removeComponents(self, layout):
        self.layout().removeItem(layout)
        self.activeInputs.clear()
        
        if not layout.count() <= 1:

            for i in reversed(range(layout.count())): 
                layout.itemAt(i).widget().setParent(None)
        
            layout.setParent(None)

    def saveProduct(self):
        product = {'barCode': int(self.activeInputs[0].text()), 'description': self.activeInputs[1].text()}
        ProductORM().insertProduct(product)

    def removeProduct(self):
        ProductORM().deleteProduct(int(self.activeInputs[0].text()))

    def newProduct(self):
        self.activeInputs[0].setText('')
        self.activeInputs[1].setText('')

    def saveProvider(self):
        product = {'cnpj': int(self.activeInputs[0].text()), 'unitPrice': float(self.activeInputs[1].text()), 'minBatchSize': int(self.activeInputs[2].text())}
        ProductORM().insertProduct(product)
    
    def removeProvider(self):
        pass

    def newProvider(self):
        self.activeInputs[0].setText('')
        self.activeInputs[1].setText('')
        self.activeInputs[2].setText('')

    def setWorkingObject(self, obj):
        if 'cnpj' in obj:
            self.provider = obj
            self.setProviderFields()
        elif 'barCode' in obj:
            self.product = obj
            self.setProductFields()
    
    def setProductFields(self):
        pass

    def setProviderFields(self):
        pass

def gui():
    root = QtWidgets.QApplication([])
    app = MainWindow()
    app.showMaximized()
    app.update()
    sys.exit(root.exec_())
    