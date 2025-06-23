import pandas as pd
from instituicao import Instituicao
from typing import List, Optional
from rich.console import Console
from rich.table import Table

class GestorInstituicoes:
    """
    Classe para gerir uma coleção de instituições.
    
    Esta classe permite carregar, manipular, pesquisar e exportar dados de instituições
    a partir de arquivos Excel, com funcionalidades de visualização usando Rich.
    
    Attributes:
        instituicoes (List[Instituicao]): Lista de instituições carregadas
        table (Table): Tabela Rich para exibição formatada
        console (Console): Console Rich para output formatado
    """
    
    def __init__(self) -> None:
        """
        Inicializa o gestor de instituições.
        
        Cria uma lista vazia de instituições e configura os componentes
        Rich para visualização (console e tabela).
        """
        self.instituicoes: List[Instituicao] = []
        self.table = None
        self.console = Console()
        
    def carregar_tabela(self) -> None:
        """
        Cria e configura a tabela Rich para exibir as instituições.
        
        Define as colunas da tabela com estilos e formatação específicos
        para uma apresentação visual organizada dos dados.
        """
        self.table = Table(title="Instituições 2025")
        self.table.add_column("Instituição", justify="right", style="cyan", no_wrap=True)
        self.table.add_column("Direção", style="magenta", no_wrap=True)
        self.table.add_column("E-Mail", justify="center", no_wrap=True)
        self.table.add_column("Telefone", justify="center", no_wrap=True)
        self.table.add_column("Morada", justify="center", no_wrap=True)
        self.table.add_column("Código Postal", justify="center", no_wrap=True)
        self.table.add_column("Observações", justify="center", no_wrap=True)
        
    def carregar_de_excel(self, caminho_arquivo: str, nome_folha: Optional[str] = None) -> None:
        """
        Carrega dados de um arquivo Excel para a lista de instituições.

        Args:
            caminho_arquivo (str): Caminho para o arquivo Excel
            nome_folha (Optional[str]): Nome da folha específica. Se None, 
                                      usa a primeira folha disponível

        Raises:
            FileNotFoundError: Se o arquivo não for encontrado
            Exception: Para outros erros durante o carregamento
            
        Note:
            Os nomes das colunas esperadas no Excel são:
            'Instituição', 'Direção', 'E-Mail', 'Telefone', 'Morada', 
            'Codigo Postal', 'Observações'
        """
        try:
            # Lê o arquivo Excel
            if nome_folha:
                df = pd.read_excel(caminho_arquivo, sheet_name=nome_folha, engine="openpyxl")
            else:
                df = pd.read_excel(caminho_arquivo, engine="openpyxl")
            
            # Limpa os nomes das colunas removendo espaços extras
            df.columns = df.columns.str.strip()
            
            # Debug: Mostra os nomes das colunas
            self.console.print(f"Colunas encontradas no Excel: {list(df.columns)}", style="yellow")
            
            # Limpa os dados e converte para objetos Instituicao
            self.instituicoes = []
            self.carregar_tabela()

            for _, row in df.iterrows():
                # Debug: Mostra os dados de uma linha para verificar
                if len(self.instituicoes) == 0:  # Só mostra a primeira linha
                    self.console.print(f"Primeira linha de dados: {dict(row)}", style="yellow")
                
                # Função auxiliar para limpar valores nan
                def limpar_valor(valor) -> str:
                    """Remove valores NaN e limpa strings."""
                    if pd.isna(valor) or valor is None:
                        return ''
                    valor_str = str(valor).strip()
                    return '' if valor_str.lower() == 'nan' else valor_str
                
                instituicao = Instituicao(
                    instituicao=limpar_valor(row.get('Instituição', '')),
                    direcao=limpar_valor(row.get('Direção', '')),
                    email=limpar_valor(row.get('E-Mail', '')),
                    telefone=limpar_valor(row.get('Telefone', '')),
                    morada=limpar_valor(row.get('Morada', '')),
                    codigo_postal=limpar_valor(row.get('Codigo Postal', '')),
                    observacoes=limpar_valor(row.get('Observações', '')) or None
                )
                self.instituicoes.append(instituicao)
                
                # Adiciona a instituição à tabela
                self.table.add_row(
                    instituicao.instituicao, 
                    instituicao.direcao,
                    instituicao.email, 
                    instituicao.telefone, 
                    instituicao.morada, 
                    instituicao.codigo_postal, 
                    instituicao.observacoes
                )
            
            self.console.print(f"Carregadas {len(self.instituicoes)} instituições do arquivo {caminho_arquivo}")
            
        except FileNotFoundError:
            self.console.print(f"Erro: Arquivo {caminho_arquivo} não encontrado.", style="bold red")
        except Exception as e:
            self.console.print(f"Erro ao carregar arquivo: {e}", style="bold red")
      
    def adicionar_instituicao(self, instituicao: Instituicao) -> None:
        """
        Adiciona uma nova instituição à lista.
        
        Args:
            instituicao (Instituicao): Objeto instituição a ser adicionado
        """
        self.instituicoes.append(instituicao)
    
    def atualizar_instituicao(self, indice: int, **kwargs) -> bool:
        """
        Atualiza dados de uma instituição específica pelo índice.

        Args:
            indice (int): Índice da instituição na lista (começa em 0)
            **kwargs: Campos a serem atualizados. Campos válidos:
                - instituicao (str): Nome da instituição
                - direcao (str): Nome de contacto da direção
                - email (str): Endereço de e-mail
                - telefone (str): Número de telefone
                - morada (str): Endereço/morada
                - codigo_postal (str): Código postal
                - observacoes (str): Observações adicionais

        Returns:
            bool: True se a atualização foi bem-sucedida, False caso contrário
            
        Example:
            >>> gestor.atualizar_instituicao(0, email="novo@email.com", telefone="123456789")
        """
        if not (0 <= indice < len(self.instituicoes)):
            self.console.print(f"Erro: Índice {indice} inválido. Deve ser entre 0 e {len(self.instituicoes)-1}", style="bold red")
            return False
        
        instituicao = self.instituicoes[indice]
        campos_atualizados = []
        
        # Atualiza apenas os campos fornecidos
        if 'instituicao' in kwargs:
            instituicao.instituicao = kwargs['instituicao']
            campos_atualizados.append('instituição')
        
        if 'direcao' in kwargs:
            instituicao.direcao = kwargs['direcao']
            campos_atualizados.append('direção')
        
        if 'email' in kwargs:
            instituicao.email = kwargs['email']
            campos_atualizados.append('email')
        
        if 'telefone' in kwargs:
            instituicao.telefone = kwargs['telefone']
            campos_atualizados.append('telefone')
        
        if 'morada' in kwargs:
            instituicao.morada = kwargs['morada']
            campos_atualizados.append('morada')
        
        if 'codigo_postal' in kwargs:
            instituicao.codigo_postal = kwargs['codigo_postal']
            campos_atualizados.append('código postal')
        
        if 'observacoes' in kwargs:
            instituicao.observacoes = kwargs['observacoes']
            campos_atualizados.append('observações')
        
        if campos_atualizados:
            self.console.print(f"Instituição {indice} atualizada. Campos alterados: {', '.join(campos_atualizados)}", style="green")
            # Recarrega a tabela para refletir as mudanças
            self._recarregar_tabela()
        else:
            self.console.print("Nenhum campo foi especificado para atualização.", style="yellow")
        
        return True
    
    def atualizar_por_nome(self, nome_busca: str, **kwargs) -> int:
        """
        Atualiza dados de uma instituição específica pelo nome.

        Args:
            nome_busca (str): Nome (ou parte do nome) da instituição para buscar
            **kwargs: Campos a serem atualizados (mesmos do atualizar_instituicao)

        Returns:
            int: Número de instituições atualizadas (0 ou 1)
            
        Note:
            Se múltiplas instituições forem encontradas, nenhuma será atualizada
            e será exibida uma lista para seleção manual por índice.
        """
        resultados = self.buscar_por_nome(nome_busca)
        
        if not resultados:
            self.console.print(f"Nenhuma instituição encontrada com o nome '{nome_busca}'", style="bold red")
            return 0
        
        if len(resultados) > 1:
            self.console.print(f"Encontradas {len(resultados)} instituições com '{nome_busca}':", style="yellow")
            for i, inst in enumerate(resultados):
                indice_real = self.instituicoes.index(inst)
                self.console.print(f"  {indice_real}: {inst.instituicao}")
            self.console.print("Use atualizar_instituicao() com o índice específico para atualizar apenas uma.", style="yellow")
            return 0
        
        # Se encontrou apenas uma, atualiza
        instituicao_encontrada = resultados[0]
        indice_real = self.instituicoes.index(instituicao_encontrada)
        return 1 if self.atualizar_instituicao(indice_real, **kwargs) else 0
    
    def _recarregar_tabela(self) -> None:
        """
        Recarrega a tabela Rich com os dados atuais.
        
        Método privado usado internamente para atualizar a visualização
        da tabela após modificações nos dados.
        """
        self.carregar_tabela()
        for instituicao in self.instituicoes:
            self.table.add_row(
                instituicao.instituicao or "-", 
                instituicao.direcao or "-",
                instituicao.email or "-", 
                instituicao.telefone or "-", 
                instituicao.morada or "-", 
                instituicao.codigo_postal or "-", 
                instituicao.observacoes or "-"
            )
    
    def listar_todas(self) -> None:
        """
        Lista todas as instituições carregadas em formato de tabela.
        
        Exibe uma tabela formatada com todas as instituições e seus dados.
        Se não houver instituições carregadas, exibe uma mensagem de aviso.
        """
        if not self.instituicoes:
            self.console.print("Nenhuma instituição carregada.", style="bold red")
            return
        print(f"\n=== LISTA DE INSTITUIÇÕES ({len(self.instituicoes)}) ===")
        self.console.print(self.table)
      
    def buscar_por_nome(self, termo: str) -> List[Instituicao]:
        """
        Busca instituições por nome usando busca parcial e case-insensitive.
        
        Args:
            termo (str): Termo de busca (pode ser parte do nome)
            
        Returns:
            List[Instituicao]: Lista de instituições que contêm o termo no nome
        """
        termo = termo.lower()
        resultados = [inst for inst in self.instituicoes 
                     if termo in inst.instituicao.lower()]
        return resultados
    
    def buscar_por_email(self, email: str) -> Optional[Instituicao]:
        """
        Busca instituição por email exato (case-insensitive).
        
        Args:
            email (str): Endereço de email para buscar
            
        Returns:
            Optional[Instituicao]: Instituição encontrada ou None se não existir
        """
        for inst in self.instituicoes:
            if inst.email.lower() == email.lower():
                return inst
        return None
    
    def filtrar_por_codigo_postal(self, codigo: str) -> List[Instituicao]:
        """
        Filtra instituições por código postal (busca parcial).
        
        Args:
            codigo (str): Código postal ou parte dele para filtrar
            
        Returns:
            List[Instituicao]: Lista de instituições com código postal correspondente
        """
        return [inst for inst in self.instituicoes 
                if codigo in inst.codigo_postal]
    
    def exportar_para_csv(self, caminho_arquivo: str) -> None:
        """
        Exporta os dados das instituições para um arquivo CSV.
        
        Args:
            caminho_arquivo (str): Caminho onde salvar o arquivo CSV
            
        Note:
            O arquivo é salvo com encoding UTF-8 e sem índice.
        """
        if not self.instituicoes:
            self.console.print("Nenhuma instituição para exportar.", style="bold red")
            return
        
        dados = []
        for inst in self.instituicoes:
            dados.append({
                'Instituição': inst.instituicao,
                'Direção': inst.direcao,
                'E-Mail': inst.email,
                'Telefone': inst.telefone,
                'Morada': inst.morada,
                'Código Postal': inst.codigo_postal,
                'Observações': inst.observacoes or ''
            })
        
        df = pd.DataFrame(dados)
        df.to_csv(caminho_arquivo, index=False, encoding='utf-8')
        self.console.print(f"Dados exportados para {caminho_arquivo}")
    
    def salvar_atualizacao_excel(self, caminho_arquivo: str = "Atualização.xlsx", 
                                nome_folha: str = "Instituições") -> bool:
        """
        Salva os dados atuais em um arquivo Excel.

        Args:
            caminho_arquivo (str): Nome do arquivo Excel a ser criado. 
                                 Default: "Atualização.xlsx"
            nome_folha (str): Nome da folha no Excel. Default: "Instituições"

        Returns:
            bool: True se salvou com sucesso, False caso contrário
            
        Note:
            Inclui todas as adições e atualizações feitas desde o carregamento inicial.
        """
        if not self.instituicoes:
            self.console.print("Nenhuma instituição para salvar.", style="bold red")
            return False
        
        try:
            dados = []
            for inst in self.instituicoes:
                dados.append({
                    'Instituição': inst.instituicao or '',
                    'Direção': inst.direcao or '',
                    'E-Mail': inst.email or '',
                    'Telefone': inst.telefone or '',
                    'Morada': inst.morada or '',
                    'Código Postal': inst.codigo_postal or '',
                    'Observações': inst.observacoes or ''
                })
            
            df = pd.DataFrame(dados)
            
            # Salva no arquivo Excel
            with pd.ExcelWriter(caminho_arquivo, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name=nome_folha, index=False)
            
            self.console.print(f"✅ Arquivo '{caminho_arquivo}' salvo com sucesso!", style="bold green")
            self.console.print(f"   📄 {len(self.instituicoes)} instituições salvas na folha '{nome_folha}'", style="green")
            return True
            
        except Exception as e:
            self.console.print(f"Erro ao salvar arquivo Excel: {e}", style="bold red")
            return False
    
    def salvar_backup_automatico(self) -> bool:
        """
        Cria um backup automático com timestamp no nome do arquivo.
        
        Returns:
            bool: True se o backup foi criado com sucesso, False caso contrário
            
        Note:
            O arquivo será nomeado como "Backup_Instituicoes_YYYYMMDD_HHMMSS.xlsx"
        """
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nome_arquivo = f"Backup_Instituicoes_{timestamp}.xlsx"
        return self.salvar_atualizacao_excel(nome_arquivo, "Backup")