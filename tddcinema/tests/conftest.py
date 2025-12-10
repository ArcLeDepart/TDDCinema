import sys
from pathlib import Path

# Ajout explicite de la racine du projet pour éviter les soucis de résolution
ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
