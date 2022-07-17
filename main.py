import telegram.ext
import os
from web3 import Web3
from dotenv import load_dotenv
import ccxt

load_dotenv()


url = os.getenv("INFURA_URL")

w3 = Web3(Web3.HTTPProvider(url))


token = os.getenv("TOKEN")



def start(update, context):
    update.message.reply_text("Hello, Welcome to the chat!, click /help for more info")

def help(update, context):
    update.message.reply_text("""
    The following are available:
    /start -> Welcome message
    /help -> provides assistance 
    /content -> all about your eth transaction
    /contact -> way to contact the developer
    /ethPrice -> gives the latest etherium price
    /ethAmount -> put in your eth address to get the amount of eth in your wallet
    /transactionDetails -> put in your transaction hash to get important details about your 
    latest transaction on the eth network
    """)

def content(update, context):
    update.message.reply_text('Get all you want to know about an eth transaction')

def contact(update, context):
    update.message.reply_text('add me up on Discord with the handle icis_04#4765')

def handle_message(update, context):
    update.message.reply_text(f"You said {update.message.text}")

def etherium_latest_price(update, context):
    binance = ccxt.binance()
    etherium_price = binance.fetch_ticker('ETH/USDC')
    update.message.reply_text(f"The latest etherium price is {etherium_price['info']['lastPrice']}")

def transaction_details(update, context):
    hash = context.args[0]
    transaction = w3.eth.get_transaction(hash)
    sender = transaction['from']
    receiver = transaction['to']
    gas = w3.fromWei(transaction.gasPrice, 'ether')
    gasPrice = w3.fromWei(transaction.gasPrice, 'ether')
    value = w3.fromWei(transaction.value, 'ether')
    update.message.reply_text(f"{value} ether was sent from {sender} to {receiver} with {gas} gas and {gasPrice} gas Price")


def eth_amount(update, context):
    address = context.args[0]
    amountWei = w3.eth.get_balance(address)
    amount = w3.fromWei(amountWei,'ether')
    update.message.reply_text(f"The amount of ether in your wallet is {amount}")


    

updater = telegram.ext.Updater(token, use_context=True)
disp = updater.dispatcher

disp.add_handler(telegram.ext.CommandHandler("start",start))
disp.add_handler(telegram.ext.CommandHandler("help",help))
disp.add_handler(telegram.ext.CommandHandler("contact",contact))
disp.add_handler(telegram.ext.CommandHandler("content",content))
disp.add_handler(telegram.ext.CommandHandler("ethPrice",etherium_latest_price))
disp.add_handler(telegram.ext.CommandHandler("transactionDetails",transaction_details))
disp.add_handler(telegram.ext.CommandHandler("ethAmount",eth_amount))
disp.add_handler(telegram.ext.MessageHandler(telegram.ext.Filters.text, handle_message))

updater.start_polling()
updater.idle()



