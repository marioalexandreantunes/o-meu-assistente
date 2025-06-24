import os
from dotenv import load_dotenv


"""
    Configuração dos servidores MCP (Model Context Protocol).

    Define os comandos e variáveis de ambiente necessárias para cada
    servidor de pesquisa disponível no sistema.

    Servidores configurados:
        - octagon-deep-research-mcp: Pesquisa profunda usando Octagon (Gratis 10/mes)
        - playwright: Automação de browser para pesquisas no Google (Gratis)
        - tavily: Serviço de pesquisa Tavily (Gratis 1000/mes)
        - brave-search: Motor de pesquisa Brave (Gratis 2000/mes)
        - perplexity-ask: Serviço de pesquisa Perplexity (Pago)
        - wikipedia: Serviço de pesquisa Wikipedia (Gratis)
        - firecrawl: Serviço de pesquisa Firecrawl (Gratis 500/mes)
        - filesystem: Acesso ao sistema de arquivos local (Gratis)
        - scrapi: Serviço de pesquisa Scrapi (Pago)
        - search1api: Serviço de pesquisa Search1API (Pago)
        - google-search: Motor de pesquisa Google (Gratis)
        - duckduckgo-search: Motor de pesquisa DuckDuckGo (Gratis)
        - facebook: Serviço de pesquisa Facebook (Pago)
        - instagram: Serviço de pesquisa Instagram (Pago)
        - linkedin: Serviço de pesquisa LinkedIn (Creditos Gratis)

    Note:
        Todos os comandos são configurados para Windows usando 'cmd /c'
        exceto brave-search que usa npx diretamente.
"""

load_dotenv()


all_mcp_servers = {
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
        "firecrawl": {
            "command": "cmd",
            "args": ["/c", "npx", "-y", "firecrawl-mcp"],
            "env": {"FIRECRAWL_API_KEY": os.getenv("FIRECRAWL_API_KEY")},
        },
        "filesystem": {
            "command": "cmd",
            "args": [
                "/c",
                "npx",
                "-y",
                "@modelcontextprotocol/server-filesystem",
                os.getcwd(),
            ],
        },
        "scrapi": {
            "command": "cmd",
            "args": ["/c", "npx", "-y", "@deventerprisesoftware/scrapi-mcp"],
            "env": {
                "SCRAPI_API_KEY": os.getenv("SCRAPI_API_KEY")
            },  # https://scrapi.tech/
        },
        "search1api": {
            "command": "cmd",
            "args": ["/c", "npx", "-y", "search1api-mcp"],
            "env": {
                "SEARCH1API_KEY": os.getenv("SEARCH1API_KEY")
            },  # https://www.search1api.com/pricing
        },
        "google-search": {
            "command": "cmd",
            "args": ["/c", "npx", "-y", "@adenot/mcp-google-search"],
            "env": {
                "GOOGLE_API_KEY": os.getenv("GOOGLE_API_KEY"),
                "GOOGLE_SEARCH_ENGINE_ID": os.getenv(
                    "GOOGLE_SEARCH_ENGINE_ID"
                ),  # https://github.com/adenot/mcp-google-search
            },
        },
        "duckduckgo-search": {
            "command": "cmd",
            "args": ["/c", "npx", "-y", "duckduckgo-mcp-server"],
        },
        "facebook": {
            "command": "cmd",
            "args": [
                "/c",
                "npx",
                "-y",
                "mcp-remote",
                "https://mcp.apify.com/sse?actors=alien_force/facebook-search-scraper",
                "--header",
                "Authorization: Bearer "
                + os.getenv(
                    "APIFY_API_KEY"
                ),  # https://apify.com/alien_force/facebook-search-scraper/api/mcp
            ],
        },
        "instagram": {
            "command": "cmd",
            "args": [
                "/c",
                "npx",
                "-y",
                "mcp-remote",
                "https://mcp.apify.com/sse?actors=apify/instagram-search-scraper",
                "--header",
                "Authorization: Bearer "
                + os.getenv(
                    "APIFY_API_KEY"
                ),  # https://apify.com/apify/instagram-search-scraper/api/mcp
            ],
        },
        "linkedin": {
            "command": "cmd",
            "args": ["/c", "npx", "-y", "@horizondatawave/mcp"],
            "env": {
                "HDW_ACCESS_TOKEN": os.getenv("HDW_ACCESS_TOKEN"),
                "HDW_ACCOUNT_ID": os.getenv("HDW_ACCOUNT_ID"),  # horizondatawave.ai
            },
        },
    }
}

web_mcp_servers = {
    "mcpServers": {
        "playwright": {
            "command": "cmd",
            "args": ["/c", "npx", "-y", "@playwright/mcp@latest", "--headless"],
        },
        "tavily": {
            "command": "cmd",
            "args": ["/c", "npx", "-y", "tavily-mcp@latest"],
            "env": {"TAVILY_API_KEY": os.getenv("TAVILY_API_KEY")},
        },
    }
}
