class ClientException(Exception):
  # Called when an exception occured on
  # http client
  pass

class RateLimited(ClientException):
  # Called when your token is ratelimited by
  # the Api
  pass

class InvalidDate(ClientException):
  # Called when a date does not match the 
  # format expected by the Api (YYYY-MM-DD) or
  # when a date is invalid
  pass

class BadArguments(ClientException):
  # Called when an argument does not match
  # the expected type
  pass