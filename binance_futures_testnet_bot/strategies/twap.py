import time,logging
from typing import Optional
from bot.utils import validate_symbol_filters
from bot.bot import BasicBot
class TWAPRunner:
  def __init__(self,bot:BasicBot): self.bot=bot; self.logger=logging.getLogger('binance.twap')
  def run(self,symbol:str,side:str,total_qty:float,slices:int,interval_sec:float,use_limit:bool=False,limit_price:Optional[float]=None,tif:str='GTC',reduce_only:Optional[bool]=None):
    if slices<=0: raise ValueError('slices must be > 0')
    if total_qty<=0: raise ValueError('total_qty must be > 0')
    info=self.bot._get_symbol_info(symbol); raw=total_qty/slices
    v=validate_symbol_filters(info,price=limit_price if use_limit else None,qty=raw)
    sq=v['qty']
    if sq<=0: raise ValueError('slice quantity became 0 after rounding')
    out=[]
    for i in range(slices):
      self.logger.info('TWAP slice %s/%s qty=%s',i+1,slices,sq)
      if use_limit:
        if limit_price is None: raise ValueError('limit_price required with --limit')
        r=self.bot.place_limit_order(symbol,side,sq,limit_price,tif=tif,reduce_only=reduce_only)
      else:
        r=self.bot.place_market_order(symbol,side,sq,reduce_only=reduce_only)
      out.append(r)
      if i<slices-1: time.sleep(interval_sec)
    return out
