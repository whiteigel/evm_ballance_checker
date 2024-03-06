from web3 import Web3
from config import *
from data import *
from prettytable import PrettyTable

with open('abi_token.json', 'r') as file:
    abi = file.read()

selected_network = "zksync"  # Изменить на "zksync", если хотите использовать другую сеть
selected_token = "usdc" # Изменить на "usdt", если хотите получить баланс другого токена

connect = Web3(Web3.HTTPProvider(rpc[selected_network]))

contract = connect.eth.contract(address=token[selected_network][selected_token], abi=abi)

decimals = contract.functions.decimals().call()

# Создание таблицы
table = PrettyTable()
table.field_names = ["Profile", "Wallet", "Tx", "ETH", "USDC"]

for profile, wallet in wallets.items():
    # Получение количества транзакций для адреса
    tx = connect.eth.get_transaction_count(wallet, "latest")
    # Получение баланса ETH для адреса, округление до 5 знака
    balance_eth = round(connect.eth.get_balance(wallet) / (10 ** 18), 5)
    # Получение баланса USDC для адреса, округление до 3 знака
    balance_usdc = round(contract.functions.balanceOf(wallet).call() / (10 ** decimals), 3)
    # Формирование таблицы для вывода
    table.add_row([profile, wallet, tx, balance_eth, balance_usdc])

# Вывод таблицы
print(table)
