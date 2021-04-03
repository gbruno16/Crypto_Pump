# 1)Sincronizzare data e ora
# 2)Controllare che sia tutto in BTC
# 3)Controllare la quantitá di BTC posseduta
# 4)Nessun ordine aperto
# 5)Aprire un grafico di binance su chrome e fare l'accesso
# 6)Impostare su sell, market
# 7)Dopo 100% vendere tutto
 

from threading import Thread
import time
from kucoin.client import Client
from binance.enums import *
from binance.exceptions import BinanceAPIException, BinanceOrderException
from kucoin.exceptions import KucoinAPIException, MarketOrderException, LimitOrderException

import math
import re
import webbrowser
import colorama
from colorama import init, Fore, Style, Back
 


k_api_key = '6057c13869dbd80006792653'
k_api_secret = '0e5e6ab8-b441-47aa-af06-9a856594569e'
k_api_passphrase= 'apipump'
k_client = Client(k_api_key, k_api_secret, k_api_passphrase)
 
def float_precision(f, n):
        n = int(math.log10(1 / float(n)))
        f = math.floor(float(f) * 10 ** n) / 10 ** n
        f = "{:0.0{}f}".format(float(f), n)
        return str(int(f)) if int(n) == 0 else f
 
def get_balance(client, coin):
  accounts = k_client.get_accounts()
  balance_curr=0
  for acc in accounts:
            if acc['currency'] == coin and float(acc['available'])>0:
                balance_curr=float(acc['available'])

  return float(balance_curr)
 
def get_price(client, symbol):
        price = None
        ticker = client.get_ticker(symbol)
        price = float(ticker['price'])
        return price
 
def get_tick_and_step_size(client, symbol):
        tick_size = None
        step_size = None
        symbol_info = client.get_symbols()
        for sym in symbol_info:
          if sym['symbol']==symbol:
            tick_size = float(sym['priceIncrement'])
            step_size = float(sym['baseIncrement'])
        
        return tick_size, step_size
 
def get_sell_info(client, coin, symbol, price, quantity):
        tick_size, step_size = get_tick_and_step_size(client, symbol)
        price_rounded = (float_precision(price, tick_size))
        quantity_rounded = float_precision(get_balance(client,coin), step_size)
        print(quantity_rounded)
        return price_rounded, quantity_rounded
 
def get_buy_info(client, symbol, balance):
        tick_size, step_size = get_tick_and_step_size(client, symbol)
        price = float(float_precision(get_price(client, symbol), tick_size))
        coin_currency_quantity = float_precision(balance / price, step_size)
        print(time.time()-tic)
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
        price, size = get_buy_info(client, symbol+'-'+currency, balance)
        buy_market = client.create_market_order(symbol+'-'+currency, Client.SIDE_BUY, size=size)
        
        #chg=float(float_precision(float(b_client.get_ticker(symbol=symbol+currency)["priceChangePercent"]),5))
        #chg=float(b_client.get_ticker(symbol=symbol+currency)["priceChangePercent"])
        print('Waiting for filling...')
        filled=False
        #while not filled:
        #    time.sleep(0.1)
        #    fills = client.get_fills(order_id=buy_market['orderId'])
        #    if fills['items']!=[]:
        #      filled=True
            
        
        price_buy=None
        quantity_buy=None
        #price_buy=float(fills['items'][0]['price'])
        #quantity_buy=float(fills['items'][0]['size'])
        
        price_buy=price
        quantity_buy=size
        
        print(Fore.GREEN+"FILLED! "+"Price: " +str(price_buy)+ ". Quantity: " +str(quantity_buy))
        print(Style.RESET_ALL) 
        print ('*' * 40)
        #open_url(symbol)
        return price_buy, quantity_buy
 
    except KucoinAPIException as e:
        # error handling goes here
        print(e)
    except MarketOrderException as e:
        # error handling goes here
        print(e)
        
def sell_limit(client, symbol,price, quantity):
          
    try:
        price_rounded, size_rounded= get_sell_info(client,symbol, symbol+'-'+currency, price*profit, quantity)
        sell_limit=client.create_limit_order(symbol+'-'+currency, Client.SIDE_SELL, price_rounded, size_rounded)
        
        pr=float(float_precision((profit-1)*100,0.01))
        print(Fore.GREEN+"FILLED! "+"Price: " +str(price_rounded)+ ". Potential profit: " +str(pr)+"%")
        print(Style.RESET_ALL) 
        print ('*' * 40)
        print(Back.YELLOW+Fore.BLUE+"TARGET Price: -> " +str(price_rounded))
        print(Style.RESET_ALL) 
        print ('*' * 40)
       
        orderId=sell_limit['orderId']
        return(orderId)
 
    except KucoinAPIException as e:
        # error handling goes here
        print(e)
    except LimitOrderException as e:
        # error handling goes here
        print(e)
 
def sell_market(client, symbol,balance):
    try:
        price, size = get_sell_info(k_client,symbol, symbol+'-'+currency, 0, balance)
        buy_market = client.create_market_order(symbol+'-'+currency, Client.SIDE_SELL, size=size)
       
        #chg=float(float_precision(float(b_client.get_ticker(symbol=symbol+currency)["priceChangePercent"]),0.01))
        print('SENT.')
        #filled=False
        #while not filled:
        #    time.sleep(0.1)
#            fills = client.get_fills(order_id=buy_market['orderId'])
        #    if fills['items']!=[]:
        #      filled=True
        
        #price_buy=None
        #quantity_buy=None
        #price_buy=float(fills['items'][0]['price'])
        #quantity_buy=float(fills['items'][0]['size'])
        #print(Fore.GREEN+"FILLED! "+"Price: " +str(price_buy)+ ". Quantity: " +str(quantity_buy))
        #print(Style.RESET_ALL) 
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
  status='b...'
  chg=0
  while (t==False):
    ticker=client.get_ticker(symbol+'-'+currency)
    price_new=float(ticker["price"])
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
         cancel = k_client.cancel_order(sell_id)
         print("DELETING LIMIT SELL!")
         print("MARKET SELL SENDING...")
         
         price_sell=sell_market(k_client, coin,quantity)
         roi=100*(price_sell-price)/price
         roi_round=float_precision(roi,0.01)
         if (roi>0):
                  print(Fore.GREEN+"PROFIT: " + str(roi_round)+ "%")
         else:
                  print(Fore.RED+"LOSS: " + str(roi_round)+ "%") 

def fire(x, tic):
    coin=x.upper()
    print ('*' * 40)
    print(Back.YELLOW+Fore.BLUE+"COIN: "+coin)
    print(Style.RESET_ALL) 
    print ('*' * 40)
    
    print("MARKET BUY ORDER SENDING...")
    price, quantity= buy(k_client, coin, amount)
 
    print("SELL LIMIT ORDER SENDING...")
    sell_id=sell_limit(k_client, coin, price,quantity)
    
  
    toc=time.time()

    print('Elapsed time: '+str(toc-tic)+' Tic: '+str(tic)+' Toc: '+str(toc))
    t1= Thread(target=realtime_chg, args=(k_client, coin,price, sell_id,), daemon=True)
    t1.start()
    panic(t1,coin, sell_id, quantity,price)
    


init(convert=True)
currency=input('Insert currency: ')
currency=currency.upper()


balance_curr=get_balance(k_client,currency)

amount_perc=float(input('Insert amount % (max av. '+str(balance_curr)+' '+currency+'): ' ))
amount=amount_perc/100*balance_curr

profit=float(input('Insert profit %:'))
profit=profit/100+1

  
t=False 
print('*' * 40)
print('SUMMARY')
print('Amount: '+str(amount)+' '+currency +' ('+ str(amount_perc)+'%)')
print('Target: '+str(profit))
print('Exchange: Kucoin')
print('Method: Manual')
print('*' * 40)

coin=input('Input the coin name: ')
tic=time.time()
fire(coin, tic)

     