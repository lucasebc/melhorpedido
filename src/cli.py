from modelORM import ProductORM, ProviderORM, OrderORM

def cli():
    while True:
        print('Digite uma opção:\n1 - Novo produto\n2 - Adicionar fornecedor\n3 - Listar produtos\n4 - Listar fornecedores\n5 - Gerar pedido\n6 - Listar pedidos\n0 - Sair')

        option = input()

        if option == '0':
            return

        if option == '1':
            while True:
                orm     = ProductORM()
            
                barCode = int(input('Digite o código de barras:\n')) 

                if orm.searchProductByBarCode(barCode):
                    print('Produto já registrado.\nOperação cancelada.\n')
                    break
                
                product = {'barCode': barCode, 'description': input('Digite a descrição:\n')}
                
                if orm.insertProduct(product):
                    print('Produto registrado com sucesso.\n')
                else:
                    print('Ocorreu um erro.\n')
                    break

                if int(input('Inserir fornecedor?(0 - Não | 1 - Sim)\n')):
                    option = '2'
                break
                
        if option == '2':
            while True:
                orm = ProviderORM()

                cnpj = int(input('Digite o CNPJ:\n'))

                if not 'product' in locals():
                    product = ProductORM().searchProductByBarCode(int(input('Digite o código de barras do produto:\n')))
                    if product == None:
                        print('Produto não registrado.\nOperação cancelada.\n')
                        break

                if orm.searchProviderByCNPJAndBarCode(cnpj, product['barCode']):
                    print('Fornecedor já registrado para este produto.\nOperação cancelada.\n')
                    break

                provider = {'cnpj': cnpj, 
                            'unitPrice': float(input('Digite o preço unitário:\n')), 
                            'minBatchSize': int(input('Digite a quantidade mínima atendida:\n')),
                            'product': product['barCode']}

                if orm.insertProvider(provider):
                    print('Fornecedor registrado com sucesso.\n')
                else:
                    print('Ocorreu um erro.\n')
                break

        if option == '3':
            products = ProductORM().getProducts()

            for p in products:
                string = 'Produto: {} - Código de barras: {}'.format(p['description'], p['barCode'])
                print(string)

        if option == '4':
            providers = ProviderORM().getProviders()

            for p in providers:
                print(p)

        if option == '5':
            whileOrder = True
            order = {
                "id": None,
                "providersCNPJ": None,
                "date": None,
                "totalPrice": 0.0,
                "products": []
                }

            while whileOrder:
                whileProvider = True
                products = None
                provider = None

                while whileProvider:
                    products = ProviderORM().searchProviderByCNPJ(int(input('Digite o cnpj do fornecedor:\n')))

                    print('Produtos oferecidos:\n')
                    for p in products:
                        print(p)
                    
                    if products == None or len(products) <= 0:
                        print('fornecedor não encontrado.\n')
                        whileOrder = False
                        break

                    order['providersCNPJ'] = products[0]['cnpj']

                    while True:
                        product = ProductORM().searchProductByBarCode(int(input('Digite o código de barras do produto:\n')))

                        if product:
                            validProduct = False

                            for p in products:
                                if p['product'] == product['barCode']:
                                    validProduct = p

                            if validProduct != False:
                                whileAmount = True
                                while whileAmount:
                                    amount = int(input('Digite a quantidade:\n'))

                                    if amount > 0 and amount >= validProduct['minBatchSize']:

                                        order['products'].append({"barCode": product['barCode'], 
                                                                    "amount": amount, 
                                                                    "totalPrice": amount * validProduct['unitPrice']})
                                        
                                        print('Produto adicionado.\n')
                                        break

                                    else:
                                        if amount < 0:
                                            print('Quantidade inválida. \n')
                                        elif amount < validProduct['minBatchSize']:
                                            print('Quantidade menor que a oferecida pelo fornecedor. \n')
                                        if not int(input('Redigitar? (0 - Não | 1 - Sim)\n')):
                                            whileAmount = False
                                    

                        if not int(input('Gostaria de adicionar outro produto? (0 - Não | 1 - Sim)\n')):
                            whileProvider   = False
                            whileOrder      = False
                            break

                if len(order['products']) > 0:
                    if OrderORM().insertOrder(order):
                        print('Pedido registrado com sucesso.\n')
                    else:
                        print('Ocorreu um erro. Operação cancelada.\n')
                else:
                    print('Operação cancelada.\n')   

        if option == '6':
            orders = OrderORM().getOrders()

            for o in orders:
                string = 'id: {} - Data: {} - valor: {}, produtos: ['.format(o['id'], o['date'], o['totalPrice'])

                for p in o['products']:
                    print(p)
                    product = ProductORM().searchProductByBarCode(p['barCode'])
                    string += '{}, {} - '.format(product['description'], p['amount'])
                string += ']'
                print(string)

        if option != '1' and option != '2' and option != '3' and option != '4' and option != '5' and option != '6':
            print('Opção digitada ('+ option +') é inválida.\n')
