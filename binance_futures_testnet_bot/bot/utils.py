import math
from typing import Optional,Dict,Any
def round_to_step(v:float,s:float)->float:
    if s==0:return v
    p=max(0,int(round(-math.log10(s))))
    return float(f"{(math.floor(v/s)*s):.{p}f}")
def validate_symbol_filters(info:Dict[str,Any],price:Optional[float]=None,qty:Optional[float]=None)->dict:
    notes=[];tick=None;step=None;mn=None;mx=None
    for f in info.get('filters',[]):
        t=f.get('filterType')
        if t=='PRICE_FILTER':tick=float(f.get('tickSize',0))
        elif t=='LOT_SIZE':step=float(f.get('stepSize',0));mn=float(f.get('minQty',0));mx=float(f.get('maxQty',0))
    ap=price;aq=qty
    if price is not None and tick:
        np=round_to_step(price,tick)
        if np!=price:notes.append(f'Rounded price {price} to {np} (tickSize={tick}).')
        ap=np
    if qty is not None and step:
        nq=round_to_step(qty,step)
        if nq!=qty:notes.append(f'Rounded qty {qty} to {nq} (stepSize={step}).')
        aq=nq
    if aq is not None and mn is not None and aq<mn:raise ValueError(f'Quantity {aq} is below minQty {mn}')
    if aq is not None and mx is not None and mx>0 and aq>mx:raise ValueError(f'Quantity {aq} is above maxQty {mx}')
    return {'price':ap,'qty':aq,'notes':notes}
