import logging
from typing import Optional,Dict,Any
from .client import BinanceFuturesREST
from .utils import validate_symbol_filters
class BasicBot:
  def __init__(self,api_key:str,api_secret:str,testnet:bool=True):
    base='https://testnet.binancefuture.com' if testnet else 'https://fapi.binance.com'
    self.client=BinanceFuturesREST(api_key,api_secret,base_url=base);self.logger=logging.getLogger('binance.bot');self._symbol_cache={}
  def _get_symbol_info(self,symbol:str)->Dict[str,Any]:
    s=symbol.upper();
    if s in self._symbol_cache:return self._symbol_cache[s]
    data=self.client.exchange_info(symbol=s);syms=data.get('symbols',[])
    if not syms:raise ValueError(f'Symbol not found: {s}')
    info=syms[0];self._symbol_cache[s]=info;return info
  def place_market_order(self,symbol:str,side:str,qty:float,reduce_only:Optional[bool]=None):
    v=validate_symbol_filters(self._get_symbol_info(symbol),price=None,qty=qty)
    p={'symbol':symbol.upper(),'side':side.upper(),'type':'MARKET','quantity':v['qty']}
    if reduce_only is not None:p['reduceOnly']='true' if reduce_only else 'false'
    self.logger.info('Placing MARKET order: %s',p);return self.client.place_order(**p)
  def place_limit_order(self,symbol:str,side:str,qty:float,price:float,tif:str='GTC',reduce_only:Optional[bool]=None):
    v=validate_symbol_filters(self._get_symbol_info(symbol),price=price,qty=qty)
    p={'symbol':symbol.upper(),'side':side.upper(),'type':'LIMIT','timeInForce':tif.upper(),'quantity':v['qty'],'price':v['price']}
    if reduce_only is not None:p['reduceOnly']='true' if reduce_only else 'false'
    self.logger.info('Placing LIMIT order: %s',p);r=self.client.place_order(**p);n=v.get('notes',[]); 
    if n:r['_notes']=n
    return r
  def place_stop_limit_order(self,symbol:str,side:str,qty:float,price:float,stop_price:float,tif:str='GTC',reduce_only:Optional[bool]=None):
    v=validate_symbol_filters(self._get_symbol_info(symbol),price=price,qty=qty)
    vs=validate_symbol_filters(self._get_symbol_info(symbol),price=stop_price,qty=None)
    p={'symbol':symbol.upper(),'side':side.upper(),'type':'STOP','timeInForce':tif.upper(),'quantity':v['qty'],'price':v['price'],'stopPrice':vs['price'],'workingType':'CONTRACT_PRICE'}
    if reduce_only is not None:p['reduceOnly']='true' if reduce_only else 'false'
    self.logger.info('Placing STOP-LIMIT order: %s',p);r=self.client.place_order(**p);n=v.get('notes',[])+vs.get('notes',[]);
    if n:r['_notes']=n
    return r
  def get_order(self,symbol:str,order_id:Optional[int]=None,client_order_id:Optional[str]=None):
    p={'symbol':symbol.upper()}
    if order_id is not None:p['orderId']=int(order_id)
    if client_order_id is not None:p['origClientOrderId']=client_order_id
    if len(p)==1:raise ValueError('Provide order_id or client_order_id')
    return self.client.get_order(**p)
  def cancel_order(self,symbol:str,order_id:Optional[int]=None,client_order_id:Optional[str]=None):
    p={'symbol':symbol.upper()}
    if order_id is not None:p['orderId']=int(order_id)
    if client_order_id is not None:p['origClientOrderId']=client_order_id
    if len(p)==1:raise ValueError('Provide order_id or client_order_id')
    return self.client.cancel_order(**p)
