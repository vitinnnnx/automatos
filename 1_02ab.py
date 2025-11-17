# -*- coding: utf-8 -*-

"""
Implementação de um Autômato Finito Não-determinístico (AFN ou NFA)
com suporte a transições vazias (lambda/epsilon).
"""

class NFA:
    """
    Esta classe representa a estrutura e o funcionamento de um AFN.
    Ela armazena os estados, o alfabeto, as transições e fornece
    um método para processar e validar cadeias de entrada.
    """

    def __init__(self):
        """
        O construtor (inicializador) da classe.
        É chamado automaticamente quando criamos um novo AFN (ex: nfa = NFA()).
        Ele prepara as estruturas de dados fundamentais do autômato.
        """
        
        # 'set()' é um CONJUNTO. Usamos conjuntos para estados e alfabeto
        # porque a ordem não importa e não queremos itens duplicados.
        self.states = set()
        self.alphabet = set()
        
        # 'self.transitions' é o cérebro do autômato. É um dicionário.
        # - Chave (Key): Uma tupla (estado_origem, simbolo_de_entrada)
        #                 Ex: ('q0', 'a')
        # - Valor (Value): Um CONJUNTO ('set') de estados de destino
        #                  Ex: {'q1', 'q2'}
        # Usamos um CONJUNTO como valor porque o não-determinismo permite
        # ir para MÚLTIPLOS estados ao mesmo tempo.
        self.transitions = {}
        
        # O estado onde o processamento sempre começa.
        self.start_state = None
        
        # Um CONJUNTO de estados que, se o autômato terminar em qualquer
        # um deles, a cadeia é considerada "ACEITA".
        self.accept_states = set()

    def set_start_state(self, state):
        """Define qual estado é o inicial."""
        self.start_state = state
        self.states.add(state) # Garante que o estado inicial exista no conjunto de estados

    def add_accept_state(self, state):
        """Adiciona um estado ao conjunto de estados de aceitação."""
        self.accept_states.add(state)
        self.states.add(state) # Garante que o estado de aceitação exista no conjunto de estados

    def add_transition(self, from_state, input_symbol, to_state):
        """
        Adiciona uma regra de transição ao autômato.
        Ex: "Do estado 'q0', lendo 'a', vá para 'q1'".

        Para transições lambda (vazias), usamos input_symbol = '' (uma string vazia).
        """
        
        # Adiciona os estados aos nossos registros, caso sejam novos
        self.states.add(from_state)
        self.states.add(to_state)
        
        # Adiciona o símbolo ao alfabeto (ignorando lambdas)
        if input_symbol != '':
            self.alphabet.add(input_symbol)

        # Cria a chave da transição
        key = (from_state, input_symbol)
        
        # Se esta é a primeira vez que vemos uma transição saindo de (from_state, input_symbol),
        # precisamos criar um conjunto vazio para armazenar seus destinos.
        if key not in self.transitions:
            self.transitions[key] = set()
            
        # Adiciona o estado 'to_state' ao CONJUNTO de destinos possíveis.
        self.transitions[key].add(to_state)

    def _get_lambda_closure(self, states):
        """
        Calcula o "Fecho-Lambda" (ou Fecho-Epsilon) para um conjunto de estados.

        Responde à pergunta: "A partir deste(s) estado(s), para quais outros
        estados eu posso 'pular' DE GRAÇA (usando apenas transições lambda '')?"
        
        Este é um método auxiliar interno (indicado pelo _ no início).
        """
        
        # O fecho (closure) inicial já contém os próprios estados de entrada.
        # (Você sempre pode "alcançar" o estado onde você já está).
        closure = set(states)
        
        # Usamos uma 'pilha' (stack) para gerenciar os estados que ainda
        # precisamos verificar se têm saídas lambda.
        # Começamos com os estados que recebemos.
        stack = list(states)

        # Enquanto houver estados na pilha para verificar...
        while stack:
            # Pega o último estado da pilha
            current_state = stack.pop()
            
            # Verifica se existe alguma transição lambda (chave com '')
            # saindo deste estado.
            key = (current_state, '')
            if key in self.transitions:
                # Se sim, olhe todos os destinos possíveis dessa transição lambda
                for next_state in self.transitions[key]:
                    # Se este 'next_state' (alcançado por lambda)
                    # ainda não está no nosso conjunto 'closure'...
                    if next_state not in closure:
                        # ...nós o adicionamos ao 'closure'...
                        closure.add(next_state)
                        # ...e o colocamos na PILHA, porque ele também
                        # pode ter suas próprias transições lambda.
                        stack.append(next_state)
                        
        # Retorna o conjunto completo de todos os estados alcançáveis via lambda.
        return closure

    def process_string(self, input_string):
        """
        Simula o AFN processando uma cadeia de entrada (input_string)
        e retorna True (ACEITA) ou False (REJEITADA).
        """
        
        if self.start_state is None:
            print("Erro: Estado inicial não definido.")
            return False

        # --- PASSO 1: ESTADO INICIAL ---
        # Em um AFN com lambdas, não começamos *apenas* no estado inicial.
        # Começamos em TODOS os estados alcançáveis a partir do estado inicial
        # usando o Fecho-Lambda.
        # 'current_states' é um CONJUNTO. Ele rastreia TODOS os lugares
        # onde o autômato pode estar "ao mesmo tempo".
        current_states = self._get_lambda_closure({self.start_state})

        # --- PASSO 2: CONSUMIR A CADEIA ---
        # Itera por cada símbolo (letra) da cadeia de entrada.
        for symbol in input_string:
            
            # 'next_states' será o conjunto de estados onde estaremos
            # APÓS consumir o 'symbol'.
            next_states = set()
            
            # Para CADA estado em que estamos atualmente...
            for state in current_states:
                
                # ...verificamos se existe uma transição definida
                # para (estado_atual, simbolo_atual).
                key = (state, symbol)
                if key in self.transitions:
                    # Se houver, pegamos TODOS os destinos dessa transição
                    # e os adicionamos ao conjunto 'next_states'.
                    for dest_state in self.transitions[key]:
                        next_states.add(dest_state)
            
            # --- PASSO 3: APLICAR LAMBDAS NOVAMENTE ---
            # Após nos movermos para 'next_states' consumindo o 'symbol',
            # devemos IMEDIATAMENTE calcular o fecho-lambda desses novos estados.
            # (Talvez possamos "pular de graça" para outros estados a partir dali).
            current_states = self._get_lambda_closure(next_states)

            # Otimização: Se em algum momento o conjunto de estados ativos
            # ficar vazio, significa que o autômato "morreu" e não
            # tem mais caminhos possíveis. Podemos parar cedo.
            if not current_states:
                break

        # --- PASSO 4: VERIFICAÇÃO FINAL ---
        # Após o loop terminar (todos os símbolos foram lidos),
        # verificamos em quais estados 'current_states' terminamos.
        
        # A cadeia é ACEITA se a INTERSEÇÃO (&) entre os estados
        # onde estamos (current_states) e os estados de aceitação
        # (self.accept_states) NÃO for vazia.
        # Ou seja, se PELO MENOS UM dos nossos estados atuais
        # for um estado de aceitação.
        return bool(current_states & self.accept_states)

# -----------------------------------------------------------------
# --- PARTE 2: DEFINIÇÃO DO AFN (Ex: aceita 'aa' OU 'bb') ---
# -----------------------------------------------------------------

# 1. Cria uma "instância" vazia da nossa classe NFA.
nfa_teste_interativo = NFA()

# 2. Define o estado inicial.
nfa_teste_interativo.set_start_state('start')

# 3. Define o estado (ou estados) de aceitação.
nfa_teste_interativo.add_accept_state('final')

# 4. Adiciona as transições (as "regras").
# Esta é a parte principal do NÃO-DETERMINISMO com LAMBDA.
# Do estado 'start', o autômato pode ir para 'path_a1' OU 'path_b1'
# sem consumir nenhuma letra (usando a transição lambda '').
print("Configurando AFN para aceitar 'aa' ou 'bb'...")
nfa_teste_interativo.add_transition('start', '', 'path_a1') # Bifurcação 1 (de graça)
nfa_teste_interativo.add_transition('start', '', 'path_b1') # Bifurcação 2 (de graça)

# Caminho para aceitar "aa"
nfa_teste_interativo.add_transition('path_a1', 'a', 'path_a2') # Lê o primeiro 'a'
nfa_teste_interativo.add_transition('path_a2', 'a', 'final') # Lê o segundo 'a' e vai para o estado final

# Caminho para aceitar "bb"
nfa_teste_interativo.add_transition('path_b1', 'b', 'path_b2') # Lê o primeiro 'b'
nfa_teste_interativo.add_transition('path_b2', 'b', 'final') # Lê o segundo 'b' e vai para o estado final


# -----------------------------------------------------------------
# --- PARTE 3: PARTE INTERATIVA (Onde você insere as letras) ---
# -----------------------------------------------------------------
print("=================================================")
print("=== Testador Interativo de AFN (NFA) ===")
print("Autômato configurado para aceitar: (aa | bb)")
print("Digite 'sair' a qualquer momento para fechar o programa.")
print("=================================================")

# Cria um loop infinito que só será quebrado se o usuário digitar 'sair'
while True:
    
    # Pede ao usuário para inserir uma cadeia de letras
    # O programa pausa aqui e espera o usuário digitar e apertar Enter
    cadeia = input("\nInsira a cadeia (letras) para testar: ")

    # Verifica se o usuário quer parar o programa
    if cadeia.lower() == 'sair':
        print("Encerrando...")
        break # Quebra o loop 'while True'

    # --- A CHAMADA PRINCIPAL ---
    # Aqui, chamamos o método 'process_string' do nosso AFN
    # e passamos a cadeia que o usuário digitou.
    # O método retornará True (se aceita) ou False (se rejeita).
    if nfa_teste_interativo.process_string(cadeia):
        # Se retornou True:
        print(f"Resultado: \t ACEITA ('{cadeia}')")
    else:
        # Se retornou False:
        print(f"Resultado: \t REJEITADA ('{cadeia}')")