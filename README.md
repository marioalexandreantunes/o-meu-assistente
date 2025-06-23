# Projeto -O meu Assistente-

## Descrição

Este projeto é um proof-of-concept de um agente IA que atualiza automaticamente um ficheiro Excel contendo nomes de instituições. O agente realiza pesquisas online para tentar atualizar todos os campos de informação disponíveis para cada instituição. O sistema utiliza múltiplos serviços de pesquisa (Google, Tavily, Brave Search) através do protocolo MCP (Model Context Protocol) para obter informações atualizadas e consolida os resultados usando LLMs (Large Language Models) para produzir dados mais completos e precisos sobre cada instituição.

## Funcionalidades Principais

- **Atualização Automática de Dados**: O agente pesquisa e atualiza automaticamente informações de instituições em um ficheiro Excel.
- **Integração com MCP Servers**: Utiliza servidores MCP para realizar pesquisas online e obter informações atualizadas.
- **Consolidação de Dados**: Usa LLMs para consolidar dados de múltiplas fontes, garantindo a maior precisão possível.
- **Interface de Consola Enriquecida**: Utiliza a biblioteca Rich para fornecer uma interface de consola formatada e informativa.

## Como configurar o ambiente

### 1. Criar um ambiente virtual
Para criar um ambiente virtual, execute o seguinte comando no terminal:

```bash
python -m venv venv
```

ou 

```bash
py -3.12 -m venv venv
```

### 2. Ativar o ambiente virtual
Para ativar o ambiente virtual, use o comando apropriado para o seu sistema operacional:

- No Windows:
  ```bash
  venv\Scripts\activate
  ```

- No macOS e Linux:
  ```bash
  source venv/bin/activate
  ```
  para atualizar pip :
  
  ```bash
  python.exe -m pip install --upgrade pip
  ```

### 3. Instalar as dependências
Com o ambiente virtual ativado, instale as dependências necessárias usando pip:

```bash
pip install -r requirements.txt
```

## Como executar o projeto
Após configurar o ambiente e instalar as dependências, você pode executar o projeto com o seguinte comando:

```bash
python main.py
```

### Estrutura dos arquivos XLSX

Os arquivos XLSX utilizados neste projeto devem ter os seguintes cabeçalhos:

- Instituição
- Direção
- E-Mail
- Telefone
- Morada
- Código Postal
- Observações

### Configuração do arquivo .env

Para configurar as variáveis de ambiente necessárias, crie um arquivo `.env` na raiz do projeto com o seguinte conteúdo:

```plaintext
# Exemplo de arquivo .env
GROQ_API_KEY=seu_groq_api_key_aqui
OPENROUTER_API_KEY=seu_openrouter_api_key_aqui
OCTAGON_API_KEY=seu_octagon_api_key_aqui
TAVILY_API_KEY=seu_tavily_api_key_aqui
BRAVE_API_KEY=seu_brave_api_key_aqui
FICHEIRO=caminho/para/seu/arquivo.xlsx
JANELA=nome_da_folha_do_excel
```

Substitua `seu_groq_api_key_aqui`, `seu_openrouter_api_key_aqui`, `seu_octagon_api_key_aqui`, `seu_tavily_api_key_aqui`, `seu_brave_api_key_aqui`, `caminho/para/seu/arquivo.xlsx` e `nome_da_folha_do_excel` pelos valores reais que você precisa para o seu ambiente.

## Estrutura do Projeto

- `main.py`: Módulo principal que implementa o sistema de atualização automática de dados de instituições.
- `gestor_instituicoes.py`: Classe para gerir uma coleção de instituições, com funcionalidades de carregamento, manipulação, pesquisa e exportação de dados.
- `instituicao.py`: Classe que representa uma instituição com todos os campos da tabela Excel.

## Tecnologias Utilizadas

- **Python**: Linguagem de programação principal
- **Pandas**: Para manipulação de dados em arquivos Excel
- **Rich**: Para interface de consola enriquecida
- **MCP (Model Context Protocol)**: Para integração com servidores de pesquisa
- **LLMs (Large Language Models)**: Para consolidação de dados

## Contribuição

Sinta-se à vontade para contribuir com este projeto. Por favor, siga as boas práticas de desenvolvimento e mantenha a documentação atualizada.

## Licença

Este projeto está licenciado sob a Licença MIT.