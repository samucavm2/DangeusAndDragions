import random
from interface_seres import Ser

class Monstro(Ser):
    def __init__(self, nome: str, vida: int = 10, ataque: int = 5, defesa: int = 3) -> None:
            super().__init__(nome, vida, defesa)  # Chama o construtor da superclasse
            self.ataque: int = ataque

    def atacar(self, oponente: Ser) -> None:
        print(f"\n{self.nome} ataca {oponente.nome}!")
        dano: int = random.randint(1, self.ataque)
        print(f'{self.nome} atacou o {oponente.nome}, causando {dano} de dano')
        oponente.receber_dano(dano)
        
    def receber_dano(self, dano: int) -> None:
        dano_recebido: int = max(0, dano)  # Garante que o dano recebido não será negativo
        self.vida = max(0, self.vida - dano_recebido)  # Garante que a vida não seja negativa
        print(f"{self.nome} recebeu {dano_recebido} de dano e agora tem {self.vida} de vida")
