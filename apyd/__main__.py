import apyd

import sys

def show_version() -> None:
  ls = []
  version_info = apyd.version_info
  ls.append(f'- Python v{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}.{sys.version_info.releaselevel}')
  ls.append(f'- apyd v{version_info.major}.{version_info.minor}.{version_info.micro}-{version_info.releaselevel}')
  print('\n'.join(ls))