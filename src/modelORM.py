import json

# import classes

from datetime import datetime

class DBConnection:
    __dbLocation = './database.json'

    def resetDB(self):
        with open(self.__dbLocation, "w") as file:
            json.dump({'products': [], 'orders': []}, file, indent=4)
        file.close()

    def readDB(self):
        with open(self.__dbLocation, "r") as file:
            db = json.loads(file.read())
        file.close()
        return db
    
    def getTB(self, objName):
        return self.readDB()[objName]

    def writeDB(self, objName, obj):
        try:
            db = self.readDB()
            db[objName] = obj

            with open(self.__dbLocation, "w") as file:
                json.dump(db, file, indent=4)

        except Exception as e:
            print(e.with_traceback)
            return False
        finally:
            file.close()
        return True
    
    def getOrderId(self):
        orderId = self.readDB()['orderIdCounter']
        self.writeDB('orderIdCounter', orderId+1)
        return orderId

class ProductORM:
    def __init__(self):
        self.products = self.getData()

    def getData(self):
        return DBConnection().getTB("products")
        

    def saveData(self):
        return DBConnection().writeDB("products", self.products)

    def searchProductByBarCode(self, value):
        for p in self.products:
            if p['barCode'] == value:
                return p
        return None

    def getProducts(self):
        return self.products

    def insertProduct(self, product):
        try:
            self.products.append(product)
            self.saveData()
        except:
            return False
        return True

    def deleteProduct(self, product):
        pass

    def alterProduct(self, product):
        for index, p in enumerate(self.products):
            if p['barCode'] == product['barCode']:
                self.products[index] = product
                self.saveData()
        return False

class ProviderORM:
    def __init__(self):
        self.providers = self.getData()

    def getData(self):
        return DBConnection().getTB("providers")
        

    def saveData(self):
        return DBConnection().writeDB("providers", self.providers)

    def searchProviderByCNPJ(self, value):
        for p in self.providers:
            if p['cnpj'] == value:
                return p
        return None

    def searchProvidersByProduct(self, barCode):
        aux = []
        for p in self.providers:
            if p['product'] == barCode:
                aux.append(p)
        return aux

    def getProviders(self):
        return self.providers

    def insertProvider(self, provider):
        try:
            self.providers.append(provider)
            self.saveData()
        except:
            return False
        return True

    def deleteProvider(self, provider):
        pass

    def alterProvider(self, provider):
        for index, p in enumerate(self.providers):
            if p['cnpj'] == provider['cnpj']:
                self.providers[index] = provider
                self.saveData()
        return False

class OrderORM:
    def __init__(self):
        self.orders = self.getData()

    def getData(self):
        return DBConnection().getTB("orders")
        

    def saveData(self):
        return DBConnection().writeDB("orders", self.orders)

    @staticmethod
    def calcTotalValue(batch, value):
        return batch * value

    def getOrders(self):
        return self.orders

    def searchOrderById(self, idOrder):
        for o in self.orders:
            if o['id'] == idOrder:
                return o
        return None

    def insertOrder(self, order):
        try:
            order['id'] = DBConnection().getOrderId()
            order['date'] = str(datetime.now())
            self.orders.append(order)
            self.saveData()
        except:
            return False
        return True

    def deleteOrder(self, order):
        pass

    def alterOrder(self, order):
        for index, o in enumerate(self.orders):
            if o['id'] == order['id']:
                self.orders[index] = order
                self.saveData()
        return False

