class NFA:
    def __init__(self):
        """Inicializa o AFN."""
        self.states = set()
        self.alphabet = set()
        self.transitions = {}  # Dicionário: (origem, simbolo) -> {destinos}
        self.start_state = None
        self.accept_states = set()

    def set_start_state(self, state):
        """Define o estado inicial."""
        self.start_state = state
        self.states.add(state)

    def add_accept_state(self, state):
        """Adiciona um estado ao conjunto de estados de aceitação."""
        self.accept_states.add(state)
        self.states.add(state)

    def add_transition(self, from_state, input_symbol, to_state):
        """
        Adiciona uma transição.
        Use input_symbol = '' (string vazia) para transições lambda.
        """
        self.states.add(from_state)
        self.states.add(to_state)
        if input_symbol != '':
            self.alphabet.add(input_symbol)

        # A chave é (estado_origem, simbolo), o valor é um CONJUNTO de destinos
        key = (from_state, input_symbol)
        if key not in self.transitions:
            self.transitions[key] = set()
        self.transitions[key].add(to_state)

    def _get_lambda_closure(self, states):
        """
        Calcula o fecho-lambda para um conjunto de estados.
        Retorna todos os estados alcançáveis a partir dos estados iniciais
        usando apenas transições vazias ('').
        """
        closure = set(states)
        stack = list(states) # Usamos uma pilha para explorar os caminhos lambda

        while stack:
            current_state = stack.pop()
            
            # Verifica se há transições lambda a partir do estado atual
            if (current_state, '') in self.transitions:
                for next_state in self.transitions[(current_state, '')]:
                    if next_state not in closure:
                        closure.add(next_state)
                        stack.append(next_state)
        return closure

    def process_string(self, input_string):
        """
        Processa uma string de entrada e determina se ela é aceita pelo AFN.
        """
        if self.start_state is None:
            return False

        # Passo inicial: Começamos no fecho-lambda do estado inicial
        current_states = self._get_lambda_closure({self.start_state})

        for symbol in input_string:
            next_states = set()
            
            # Para cada estado ativo no momento, verificamos as transições possíveis com o símbolo atual
            for state in current_states:
                if (state, symbol) in self.transitions:
                    # Adiciona todos os possíveis destinos ao próximo conjunto de estados
                    for dest_state in self.transitions[(state, symbol)]:
                        next_states.add(dest_state)
            
            # O novo conjunto de estados ativos deve incluir o fecho-lambda deles
            current_states = self._get_lambda_closure(next_states)

            # Se em algum momento não houver estados ativos, a string já foi rejeitada
            if not current_states:
                break

        # Verifica se algum dos estados ativos atuais é um estado de aceitação
        return bool(current_states & self.accept_states)

    def __repr__(self):
        return f"NFA(Start: {self.start_state}, Accept: {self.accept_states}, Transitions: {self.transitions})"

# -----------------------------------------------------------------
# --- DEFINIÇÃO DO AFN (Exemplo: aceita 'aa' OU 'bb') ---
# -----------------------------------------------------------------
nfa_teste_interativo = NFA()
nfa_teste_interativo.set_start_state('start')
nfa_teste_interativo.add_accept_state('final')

# Transições lambda (representadas por '') do estado inicial para os dois caminhos
nfa_teste_interativo.add_transition('start', '', 'path_a1')
nfa_teste_interativo.add_transition('start', '', 'path_b1')

# Caminho 'aa'
nfa_teste_interativo.add_transition('path_a1', 'a', 'path_a2')
nfa_teste_interativo.add_transition('path_a2', 'a', 'final')

# Caminho 'bb'
nfa_teste_interativo.add_transition('path_b1', 'b', 'path_b2')
nfa_teste_interativo.add_transition('path_b2', 'b', 'final')


# -----------------------------------------------------------------
# --- PARTE INTERATIVA (Onde você insere as letras) ---
# -----------------------------------------------------------------
print("=================================================")
print("=== Testador Interativo de AFN (NFA) ===")
print("Autômato configurado para aceitar: (aa | bb)")
print("Digite 'sair' a qualquer momento para fechar o programa.")
print("=================================================")

while True:
    # Pede ao usuário para inserir as letras
    cadeia = input("\nInsira a cadeia (letras) para testar: ")

    # Condição de saída
    if cadeia.lower() == 'sair':
        print("Encerrando...")
        break

    # Processa a cadeia usando o método do AFN
    if nfa_teste_interativo.process_string(cadeia):
        print(f"Resultado: \t ACEITA ('{cadeia}')")
    else:
        print(f"Resultado: \t REJEITADA ('{cadeia}')")