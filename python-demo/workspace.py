"""Local Python retrieval + MCP tool demo. Run: python workspace.py
No external packages, employer data, model connection, or cloud credentials.
Use --export index.html to export the same UI for static hosting.
"""
import argparse
import html
import json
import re
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

DOCUMENTS = [
    {'id': 'deployment', 'title': 'Java service deployment', 'text': 'Build and test the Java service. Review configuration and identity permissions. Deploy to a staging environment, then check application logs before promoting a release.'},
    {'id': 'identity', 'title': 'Service identity and access', 'text': 'Give each service an explicit identity. Grant only the permissions needed for its task. Check authorization before reading documents or invoking a backend tool.'},
    {'id': 'storage', 'title': 'Object storage integration', 'text': 'Keep application documents in object storage. Validate object identifiers, check read permissions, and handle missing objects without exposing internal details.'},
]

def search_documents(query):
    if not isinstance(query, str) or not query.strip() or len(query) > 500:
        raise ValueError('Enter a search query between 1 and 500 characters.')
    terms = set(re.findall(r'[a-z0-9]+', query.lower()))
    ranked = sorted(DOCUMENTS, key=lambda d: -len(terms & set(re.findall(r'[a-z0-9]+', (d['title'] + ' ' + d['text']).lower()))))
    return [d for d in ranked if terms & set(re.findall(r'[a-z0-9]+', (d['title'] + ' ' + d['text']).lower()))]

def read_document(document_id):
    for document in DOCUMENTS:
        if document['id'] == document_id:
            return document
    raise ValueError('Document not found.')

TOOLS = [
    {'name': 'search_documents', 'description': 'Search the sample engineering documents using keyword retrieval.', 'inputSchema': {'type': 'object', 'properties': {'query': {'type': 'string', 'minLength': 1, 'maxLength': 500}}, 'required': ['query'], 'additionalProperties': False}},
    {'name': 'read_document', 'description': 'Read a sample document by its identifier.', 'inputSchema': {'type': 'object', 'properties': {'document_id': {'type': 'string'}}, 'required': ['document_id'], 'additionalProperties': False}},
]

def rpc(message):
    """Small stateless JSON-RPC endpoint for MCP initialize and tool requests."""
    if not isinstance(message, dict) or message.get('jsonrpc') != '2.0':
        return {'jsonrpc': '2.0', 'id': None, 'error': {'code': -32600, 'message': 'Invalid request'}}
    if 'id' not in message:
        return None
    identity = message['id']
    method = message.get('method')
    params = message.get('params', {})
    try:
        if not isinstance(params, dict):
            raise ValueError('Parameters must be an object.')
        if method == 'initialize':
            result = {'protocolVersion': '2025-03-26', 'capabilities': {'tools': {}}, 'serverInfo': {'name': 'portfolio-python-workspace', 'version': '1.0.0'}}
        elif method == 'ping':
            result = {}
        elif method == 'tools/list':
            result = {'tools': TOOLS}
        elif method == 'tools/call':
            name, args = params.get('name'), params.get('arguments', {})
            if not isinstance(args, dict):
                raise ValueError('Tool arguments must be an object.')
            try:
                if name == 'search_documents':
                    if set(args) != {'query'}:
                        raise ValueError('search_documents requires only query.')
                    value = search_documents(args['query'])
                elif name == 'read_document':
                    if set(args) != {'document_id'} or not isinstance(args['document_id'], str):
                        raise ValueError('read_document requires document_id.')
                    value = read_document(args['document_id'])
                else:
                    raise ValueError('Unknown tool.')
                result = {'content': [{'type': 'text', 'text': json.dumps(value)}], 'isError': False}
            except ValueError as error:
                result = {'content': [{'type': 'text', 'text': str(error)}], 'isError': True}
        else:
            return {'jsonrpc': '2.0', 'id': identity, 'error': {'code': -32601, 'message': 'Method not found'}}
        return {'jsonrpc': '2.0', 'id': identity, 'result': result}
    except ValueError as error:
        return {'jsonrpc': '2.0', 'id': identity, 'error': {'code': -32602, 'message': str(error)}}

HTML = r'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Python tool workspace</title><style>
*{box-sizing:border-box}body{margin:0;background:#fff;color:#26313b;font:14px/1.5 system-ui,sans-serif}header{padding:16px 24px;border-bottom:1px solid #e3e7eb;display:flex;justify-content:space-between;gap:16px;align-items:center}h1{font-size:18px;margin:0;font-weight:600}.badge{font-size:11px;background:#edf4ed;color:#446249;padding:4px 8px;border-radius:4px}.layout{display:grid;grid-template-columns:160px 1fr;min-height:470px}nav{background:#f7f8fa;padding:24px 12px;border-right:1px solid #e3e7eb}nav p{padding:8px 12px;color:#73808b;font-size:12px;margin:0 0 8px}.active{background:#e9edf2;border-radius:4px;color:#26313b!important}main{padding:24px;min-width:0}.label{font-size:11px;color:#74818a;text-transform:uppercase;letter-spacing:1px}h2{font-size:16px;font-weight:600;margin:4px 0 16px}form{display:flex;gap:8px;margin:0 0 20px}input{flex:1;min-width:0;padding:10px 12px;border:1px solid #ced6de;border-radius:4px;font:inherit}button{border:1px solid #273746;background:#273746;color:#fff;border-radius:4px;padding:8px 16px;font:inherit;cursor:pointer}button:focus-visible,input:focus-visible{outline:2px solid #5189bd;outline-offset:3px}.columns{display:grid;grid-template-columns:1.4fr 1fr;gap:20px}.panel{border:1px solid #e1e6eb;border-radius:6px;padding:16px;min-width:0}.panel h3{font-size:13px;margin:0 0 12px;font-weight:600}.document{padding:12px 0;border-top:1px solid #e8edf1}.document:first-child{padding-top:0;border-top:0}.document strong{font-size:13px;font-weight:600}.document p{color:#69757e;font-size:12px;margin:6px 0 0}.trace{font:11px/1.8 ui-monospace,monospace;white-space:pre-wrap;overflow-wrap:anywhere;color:#586774;margin:0}.tools{border-top:1px solid #e3e7eb;margin-top:20px;padding-top:16px;font-size:12px;color:#74818a}.tools code{color:#405568;margin-left:12px}footer{padding:12px 24px;border-top:1px solid #e3e7eb;font-size:11px;color:#74818a}.status{font-size:11px;color:#74818a;margin:12px 0 0}@media(max-width:650px){.layout{grid-template-columns:1fr}nav{display:none}.columns{grid-template-columns:1fr}main{padding:16px}header{padding:16px;align-items:flex-start;flex-direction:column;gap:6px}form{flex-wrap:wrap}.trace{font-size:11px}}@media(prefers-reduced-motion:reduce){*{scroll-behavior:auto}}
</style></head><body><header><h1>Engineering knowledge</h1><span class="badge">Python / MCP demo · Sample documents</span></header><div class="layout"><nav aria-label="Workspace areas"><p class="active">Document search</p><p>Available tools</p><p>Request activity</p></nav><main><span class="label">Retrieval workspace</span><h2>Find guidance, inspect the tool call.</h2><form id="search"><input id="query" aria-label="Search sample documents" value="Java service deployment" maxlength="500" required><button>Search</button></form><div class="columns"><section class="panel"><h3>Source documents</h3><div id="results">__INITIAL__</div></section><section class="panel"><h3>Tool activity</h3><pre class="trace" id="trace">search_documents
query: Java service deployment

read_document
id: deployment

Review source before use.</pre><p id="status" class="status" aria-live="polite">Static preview. Run the Python file to use its MCP endpoint.</p></section></div><div class="tools">Python tools<code>search_documents</code><code>read_document</code></div></main></div><footer>Runnable portfolio demo. Local sample documents; keyword retrieval, no connected language model or employer data.</footer><script>
const samples=__DOCUMENTS__;
const result=document.querySelector('#results'),trace=document.querySelector('#trace'),status=document.querySelector('#status');
function render(docs){result.replaceChildren();if(!docs.length){const p=document.createElement('p');p.textContent='No matching documents. Try “identity”, “Java”, or “storage”.';result.append(p);}docs.forEach(d=>{const article=document.createElement('article');article.className='document';const name=document.createElement('strong'),text=document.createElement('p');name.textContent=d.title;text.textContent=d.text;article.append(name,text);result.append(article);});}
async function call(name,args){const response=await fetch('/mcp',{method:'POST',headers:{'Content-Type':'application/json','Accept':'application/json'},body:JSON.stringify({jsonrpc:'2.0',id:1,method:'tools/call',params:{name,arguments:args}})});if(!response.ok)throw Error('Python endpoint unavailable.');const data=await response.json();if(data.error||data.result?.isError)throw Error(data.error?.message||data.result.content[0].text);return JSON.parse(data.result.content[0].text);}
document.querySelector('#search').addEventListener('submit',async event=>{event.preventDefault();const query=document.querySelector('#query').value.trim();if(!query)return;let docs,local=false;try{docs=await call('search_documents',{query});if(docs.length)await call('read_document',{document_id:docs[0].id});local=true;}catch(error){const words=new Set(query.toLowerCase().match(/[a-z0-9]+/g)||[]);docs=samples.map(d=>({...d,score:[...words].filter(w=>(d.title+' '+d.text).toLowerCase().split(/[^a-z0-9]+/).includes(w)).length})).filter(d=>d.score).sort((a,b)=>b.score-a.score);}render(docs);trace.textContent='search_documents\nquery: '+query+'\n\n'+(docs.length?'read_document\nid: '+docs[0].id:'No matching sources.')+'\n\nReview source before use.';status.textContent=local?'Python MCP endpoint · tool calls completed.':'Static preview · browser-only sample search. Run workspace.py for Python tool calls.';});
</script></body></html>'''

def render_page():
    initial = ''.join('<article class="document"><strong>' + html.escape(d['title']) + '</strong><p>' + html.escape(d['text']) + '</p></article>' for d in search_documents('Java service deployment'))
    return HTML.replace('__INITIAL__', initial).replace('__DOCUMENTS__', json.dumps(DOCUMENTS))

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path not in ('/', '/index.html'):
            self.send_error(404)
            return
        data = render_page().encode()
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.send_header('Content-Length', str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_POST(self):
        if self.path != '/mcp':
            self.send_error(404)
            return
        try:
            length = int(self.headers.get('Content-Length', 0))
            if length <= 0 or length > 16384:
                self.send_error(413)
                return
            message = json.loads(self.rfile.read(length))
            answer = rpc(message)
        except (ValueError, UnicodeDecodeError):
            answer = {'jsonrpc': '2.0', 'id': None, 'error': {'code': -32700, 'message': 'Parse error'}}
        if answer is None:
            self.send_response(202)
            self.end_headers()
            return
        data = json.dumps(answer).encode()
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(data)))
        self.end_headers()
        self.wfile.write(data)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--export', type=Path)
    parser.add_argument('--port', type=int, default=8765)
    args = parser.parse_args()
    if args.export:
        args.export.write_text(render_page(), encoding='utf-8')
    else:
        print(f'Open http://127.0.0.1:{args.port} — MCP endpoint: /mcp', flush=True)
        ThreadingHTTPServer(('127.0.0.1', args.port), Handler).serve_forever()
