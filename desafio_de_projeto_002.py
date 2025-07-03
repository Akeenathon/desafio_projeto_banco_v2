from time import sleep

clients = []
accounts = []
deposit_register = []
withdraw_register = []


def loading():
    print('.', end='', flush=True)
    sleep(.5)
    print('..', end='', flush=True)
    sleep(.5)
    print('...', end='', flush=True)
    sleep(.5)
    print('....\n', flush=True)
    sleep(.5)


def add_client(self):
        name = input('Digite seu nome completo: ').strip()
        while True:
            cpf = input('Digite seu CPF (apenas números): ').strip()
            if not cpf.isdigit():
                print('CPF inválido, digite apenas números.\n')
                continue
            elif len(cpf) != 11:
                print('CPF inválido, deve ter 11 dígitos.\n')
                continue
            cpf_exists = any(client['cpf'] == cpf for client in clients)
            if cpf_exists:
                print('CPF já cadastrado, tente novamente.\n')
                continue
            break
        while True:
            date_of_birth = input('Digite sua data de nascimento (ex: DD/MM/AAAA): ').strip()
            if date_of_birth[2] != '/' or date_of_birth[5] != '/' or len(date_of_birth) != 10:
                print('Data inválida, use o formato DD/MM/AAAA.\n')
            else:
                break
        street = input('Digite seu endereço(ex: rua, numero): ').strip()
        neighborhood = input('Digite o nome do seu bairro: ').strip()
        while True:
            city = input('Digite o nome de sua cidade e sigla do estado (ex: Cidade/UF): ').strip()
            if city[-3] != '/' or city.count('/') != 1:
                print('Formato inválido, use Cidade/UF.\n')
            else:
                break
        adress = f'{street} - {neighborhood} - {city}'
        clients.append({
        'name': name,
        'cpf': cpf,
        'date_of_birth': date_of_birth,
        'adress': adress
    })
        print(f'Criando novo cadastro para {name}', end='', flush=True)
        loading()
        return print('Cadastro realizado com sucesso!\n')


def add_account(name, cpf, accounts):
    if accounts:
        account_number = accounts[-1]['number'] + 1
    else:
        account_number = 1
    accounts.append({
        'agency': '0001',
        'number': account_number,
        'name': name,
        'cpf': cpf,
        'withdraw_limit': 3,
        'account_balance': 0.0
    })
    print('Criando uma nova conta para você :) ', end='', flush=True)
    loading()
    print(f'Conta criada com sucesso! Número da conta: {accounts[-1]['number']}\n')


def find_account(accounts, client_found):
    print('Procurando por sua(s) conta(s)', end='', flush=True)
    loading()
    account_found = [account for account in accounts if account['cpf'] == client_found['cpf']]
    if account_found:
        print(f'{len(account_found)} conta(s) encontrada(s)\n')
        for account in account_found:
            print(f"- Agência: {account['agency']} | Número da conta: {account['number']} | Nome: {account['name']}\n")

    else:
        print('Conta não encontrada!')
        add_account(client_found['name'], client_found['cpf'], accounts)


def deposit(balance, deposit, account_found):
        if deposit > 0:
            balance += deposit
            print(f'Depósito de R${deposit:.2f} realizado com sucesso.')
            deposit_register.append(f'Depósito de R${deposit:.2f} realizado.')
            account_found['account_balance'] = deposit
        else:
            print('\033[31mValor inválido. O depósito deve ser maior que zero.\033[m')

        return balance


def withdraw(balance, withdraw, withdraw_limit, account_found):
        if withdraw_limit > 0:
            if withdraw > balance:
                print('\033[31mSaldo insuficiente para saque.\033[m')
            elif withdraw > 500:
                print('\033[31mValor do saque excede o limite de R$500,00 por saque.\033[m')
            else:
                print(f'Saque de R${withdraw:.2f} realizado com sucesso.')
                balance -= withdraw
                withdraw_limit -= 1
                withdraw_register.append(f'Saque de R${withdraw:.2f} realizado.')
                account_found['withdraw_limit'] = withdraw_limit
                account_found['account_balance'] = balance
                print(f'Você ainda pode realizar {withdraw_limit} saques hoje.')
            return balance


def balance(deposit_register, withdraw_register, /, *, account_balance):
    if deposit_register:
        print('Extrato de Depósitos:')
        for record in deposit_register:
            print(record)
    else:
        print('Nenhum depósito realizado hoje.')
    print('================================')
    if withdraw_register:
        print('Extrato de Saques:')
        for record in withdraw_register:
            print(record)
    else:
        print('Nenhum saque realizado hoje.')
    print('================================')
    print(f'Seu saldo atual é de R${account_balance:.2f}')


print('Bem vindo ao DIO Bank!\n')
while True:
    print('Você já é nosso cliente?')
    print('[1] Sim \n[2] Não, realizar cadastro\n[3] Sair\n')
    is_client = input('Digite a opção desejada: ').strip()

    if is_client == '1':
        cpf = input('Digite seu CPF (apenas números): ').strip()
        client_found = next((client for client in clients if client['cpf'] == cpf), None)
        if client_found:
            print(f'Bem vindo de volta, {client_found['name']}!\n')
            find_account(accounts, client_found)
            print('Bem vindo ao MENU de sua conta!\n')
            while True:
                print('=================================')
                print('|        Menu de Contas:        |')
                print('=================================')
                print('[1] Acessar conta\n[2] Listar suas contas\n[3] Criar nova conta\n[4] Sair\n')
                account_option = input('Digite a opção desejada: ').strip()

                if account_option == '1':
                    while True:
                        print('Acessar conta:')
                        account_number = input('Digite o número da conta que deseja acessar(somente digitos): ').strip()
                        account_found = next((account for account in accounts if account['number'] == int(account_number) and account['cpf'] == client_found['cpf']), None)
                        if account_found:
                            print(f'Conta encontrada! Agência: {account_found['agency']} | Número da conta: {account_found['number']} | Nome: {account_found['name']}\n')
                            break
                        else:
                            print('Conta não encontrada ou CPF inválido, por favor verifique os digitos e tente novamente. \n')
                        continue
                    deposit_register.clear()
                    withdraw_register.clear()

                    print('Bem vindo ao menu de operações da sua conta!')

                    while True:
                        account_balance = account_found['account_balance']
                        print('\n=================================')
                        print('|     Menu de Operações:        |')
                        print('=================================')
                        print('[1] Deposito\n[2] Saque\n[3] Extrato\n[4] Sair\n')
                        print(f'Seu saldo atual é: R${account_balance:.2f}\n')
                        operation = input('Digite a opção desejada: ').strip()

                        if operation == '1':
                            account_deposit = float(input('Digite o valor do depósito: ').replace(',', '.'))
                            account_balance = deposit(account_balance, account_deposit, account_found)

                        elif operation == '2':
                            account_withdraw = float(input('Digite o valor do saque: ').replace(',', '.'))
                            withdraw_limit = account_found['withdraw_limit']
                            account_balance = withdraw(account_balance, account_withdraw, withdraw_limit, account_found)

                        elif operation == '3':
                            balance(deposit_register, withdraw_register, account_balance=account_balance)
                            continue
                            
                        elif operation == '4':
                            print('Saindo do menu de operações', end='', flush=True)
                            loading()
                            account_found['account_balance'] = account_balance
                            break

                        else:
                            print('Opção inválida, por favor digite 1, 2, 3 ou 4.')
                            continue

                elif account_option == '2':
                    find_account(accounts, client_found)
                    continue
            
                elif account_option == '3':
                    add_account(client_found['name'], client_found['cpf'], accounts)
                    print(f'Nova conta criada com sucesso! Número da conta: {accounts[-1]['number']}\n')
                    continue

                elif account_option == '4':
                    print('Saindo do menu de contas', end='', flush=True)
                    loading()
                    break

                else:
                    print('Opção inválida, por favor digite 1, 2, 3 ou 4.')
                    continue
        else:
            while True:
                register = input('CPF não encontrado, deseja se cadastrar? [S/N]\n').strip().upper()
                if register not in ['S', 'SIM', 'N', 'NAO', 'NÃO']:
                    print('Opção inválida, por favor digite S para Sim ou N para Não.\n')
                else:
                    if register == 'S':
                        is_client = '2'
                        break
                    else:
                        continue

    if is_client == '2':
        add_client(clients)
        continue

    elif is_client == '3':
        print('Até logo, obrigado por usar nossos serviços!')
        exit()

    elif is_client not in ['1', '2', '3']:
        print('Opção inválida, por favor digite 1, 2 ou 3.')
        continue
