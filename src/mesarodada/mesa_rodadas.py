import random
import logging


class MesaRodadas:
    def __init__(
        self, num_participantes=96, num_mesas=12, lugares_por_mesa=8, num_rodadas=12
    ):
        self.num_participantes = num_participantes
        self.num_mesas = num_mesas
        self.lugares_por_mesa = lugares_por_mesa
        self.num_rodadas = num_rodadas
        self.participantes = list(range(1, num_participantes + 1))
        self.rodadas = []
        self.encontros = {p: set() for p in self.participantes}

        # Configuração do logger
        logging.basicConfig(
            filename="alocacao_participantes.log",
            filemode="w",
            level=logging.INFO,
            format="%(message)s",
        )
        self.logger = logging.getLogger()

        # Verificar se a divisão é possível
        if self.num_participantes % self.lugares_por_mesa != 0:
            raise ValueError(
                "O número de participantes deve ser divisível pelo número de lugares por mesa."
            )

    def gerar_rodadas(self):
        for rodada_num in range(1, self.num_rodadas + 1):
            self.logger.info(f"--- Rodada {rodada_num} ---")
            sucesso = self.alocar_participantes()
            if not sucesso:
                print(
                    f"Não foi possível encontrar uma alocação válida para a rodada {rodada_num}."
                )
                break
            self.registrar_alocacao(self.rodadas[-1])

    def alocar_participantes(self):
        max_tentativas = 1000
        melhor_alocacao = None
        melhor_pontuacao = -1
        for _ in range(max_tentativas):
            participantes_disponiveis = self.participantes.copy()
            random.shuffle(participantes_disponiveis)
            alocacao_rodada = {}

            for mesa_num in range(1, self.num_mesas + 1):
                mesa = []
                while len(mesa) < self.lugares_por_mesa and participantes_disponiveis:
                    participante = participantes_disponiveis.pop()
                    mesa.append(participante)
                alocacao_rodada[mesa_num] = mesa
            novos_encontros = self.calcular_novos_encontros(alocacao_rodada)
            if novos_encontros > melhor_pontuacao:
                melhor_pontuacao = novos_encontros
                melhor_alocacao = alocacao_rodada
            if (
                novos_encontros
                == (self.num_participantes * (self.lugares_por_mesa - 1)) // 2
            ):
                break
        if melhor_alocacao:
            self.rodadas.append(melhor_alocacao)
            self.atualizar_encontros_rodada(melhor_alocacao)
            return True
        else:
            return False

    def calcular_novos_encontros(self, alocacao_rodada):
        novos_encontros = 0
        for mesa_participantes in alocacao_rodada.values():
            for i in mesa_participantes:
                for j in mesa_participantes:
                    if i != j and j not in self.encontros[i]:
                        novos_encontros += 1
        return novos_encontros // 2

    def atualizar_encontros_rodada(self, alocacao_rodada):
        for mesa_participantes in alocacao_rodada.values():
            for i in mesa_participantes:
                self.encontros[i].update(mesa_participantes)
                self.encontros[i].remove(i)

    def registrar_alocacao(self, alocacao_rodada):
        for mesa in sorted(alocacao_rodada.keys()):
            participantes = ", ".join(map(str, alocacao_rodada[mesa]))
            self.logger.info(f"Mesa {mesa}: {participantes}")
        self.logger.info("\n")

    def imprimir_rodadas(self):
        for idx, rodada in enumerate(self.rodadas, 1):
            print(f"Rodada {idx}:")
            for mesa in sorted(rodada.keys()):
                participantes = ", ".join(map(str, rodada[mesa]))
                print(f"  Mesa {mesa}: {participantes}")
            print()
