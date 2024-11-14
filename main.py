import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, "src")
sys.path.insert(0, src_dir)

from mesarodada.mesa_rodadas import MesaRodadas

if __name__ == "__main__":
    mr = MesaRodadas()
    mr.gerar_rodadas()
    mr.imprimir_rodadas()
