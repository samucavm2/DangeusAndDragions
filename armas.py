import random
from interface_armas import InterfaceArmas

class Armas(InterfaceArmas):
    def __init__(self, 
                 nome: str, 
                 valor: int, 
                 moeda: str, 
                 dano: str, 
                 tipo_de_dano: str, 
                 peso: float, 
                 medida_de_peso: str, 
                 propriedades: str) -> None:
        self.nome = nome
        self.valor = valor
        self.moeda = moeda
        self.dano = dano
        self.tipo_de_dano = tipo_de_dano
        self.peso = peso
        self.medida_de_peso = medida_de_peso
        self.propriedades = propriedades

    def ataque_rapido(self)-> int:
        vezes = int(self.dano[0])
        dano = int(self.dano[2:])
        total = vezes * random.randint(1, dano)
        return total

    def ataque_duas_maos(self)-> int:
        vezes = int(self.dano[0])
        dano = int(self.dano[2:])
        total = 2 * vezes * random.randint(1, dano // 2)
        return total

    def ataque_furioso(self) -> int:
        vezes = int(self.dano[0])
        dano = int(self.dano[2:])
        if random.randint(1, 20) > 10:
            print(f"\nVoce prepara um ataque furioso com sua {self.nome}")
            total = vezes * dano
            return total
        else:
            print("\nA raiva faz voce perder o foco no ataque")
            return 0
