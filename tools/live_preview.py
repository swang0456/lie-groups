"""Save-triggered PreTeXt build and localhost preview with automatic refresh."""
import functools
import http.server
import json
from pathlib import Path
import subprocess
import sys
import threading
import time

ROOT = Path(__file__).resolve().parents[1]
WEB = ROOT / 'output/web'
STATE = {'revision': 0, 'status': 'ready'}
LOCK = threading.Lock()
SCRIPT = r'''<script>(()=>{let revision=null;const key='ptx-scroll:'+location.pathname;
const y=sessionStorage.getItem(key);if(y!==null){addEventListener('load',()=>setTimeout(()=>scrollTo(0,+y),300),{once:true});}
setInterval(async()=>{try{const s=await(await fetch('/__preview_status',{cache:'no-store'})).json();
let b=document.getElementById('preview-build-status');if(!b){b=document.createElement('div');b.id='preview-build-status';b.style='position:fixed;top:0;right:0;z-index:99999;background:#fff5cf;color:#332900;padding:5px 12px;font:13px sans-serif';document.body.appendChild(b);}
b.textContent=s.status==='building'?'Rebuilding…':s.status==='error'?'Build failed — see .preview/build.log':'';b.hidden=s.status==='ready';
if(revision===null)revision=s.revision;else if(s.revision!==revision){sessionStorage.setItem(key,scrollY);location.reload();}}catch(e){}},800);})();</script>'''

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path.split('?')[0] == '/__preview_status':
            with LOCK: data=json.dumps(STATE).encode()
            self.send_response(200);self.send_header('Content-Type','application/json');self.send_header('Cache-Control','no-store');self.end_headers();self.wfile.write(data);return
        path=Path(self.translate_path(self.path))
        if path.suffix=='.html' and path.is_file():
            data=path.read_bytes().replace(b'</body>',SCRIPT.encode()+b'</body>')
            self.send_response(200);self.send_header('Content-Type','text/html; charset=utf-8');self.send_header('Cache-Control','no-store');self.end_headers();self.wfile.write(data);return
        super().do_GET()
    def log_message(self,*args): pass

def snapshot():
    paths=[ROOT/'project.ptx',*ROOT.glob('source/**/*.ptx'),*ROOT.glob('publication/**/*.ptx')]
    return tuple(sorted((str(p),p.stat().st_mtime_ns) for p in paths if p.exists()))

def watch():
    previous=None
    while True:
        current=snapshot()
        if current!=previous:
            time.sleep(.7)
            current=snapshot()
            with LOCK: STATE['status']='building'
            print('Building saved source…',flush=True)
            with (ROOT/'.preview/build.log').open('w') as log:
                result=subprocess.run([sys.executable,'-m','pretext','build','web','--no-generate'],cwd=ROOT,stdout=log,stderr=subprocess.STDOUT)
            with LOCK:
                STATE['status']='ready' if result.returncode==0 else 'error'
                if result.returncode==0: STATE['revision']+=1
            print('Preview updated.' if result.returncode==0 else 'Build failed: .preview/build.log',flush=True)
            previous=current
        time.sleep(.4)

if __name__=='__main__':
    (ROOT/'.preview').mkdir(exist_ok=True)
    server=http.server.ThreadingHTTPServer(('127.0.0.1',8766),functools.partial(Handler,directory=str(WEB)))
    threading.Thread(target=watch,daemon=True).start()
    print('Live preview: http://127.0.0.1:8766/construction.html',flush=True)
    try:server.serve_forever()
    except KeyboardInterrupt:server.server_close()
