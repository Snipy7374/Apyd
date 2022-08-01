from . import __version__
from . import image
from . import errors

from typing import (
  Dict, 
  List, 
  Any, 
  Optional, 
  Union, 
  ClassVar
)

import datetime
import requests
import sys



class Route:
  BASE: ClassVar[str] = 'https://api.nasa.gov/planetary/apod'
  
  def __init__(self, path: str) -> None:
    self.path: str = path
    self.url: str = self.BASE + self.path

  @property
  def full_path(self) -> str:
    return f'{self.url}'



class RateLimit:
  """
  Represents a NASA rate limit
  """
  def __init__(self, headers: Dict[str, Union[str, int]]) -> None:
    self.max_limit: int = int(headers.get('X-Ratelimit-Limit', 0))
    self.remaining: int = int(headers.get('X-Ratelimit-Remaining', 0))
    self.max_reset_after: datetime.timedelta = datetime.timedelta(hours=1)
    self.used_request: int = self.max_limit - self.remaining

  def __repr__(self) -> str:
    return f'<RateLimit max_limit={self.max_limit} remaining={self.remaining} used_request={self.used_request} max_reset_after={self.max_reset_after} rate_limited={self.is_ratelimited()}>'

  def is_ratelimited(self) -> bool:
    if self.remaining == 1000:
      return True
    return False



class HTTPClient:
  """
  Represents an HTTP Client that sends requests to the NASA's API
  """
  def __init__(self, token) -> None:
    self.token: Optional[Union[str, Any]] = token
    self.params: Dict[str, Union[str, Any]] = {}
  
      
    user_agent = f'Apyd (https://github.com/Snipy7374 {__version__}) Python/{sys.version_info[0]}.{sys.version_info[1]} Requests/{requests.__version__}'
    self.user_agent: str = user_agent

  def request(self, route: Route) -> Union[Dict[str, str], List[Dict[str, str]]]:
    headers: Dict[str, str] = {
      'User-Agent': self.user_agent
    }
    if self.token is not None:
      self.params['api_key'] = self.token

    try:
      get = requests.get(route.url, headers=headers, params=self.params)
      out = get.json()
      heads = get.headers
    except:
      pass
    
    set_limit = RateLimit({'X-Ratelimit-Limit': heads.get('X-Ratelimit-Limit', 0), 'X-Ratelimit-Remaining': heads.get('X-Ratelimit-Remaining', 0)})
    
    if set_limit.is_ratelimited():
      raise errors.RateLimited(f'RateLimited from {Route.BASE} | {print(set_limit)}')
    
    return out

  def get_params(self) -> Dict[str, str]:
    return self.params


  def _check_api_error(self, *, response: Union[Dict[str, str], List[Dict[str, str]]]) -> None:
    if isinstance(response, dict):
      keys = response.keys()
      if 'code' in keys:
        raise errors.ClientException(f'Api error http_code {response["code"]} error_msg {response["msg"]}')

    elif isinstance(response, list):
      pass


  def _check_date(self, date: str) -> bool:
    try:
      datetime.datetime.strptime(date, '%Y-%m-%d')
      return True
    except:
      raise errors.InvalidDate(f'Date "{date}" does not match the Api date format (YYYY-MM-DD) or is invalid')

  def _clear_params(self, *, keys: Union[str, List[str]]) -> None:
    if isinstance(keys, str):
      self.params.pop(keys)

    elif isinstance(keys, list):
      for i in keys:
        if isinstance(i, str):
          self.params.pop(i)

  
  def get_date(self, *, date: Optional[Union[str, None]] = None) -> image.Image:
    if date is None:
      req = self.request(Route('/'))
      self._check_api_error(response=req)
      img = image.Image(data=req)

    elif date is not None:
      self._check_date(date)
      self.params['date'] = date
      req = self.request(Route('/'))
      self._clear_params(keys='date')
      self._check_api_error(response=req)
      img = image.Image(data=req)
    
    return img

  
  def get_spec_dates(self, *, start_date: Optional[Union[str, None]] = None, end_date: Optional[Union[str, None]] = None) -> List[image.Image]:
    used_params = []
    if start_date is not None:
      if self._check_date(start_date):
        self.params['start_date'] = start_date
        used_params.append('start_date')

    if end_date is not None:
      if self._check_date(end_date):
        self.params['end_date'] = end_date
        used_params.append('end_date')

    req = self.request(Route('/'))
    self._clear_params(keys=used_params)
    self._check_api_error(response=req)
      
    out_ls = []
    i: Union[Dict[str, str], Any]
    for i in req:
      out_ls.append(image.Image(data=i))
    return out_ls

  def get_random_img(self, *, count: int) -> List[image.Image]:
    if isinstance(count, int):
      self.params['count'] = count
      req = self.request(Route('/'))
      self._clear_params(keys='count')
      self._check_api_error(response=req)

      if isinstance(req, list):
        out_ls = []
        for i in req:
          out_ls.append(image.Image(data=i))
        return out_ls

    else:
      raise errors.BadArguments(f'"count" parameter must be of type "int" not of type {type(count)}')