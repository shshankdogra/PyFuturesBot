import time,hmac,hashlib,logging,requests
from typing import Any,Dict,Optional
from urllib.parse import urlencode
class BinanceFuturesREST:
  def __init__(self,api_key:str,api_secret:str,base_url:str='https://testnet.binancefuture.com',timeout:int=30,max_retries:int=2):
    self.api_key=api_key;self.api_secret=api_secret.encode();self.base_url=base_url.rstrip('/');self.timeout=timeout;self.max_retries=max_retries
    self.session=requests.Session();
    if api_key:self.session.headers.update({'X-MBX-APIKEY':api_key})
    self.logger=logging.getLogger('binance.client')
  def _sign(self,params:Dict[str,Any])->str:
    qs=urlencode(params,doseq=True)
    return hmac.new(self.api_secret,qs.encode(),hashlib.sha256).hexdigest()
  def _request(self,method:str,path:str,params:Optional[Dict[str,Any]]=None,signed:bool=False)->Dict[str,Any]:
    url=f"{self.base_url}{path}";params=params or {}
    if signed:
      params.setdefault('timestamp',int(time.time()*1000));params.setdefault('recvWindow',5000);params['signature']=self._sign(params)
    safe={k:('***' if k.lower()=='signature' else v) for k,v in params.items()};self.logger.info('%s %s %s',method,url,safe)
    for a in range(self.max_retries+1):
      try:
        resp=self.session.request(method,url,params=params,timeout=self.timeout)
        self.logger.info('Response %s: %s',resp.status_code,resp.text[:500]);resp.raise_for_status();return resp.json()
      except requests.HTTPError as e:
        st=e.response.status_code if e.response is not None else None
        if st and 500<=st<600 and a<self.max_retries: time.sleep(1.0*(a+1));continue
        self.logger.exception('HTTP error');raise
      except requests.RequestException:
        self.logger.exception('Request exception');raise
  def ping(self):return self._request('GET','/fapi/v1/ping')
  def time(self):return self._request('GET','/fapi/v1/time')
  def exchange_info(self,symbol:Optional[str]=None):
    p={};
    if symbol:p['symbol']=symbol.upper()
    return self._request('GET','/fapi/v1/exchangeInfo',params=p)
  def place_order(self,**p):return self._request('POST','/fapi/v1/order',params=p,signed=True)
  def get_order(self,**p):return self._request('GET','/fapi/v1/order',params=p,signed=True)
  def cancel_order(self,**p):return self._request('DELETE','/fapi/v1/order',params=p,signed=True)
