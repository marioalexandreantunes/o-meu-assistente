import os
    
"""
    Configuração dos servidores MCP (Model Context Protocol).
    
    Define os comandos e variáveis de ambiente necessárias para cada
    servidor de pesquisa disponível no sistema.
    
    Servidores configurados:
        - octagon-deep-research-mcp: Pesquisa profunda usando Octagon
        - playwright: Automação de browser para pesquisas no Google
        - tavily: Serviço de pesquisa Tavily
        - brave-search: Motor de pesquisa Brave
    
    Note:
        Todos os comandos são configurados para Windows usando 'cmd /c'
        exceto brave-search que usa npx diretamente.
"""
    
config = {
    "mcpServers": {
        "octagon-deep-research-mcp": {
            "command": "cmd",
            "args": ["/c", "npx", "-y", "octagon-deep-research-mcp@latest"],
            "env": {"OCTAGON_API_KEY": os.getenv("OCTAGON_API_KEY")},
        },
        "playwright": {
            "command": "cmd",
            "args": ["/c", "npx", "-y", "@playwright/mcp@latest", "--headless"],
        },
        "tavily": {
            "command": "cmd",
            "args": ["/c", "npx", "-y", "tavily-mcp@latest"],
            "env": {"TAVILY_API_KEY": os.getenv("TAVILY_API_KEY")},
        },
        "brave-search": {
            "command": "cmd",
            "args": ["/c", "npx", "-y", "@modelcontextprotocol/server-brave-search"],
            "env": {"BRAVE_API_KEY": os.getenv("BRAVE_API_KEY")},
        },
        "perplexity-ask": {
            "command": "cmd",
            "args": ["/c", "npx", "-y", "server-perplexity-ask"],
            "env": {"PERPLEXITY_API_KEY": os.getenv("PERPLEXITY_API_KEY")},
        },
        "wikipedia": {
            "command": "cmd",
            "args": ["/c", "npx", "-y", "wikipedia-mcp-server"],
        },
        "firecrawl-mcp": {
            "command": "cmd",
            "args": ["/c", "npx", "-y", "firecrawl-mcp"],
            "env": {"FIRECRAWL_API_KEY": os.getenv("FIRECRAWL_API_KEY")},
        },
    }
}