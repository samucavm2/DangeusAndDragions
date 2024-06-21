import re
import random
import pandas as pd
import os
import sys
from typing import List, Dict, Optional, Any, Tuple, Union
from jogador import Jogador
from armas import Armas
from classes import Classe
from salvar_jogo import SalvarJogo
from monstro import Monstro

class Game:
    def __init__(self) -> None:
        self.jogadores: List[Jogador] = []
        self.local: int = 0
        self.monstros: List[Monstro] = self.criar_monstros()
        self.save: Optional[SalvarJogo] = None
        self.nome_campanha: Optional[str] = None
        self.inicializar_jogo()
        
    def inicializar_jogo(self) -> None:
        print('Bem vindo ao RPG ONLINE')
        
        # Menu de opções
        print("Escolha uma opção:")
        print("1 - Nova campanha")
        print("2 - Campanhas salvas")
        
        while True:
            try:
                escolha = int(input("Digite o número da sua escolha: "))
                if escolha == 1:
                    self.nova_campanha()
                    break
                elif escolha == 2:
                    self.ver_campanhas_salvas()
                    break
                else:
                    print("Opção inválida. Tente novamente.")
            except ValueError:
                print("Entrada inválida. Por favor, insira um número.")
                
    def nova_campanha(self) -> None:
        while True:
            nome_campanha = input("Digite o nome da nova campanha: ")
            if self.validar_nome_arquivo(nome_campanha):
                print(f"Iniciando uma nova campanha: {nome_campanha}")
                self.nome_campanha = nome_campanha
                self.save = SalvarJogo(nome_campanha)
                self.save.progresso(0)
                self.local = 0
                self.criar_jogadores()
                self.gerenciar_batalhas()
                break
            else:
                print("\nNome de campanha inválido. Tente novamente.")
                print('Tente não usar caracteres especiais e utilize underline (_) como espaço.\n')
                
    def validar_nome_arquivo(self, nome) -> bool:
        # Verificar se o nome do arquivo é válido
        # Caracteres inválidos em muitos sistemas de arquivos: \ / : * ? " < > | e espaço
        if re.search(r'[\/:*?"<>|\s]', nome):
            return False
        return True
    
    def criar_jogadores(self) -> None:
        '''Definir quantos jogadores irao jogar'''
        while True:
            try:
                quantidade_jogadores = int(input('Quantos jogadores irao jogar?: '))
                if quantidade_jogadores <= 0:
                    print("Por favor, insira um número maior que 0.")
                else:
                    break
            except ValueError:
                print("Entrada inválida. Por favor, insira um número.")
        
        '''Criaçao de cada jogador'''
        for i in range(1,quantidade_jogadores+1):
            while True:
                nome = input(f'Qual será o nome do Jogador {i}?: ')
                if self.validar_nome_arquivo(nome):
                    
                    classe = self.escolher_classe()                        
                    espada =  self.escolher_tipo_espada()
                    jogador = Jogador(nome, classe, espada)
                    jogador.definir_atributos()
                    jogador.imprimir_atributos()
                    self.jogadores.append(jogador)
                    break
                else:
                    print("Nome de Jogador inválido. Tente novamente.")
                    print('Tente não usar caracteres especiais e utilize underline (_) como espaço.')
            
        for i in self.jogadores:
            self.save.adicionar_jogador(i)
        
        self.local = 1
        self.save.progresso(1)
        
    def escolher_classe(self) -> Classe:
        classes = [['Barbaro', 12, 7],
                   ['Bardo', 8, 5],
                   ['Bruxo', 8, 5],
                   ['Clerigo', 8, 5],
                   ['Druida', 8, 5],
                   ['Feiticeiro', 6, 4],
                   ['Guerreiro', 10, 6],
                   ['Ladino', 8, 5],
                   ['Mago', 6, 4],
                   ['Monge', 8, 5],
                   ['Paladino', 10, 6],
                   ['Patrulheiro', 10, 6]]
        print('\nEscolha uma classe')
        for i in range(len(classes)):
            print(f'{i+1} - {classes[i][0]}, vida base: {classes[i][1]}, vida nos leveis seguintes: {classes[i][2]}')
        
        while True:
            classe_escolhida = input('Digite o nome da classe da sua escolha: ').capitalize().strip()
            for classe in classes:
                if classe_escolhida == classe[0]:
                    classe_certa = Classe(*classe)
                    return classe_certa
            print('Classe não encontrada digite novamente')
        
    def ler_arquivo_arma(self, caminho_arquivo: str) -> pd.DataFrame:
        "le o input caminho_arquivo e passa seus valores para um dataFrame"
        with open(caminho_arquivo, 'r', encoding='utf-8') as file:
            linhas: List[List[str]] = [linha.strip().split(' ', 7) for linha in file if linha.strip()]
    
        colunas: List[str] = ['nome', 'valor', 'moeda', 'dano', 'tipo_de_dano', 'peso', 'medida_de_peso', 'propriedades']
        dados: List[List[str]] = [linha for linha in linhas if len(linha) == 8]
        print("\nA tabela abaixo contém as armas que você pode escolher, digite o primeiro nome da arma para confirmar sua escolha")
        print(' '.join(colunas))
        for linha in dados:
            print(' '.join(linha))
    
        df: pd.DataFrame = pd.DataFrame(dados, columns=colunas)
        return df
    
    def escolher_espada(self, nome_espada: str, df: pd.DataFrame) -> dict | None:
        linha = df[df['nome'].str.capitalize() == nome_espada.capitalize()]
        if not linha.empty:
            return linha.iloc[0].to_dict()
        else:
            print(f"O valor '{nome_espada}' não foi encontrado na primeira coluna.")
            return None
    
    def escolher_tipo_espada(self) -> Armas:
        tipos_arma: Dict[str, str] = {
            '1': 'armas//Armas_Simples_Corpo_a_Corpo.txt',
            '2': 'armas//Armas_Simples_a_Distancia.txt',
            '3': 'armas//Armas_Marciais_Corpo_a_Corpo.txt',
            '4': 'armas//Armas_Marciais_a_Distancia.txt'
        }
        
        print("\nQual tipo de arma você quer usar?\n")
        print("1 - Armas Simples Corpo a Corpo")
        print("2 - Armas Simples a Distância")
        print("3 - Armas Marciais Corpo a Corpo")
        print("4 - Armas Marciais à Distância")
    
        while True:
            tipo: str = input("\nQual sua escolha?: ")
            if tipo in tipos_arma:
                tipo_escolhido: pd.DataFrame = self.ler_arquivo_arma(tipos_arma[tipo])
                while True:
                    nome_espada: str = input('\nDigite o nome da arma da sua escolha: ').capitalize()
                    espada_escolhida: Optional[Dict[str, Any]] = self.escolher_espada(nome_espada, tipo_escolhido)
    
                    if espada_escolhida is None:
                        print("\nA arma escolhida não foi encontrada na lista. Verifique o nome e tente novamente.\n")
                    else:
                        return Armas(**espada_escolhida)
            else:
                print("\nDigite uma opção válida!")
    
    def tem_alguem_vivo(self, personagens: List[Jogador]) -> bool:
        return any(personagem.vida_atual > 0 for personagem in personagens)

    def introduzir_monstro(self, monstro: Monstro) -> None:
        mensagens: Dict[str, str] = {
            'Goblin': "\nMarchando a passos firmes, na vasta e indomável terra de Eldoria, surge por entre as sombras um Goblin",
            'Esqueleto': "\nProsseguindo a aventura, um novo oponente aparece em sobressalto. Seu nome é Esqueleto",
            'Dragão': "\nEis que é chegado o Desafio Final, prepare-se para a última batalha épica que vai definir o destino de Eldoria.\nVocê vai enfrentar o DRAGÃO"
        }
        print(mensagens.get(monstro.nome, "Um novo oponente aparece!"))

    def determinar_ordem_iniciativa(self) -> List[Tuple[Jogador, int]]:
        ordem: Dict[Jogador, int] = {personagem: personagem.iniciativa + random.randint(1, 20) for personagem in self.jogadores + [self.monstros[self.local - 1]]}
        ordem_ordenada: List[Tuple[Jogador, int]] = sorted(ordem.items(), key=lambda x: x[1], reverse=True)
        return ordem_ordenada

    def mostrar_ordem_iniciativa(self, ordem_ordenada: List[Tuple[Jogador, int]]) -> None:
        print("\nOrdem de iniciativa:")
        for personagem, iniciativa in ordem_ordenada:
            print(f"{personagem.nome} - iniciativa: {iniciativa}")
        print()

    def realizar_turno_jogador(self, jogador: Jogador, monstro: Monstro) -> None:
        if jogador.vida_atual > 0:
            print(f"\nO movimento pertence ao jogador {jogador.nome}")
            print(f"O jogador {jogador.nome} tem {jogador.vida_atual} de vida")
            jogador.atacar(monstro)
        else:
            print(f"\n{jogador.nome} já foi derrotado.")

    def realizar_turno_monstro(self, monstro: Monstro) -> None:
        alvo: Jogador = random.choice([jogador for jogador in self.jogadores if jogador.vida_atual > 0])
        monstro.atacar(alvo)
        
    def gerenciar_batalhas(self) -> None:
        for i in range(3):
            jogando: bool = self.batalha()
            if not jogando:
                print('FIM DE JOGO')
                self.save = SalvarJogo(self.nome_campanha)
                self.local += 1
                self.save.progresso(self.local)
                break
            else:
                self.save = SalvarJogo(self.nome_campanha)
                self.local += 1
                self.save.progresso(self.local)
                for jogador in self.jogadores:
                    jogador.upar()
                    jogador.descansar()
                    self.save.adicionar_jogador(jogador)
                    
        if self.tem_alguem_vivo(self.jogadores):         
            print("VOCÊS VENCERAM!!")
        else:
            print("VOCES PERDERAM")
        
    def batalha(self) -> bool:
            if not self.tem_alguem_vivo(self.jogadores):
                return False
            
            try:
                monstro = self.monstros[self.local - 1]
            except IndexError:
                print("Não há mais monstros para lutar. Jogo finalizado.")
                sys.exit()
            
            self.introduzir_monstro(monstro)
            
            print("Uma batalha vai começar!")
            input("Caso esteja preparado, Pressione ENTER")
            
            print(f"\nBatalha iniciada contra o {monstro.nome.capitalize()}!")
            
            ordem_ordenada: List[Tuple[Union[Jogador, Monstro], int]] = self.determinar_ordem_iniciativa()
            input("Pressione ENTER para rolar os dados...")
            
            self.mostrar_ordem_iniciativa(ordem_ordenada)
            
            round_num = 1
            
            while monstro.vida > 0 and self.tem_alguem_vivo(self.jogadores):
                print(f"Round {round_num}:")
                round_num += 1
                for personagem, _ in ordem_ordenada:
                    if monstro.vida <= 0:
                        break
                    if isinstance(personagem, Jogador):
                        self.realizar_turno_jogador(personagem, monstro)
                    else:
                        self.realizar_turno_monstro(personagem)
            
            if monstro.vida <= 0:
                print(f"{monstro.nome} derrotado!")
                return True
            
            print("\nTodos os jogadores foram derrotados. Fim de jogo!")
            return False
        
    def criar_monstros(self) -> List[Monstro]:
        monstros: List[Monstro] = [
            Monstro("Goblin", 10, 3, 3),
            Monstro("Esqueleto", 15, 6, 6),
            Monstro("Dragão", 30, 20, 10)
        ]
        return monstros

    def ver_campanhas_salvas(self) -> None:
        '''Exibe as campanhas salvas'''
        caminho_campanhas = "campanhas_salvas"
        if not os.path.exists(caminho_campanhas):
            os.mkdir(caminho_campanhas)
        campanhas = [d for d in os.listdir(caminho_campanhas) if os.path.isdir(os.path.join(caminho_campanhas, d))]

        if not campanhas:
            print("\nNão há campanhas salvas.\n")
        else:
            print("\nCampanhas salvas:")
            for i, campanha in enumerate(campanhas, start=1):
                print(f"{i}. {campanha}")
            
            while True:
                try:
                    escolha = int(input("\nDigite o número da campanha que deseja carregar: "))
                    if 1 <= escolha <= len(campanhas):
                        nome_campanha = campanhas[escolha - 1]
                        print(f"\nCarregando campanha: {nome_campanha}")
                        self.nome_campanha = nome_campanha
                        self.carregar_local(nome_campanha)
                        if self.local == 0:
                            self.save = SalvarJogo(nome_campanha)
                            self.save.progresso(0)
                            self.criar_jogadores()
                        else:
                            self.carregar_jogadores(nome_campanha)
                        
                        self.gerenciar_batalhas()
                        break
                    else:
                        print("Escolha inválida. Tente novamente.")
                except ValueError:
                    print("Entrada inválida. Por favor, insira um número.")
                   
    def carregar_local(self, nome_campanha) -> None:
        local_dir = f"campanhas_salvas//{nome_campanha}/progresso.txt"
        with open(local_dir, 'r') as file:
            self.local = int(file.read())
   
    def carregar_jogadores(self, nome_campanha) -> None:
       '''Carrega os jogadores de uma campanha salva'''
       jogadores_dir = f"campanhas_salvas//{nome_campanha}/jogadores"
     
       
       for jogador_dir in os.listdir(jogadores_dir):
           jogador_path = os.path.join(jogadores_dir, jogador_dir)
  
           # Carregar atributos do jogador
           atributos_path = os.path.join(jogador_path, 'atributos.csv')
           atributos_df = pd.read_csv(atributos_path)
           atributos = atributos_df.to_dict(orient='records')[0]
     
           # Carregar arma do jogador
           arma_path = os.path.join(jogador_path, 'arma.csv')
           arma_df = pd.read_csv(arma_path)
           arma = arma_df.to_dict(orient='records')[0]
           espada = Armas(**arma)
       
           # Carregar classe do jogador
           classe_path = os.path.join(jogador_path, 'classe.csv')
           classe_df = pd.read_csv(classe_path)
           classe = classe_df.to_dict(orient='records')[0]
           classe_obj = Classe(classe['nome'], classe['vida_base'], classe['vida_level'])
         
           # Criar instância do jogador
           jogador = Jogador(atributos['nome'], classe_obj, espada)
           jogador.nivel = atributos['nivel']
           jogador.vida = atributos['vida']
           jogador.vida_atual = atributos['vida_atual']
           jogador.set_forca(atributos['forca'])
           jogador.set_destreza(atributos['destreza'])
           jogador.set_inteligencia(atributos['inteligencia'])
           jogador.set_constituicao(atributos['constituicao'])
           jogador.set_defesa(atributos['defesa'])
           jogador.iniciativa = atributos['iniciativa']
           
           jogador.apresentaJogador()
           jogador.imprimir_atributos()
           self.jogadores.append(jogador)
