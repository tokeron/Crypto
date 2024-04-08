# #import libraries
# from hdwallet import BIP44HDWallet
# from hdwallet.cryptocurrencies import EthereumMainnet
# from hdwallet.derivations import BIP44Derivation
# from hdwallet.utils import generate_mnemonic
# from web3 import Web3
# from compound import Compound
# import requests
#
# #define a base class for the wallet
# class Wallet:
#     #initialize the wallet with a mnemonic phrase and a web3 provider
#     def __init__(self, mnemonic=None, provider=None):
#         #if no mnemonic is given, generate a new one
#         if mnemonic is None:
#             mnemonic = generate_mnemonic(language="english", strength=128)
#         #create a BIP44 HD wallet for Ethereum
#         self.wallet = BIP44HDWallet(cryptocurrency=EthereumMainnet)
#         self.wallet.from_mnemonic(mnemonic=mnemonic, language="english")
#         #get the first account from the wallet
#         self.wallet.from_index(44, hardened=True)
#         self.wallet.from_index(60, hardened=True)
#         self.wallet.from_index(0, hardened=True)
#         self.wallet.from_index(0)
#         self.wallet.from_index(0)
#         #get the address and private key of the account
#         self.address = self.wallet.address()
#         self.private_key = self.wallet.private_key()
#         #connect to a web3 provider
#         self.web3 = Web3(provider)
#         #set the default gas price and limit
#         self.gas_price = self.web3.toWei(20, "gwei")
#         self.gas_limit = 21000
#
#     #generate a new pair of keys and update the wallet
#     def generate_keys(self):
#         #generate a new mnemonic phrase
#         mnemonic = generate_mnemonic(language="english", strength=128)
#         #create a new BIP44 HD wallet for Ethereum
#         self.wallet = BIP44HDWallet(cryptocurrency=EthereumMainnet)
#         self.wallet.from_mnemonic(mnemonic=mnemonic, language="english")
#         #get the first account from the wallet
#         self.wallet.from_index(44, hardened=True)
#         self.wallet.from_index(60, hardened=True)
#         self.wallet.from_index(0, hardened=True)
#         self.wallet.from_index(0)
#         self.wallet.from_index(0)
#         #get the new address and private key of the account
#         self.address = self.wallet.address()
#         self.private_key = self.wallet.private_key()
#         #return the mnemonic phrase, address, and private key
#         return mnemonic, self.address, self.private_key
#
#     #get the balance of the wallet in Ether
#     def get_balance(self):
#         #get the balance from the web3 provider
#         balance = self.web3.eth.get_balance(self.address)
#         #convert the balance from Wei to Ether
#         balance = self.web3.fromWei(balance, "ether")
#         #return the balance
#         return balance
#
#     #send Ether to another address
#     def send_transaction(self, to, amount):
#         #create a transaction dictionary
#         tx = {
#             "from": self.address,
#             "to": to,
#             "value": self.web3.toWei(amount, "ether"),
#             "gasPrice": self.gas_price
#
# #
# #
# # import tkinter as tk
# # from web3 import Web3
# #
# # # Connect to Ethereum network using Infura API
# # infura_url = "https://mainnet.infura.io/v3/4ceeef42b5604282996b92143340c06d"
# # web3 = Web3(Web3.HTTPProvider(infura_url))
# #
# # #Check Connection
# # t=web3.is_connected()
# # print(t)
# #
# # # Generate a new pair of public and private keys
# # def generate_keys():
# #     local_account = web3.eth.account.create()
# #     private_key = local_account.privateKey.hex()
# #     public_key = web3.eth.account.privateKeyToAccount(private_key).address
# #     return private_key, public_key
# #
# # # Display Ether balance for a given address
# # def get_balance(address):
# #     balance_wei = web3.eth.getBalance(address)
# #     balance_eth = web3.fromWei(balance_wei, "ether")
# #     return balance_eth
# #
# # # Send Ether from one address to another
# # def send_transaction(sender_private_key, recipient_address, amount_eth):
# #     sender_address = web3.eth.account.privateKeyToAccount(sender_private_key).address
# #     nonce = web3.eth.getTransactionCount(sender_address)
# #     tx = {
# #         "nonce": nonce,
# #         "to": recipient_address,
# #         "value": web3.toWei(amount_eth, "ether"),
# #         "gas": 2000000,
# #         "gasPrice": web3.toWei("50", "gwei"),
# #     }
# #     signed_tx = web3.eth.account.signTransaction(tx, sender_private_key)
# #     tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
# #     return tx_hash.hex()
# #
# # # Button click handlers
# # def generate_keys_handler():
# #     private_key, public_key = generate_keys()
# #     result_label.config(text=f"Private Key: {private_key}\nPublic Key (Address): {public_key}")
# #
# # def balance_handler():
# #     address_to_check = address_entry.get()
# #     balance = get_balance(address_to_check)
# #     result_label.config(text=f"Balance for address {address_to_check}: {balance} ETH")
# #
# # def send_handler():
# #     sender_private_key = sender_key_entry.get()
# #     recipient_address = recipient_entry.get()
# #     amount_eth_to_send = float(amount_entry.get())
# #     tx_hash = send_transaction(sender_private_key, recipient_address, amount_eth_to_send)
# #     result_label.config(text=f"Transaction sent! Transaction hash: {tx_hash}")
# #
# # # Create GUI
# # root = tk.Tk()
# # root.title("Ethereum Wallet")
# #
# # generate_keys_button = tk.Button(root, text="Generate Keys", command=generate_keys_handler)
# # generate_keys_button.pack()
# #
# # address_label = tk.Label(root, text="Enter Ethereum Address:")
# # address_label.pack()
# # address_entry = tk.Entry(root)
# # address_entry.pack()
# #
# # balance_button = tk.Button(root, text="Check Balance", command=balance_handler)
# # balance_button.pack()
# #
# # sender_key_label = tk.Label(root, text="Enter Sender's Private Key:")
# # sender_key_label.pack()
# # sender_key_entry = tk.Entry(root)
# # sender_key_entry.pack()
# #
# # recipient_label = tk.Label(root, text="Enter Recipient's Address:")
# # recipient_label.pack()
# # recipient_entry = tk.Entry(root)
# # recipient_entry.pack()
# #
# # amount_label = tk.Label(root, text="Enter Amount (ETH):")
# # amount_label.pack()
# # amount_entry = tk.Entry(root)
# # amount_entry.pack()
# #
# # send_button = tk.Button(root, text="Send Transaction", command=send_handler)
# # send_button.pack()
# #
# # result_label = tk.Label(root, text="")
# # result_label.pack()
# #
# # root.mainloop()
# #
# #
# # # # Import necessary libraries
# # # from web3 import Web3
# # # from flask import Flask, render_template, request
# # #
# # # app = Flask(__name__)
# # #
# # # # Connect to Ethereum network using Infura API
# # # infura_url = "https://mainnet.infura.io/v3/YOUR_INFURA_PROJECT_ID"
# # # web3 = Web3(Web3.HTTPProvider(infura_url))
# # #
# # # # Generate a new pair of public and private keys
# # # def generate_keys():
# # #     private_key = web3.eth.account.create().privateKey.hex()
# # #     public_key = web3.eth.account.privateKeyToAccount(private_key).address
# # #     return private_key, public_key
# # #
# # # # Display Ether balance for a given address
# # # def get_balance(address):
# # #     balance_wei = web3.eth.getBalance(address)
# # #     balance_eth = web3.fromWei(balance_wei, "ether")
# # #     return balance_eth
# # #
# # # # Send Ether from one address to another
# # # def send_transaction(sender_private_key, recipient_address, amount_eth):
# # #     sender_address = web3.eth.account.privateKeyToAccount(sender_private_key).address
# # #     nonce = web3.eth.getTransactionCount(sender_address)
# # #     tx = {
# # #         "nonce": nonce,
# # #         "to": recipient_address,
# # #         "value": web3.toWei(amount_eth, "ether"),
# # #         "gas": 2000000,
# # #         "gasPrice": web3.toWei("50", "gwei"),
# # #     }
# # #     signed_tx = web3.eth.account.signTransaction(tx, sender_private_key)
# # #     tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
# # #     return tx_hash.hex()
# # #
# # # # Display market chart data for a specific contract
# # # # def get_market_chart(contract_address):
# # #     # Fetch data from CoinGecko API or other sources
# # #     # Display historical market chart data in USD
# # #
# # # # Routes
# # # @app.route("/")
# # # def home():
# # #     return render_template("index.html")
# # #
# # # @app.route("/generate_keys")
# # # def keys():
# # #     private_key, public_key = generate_keys()
# # #     return f"Private Key: {private_key}\nPublic Key (Address): {public_key}"
# # #
# # # @app.route("/balance/<address>")
# # # def balance(address):
# # #     balance = get_balance(address)
# # #     return f"Balance for address {address}: {balance} ETH"
# # #
# # # @app.route("/send_transaction", methods=["POST"])
# # # def send():
# # #     sender_private_key = request.form["private_key"]
# # #     recipient_address = request.form["recipient_address"]
# # #     amount_eth = float(request.form["amount"])
# # #     tx_hash = send_transaction(sender_private_key, recipient_address, amount_eth)
# # #     return f"Transaction sent! Transaction hash: {tx_hash}"
# # #
# # # if __name__ == "__main__":
# # #     app.run(debug=True)
# # #