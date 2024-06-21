import pandas as pd
import os
import shutil
from jogador import Jogador

class SalvarJogo():
    def __init__(self, nome_campanha:str) -> None:
        self.nome_campanha: str = nome_campanha
        self.jogadores: list[Jogador] = []
        self.local: int = 0
        self.criar_arquivo()
   
    "Cria um arquivo com o nome da campanha onde ficara salvo os dados dos jogadores"
    def criar_arquivo(self) -> None:
        '''Cria uma pasta de arquivo com o nome da campanha e uma subpasta chamada jogadores'''
        if not os.path.exists(f"campanhas_salvas//{self.nome_campanha}"):
            os.mkdir(f"campanhas_salvas//{self.nome_campanha}")
        if not os.path.exists(f"campanhas_salvas//{self.nome_campanha}//jogadores"):
            os.mkdir(f"campanhas_salvas//{self.nome_campanha}/jogadores")
         
    def adicionar_jogador(self, jogador) -> None:
        '''Recebe uma classe jogador e cria uma pasta com o nome jogador.nome em jogadores'''
        jogador_pasta = f"campanhas_salvas//{self.nome_campanha}/jogadores/{jogador.nome}"
        
        # Se o diretório do jogador já existir, remove-o para sobrescrever os dados
        if os.path.exists(jogador_pasta):
            shutil.rmtree(jogador_pasta)
        
        # Cria o diretório novamente
        os.makedirs(jogador_pasta)
        
        # Salvar atributos
        atributos = {
            'nome': [jogador.nome],
            'classe': [jogador.classe.nome],
            'nivel': [jogador.nivel],
            'vida': [jogador.vida],
            'vida_atual': [jogador.vida_atual],
            'forca': [jogador.get_forca()],
            'destreza': [jogador.get_destreza()],
            'inteligencia': [jogador.get_inteligencia()],
            'constituicao': [jogador.get_constituicao()],
            'defesa': [jogador.get_defesa()],
            'iniciativa': [jogador.iniciativa]
        }
        df_atributos = pd.DataFrame(atributos)
        df_atributos.to_csv(f"{jogador_pasta}/atributos.csv", index=False)
        
        # Salvar arma
        arma = {
            'nome': [jogador.arma.nome],
            'valor': [jogador.arma.valor],
            'moeda': [jogador.arma.moeda],
            'dano': [jogador.arma.dano],
            'tipo_de_dano': [jogador.arma.tipo_de_dano],
            'peso': [jogador.arma.peso],
            'medida_de_peso': [jogador.arma.medida_de_peso],
            'propriedades': [jogador.arma.propriedades]
        }
        df_arma = pd.DataFrame(arma)
        df_arma.to_csv(f"{jogador_pasta}/arma.csv", index=False)
        
        # Salvar classe
        classe = {
            'nome': [jogador.classe.nome],
            'vida_base': [jogador.classe.vida_base],
            'vida_level': [jogador.classe.vida_level]
        }
        df_classe = pd.DataFrame(classe)
        df_classe.to_csv(f"{jogador_pasta}/classe.csv", index=False)
    
    "Salva qual ponto o jogador está"
    def progresso(self, local) -> None:
        '''Em um arquivo define onde os jogadores estão'''
        with open(f"campanhas_salvas//{self.nome_campanha}/progresso.txt", 'w') as file:
            file.write(str(local))
