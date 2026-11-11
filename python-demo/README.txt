Python / MCP workspace

Requires Python 3.10 or newer. No packages or API keys are required.

Run: python workspace.py
Open: http://127.0.0.1:8765

The /mcp endpoint accepts JSON-RPC initialize, ping, tools/list, and tools/call requests. Available tools: search_documents and read_document. This is a small stateless demo, not a full production MCP deployment.

The demo uses local sample documents and keyword retrieval. It does not call an LLM or claim to reproduce an employer application. When exported to index.html, browser-side sample search works without Python; local Python mode makes actual tool requests to /mcp.

Export static UI: python workspace.py --export index.html
