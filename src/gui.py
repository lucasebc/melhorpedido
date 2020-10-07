import sys

from PySide2 import QtWidgets, QtGui, QtCore

from modelORM import ProviderORM, ProductORM, OrderORM

class ProductsTable(QtWidgets.QTableWidget):
    def __init__(self, data, parent = None):
        super(ProductsTable, self).__init__()
        self.product = {'barCode': None, 'description': None}

        if parent:
            self.parentWasSet = True
            self.parent = parent
        else:
            self.parentWasSet = False

        print(self.parentWasSet)

        self.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)

        self.setColumnCount(2)
        self.setHorizontalHeaderLabels(['Código de barras', 'Descrição'])

        self.horizontalHeader().setStretchLastSection(True)
        self.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        self.itemSelectionChanged.connect(self.itemSelected)

        self.displayData(data)

    def displayData(self, data): 
        self.setRowCount(len(data))

        for i, product in enumerate(data):
            self.setItem(i, 0, QtWidgets.QTableWidgetItem(str(product['barCode'])))
            self.setItem(i, 1, QtWidgets.QTableWidgetItem(product['description']))

    def itemSelected(self):
        self.product = ProductORM().searchProductByBarCode(int(self.selectedItems()[0].text()))
        if self.parentWasSet:
            print(self.parent)
            self.parent.setProvidersProduct(self.product)
        else:
            self.parent().setProduct(self.product)
        # todo: remove
        print(self.product)

    def reload(self, data):
        self.setRowCount(0)
        self.displayData(data)


class ProvidersTable(QtWidgets.QTableWidget):
    def __init__(self, data):
        super(ProvidersTable, self).__init__()
        self.data = data
        self.provider = {'cnpj': None, 'unitPrice': None,
                         'minBatchSize': None, 'product': None}

        self.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)

        self.setColumnCount(5)
        self.setHorizontalHeaderLabels(['CNPJ', 'Preço unitário', 'Quantidade Mínima', 'Preço total(qtde. min.)', 'Produto'])

        self.horizontalHeader().setStretchLastSection(True)
        self.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        self.itemSelectionChanged.connect(self.itemSelected)

        self.displayData(data)

    def displayData(self, data):
        self.setRowCount(len(data))

        for i, provider in enumerate(data):
            self.setItem(i, 0, QtWidgets.QTableWidgetItem(str(provider['cnpj'])))
            self.setItem(i, 1, QtWidgets.QTableWidgetItem(str(provider['unitPrice'])))
            self.setItem(i, 2, QtWidgets.QTableWidgetItem(str(provider['minBatchSize'])))
            self.setItem(i, 3, QtWidgets.QTableWidgetItem(str(provider['unitPrice'] * provider['minBatchSize'])))
            self.setItem(i, 4, QtWidgets.QTableWidgetItem(str(ProductORM().searchProductByBarCode(provider['product'])['description'])))

    def itemSelected(self):
        if len(self.selectedIndexes()) < 1:
            return
        self.provider = self.data[self.selectedIndexes()[0].row()]

        # self.provider = ProviderORM().searchProviderByCNPJAndBarCode(int(self.selectedItems()[0].text()), int(self.selectedItems()[5].text()))
        self.parent().setProvider(self.provider)

    def reload(self, data):
        self.clearSelection()
        self.setRowCount(0)
        self.data = data
        self.displayData(data)

class customActionGroup(QtWidgets.QWidget):
    def __init__(self, actFor, functions=[], parent=None):
        super(customActionGroup, self).__init__(parent)

        self.buttonNew      = QtWidgets.QPushButton('Novo ' + actFor)
        self.buttonSave     = QtWidgets.QPushButton('Salvar ' + actFor)
        self.buttonDelete   = QtWidgets.QPushButton('Excluir ' + actFor)

        self.layout = QtWidgets.QHBoxLayout()

        self.buttonSave.clicked.connect(lambda: self.clickSave(functions[0]))
        self.buttonDelete.clicked.connect(lambda: self.clickDelete(functions[1]))
        self.buttonNew.clicked.connect(lambda: self.clickNew(functions[2]))

        self.buttonNew.setDisabled(True)
        self.buttonDelete.setDisabled(True)

        self.layout.addWidget(self.buttonNew)
        self.layout.addWidget(self.buttonSave)
        self.layout.addWidget(self.buttonDelete)

        self.setLayout(self.layout)

    def setEditMode(self):
        self.buttonNew.setDisabled(False)
        self.buttonSave.setDisabled(False)
        self.buttonDelete.setDisabled(False)

    def setNewMode(self):
        self.buttonNew.setDisabled(True)
        self.buttonSave.setDisabled(False)
        self.buttonDelete.setDisabled(True)

    def clickSave(self, function):
        function()
        self.setNewMode()

    def clickNew(self, function):
        function()
        self.setNewMode()

    def clickDelete(self, function):
        function()
        self.setNewMode()

class OrderForm(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(OrderForm, self).__init__(parent)

        self.provider   = None
        self.cnpj       = None
        self.products   = []

        self.layout     = QtWidgets.QGridLayout()

        self.setLayout(self.layout)

        self.mount()

    def mount(self):
        self.tableProducts       = ProvidersTable(ProviderORM().getProviders())
        self.tableProducts.setDisabled(True)
        
        self.stepLayout     = QtWidgets.QGridLayout()

        self.labelCnpj      = QtWidgets.QLabel('CNPJ do fornecedor:')
        self.inputCnpj      = QtWidgets.QLineEdit()
        self.buttonCnpj     = QtWidgets.QPushButton('Filtrar')

        self.buttonAddProd  = QtWidgets.QPushButton('Adicionar produto')
        self.labelAmount    = QtWidgets.QLabel('Quantidade:')
        self.inputAmount    = QtWidgets.QLineEdit()

        self.buttonCnpj.clicked.connect(self.filterProducts)
        self.buttonAddProd.clicked.connect(self.addProduct)

        self.prodLayout     = QtWidgets.QVBoxLayout()

        self.stepLayout.addWidget(self.labelCnpj,0,0)
        self.stepLayout.addWidget(self.inputCnpj,0,1)
        self.stepLayout.addWidget(self.buttonCnpj,0,2)

        self.stepLayout.addLayout(self.prodLayout,1,0,1,3)

        self.stepLayout.addWidget(self.tableProducts,2,0,1,3)

        self.stepLayout.addWidget(self.labelAmount, 3, 0)
        self.stepLayout.addWidget(self.inputAmount, 3, 1)
        self.stepLayout.addWidget(self.buttonAddProd, 3, 2)

        self.buttonOrder = QtWidgets.QPushButton('Efetuar pedido')
        self.buttonOrder.clicked.connect(self.saveOrder)
        self.stepLayout.addWidget(self.buttonOrder, 4, 0, 1, 1)

        self.layout.addLayout(self.stepLayout, 0, 0)

    def clearComponents(self):
        count = len(self.products)
        self.provider   = None
        self.cnpj       = None
        self.products   = []

        self.inputAmount.setText('')
        self.inputCnpj.setText('')
        self.tableProducts.reload(ProviderORM().getProviders())
        self.tableProducts.setDisabled(True)

        for i in reversed(range(0, self.prodLayout.layout().count())):
            for j in reversed(range(0, self.prodLayout.layout().itemAt(0).layout().count())):
                self.prodLayout.layout().itemAt(i).layout().itemAt(j).widget().setParent(None)
            self.prodLayout.layout().itemAt(i).layout().setParent(None)


    def saveOrder(self):
        order = {
            'id': None,
            'providersCNPJ': self.cnpj,
            'date': None,
            'totalPrice': 0,
            'products': []
        }

        for p in self.products:
            order['totalPrice'] += p['totalPrice']
            order['products'].append(p)

        OrderORM().insertOrder(order)

        self.clearComponents()

    def addProduct(self):
        if self.provider == None or self.inputAmount.text() == '':
            return        
        if self.provider['minBatchSize'] > int(self.inputAmount.text()):
            return

        product = ProductORM().searchProductByBarCode(self.provider['product'])

        addedProduct = {'barCode': product['barCode'], 
                        'amount': self.inputAmount.text(), 
                        'totalPrice': self.provider['unitPrice'] * int(self.inputAmount.text())
                        }

        self.products.append(addedProduct)

        itemLayout = QtWidgets.QHBoxLayout()

        # buttonDelete = QtWidgets.QPushButton('Excluir')
        # buttonDelete.setParent(itemLayout)
        # buttonDelete.clicked.connect(lambda : print(buttonDelete.parent()))

        itemLayout.addWidget(QtWidgets.QLabel(str(self.provider['product'])))
        itemLayout.addWidget(QtWidgets.QLabel(product['description']))
        itemLayout.addWidget(QtWidgets.QLabel('Quantidade:'))
        itemLayout.addWidget(QtWidgets.QLabel(str(addedProduct['amount'])))
        itemLayout.addWidget(QtWidgets.QLabel('Valor total:'))
        itemLayout.addWidget(QtWidgets.QLabel(str(addedProduct['totalPrice'])))
        # itemLayout.addWidget(buttonDelete)

        self.prodLayout.addLayout(itemLayout)

        self.inputAmount.setText('')

    def filterProducts(self):
        self.cnpj = int(self.stepLayout.itemAt(1).widget().text())

        if self.cnpj < 1 or self.cnpj == None:
            return

        products = ProviderORM().searchProviderByCNPJ(self.cnpj)

        if len(products) > 0:
            self.tableProducts.reload(products)

        self.tableProducts.setDisabled(False)

    def setProvider(self, provider):
        self.provider = provider

class MainWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setWindowTitle('Melhor opção de compra')
        self.setWindowIcon(QtGui.QIcon('icon.ico'))

        self.masterLayout = QtWidgets.QHBoxLayout()

        self.menuLayout = QtWidgets.QVBoxLayout()
        self.menuLayout.setMargin(0)
        self.menuLayout.setContentsMargins(20, 0, 20, 0)

        self.activeInputs = []

        self.mainLayout = QtWidgets.QVBoxLayout()
        self.mainLayout.addSpacerItem(QtWidgets.QSpacerItem(1, 1, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum))

        self.createMenu()

        self.masterLayout.addLayout(self.menuLayout)
        self.masterLayout.addLayout(self.mainLayout)
        self.setLayout(self.masterLayout)

        self.product = None
        self.provider = None

    # method to create the menu on the left
    def createMenu(self):
        self.buttonNewProduct = QtWidgets.QPushButton('Novo produto')
        self.buttonNewProvider = QtWidgets.QPushButton('Novo fornecedor')
        self.buttonNewOrder = QtWidgets.QPushButton('Novo pedido')
        self.menuSpacer = QtWidgets.QSpacerItem(1, 1, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)

        self.buttonNewProduct.clicked.connect(self.clickMenuProduct)
        self.buttonNewProvider.clicked.connect(self.clickMenuProvider)
        self.buttonNewOrder.clicked.connect(self.clickMenuOrder)

        self.menuLayout.addWidget(self.buttonNewProduct)
        self.menuLayout.addWidget(self.buttonNewProvider)
        self.menuLayout.addWidget(self.buttonNewOrder)
        self.menuLayout.addSpacerItem(self.menuSpacer)

    # method to create the products form
    def createFormProduct(self):
        self.removeComponents(self.mainLayout)

        self.products = ProductORM().getProducts()

        self.mainLayout = QtWidgets.QFormLayout()

        buttonGroup = customActionGroup('produto', [self.saveProduct, self.removeProduct, self.newProduct])

        self.mainLayout.addWidget(buttonGroup)

        labelProdDesc = QtWidgets.QLabel('Descrição: ')
        labelProdBarCode = QtWidgets.QLabel('Código de barras: ')

        inputProdDesc = QtWidgets.QLineEdit()
        inputProdBarCode = QtWidgets.QLineEdit()

        self.activeInputs.append(inputProdBarCode)
        self.activeInputs.append(inputProdDesc)

        self.mainLayout.addRow(labelProdDesc, inputProdDesc)
        self.mainLayout.addRow(labelProdBarCode, inputProdBarCode)

        tableProducts = ProductsTable(self.products)
        self.mainLayout.addRow(tableProducts)

        self.masterLayout.addLayout(self.mainLayout)

    # method to create the providers form
    def createFormProvider(self):
        self.removeComponents(self.mainLayout)

        self.providers = ProviderORM().getProviders()

        self.mainLayout = QtWidgets.QFormLayout()

        buttonGroup = customActionGroup('fornecedor', [self.saveProvider, self.removeProvider, self.newProvider])
        self.mainLayout.addWidget(buttonGroup)

        labelCnpj = QtWidgets.QLabel('CNPJ: ')
        labelPrice = QtWidgets.QLabel('Preço: ')
        labelAmount = QtWidgets.QLabel('Quantidade: ')

        inputCnpj = QtWidgets.QLineEdit()
        inputPrice = QtWidgets.QLineEdit()
        inputAmount = QtWidgets.QLineEdit()

        self.activeInputs.append(inputCnpj)
        self.activeInputs.append(inputPrice)
        self.activeInputs.append(inputAmount)

        self.mainLayout.addRow(labelCnpj, inputCnpj)
        self.mainLayout.addRow(labelPrice, inputPrice)
        self.mainLayout.addRow(labelAmount, inputAmount)

        # ? definiton of the product selection
        groupProviders = QtWidgets.QGroupBox('Produtos')
        groupProvLayout = QtWidgets.QGridLayout()
        groupProviders.setLayout(groupProvLayout)
        self.createProductFields(groupProvLayout)
        # buttonAddProvider = QtWidgets.QPushButton('adicionar')
        # groupProvLayout.addWidget(buttonAddProvider, 2, 0)

        tableProducts = ProductsTable(ProductORM().getProducts(), self)
        groupProvLayout.addWidget(tableProducts, 2, 0, 1, 2)

        self.mainLayout.addRow(groupProviders)

        tableProviders = ProvidersTable(self.providers)
        self.mainLayout.addRow(tableProviders)

        self.masterLayout.addLayout(self.mainLayout)

    # todo: method to create fields for orders window
    def createFormOrder(self):
        self.removeComponents(self.mainLayout)

        self.mainLayout = QtWidgets.QFormLayout()

        self.mainLayout.addWidget(OrderForm())

        self.masterLayout.addLayout(self.mainLayout)

    # method to create fields for product window
    def createProductFields(self, layout):
        labelProdDesc       = QtWidgets.QLabel('Descrição: ')
        labelProdBarCode    = QtWidgets.QLabel('Código de barras: ')

        inputProdDesc       = QtWidgets.QLineEdit()
        inputProdBarCode    = QtWidgets.QLineEdit()

        inputProdBarCode.setDisabled(True)
        inputProdDesc.setDisabled(True)

        layout.addWidget(labelProdDesc, 0, 0)
        layout.addWidget(inputProdDesc, 0, 1)
        layout.addWidget(labelProdBarCode, 1, 0)
        layout.addWidget(inputProdBarCode, 1, 1)

    # method to create fields for provider window
    def createProviderFields(self, layout):
        labelCnpj = QtWidgets.QLabel('CNPJ: ')
        labelPrice = QtWidgets.QLabel('Preço: ')
        labelAmount = QtWidgets.QLabel('Quantidade: ')

        inputCnpj = QtWidgets.QLineEdit()
        inputPrice = QtWidgets.QLineEdit()
        inputAmount = QtWidgets.QLineEdit()

        layout.addWidget(labelCnpj, 0, 0)
        layout.addWidget(inputCnpj, 0, 1)
        layout.addWidget(labelPrice, 1, 0)
        layout.addWidget(inputPrice, 1, 1)
        layout.addWidget(labelAmount, 2, 0)
        layout.addWidget(inputAmount, 2, 1)

    # method to clean window
    def removeComponents(self, layout):
        self.layout().removeItem(layout)
        self.activeInputs.clear()
        self.product = None
        self.provider = None

        if not layout.count() <= 1:

            for i in reversed(range(layout.count())):
                layout.itemAt(i).widget().setParent(None)
        
        if not layout.itemAt(0).widget() == None:
            layout.itemAt(0).widget().setParent(None)

        layout.setParent(None)

    # methods to set fields in forms (product)
    def saveProduct(self):
        product = {'barCode': int(self.activeInputs[0].text()), 'description': self.activeInputs[1].text()}

        if self.product:
            ProductORM().alterProduct(product)
        else:
            ProductORM().insertProduct(product)

        self.newProduct()

    def removeProduct(self):
        ProductORM().deleteProduct(self.product)
        self.newProduct()

    def newProduct(self):
        self.product = None
        self.activeInputs[0].setText('')
        self.activeInputs[1].setText('')
        self.mainLayout.itemAt(5).widget().reload(ProductORM().getProducts())

    # methods to set fields in forms (providers)
    def saveProvider(self):
        provider = { 'cnpj': int(self.activeInputs[0].text()), 
                    'unitPrice': float(self.activeInputs[1].text()), 
                    'minBatchSize': int(self.activeInputs[2].text()),
                    'product': int(self.mainLayout.itemAt(7).widget().layout().itemAt(3).widget().text())}

        print(provider)
        
        if self.provider:
            ProviderORM().alterProvider(provider)
        else:
            ProviderORM().insertProvider(provider)

        self.newProvider()

    def removeProvider(self):
        ProviderORM().deleteProvider(self.provider)
        self.newProvider()

    def newProvider(self):
        self.provider   = None
        self.product    = None

        groupProduct = self.mainLayout.itemAt(7).widget()

        groupProduct.layout().itemAt(1).widget().setText('')
        groupProduct.layout().itemAt(3).widget().setText('')

        groupProduct.layout().itemAt(4).widget().setDisabled(False)

        self.activeInputs[0].setText('')
        self.activeInputs[1].setText('')
        self.activeInputs[2].setText('')

        self.mainLayout.itemAt(8).widget().reload(ProviderORM().getProviders())

    # methods to set selected objects
    def setProduct(self, product):
        self.product = product
        self.activeInputs[0].setText(str(self.product['barCode']))
        self.activeInputs[1].setText(str(self.product['description']))
        self.mainLayout.itemAt(0).widget().setEditMode()

    def setProvidersProduct(self, product):
        self.product = product

        print(self.mainLayout.itemAt(7).widget())

        groupProduct = self.mainLayout.itemAt(7).widget()

        groupProduct.layout().itemAt(1).widget().setText(self.product['description'])
        groupProduct.layout().itemAt(3).widget().setText(str(self.product['barCode']))

    def setProvider(self, provider):
        self.provider = provider
        self.product = ProductORM().searchProductByBarCode(self.provider['product'])
        print(self.product)
        self.activeInputs[0].setText(str(provider['cnpj']))
        self.activeInputs[1].setText(str(provider['unitPrice']))
        self.activeInputs[2].setText(str(provider['minBatchSize']))

        if self.product:
            groupProduct = self.mainLayout.itemAt(7).widget()

            groupProduct.layout().itemAt(1).widget().setText(self.product['description'])
            groupProduct.layout().itemAt(3).widget().setText(str(self.product['barCode']))

            groupProduct.layout().itemAt(4).widget().setDisabled(True)

        self.mainLayout.itemAt(0).widget().setEditMode()

    def setOrder(self, order):
        pass

    # menu click events
    def clickMenuProduct(self):
        self.createFormProduct()
        self.buttonNewProduct.setDisabled(True)
        self.buttonNewProvider.setDisabled(False)
        self.buttonNewOrder.setDisabled(False)

    def clickMenuProvider(self):
        self.createFormProvider()
        self.buttonNewProduct.setDisabled(False)
        self.buttonNewProvider.setDisabled(True)
        self.buttonNewOrder.setDisabled(False)

    def clickMenuOrder(self):
        self.createFormOrder()
        self.buttonNewProduct.setDisabled(False)
        self.buttonNewProvider.setDisabled(False)
        self.buttonNewOrder.setDisabled(True)

def gui():
    root = QtWidgets.QApplication([])
    app = MainWindow()
    app.showMaximized()
    app.update()
    sys.exit(root.exec_())
