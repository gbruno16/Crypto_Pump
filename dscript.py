# 1)Sincronizzare data e ora
# 2)Controllare che sia tutto in BTC
# 3)Controllare la quantitá di BTC posseduta
# 4)Nessun ordine aperto
# 5)Aprire un grafico di binance su chrome e fare l'accesso
# 6)Impostare su sell, market
# 7)Dopo 100% vendere tutto
 
import discord
from threading import Thread
import time
from binance.client import Client
from binance.enums import *
from binance.exceptions import BinanceAPIException, BinanceOrderException
import math
import re
import webbrowser
import colorama
from colorama import init, Fore, Style, Back
 


b_api_key = 'AIE8XPOvBgwe9ZXBB5Jkk91tnk88A9pFk2NgD5bbbnwhVfPkU6K7pltknDJlgMIf'
b_api_secret = 'MLuNBCthKUi0SneEUco05zdWj0ILCYg21wUCMZlg3u3IkgguWb5kRGUSd8jtlisg'
b_client = Client(b_api_key, b_api_secret)
 
def float_precision(f, n):
        n = int(math.log10(1 / float(n)))
        f = math.floor(float(f) * 10 ** n) / 10 ** n
        f = "{:0.0{}f}".format(float(f), n)
        return str(int(f)) if int(n) == 0 else f
 
def get_balance(client, coin):
  return float(client.get_asset_balance(asset=coin)['free'])
 
def get_price(client, symbol):
        price = None
        tickers = client.get_all_tickers()
        for ticker in tickers:
            if ticker['symbol'] == symbol:
                price = float(ticker['price'])
        return price
 
def get_tick_and_step_size(client, symbol):
        tick_size = None
        step_size = None
        symbol_info = client.get_symbol_info(symbol)
        for filt in symbol_info['filters']:
            if filt['filterType'] == 'PRICE_FILTER':
                tick_size = float(filt['tickSize'])
            elif filt['filterType'] == 'LOT_SIZE':
                step_size = float(filt['stepSize'])
        return tick_size, step_size
 
def get_sell_info(client, coin, symbol, price, quantity):
        tick_size, step_size = get_tick_and_step_size(client, symbol)
        price_rounded = (float_precision(price, tick_size))
        quantity_rounded = (float_precision(get_balance(client,coin), step_size))
        return price_rounded, quantity_rounded
 
def get_buy_info(client, symbol, balance):
        tick_size, step_size = get_tick_and_step_size(client, symbol)
        price = float(float_precision(get_price(client, symbol), tick_size))
        coin_currency_quantity = float_precision(balance / price, step_size)
        return price, coin_currency_quantity

 
def open_url(symbol):
    url = 'https://www.binance.com/en/trade/'+symbol+'_'+currency+'?layout=classic'
    webbrowser.register('chrome',
    None,
    webbrowser.BackgroundBrowser("C://Program Files (x86)//Google//Chrome//Application//chrome.exe"))
    webbrowser.get('chrome').open_new_tab(url)
 
def sell_status(symbol,sell_id):
  status=b_client.get_order(symbol=symbol, orderId=sell_id)['status']
  return str(status)
  
def buy(client, symbol,balance):
    try:
        price, quantity = get_buy_info(b_client, symbol+currency, balance)
        buy_market = b_client.create_order(
            symbol=symbol+currency,
            side='BUY',
            type='MARKET',
            quantity=quantity)
        #chg=float(float_precision(float(b_client.get_ticker(symbol=symbol+currency)["priceChangePercent"]),5))
        #chg=float(b_client.get_ticker(symbol=symbol+currency)["priceChangePercent"])
        price_buy=float(buy_market['fills'][0]['price'])
        quantity_buy=float(buy_market['fills'][0]['qty'])
        print(Fore.GREEN+buy_market['status']+ "! "+"Price: " +str(price_buy)+ ". Quantity: " +str(quantity_buy))
        print(Style.RESET_ALL) 
        print ('*' * 40)
        #open_url(symbol)
        return price_buy, quantity_buy
 
    except BinanceAPIException as e:
        # error handling goes here
        print(e)
    except BinanceOrderException as e:
        # error handling goes here
        print(e)
        
def sell_limit(client, symbol,price, quantity):
    try:
        price_rounded, quantity_rounded= get_sell_info(b_client,symbol, symbol+currency, price*profit, quantity)
        sell_limit = b_client.create_order(
            symbol=symbol+currency,
            side='SELL',
            type='LIMIT',
            timeInForce='GTC',
            quantity=quantity_rounded,
            price=price_rounded)
        pr=float(float_precision((profit-1)*100,0.01))
        print(Fore.GREEN+"FILLED! "+"Price: " +str(price_rounded)+ ". Potential profit: " +str(pr)+"%")
        print(Style.RESET_ALL) 
        print ('*' * 40)
        print(Back.YELLOW+Fore.BLUE+"TARGET Price: -> " +str(price_rounded))
        print(Style.RESET_ALL) 
        print ('*' * 40)
       
        orderId=sell_limit['orderId']
        return(orderId)
 
    except BinanceAPIException as e:
        # error handling goes here
        print(e)
    except BinanceOrderException as e:
        # error handling goes here
        print(e)
 
def sell_market(client, symbol,balance):
    try:
        price, quantity = get_sell_info(b_client,symbol, symbol+currency, 0, balance)
        buy_market = b_client.create_order(
            symbol=symbol+currency,
            side='SELL',
            type='MARKET',
            quantity=quantity)
        #chg=float(float_precision(float(b_client.get_ticker(symbol=symbol+currency)["priceChangePercent"]),0.01))
        price_buy=float(buy_market['fills'][0]['price'])
        quantity_buy=float(buy_market['fills'][0]['qty'])
        print(Fore.GREEN+buy_market['status']+ "! "+"Price: " +str(price_buy)+ ". Quantity: " +str(quantity_buy))
        print(Style.RESET_ALL) 
        print ('*' * 40)
        return price_buy
 
    except BinanceAPIException as e:
        # error handling goes here
        print(e)
    except BinanceOrderException as e:
        # error handling goes here
        print(e)
 
def realtime_chg(client, symbol, price,sell_id):
  #j=1
  #status=sell_status(symbol+currency,sell_id)
  status='...'
  while (t==False):
    ticker=b_client.get_ticker(symbol=symbol+currency)
    chg=float(ticker["priceChangePercent"])
    price_new=float(b_client.get_ticker(symbol=symbol+currency)["bidPrice"])
    roi=100*(price_new-price)/price
    roi_round=float_precision(roi,0.01)
    
    #if (j==5):
    #    status=sell_status(symbol+currency,sell_id)
    #    j=0
        
    if (roi<0):
            print(Fore.RED+'\rRealTime 24h Chg:'+str(chg)+'%'+' STATUS: '+str(status) +' LOSS:'+str(roi_round)+'%', end='')
    elif (roi/100>profit-1):
            print(Fore.GREEN+'\rRealTime 24h Chg:'+str(chg)+'%'+' STATUS: '+str(status)+' PROFIT:'+str(roi_round)+'%', end='')
    else:
            print(Fore.YELLOW+'\rRealTime 24h Chg:'+str(chg)+'%'+' STATUS: '+str(status) +' PROFIT:'+str(roi_round)+'%', end='')    
    # j=j+1
        
    time.sleep(0.2)
 
def panic(t1, coin, sell_id, quantity, price):
  global t
  print("Press ENTER to PANIC SELL...")
  y=input()
  if y=="":
         t=True
         t1.join()
         cancel = b_client.cancel_order(symbol=coin+currency, orderId=sell_id)
         print(cancel["status"]+" LIMIT SELL!")
         print("MARKET SELL SENDING...")
         
         price_sell=sell_market(b_client, coin,quantity)
         roi=100*(price_sell-price)/price
         roi_round=float_precision(roi,0.01)
         if (roi>0):
                  print(Fore.GREEN+"PROFIT: " + str(roi_round)+ "%")
         else:
                  print(Fore.RED+"LOSS: " + str(roi_round)+ "%") 

async def fire(x, tic):
    coin=x.upper()
    print ('*' * 40)
    print(Back.YELLOW+Fore.BLUE+"COIN DETECTED: "+coin)
    print(Style.RESET_ALL) 
    print ('*' * 40)
    
    print("MARKET BUY ORDER SENDING...")
    price, quantity= buy(b_client, coin, amount)
 
    print("SELL LIMIT ORDER SENDING...")
    sell_id=sell_limit(b_client, coin, price,quantity)
    await client.logout()
  
    toc=time.time()

    print('Elapsed time: '+str(toc-tic)+' Tic: '+str(tic)+' Toc: '+str(toc))
    t1= Thread(target=realtime_chg, args=(b_client, coin,price, sell_id,), daemon=True)
    t1.start()
    panic(t1,coin, sell_id, quantity,price)
    
class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user)
        print('Waiting for coin message...')
    async def on_message(self, message):
        #match=re.search('[#$]([a-zA-Z]*)',message.content)
        #match=re.search('([a-zA-Z]*)\/',message.content)
        match=re.search(pattern,message.content)
        if match:
              tic=time.time()
              coin=match.group(1)
              await fire(coin, tic)

init(convert=True)
currency=input('Insert currency: ')
currency=currency.upper()

balance_curr=float(get_balance(b_client,currency))
amount_perc=float(input('Insert amount % (max av. '+str(balance_curr)+' '+currency+'): ' ))
amount=amount_perc/100*balance_curr

profit=float(input('Insert profit %:'))
profit=profit/100+1

pat=input("What pattern? a)#$ or b)/")
if (pat=='a'):
  pattern='[#$]([a-zA-Z]*)'
elif (pat=='b'):
  pattern='([a-zA-Z]*)\/'
else:
  print('Not an option')
  
t=False 
print('*' * 40)
print('SUMMARY')
print('Amount: '+str(amount)+' '+currency +' ('+ str(amount_perc)+'%)')
print('Target: '+str(profit))
print('Pattern: '+str(pattern))
print('Platform: Discord')
print('*' * 40)

client = MyClient()
client.run("NzcyNTg5NTk5MzMxMDU3Njk0.YEhy5A.wKYqC_680_M1IQa0wSiSH-xjb4g", bot=False)


    