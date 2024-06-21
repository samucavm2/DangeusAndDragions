class Classe:
    def __init__(self, nome, vida_base: int, vida_level: int, mana: int = 200, dano_especial: int = 4, mana_especial: int = 100):
        self.nome = nome
        self.vida_base = vida_base
        self.vida_level = vida_level
        self.mana = mana
        self.mana_atual = mana
        self.dano_especial = dano_especial
        self.mana_especial = mana_especial
        
    def ataque_especial(self) -> int:
        print(f"\nVoce prepera um ataque especial de {self.nome}")
        if self.mana_atual >= self.mana_especial:
            self.mana_atual -= self.mana_especial
            return self.dano_especial
        else:
            print("\nVoce não tinha mana para atacar. Voce se distrai e perde sua vez.")
            return 0
        
    def curar_se(self) -> int:
        print(f"\nVoce prepera uma habilidade de cura de {self.nome}")
        if self.mana_atual >= self.mana_especial:
            self.mana_atual -= self.mana_especial
            return self.dano_especial
        else:
            print("\nVoce não tinha mana para curar. Voce se distrai e perde sua vez.")
            return 0
    
    def recuperar_mana(self) -> None:
        self.mana_atual = self.mana
