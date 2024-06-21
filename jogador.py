import random
from armas import Armas
from classes import Classe
from interface_seres import Ser

class Jogador(Ser):
    def __init__(self, nome: str, classe: Classe, arma: Armas, defesa: int = 5, nivel: int = 1) -> None:
        super().__init__(nome, classe.vida_base, defesa)  # Chama o construtor da superclasse
        self.__forca: int = 0
        self.__destreza: int = 0
        self.__inteligencia: int = 0
        self.__constituicao: int = 0
        self.classe: Classe = classe
        self.arma: Armas = arma
        self.nivel: int = nivel
        self.vida_atual: int = self.vida

    # Getters
    def get_forca(self) -> int:
        return self.__forca

    def get_destreza(self) -> int:
        return self.__destreza

    def get_inteligencia(self) -> int:
        return self.__inteligencia

    def get_constituicao(self) -> int:
        return self.__constituicao

    def get_defesa(self) -> int:
        return self.defesa

    # Setters
    def set_forca(self, valor: int) -> None:
        self.__forca = valor

    def set_destreza(self, valor: int) -> None:
        self.__destreza = valor

    def set_inteligencia(self, valor: int) -> None:
        self.__inteligencia = valor

    def set_constituicao(self, valor: int) -> None:
        self.__constituicao = valor

    def set_defesa(self, valor: int) -> None:
        self.__defesa = valor

    def upar(self) -> None:
        self.nivel += 1
        self.__forca += 2
        self.__destreza += 2
        self.__inteligencia += 2
        self.__constituicao += 2
        self.defesa += 2
        self.vida += self.classe.vida_level + self.modificador(self.__constituicao)
        self.iniciativa = self.modificador(self.__destreza)
 
    def modificador(self, x: int) -> int:
        if x > 10:
            return (x - 10) // 2
        else:
            return 0
                   
    def definir_atributos(self) -> None:
        atributos: list[int] = [random.randint(1, 20) for _ in range(4)]
        atributos_mapping: list[str] = ['forca', 'destreza', 'inteligencia', 'constituicao']
        
        print("\nVamos definir agora os atributos do seu personagem")
        input("\nPressione ENTER para a rolagem dos dados")
        print(f"\nVocê jogou os dados e obteve os seguintes valores: {atributos}")
        
        for i, atributo in enumerate(atributos_mapping):
            if atributo == 'constituicao':
                valor = atributos[0]
                self.__constituicao = valor
                self.vida = self.classe.vida_base + self.modificador(self.__constituicao) * self.nivel
                self.vida_atual = self.vida
                print(f"\nComo só sobrou o valor {valor}, ele foi alocado automaticamente em CONSTITUICAO")
                input("\nPressione ENTER para concluirmos")
            else:
                while True:
                    try:
                        valor = int(input(f"\nDefina qual desses valores você quer alocar em {atributo.upper()}: {atributos} "))
                        if valor in atributos:
                            if atributo == 'forca':
                                self.__forca = valor
                            elif atributo == 'destreza':
                                self.__destreza = valor
                            elif atributo == 'inteligencia':
                                self.__inteligencia = valor

                            atributos.remove(valor)
                            print(f"\nVocê alocou {valor} em {atributo.upper()}")
                            print(f"\nValores restantes: {atributos}")
                            break
                        else:
                            print("\nDigite um valor válido")
                    except ValueError:
                        print("\nPor favor, insira um número válido")               
                        
        self.iniciativa = self.modificador(self.__destreza)

    def atacar(self, oponente: Ser) -> None:
        dano = 0
        while True:
            try:
                print('\nInterações')
                print("Ataque Rapido - 1")
                print("Ataque com Duas Mãos - 2")
                print("Ataque especial da Classe - 3")
                print("Ataque furioso - 4")
                print("Curar a si mesmo - 5")
                ataque = int(input("Escolha uma interação: "))
                if ataque == 2:
                    dano = self.arma.ataque_duas_maos() + self.modificador(self.__forca)
                    break
                elif ataque == 1:
                    dano = self.arma.ataque_rapido() + self.modificador(self.__forca)
                    break
                elif ataque == 3:
                    dano = self.classe.ataque_especial()
                    break
                elif ataque == 4:
                    dano = self.arma.ataque_furioso() + self.modificador(self.__forca)
                    break
                elif ataque == 5:
                    cura = self.classe.curar_se()
                    self.vida_atual += cura
                    print(f"{self.nome} se cura em {cura} pontos de vida, ficando com {self.vida_atual} pontos de vida atual")
                    break
                else:
                    print("Por favor, digite apenas 1, 2, 3, 4 ou 5.")
            except ValueError:
                print("Entrada inválida. Por favor, insira um número.")
        print(f'{self.nome} atacou o {oponente.nome}, com {dano} de dano')
        oponente.receber_dano(dano)

    def receber_dano(self, dano: int) -> None:
        acerto = random.randint(1, 20)
        if acerto > self.defesa:
            dano_recebido = max(0, dano)
            self.vida_atual = max(0, self.vida_atual - dano_recebido)
            print(f"{self.nome} recebeu {dano_recebido} de dano e agora tem {self.vida_atual} de vida")
        else:
            print(f"{self.nome} desviou do ataque")
            
    def descansar(self) -> None:
        self.classe.recuperar_mana()
        self.vida_atual = self.vida
        
    def apresentaJogador(self) -> None:
        print(f"\nO jogador {self.nome.capitalize()} pertence a classe {self.classe.nome.capitalize()}, empunha a arma {self.arma.nome.capitalize()} e está pronto para a aventura!")
        
    def imprimir_atributos(self) -> None:
        print(f"Nome: {self.nome}")
        print(f"Classe: {self.classe.nome}")
        print(f"Nível: {self.nivel}")
        print(f"Vida: {self.vida}")
        print(f"Força: {self.__forca} + {self.modificador(self.__forca)}")
        print(f"Destreza: {self.__destreza} + {self.modificador(self.__destreza)}")
        print(f"Inteligência: {self.__inteligencia} + {self.modificador(self.__inteligencia)}")
        print(f"Constituição: {self.__constituicao} + {self.modificador(self.__constituicao)}")
        print(f"Defesa: {self.defesa}")
        print(f"Iniciativa: {self.iniciativa}")
        print(f"Arma: {self.arma.nome}")
        print(f"Dano: {self.arma.dano}")
