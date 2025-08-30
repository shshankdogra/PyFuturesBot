import os
from bot import BasicBot
def load_env_file():
  p=os.path.join('config','.env')
  if os.path.exists(p):
    try:
      for line in open(p,'r',encoding='utf-8'):
        line=line.strip()
        if not line or line.startswith('#'): continue
        if '=' in line:
          k,v=line.split('=',1); os.environ.setdefault(k.strip(),v.strip())
    except Exception: pass
def prompt(m,d=None):
  v=input(f"{m}{' ['+str(d)+']' if d is not None else ''}: ").strip(); return v or (str(d) if d is not None else '')
def main():
  load_env_file(); print('=== Binance Futures Testnet Bot - Simple UI ===')
  ak=os.getenv('API_KEY'); sc=os.getenv('API_SECRET')
  if not ak or not sc: print('Missing API_KEY/API_SECRET. Put in config/.env'); return
  bot=BasicBot(ak,sc,testnet=True)
  while True:
    print('\n1) MARKET order\n2) LIMIT order\n3) STOP-LIMIT order\n4) TWAP (Market)\n5) Order status\n6) Cancel order\n7) Exit')
    c=input('> ').strip()
    try:
      if c=='1':
        s=prompt('Symbol','BTCUSDT'); sd=prompt('Side (BUY/SELL)','BUY').upper(); q=float(prompt('Quantity','0.001'))
        print(bot.place_market_order(s,sd,q))
      elif c=='2':
        s=prompt('Symbol','BTCUSDT'); sd=prompt('Side (BUY/SELL)','SELL').upper(); q=float(prompt('Quantity','0.001')); p=float(prompt('Price','100000')); tif=prompt('TIF (GTC/IOC/FOK)','GTC').upper()
        print(bot.place_limit_order(s,sd,q,p,tif=tif))
      elif c=='3':
        s=prompt('Symbol','BTCUSDT'); sd=prompt('Side (BUY/SELL)','SELL').upper(); q=float(prompt('Quantity','0.001')); p=float(prompt('Limit price','100000')); sp=float(prompt('Stop price','101000')); tif=prompt('TIF','GTC').upper()
        print(bot.place_stop_limit_order(s,sd,q,p,sp,tif=tif))
      elif c=='4':
        from strategies.twap import TWAPRunner
        s=prompt('Symbol','BTCUSDT'); sd=prompt('Side (BUY/SELL)','BUY').upper(); tq=float(prompt('Total qty','0.003')); n=int(prompt('Slices','3')); it=float(prompt('Interval (sec)','5'))
        rn=TWAPRunner(bot); res=rn.run(s,sd,tq,n,it,use_limit=False)
        [print(r) for r in res]
      elif c=='5':
        s=prompt('Symbol','BTCUSDT'); oid=int(prompt('orderId'))
        print(bot.get_order(s,order_id=oid))
      elif c=='6':
        s=prompt('Symbol','BTCUSDT'); oid=int(prompt('orderId'))
        print(bot.cancel_order(s,order_id=oid))
      elif c=='7': print('Bye'); break
      else: print('Invalid option')
    except Exception as e:
      print('Error:',e)
if __name__=='__main__': main()
