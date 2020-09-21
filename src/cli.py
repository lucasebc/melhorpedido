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

            while whileOrder:
                whileProduct = True
                product = None
                providers = None

                while whileProduct:
                    product = ProductORM().searchProductByBarCode(int(input('Digite o código de barras do produto:\n')))

                    if product:

                        while True:
                            amount = int(input('Digite a quantidade:\n'))

                            if amount > 0:
                                providers = ProviderORM().searchProvidersByProductAndAmount(product['barCode'], amount)

                                if len(providers) == 0:
                                    print('Produto não tem fornecedores que atendem esta quantidade.\nOperação cancelada.\n')
                                    whileOrder      = False
                                    whileProduct    = False
                                    break
                                else:
                                    print('Fornecedores disponíveis:\n')
                                    bestCost = None
                                    for p in providers:
                                        if bestCost == None:
                                            bestCost = p
                                        elif bestCost['unitPrice'] > p['unitPrice']:
                                            bestCost = p
                                        print(p)
                                    print('Fornecedor recomendado: ')
                                    print(bestCost)

                                    provider = ProviderORM().searchProviderByCNPJ(int(input('Digite o CNPJ do fornecedor desejado:\n')))

                                    if provider:
                                        order = {   'id': None, 'providersCNPJ': provider['cnpj'], 
                                                    'date': None, 'totalValue': None, 'amount': amount, 
                                                    'product': product['barCode'] }
                                        order['totalValue'] = order['amount'] * provider['unitPrice']

                                        if OrderORM().insertOrder(order):
                                            print('Pedido registrado com sucesso.\n')
                                        else:
                                            print('Ocorreu um erro. Operação cancelada.\n')
                                                
                                            whileOrder      = False
                                            whileProduct    = False
                                            break

                            elif not input('Quantidade inválida. Redigitar? (0 - Não | 1 - Sim)\n'):
                                print('Operação cancelada.\n')
                                whileOrder      = False
                                whileProduct    = False
                                break

                    elif not int(input('Produto não registrado. Gostaria de redigitar? (0 - Não | 1 - Sim)\n')):
                        whileOrder      = False
                        whileProduct    = False  

        if option == '6':
            orders = OrderORM().getOrders()

            for o in orders:
                p = ProductORM().searchProductByBarCode(o['product'])
                string = 'id: {} - Data: {} - valor: {}, quantidade: {}, produto: {}'.format(o['id'], o['date'], o['totalValue'], o['amount'], p['description'])
                print(string)

        if option != '1' and option != '2' and option != '3' and option != '4' and option != '5' and option != '6':
            print('Opção digitada ('+ option +') é inválida.\n')
