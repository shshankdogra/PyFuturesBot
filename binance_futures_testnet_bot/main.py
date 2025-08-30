import argparse,json,logging,os,sys
from typing import Optional
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
def setup_logging():
  os.makedirs('logs',exist_ok=True)
  logging.basicConfig(level=logging.INFO,format='%(asctime)s | %(levelname)s | %(name)s | %(message)s',handlers=[logging.StreamHandler(sys.stdout),logging.FileHandler(os.path.join('logs','bot.log'),mode='a',encoding='utf-8')])
def req(v:Optional[str],key:str)->str:
  if v: return v
  e=os.getenv(key)
  if e: return e
  raise SystemExit(f'Missing required value. Provide flag or set {key}.')
def to_f(v:Optional[str],name:str):
  if v is None: return None
  try: return float(v)
  except: raise SystemExit(f'Invalid {name}: {v}')
def pjson(d): print(json.dumps(d,indent=2,sort_keys=True))
def main():
  load_env_file(); setup_logging()
  ap=argparse.ArgumentParser(description='Binance USDT-M Futures Testnet Bot (REST)')
  sub=ap.add_subparsers(dest='cmd',required=True)
  def add_auth(p):
    p.add_argument('--api-key'); p.add_argument('--api-secret'); p.add_argument('--prod',action='store_true')
  po=sub.add_parser('order'); add_auth(po)
  po.add_argument('--symbol',required=True); po.add_argument('--side',required=True,choices=['BUY','SELL','buy','sell'])
  po.add_argument('--type',required=True,choices=['MARKET','LIMIT','STOP_LIMIT','market','limit','stop_limit'])
  po.add_argument('--qty',required=True); po.add_argument('--price'); po.add_argument('--stop-price',dest='stop_price'); po.add_argument('--tif',default='GTC'); po.add_argument('--reduce-only',action='store_true')
  ps=sub.add_parser('status'); add_auth(ps); ps.add_argument('--symbol',required=True); gs=ps.add_mutually_exclusive_group(required=True); gs.add_argument('--order-id',type=int); gs.add_argument('--client-id')
  pc=sub.add_parser('cancel'); add_auth(pc); pc.add_argument('--symbol',required=True); gc=pc.add_mutually_exclusive_group(required=True); gc.add_argument('--order-id',type=int); gc.add_argument('--client-id')
  pi=sub.add_parser('info'); pi.add_argument('--symbol',required=True)
  pt=sub.add_parser('twap'); add_auth(pt); pt.add_argument('--symbol',required=True); pt.add_argument('--side',required=True,choices=['BUY','SELL','buy','sell'])
  pt.add_argument('--total-qty',required=True); pt.add_argument('--slices',type=int,default=3); pt.add_argument('--interval',type=float,default=5.0); pt.add_argument('--limit',action='store_true'); pt.add_argument('--price'); pt.add_argument('--tif',default='GTC')
  a=ap.parse_args()
  if a.cmd=='info':
    from bot.client import BinanceFuturesREST
    c=BinanceFuturesREST(api_key='',api_secret='',base_url='https://testnet.binancefuture.com'); pjson(c.exchange_info(symbol=a.symbol.upper())); return
  ak=req(getattr(a,'api_key',None),'API_KEY'); asct=req(getattr(a,'api_secret',None),'API_SECRET'); bot=BasicBot(ak,asct,testnet=(not getattr(a,'prod',False)))
  if a.cmd=='order':
    side=a.side.upper(); typ=a.type.upper(); qty=to_f(a.qty,'qty'); price=to_f(a.price,'price'); sp=to_f(a.stop_price,'stop_price')
    if typ=='MARKET': r=bot.place_market_order(a.symbol,side,qty,reduce_only=a.reduce_only)
    elif typ=='LIMIT':
      if price is None: raise SystemExit('LIMIT order requires --price')
      r=bot.place_limit_order(a.symbol,side,qty,price,tif=a.tif,reduce_only=a.reduce_only)
    elif typ=='STOP_LIMIT':
      if price is None or sp is None: raise SystemExit('STOP_LIMIT requires --price and --stop-price')
      r=bot.place_stop_limit_order(a.symbol,side,qty,price,sp,tif=a.tif,reduce_only=a.reduce_only)
    else: raise SystemExit(f'Unsupported type: {typ}')
    pjson(r)
  elif a.cmd=='status':
    r=bot.get_order(a.symbol,order_id=a.order_id) if a.order_id is not None else bot.get_order(a.symbol,client_order_id=a.client_id); pjson(r)
  elif a.cmd=='cancel':
    r=bot.cancel_order(a.symbol,order_id=a.order_id) if a.order_id is not None else bot.cancel_order(a.symbol,client_order_id=a.client_id); pjson(r)
  elif a.cmd=='twap':
    from strategies.twap import TWAPRunner
    side=a.side.upper(); tq=to_f(a.total_qty,'total-qty'); lp=to_f(a.price,'price'); rn=TWAPRunner(bot)
    pjson(rn.run(a.symbol,side,tq,a.slices,a.interval,use_limit=a.limit,limit_price=lp,tif=a.tif))
if __name__=='__main__': main()
