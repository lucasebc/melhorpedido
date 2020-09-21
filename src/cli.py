from modelORM import ProductORM, ProviderORM, OrderORM

def cli():
    while True:
        print('Digite uma opção:\n1 - Novo produto\n2 - Adicionar fornecedor\n3 - Listar produtos\n4 - Listar fornecedores\n5 - Gerar pedido\n0 - Sair')

        option = input()

        if option == '0':
            return

        if option == '1':
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

            if input('Inserir fornecedor?(0 - Não | 1 - Sim)\n'):
                option = '2'
                
        if option == '2':
            orm = ProviderORM()

            cnpj = int(input('Digite o CNPJ:\n'))

            if orm.searchProviderByCNPJ(cnpj):
                print('Fornecedor já registrado.\nOperação cancelada.\n')
                break

            if product == None:
                product = ProductORM().searchProductByBarCode(int(input('Digite o código de barras do produto:\n')))
                if product == None:
                    print('Produto não registrado.\nOperação cancelada.\n')
                    break

            provider = {'cnpj': cnpj, 'unitPrice': float(input('Digite o preço unitário:\n')), 'minBatchSize': int(input('Digite a quantidade mínima atendida:\n'))}

            if orm.insertProvider(provider):
                print('Fornecedor registrado com sucesso.\n')
            else:
                print('Ocorreu um erro.\n')

        if option == '3':
            products = ProductORM().getProducts()

            for p in products:
                print(p)

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
                        providers = ProviderORM().searchProvidersByProduct(product['barCode'])

                        if len(providers) == 0:
                            print('Produto não tem fornecedores registrados.\nOperação cancelada.\n')
                            whileOrder      = False
                            whileProduct    = False
                        else:
                            print('Fornecedores disponíveis:\n')
                            for p in providers:
                                print(p)

                            provider = ProviderORM().searchProviderByCNPJ(int(input('Digite o CNPJ do fornecedor:\n')))

                            if provider:
                                while True:
                                    amount = int(input('Digite a quantidade:\n'))

                                    if amount > 0 and amount >= provider['minBatchSize']:

                                        order = {   'id': None, 'providersCNPJ': provider['cnpj'], 
                                                    'date': None, 'totalValue': None, 'amount': amount, 
                                                    'product': product['barCode'] }
                                        order['totalValue'] = order['amount'] * provider['unitPrice']

                                        if OrderORM().insertOrder(order):
                                            print('pedido registrado com sucesso.\n')
                                        else:
                                            print('ocorreu um erro. Operação cancelada.\n')
                                        
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