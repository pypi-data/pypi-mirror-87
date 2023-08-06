from fastcore.script import *
from fastcore.utils import *
from fastcgi import fastcgi
from ghapi.build_lib import GH_OPENAPI_URL
from jsonref import loads

path,pre = Path('api.json'),'/repos/{owner}/{repo}'
try:
    s = urlread(GH_OPENAPI_URL).decode()
    path.write_text(s)
except Exception as e:
    print(e)
    s = path.read_text()
js = loads(s)['paths']

@fastcgi
#@call_parse
def run():
    r = sys.stdin.read().strip()
    print("Content-type: text/plain\n")
    if not r: return
    print(js[pre+r])

