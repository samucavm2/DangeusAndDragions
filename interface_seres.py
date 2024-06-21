from abc import ABC, abstractmethod
from typing import Optional
class Ser(ABC):
    def __init__(self, nome: str, vida: int = 10, defesa: int = 3) -> None:
        self.nome: str = nome
        self.vida: int = vida
        self.defesa: int = defesa
        self.iniciativa: int = 0
        
    @abstractmethod
    def atacar(self, oponente: Optional['Ser']) -> None:
        pass

    @abstractmethod
    def receber_dano(self, dano: int) -> None:
        pass
