import datetime

from typing import (
  Dict, 
  Optional, 
  Union,
  List,
  Any
)


class Image:

  __slots__ = (
    'copyright',
    'date',
    'explanation',
    'hdurl',
    'mediatype',
    'serviceversion',
    'title',
    'url'
  )

  copyright: str
  date: datetime.datetime
  explanation: str
  hdurl: str
  mediatype: str
  serviceversion: str
  title: str
  url: str

  def __init__(self, *, data: Union[Dict[str, str], Any]) -> None:
    self.copyright: str = data.get('copyright', '')
    self.date: Union[datetime.datetime, str] = datetime.datetime.strptime(data.get('date', '1900-01-01'), '%Y-%m-%d')
    self.explanation: str = data.get('explanation', '')
    self.hdurl: str = data.get('hdurl', '')
    self.mediatype: str = data.get('mediatype', '')
    self.serviceversion: str = data.get('serviceversion', '')
    self.title: str = data.get('title', '')
    self.url: str = data.get('url', '')

  def __repr__(self) -> str:
    return f'<copyright="{self.copyright}" date="{self.date}" hdurl="{self.hdurl}" mediatype="{self.mediatype}" serviceversion="{self.serviceversion}" title="{self.title}" explanation="{self.explanation}" url="{self.url}">'

#  @property
#  def display_info(self) -> str:
#    return f'title: {self.title}, date: {self.date}, explanation: {self.explanation}, url: {self.url}, hdurl: {self.hdurl}, copyright: {self.copyright}'