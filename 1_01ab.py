class AFD:
    """
    Implementa a representação de um Autômato Finito Determinístico (AFD)[cite: 15].
    Armazena os estados, alfabeto, transições, estado inicial e estados finais.
    """
    def __init__(self, estados, alfabeto, transicoes, estado_inicial, estados_finais):
        self.estados = set(estados)
        self.alfabeto = set(alfabeto)
        self.transicoes = transicoes
        self.estado_inicial = estado_inicial
        self.estados_finais = set(estados_finais)

    def simular(self, cadeia):
        """
        Simula a execução do AFD para uma cadeia de entrada,
        verificando se ela é ACEITA ou REJEITADA.
        """
        estado_atual = self.estado_inicial
        
        print(f"--- Simulando cadeia: '{cadeia}' ---")
        print(f"Estado inicial: {estado_atual}")

        for simbolo in cadeia:
            # Verifica se o símbolo lido pertence ao alfabeto
            if simbolo not in self.alfabeto:
                print(f"Símbolo '{simbolo}' não pertence ao alfabeto. REJEITA.")
                return False

            # Busca o próximo estado na função de transição
            estado_atual = self.transicoes.get((estado_atual, simbolo))

            # Se a transição não existe (estado de erro implícito)
            if estado_atual is None:
                print(f"Transição inválida a partir do estado anterior com o símbolo '{simbolo}'. REJEITA.")
                return False
            
            print(f"Leu '{simbolo}' -> foi para o estado: {estado_atual}")

        # Ao final da cadeia, verifica se o estado atual é final
        if estado_atual in self.estados_finais:
            print(f"Fim da cadeia. Estado final '{estado_atual}'. ACEITA.")
            return True
        else:
            print(f"Fim da cadeia. Estado '{estado_atual}' não é final. REJEITA.")
            return False

# --- Ponto de Execução Principal ---
if __name__ == "__main__":
    
    # 1. Definição do AFD (mesmo exemplo: aceita strings que terminam com '1')
    estados_afd = {'q0', 'q1'}
    alfabeto_afd = {'0', '1'}
    transicoes_afd = {
        ('q0', '0'): 'q0',
        ('q0', '1'): 'q1',
        ('q1', '0'): 'q0',
        ('q1', '1'): 'q1'
    }
    estado_inicial_afd = 'q0'
    estados_finais_afd = {'q1'}

    # 1.a. Cria a instância do AFD [cite: 15]
    meu_afd = AFD(estados_afd, alfabeto_afd, transicoes_afd, estado_inicial_afd, estados_finais_afd)

    print("--- Simulador de AFD ---")
    print("O AFD de exemplo aceita cadeias de 0s e 1s que terminam com '1'.")
    print("Digite 'sair' para fechar o programa.")
    print("-" * 28)

    # 2. Loop interativo para testar cadeias
    while True:
        # Pede ao usuário para digitar uma cadeia
        cadeia_usuario = input("Digite a cadeia para testar: ")
        
        # Condição de saída
        if cadeia_usuario.lower() == 'sair':
            print("Encerrando...")
            break
        
        # 1.b. Simula o AFD com a cadeia fornecida 
        meu_afd.simular(cadeia_usuario)
        print("-" * 28) # Adiciona um separador