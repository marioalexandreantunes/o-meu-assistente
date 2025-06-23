from typing import Optional
from dataclasses import dataclass

@dataclass
class Instituicao:
    """
    Classe para representar uma instituição com todos os campos da tabela Excel.
    
    Attributes:
        instituicao (str): Nome da instituição
        direcao (str): Nome de contacto da Direção da instituição
        email (str): Endereço de e-mail da instituição
        telefone (str): Número de telefone da instituição
        morada (str): Morada (endereço) da instituição
        codigo_postal (str): Código postal da instituição
        observacoes (Optional[str]): Observações adicionais ou URL de websites
    """
    
    instituicao: str
    direcao: str
    email: str
    telefone: str
    morada: str
    codigo_postal: str
    observacoes: Optional[str] = None
    
    def __str__(self) -> str:
        """
        Representação em string da instituição.
        
        Returns:
            str: Formato "Nome da Instituição - Direção (email)"
        """
        return f"{self.instituicao} - {self.direcao} ({self.email})"
    
    def exibir_detalhes(self) -> None:
        """
        Exibe todos os detalhes da instituição de forma formatada.
        
        Imprime no console todas as informações da instituição,
        incluindo observações se existirem.
        """
        print(f"Instituição: {self.instituicao}")
        print(f"Direção: {self.direcao}")
        print(f"E-Mail: {self.email}")
        print(f"Telefone: {self.telefone}")
        print(f"Morada: {self.morada}")
        print(f"Código Postal: {self.codigo_postal}")
        if self.observacoes:
            print(f"Observações: {self.observacoes}")
        print("-" * 50)