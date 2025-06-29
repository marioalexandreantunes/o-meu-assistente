"""
Sistema de Atualização Automática de Dados de Instituições

Este módulo implementa um sistema automatizado para pesquisar e atualizar
informações de instituições usando múltiplos serviços de pesquisa (Google,
Tavily, Brave Search) através do protocolo MCP (Model Context Protocol).

O sistema carrega dados de um arquivo Excel, pesquisa informações atualizadas
online e consolida os resultados usando LLMs para produzir dados mais completos
e precisos sobre cada instituição.

Dependências:
    - asyncio: Para operações assíncronas
    - os: Para variáveis de ambiente
    - json: Para manipulação de dados JSON
    - mcp_use: Para integração com servidores MCP
    - gestor_instituicoes: Classe personalizada para gestão de instituições
    - rich: Para output formatado no console
    - dotenv: Para carregamento de variáveis de ambiente
    - langchain_openai: Para integração com LLMs

Variáveis de ambiente necessárias:
    - GROQ_API_KEY: Chave da API Groq
    - OPENROUTER_API_KEY: Chave da API OpenRouter
    - OCTAGON_API_KEY: Chave da API Octagon
    - TAVILY_API_KEY: Chave da API Tavily
    - BRAVE_API_KEY: Chave da API Brave Search
    - FICHEIRO: Caminho para o arquivo Excel de entrada
    - JANELA: Nome da folha do Excel a ser processada
"""

import asyncio
import os
import json
import mcp_use

from gestor_instituicoes import GestorInstituicoes
from rich.console import Console
from rich.panel import Panel
from rich import print
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from mcp_use import MCPAgent, MCPClient
from instituicao import Instituicao
from mcp_servers import all_mcp_servers, web_mcp_servers

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()


async def processar_instituicao_google(
    agent: MCPAgent, instituicao: Instituicao, console: Console
) -> dict:
    """
    Pesquisa informações da instituição no Google.

    Args:
        agent (MCPAgent): Agente MCP configurado para pesquisa
        instituicao (Instituicao): Instituição a ser pesquisada
        console (Console): Console Rich para output formatado

    Returns:
        dict: Dados encontrados no Google ou dicionário vazio em caso de erro
    """
    console.print("🔍 Pesquisando no Google...", style="cyan")

    try:
        playwright_prompt = f"""  # Prompt para pesquisa no Google, usando browser_navigate
                Procura informações sobre '{instituicao.instituicao}' em Portugal usando o Google.
              
                Passos:
                1. Navega para https://www.google.com/search?q={instituicao.instituicao.replace(" ", "+")}+Portugal+contacto
                2. Procura pelos dados: email, telefone, morada, código postal com localidade, pessoa de contacto, website
                3. Extrai as informações encontradas
                4. Retorna APENAS um JSON válido no formato:
                {{
                    "Instituição": "{instituicao.instituicao}",
                    "Direção": "Pessoa contacto encontrada ou vazio",
                    "E-Mail": "email encontrado ou vazio",
                    "Telefone": "telefone encontrado ou vazio", 
                    "Morada": "morada encontrada ou vazio",
                    "Codigo Postal": "código postal encontrado ou vazio",
                    "Observações": "website url"
                }}
                """

        playwright_response = await agent.run(
            playwright_prompt,
            max_steps=20,
            manage_connector=True,
        )

        # Extrair JSON da resposta
        if playwright_response:
            start_idx = playwright_response.find("{")
            end_idx = playwright_response.rfind("}") + 1
            if start_idx != -1 and end_idx > start_idx:
                json_str = playwright_response[start_idx:end_idx]
                return json.loads(json_str)
            else:
                console.print(
                    "⚠️ Resposta do Google não contém JSON válido", style="yellow"
                )
                return {}

    except Exception as e:
        console.print(f"⚠️ Erro na pesquisa Google: {str(e)}", style="yellow")
        return {}


async def processar_instituicao_tavily(
    agent: MCPAgent, instituicao: Instituicao, console: Console
) -> dict:
    """
    Pesquisa informações da instituição usando Tavily.

    Args:
        agent (MCPAgent): Agente MCP configurado para pesquisa
        instituicao (Instituicao): Instituição a ser pesquisada
        console (Console): Console Rich para output formatado

    Returns:
        dict: Dados encontrados no Tavily ou dicionário vazio em caso de erro
    """
    console.print("🔍 Pesquisando com Tavily...", style="cyan")

    try:
        tavily_prompt = f"""  # Prompt para pesquisa com Tavily
                Usando tavily-search, procura informações sobre '{instituicao.instituicao}' em Portugal.
                Procura por: email, telefone, morada, código postal com localidade, pessoa de contacto, website.
              
                Retorna APENAS um JSON válido no formato:
                {{
                    "Instituição": "{instituicao.instituicao}",
                    "Direção": "pessoa de contacto encontrada ou vazio",
                    "E-Mail": "email encontrado ou vazio",
                    "Telefone": "telefone encontrado ou vazio",
                    "Morada": "morada encontrada ou vazio", 
                    "Codigo Postal": "código postal encontrado ou vazio",
                    "Observações": "website url"
                }}
                """

        tavily_response = await agent.run(
            tavily_prompt,
            max_steps=20,
            manage_connector=True,
        )

        # Extrair JSON da resposta
        if tavily_response:
            start_idx = tavily_response.find("{")
            end_idx = tavily_response.rfind("}") + 1
            if start_idx != -1 and end_idx > start_idx:
                json_str = tavily_response[start_idx:end_idx]
                return json.loads(json_str)
            else:
                console.print(
                    "⚠️ Resposta do Tavily não contém JSON válido", style="yellow"
                )
                return {}

    except Exception as e:
        console.print(f"⚠️ Erro na pesquisa Tavily: {str(e)}", style="yellow")
        return {}


def consolidar_dados(
    dados_originais: dict,
    dados_google: dict,
    dados_tavily: dict,
    llm: ChatOpenAI,
    instituicao_nome: str,
    console: Console,
) -> dict:
    """
    Consolida dados de múltiplas fontes usando LLM.

    Args:
        dados_originais (dict): Dados originais da instituição
        dados_google (dict): Dados encontrados no Google
        dados_tavily (dict): Dados encontrados no Tavily
        llm (ChatOpenAI): Modelo de linguagem para consolidação
        instituicao_nome (str): Nome da instituição
        console (Console): Console Rich para output formatado

    Returns:
        dict: Dados consolidados ou dados originais em caso de erro
    """
    console.print("🔄 Consolidando dados...", style="cyan")

    final_prompt = f"""  # Prompt para consolidação de dados
            És um especialista em resumir, compilar e verificar dados. Apenas analisa os dados fornecidos e produz um JSON válido.
            Analisa e consolida os seguintes dados sobre '{instituicao_nome}':

            DADOS ORIGINAIS:
            {json.dumps(dados_originais, indent=2, ensure_ascii=False)}

            DADOS DO GOOGLE:
            {json.dumps(dados_google or {}, indent=2, ensure_ascii=False)}

            DADOS DO TAVILY:
            {json.dumps(dados_tavily or {}, indent=2, ensure_ascii=False)}

            Tarefa:
            1. Compara todos os dados
            2. Escolhe a informação mais completa e confiável para cada campo
            3. Prefere dados dos motores de pesquisa se forem mais completos
            4. Mantém dados originais se os novos estiverem vazios
            5. Combina observações, só deixando endereços de url

            Retorna APENAS um JSON válido no formato:
            {{
                "Instituição": "nome da instituição",
                "Direção": "direção/responsável/contacto",
                "E-Mail": "email consolidado",
                "Telefone": "telefone consolidado",
                "Morada": "morada consolidada",
                "Codigo Postal": "código postal consolidado",
                "Observações": "observações consolidadas só deixando endereços de url"
            }}
            """

    try:
        final_response = llm.invoke(final_prompt)

        if final_response:
            start_idx = final_response.content.find("{")
            end_idx = final_response.content.rfind("}") + 1
            if start_idx != -1 and end_idx > start_idx:
                json_str = final_response.content[start_idx:end_idx]
                return json.loads(json_str)
            else:
                raise ValueError("Resposta final não contém JSON válido")
        else:
            raise ValueError("Resposta final vazia")

    except Exception as e:
        console.print(f"⚠️ Erro na consolidação: {str(e)}", style="yellow")
        console.print("📋 Usando dados originais...", style="cyan")
        return dados_originais


async def processar_instituicao(
    instituicao: Instituicao,
    agent: MCPAgent,
    llm_consolidacao: ChatOpenAI,
    console: Console,
) -> Instituicao:
    """
    Processa uma instituição individual: pesquisa e consolida dados.

    Args:
        instituicao (Instituicao): Instituição a ser processada
        agent (MCPAgent): Agente MCP para pesquisas
        llm_consolidacao (ChatOpenAI): LLM para consolidação de dados
        console (Console): Console Rich para output

    Returns:
        Instituicao: Nova instituição com dados consolidados
    """
    # Preparar dados originais
    dados_originais = {
        "Instituição": instituicao.instituicao,
        "Direção": instituicao.direcao,
        "E-Mail": instituicao.email,
        "Telefone": instituicao.telefone,
        "Morada": instituicao.morada,
        "Codigo Postal": instituicao.codigo_postal,
        "Observações": instituicao.observacoes,
    }

    console.print("Dados originais:", style="yellow")
    console.print(dados_originais)

    # Pesquisar em múltiplas fontes
    dados_google = await processar_instituicao_google(agent, instituicao, console)
    if dados_google:
        print(Panel(str(dados_google), title="✅ Dados do Google", style="yellow"))

    dados_tavily = await processar_instituicao_tavily(agent, instituicao, console)
    if dados_tavily:
        print(Panel(str(dados_tavily), title="✅ Dados do Tavily", style="yellow"))

    # Consolidar dados
    dados_consolidados = consolidar_dados(
        dados_originais,
        dados_google,
        dados_tavily,
        llm_consolidacao,
        instituicao.instituicao,
        console,
    )

    # Criar nova instituição com dados consolidados
    instituicao_consolidada = Instituicao(
        instituicao=dados_consolidados.get("Instituição", instituicao.instituicao),
        direcao=dados_consolidados.get("Direção", instituicao.direcao),
        email=dados_consolidados.get("E-Mail", instituicao.email),
        telefone=dados_consolidados.get("Telefone", instituicao.telefone),
        morada=dados_consolidados.get("Morada", instituicao.morada),
        codigo_postal=dados_consolidados.get(
            "Codigo Postal", instituicao.codigo_postal
        ),
        observacoes=dados_consolidados.get("Observações", instituicao.observacoes),
    )

    console.print("✅ Dados finais consolidados:", style="green")
    console.print(dados_consolidados)

    return instituicao_consolidada


async def main() -> None:
    """
    Função principal do sistema de atualização de instituições.

    Fluxo de execução:
    1. Configura clientes MCP e LLMs
    2. Carrega dados do Excel
    3. Processa cada instituição (pesquisa + consolidação)
    4. Salva backups periódicos
    5. Gera arquivo final com dados atualizados

    Raises:
        ValueError: Se GROQ_API_KEY não estiver definida
        Exception: Para outros erros durante o processamento
    """
    # Ativar modo de depuração
    mcp_use.set_debug(1)

    # Verificar chave de API obrigatória
    if not os.getenv("GROQ_API_KEY"):
        raise ValueError("GROQ_API_KEY not set in environment variables")

    # Inicializar componentes
    mcp_servers = MCPClient.from_dict(all_mcp_servers)
    # se quiser so inicializar algumas ferramentas!
    mcp_servers_just_for_web = MCPClient.from_dict(web_mcp_servers)
    
    ficheiro_original = GestorInstituicoes()
    ficheiro_final = GestorInstituicoes()
    console = Console()

    print(Panel(str(mcp_servers.get_server_names()), title="SERVIDORES MCP DISPONIVEIS", style="yellow"))
    print(Panel(str(mcp_servers_just_for_web.get_server_names()), title="SERVIDORES MCP USAR", style="yellow"))
    console.print("\n=== GESTOR DE INSTITUIÇÕES ===", style="yellow")

    # Carregar dados de entrada
    print("1. Carregar dados do ficheiro excel (*.xlsx)")
    ficheiro_original.carregar_de_excel(os.getenv("FICHEIRO"), os.getenv("JANELA"))

    print("\n2. Listando todas as instituições:")
    ficheiro_original.listar_todas()

    # Configurar LLMs
    openrouter_consolidacao = ChatOpenAI(
        model="mistralai/devstral-small:free",
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv("OPENROUTER_API_KEY"),
        temperature=0.3,
        top_p=0.7,
    )

    # google/gemini-2.0-flash-lite-001 , $0.075/M input tokens - $0.30/M output tokens
    # openai/gpt-4.1-nano , $0.10/M input tokens - $0.40/M output tokens
    # nem todos os modelos suportam function/tool calling [https://openrouter.ai/models?fmt=cards&supported_parameters=tools&order=pricing-low-to-high]
    # mesmo que suportem function/tool calling, verifica se os resultados são válidos, modelos da Google Gemini, OpenAI ou da Anthropic funcionam bem. 
    # Apesar de haver mais modelos que suportam function/tool calling nativamente poderão não ser suportados atravez da OpenRouter.ai
    openrouter_ferramentas = ChatOpenAI(
        model="openai/gpt-4.1-nano",
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv("OPENROUTER_API_KEY"),
        temperature=0.3,
        top_p=0.7,
    )

    # Configurar agente MCP
    # https://docs.mcp-use.com/essentials/agent-configuration
    agent = MCPAgent(
        llm=openrouter_ferramentas,
        client=mcp_servers_just_for_web,
        max_steps=30,
        use_server_manager=True,
        memory_enabled=False,
        auto_initialize=True,
        system_prompt="És um especialista em pesquisar informações de instituições. Sempre usa URLs válidos quando usares browser_navigate. Para pesquisar no Google, usa o formato: https://www.google.com/search?q=TERMO_DE_PESQUISA",
        disallowed_tools=[]
    )

    # Processar cada instituição
    total_instituicoes = len(ficheiro_original.instituicoes)
    console.print(
        f"🔍 Irei processar {total_instituicoes} instituições...", style="cyan"
    )

    for idx, instituicao in enumerate(ficheiro_original.instituicoes, 1):
        console.print(
            f"\n=== 🚀 Processando {idx}/{total_instituicoes}: {instituicao.instituicao} ===",
            style="blue",
        )

        try:
            # Processar instituição
            instituicao_consolidada = await processar_instituicao(
                instituicao, agent, openrouter_consolidacao, console
            )

            ficheiro_final.adicionar_instituicao(instituicao_consolidada)

            # Backup periódico
            if idx % 5 == 0:
                console.print(
                    f"💾 Salvando backup após {idx} instituições...", style="cyan"
                )
                ficheiro_final.salvar_backup_automatico()

        except Exception as e:
            console.print(
                f"❌ Erro ao processar {instituicao.instituicao}: {str(e)}", style="red"
            )

            # Em caso de erro, usar dados originais
            instituicao_original = Instituicao(
                instituicao=instituicao.instituicao,
                direcao=instituicao.direcao,
                email=instituicao.email,
                telefone=instituicao.telefone,
                morada=instituicao.morada,
                codigo_postal=instituicao.codigo_postal,
                observacoes=instituicao.observacoes,
            )
            ficheiro_final.adicionar_instituicao(instituicao_original)

        # Pausa para evitar limitação de taxa
        await asyncio.sleep(2)

    # Salvar resultados finais
    console.print("\n💾 Gravando resultado final...", style="cyan")
    ficheiro_final.salvar_backup_automatico()
    ficheiro_final.salvar_atualizacao_excel("Instituicoes_Atualizadas_Final.xlsx")

    console.print(
        f"\n✅ Processamento concluído! {len(ficheiro_final.instituicoes)} instituições processadas.",
        style="green",
    )


if __name__ == "__main__":
    """
    Ponto de entrada do programa.

    Executa a função principal com tratamento de exceções para:
    - Interrupção pelo usuário (Ctrl+C)
    - Outros erros com traceback completo
    """
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n⚠️ Interrompido pelo utilizador. A sair...")
    except Exception as e:
        print(f"❌ Ocorreu um erro: {e}")
        import traceback

        traceback.print_exc()
