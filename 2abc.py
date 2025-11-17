# -*- coding: utf-8 -*-

"""
Implementação da ESTRUTURA de um 
Autômato a Pilha Não-Determinístico (APN ou PDA)
[Referente à Questão 2.1]
"""

class PDA:
    """
    Implementa a representação de um Autômato a Pilha 
    Não Determinístico (APN).
    [Referente à Questão 2.1.a]
    """
    
    def __init__(self):
        """
        Inicializa as estruturas do APN.
        """
        self.states = set()
        self.input_alphabet = set()
        self.stack_alphabet = set()
        
        # O cérebro do APN: a função de transição.
        # É um dicionário onde:
        # Chave: (estado, simbolo_entrada, simbolo_topo_pilha)
        # Valor: um CONJUNTO de tuplas (novo_estado, simbolos_a_empilhar)
        self.transitions = {}
        
        self.start_state = None
        self.start_symbol = None  # Símbolo inicial da pilha (ex: 'Z')
        self.final_states = set()

    def add_transition(self, from_state, input_sym, stack_top, to_state, push_symbols):
        """
        Adiciona uma regra de transição ao APN.
        
        A lógica da pilha está em 'stack_top' (verificar o topo) 
        e 'push_symbols' (o que empilhar).
        [Referente à Questão 2.1.b]
        
        Args:
            from_state (str): Estado de origem
            input_sym (str): Símbolo de entrada ('', 'a', 'b', ...)
            stack_top (str): Símbolo que deve estar no topo da pilha para 
                             que a transição ocorra.
            to_state (str): Estado de destino
            push_symbols (str): Símbolos para empilhar.
                                A simulação (Parte 2.2) implementará:
                                - Se 'push_symbols' = 'AB', 'B' vai para o topo.
                                - Se 'push_symbols' = '', é uma ação de POP.
        """
        # Adiciona os estados e símbolos aos registros
        self.states.update([from_state, to_state])
        if input_sym != '':
            self.input_alphabet.add(input_sym)
        self.stack_alphabet.add(stack_top)
        
        # Cria a chave da transição
        key = (from_state, input_sym, stack_top)
        
        # Cria um conjunto vazio se for a primeira transição para esta chave
        if key not in self.transitions:
            self.transitions[key] = set()
            
        # Adiciona o resultado da transição (não-determinístico)
        self.transitions[key].add((to_state, push_symbols))

    def set_start(self, state, symbol):
        """Define o estado inicial e o símbolo inicial da pilha."""
        self.start_state = state
        self.start_symbol = symbol
        self.states.add(state)
        self.stack_alphabet.add(symbol)

    def add_final_state(self, state):
        """Adiciona um estado ao conjunto de aceitação (estados finais)."""
        self.final_states.add(state)
        self.states.add(state)

# -----------------------------------------------------------------
# --- Exemplo de Uso (Definindo o APN) ---
# -----------------------------------------------------------------
# Vamos definir a ESTRUTURA de um APN que aceita 0^n 1^n

print("Criando a estrutura do APN para L = {0^n 1^n | n >= 1}...")
meu_apn = PDA()

# 1. Define estado inicial e símbolo inicial da pilha
meu_apn.set_start('q0', 'Z')

# 2. Define o estado final (opcional, aceitação pode ser por pilha vazia)
meu_apn.add_final_state('q_final') # Exemplo, embora 0^n 1^n seja mais fácil por pilha vazia

# 3. Adiciona as transições (regras)
# (estado, entrada, topo_pilha) -> (novo_estado, [empilhar])

# Regra 1: Empilha '0's
meu_apn.add_transition('q0', '0', 'Z', 'q0', '0Z')
meu_apn.add_transition('q0', '0', '0', 'q0', '00')

# Regra 2: Muda de '0's para '1's (começa a desempilhar)
meu_apn.add_transition('q0', '1', '0', 'q1', '') # '' = desempilha (pop)

# Regra 3: Continua desempilhando '0's para cada '1' lido
meu_apn.add_transition('q1', '1', '0', 'q1', '')

# Regra 4: Se a pilha ficar com 'Z', podemos ir para o estado final
meu_apn.add_transition('q1', '', 'Z', 'q_final', 'Z') # Transição lambda


print("\n--- Estrutura do APN Criada ---")
print(f"Estado Inicial: {meu_apn.start_state}")
print(f"Símbolo Inicial da Pilha: {meu_apn.start_symbol}")
print(f"Estados Finais: {meu_apn.final_states}")
print("\nTransições Definidas:")
for chave, valor in meu_apn.transitions.items():
    print(f"  Se {chave} -> ir para {valor}")

print("\n(Nota: A lógica de simulação [Questão 2.2] é que irá de fato executar as operações de 'push' e 'pop'.)")