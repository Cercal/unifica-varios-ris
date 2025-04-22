import os
import glob
import shutil
from pathlib import Path

# --------------------------------------------------
# CONFIGURAÇÕES DE DIRETÓRIOS
# --------------------------------------------------
# Usa a pasta Downloads do seu usuário Windows
DOWNLOADS_DIR = Path.home() / "Downloads"
TMP_DIR = Path.cwd() / "tmp_txt"
UNIFIED_TXT = Path.cwd() / "unified.txt"
UNIFIED_RIS = Path.cwd() / "unified.ris"

def ensure_tmp_dir():
    TMP_DIR.mkdir(exist_ok=True)

def ris_to_txt():
    """
    Para cada .ris em DOWNLOADS_DIR, copia seu conteúdo para TMP_DIR como .txt
    """
    ris_files = list(DOWNLOADS_DIR.glob("*.ris"))
    if not ris_files:
        print(f"Nenhum arquivo .ris encontrado em {DOWNLOADS_DIR}")
        return
    for ris_path in ris_files:
        txt_path = TMP_DIR / (ris_path.stem + ".txt")
        # lê com fallback para latin-1 caso haja caracteres irregulares
        with ris_path.open("r", encoding="utf-8", errors="replace") as rf, \
             txt_path.open("w", encoding="utf-8") as tf:
            shutil.copyfileobj(rf, tf)
        print(f"Convertido: {ris_path.name} → {txt_path.name}")

def unify_txt():
    """
    Concatena todos os .txt de TMP_DIR em unified.txt
    """
    txt_files = sorted(TMP_DIR.glob("*.txt"))
    if not txt_files:
        print(f"Nenhum arquivo .txt em {TMP_DIR} para unificar.")
        return
    with UNIFIED_TXT.open("w", encoding="utf-8") as out:
        for txt_path in txt_files:
            with txt_path.open("r", encoding="utf-8") as rf:
                out.write(rf.read())
                out.write("\n")  # separa entradas
    print(f"Unificados {len(txt_files)} arquivos em {UNIFIED_TXT.name}")

def txt_to_ris():
    """
    Renomeia unified.txt para unified.ris
    """
    if not UNIFIED_TXT.exists():
        print(f"{UNIFIED_TXT.name} não encontrado, nada para renomear.")
        return
    if UNIFIED_RIS.exists():
        UNIFIED_RIS.unlink()
    UNIFIED_TXT.rename(UNIFIED_RIS)
    print(f"Arquivo final RIS criado: {UNIFIED_RIS.name}")

def cleanup():
    """
    Remove a pasta temporária TMP_DIR
    """
    if TMP_DIR.exists():
        shutil.rmtree(TMP_DIR)
        print(f"Pasta temporária removida: {TMP_DIR}")

def main():
    print(f"Pasta de downloads: {DOWNLOADS_DIR}")
    ensure_tmp_dir()
    ris_to_txt()
    unify_txt()
    txt_to_ris()
    cleanup()

if __name__ == "__main__":
    main()