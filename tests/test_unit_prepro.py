# tests/test_unit_prepro.py
import pandas as pd

# Ajusta el import si tu función/archivo tienen otro nombre
from src.preproceso import aplicar_limpieza

def test_aplicar_limpieza_crea_texto_limpio():
    df = pd.DataFrame({
        "raw": [
            "Hello!!! Visit http://x.com",
            "Email me at a@b.com please",
            "Nice   day   :)"
        ]
    })
    out = aplicar_limpieza(df, col_in="raw", col_out="texto_limpio")
    assert "texto_limpio" in out.columns
    assert "http" not in out.loc[0, "texto_limpio"]
    assert "@" not in out.loc[1, "texto_limpio"]
    assert "  " not in out.loc[2, "texto_limpio"]
