import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from mesarodada.mesa_rodadas import MesaRodadas
import pytest


@pytest.fixture
def mesa_rodadas():
    mr = MesaRodadas(num_rodadas=5)  # Por exemplo, 5 rodadas
    mr.gerar_rodadas()
    return mr


def test_numero_de_rodadas(mesa_rodadas):
    assert len(mesa_rodadas.rodadas) <= mesa_rodadas.num_rodadas


def test_todos_participantes_alocados(mesa_rodadas):
    for rodada in mesa_rodadas.rodadas:
        participantes_alocados = []
        for mesa in rodada.values():
            participantes_alocados.extend(mesa)
        assert sorted(participantes_alocados) == mesa_rodadas.participantes


def test_maximiza_novos_encontros(mesa_rodadas):
    total_encontros = sum(
        len(encontros) for encontros in mesa_rodadas.encontros.values()
    )
    media_encontros_por_participante = total_encontros / mesa_rodadas.num_participantes
    encontros_esperados = (mesa_rodadas.lugares_por_mesa - 1) * len(
        mesa_rodadas.rodadas
    )
    # Permite uma margem de 80% dos encontros esperados serem únicos
    assert media_encontros_por_participante >= encontros_esperados * 0.8
