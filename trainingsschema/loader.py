import os

def get_schema_path() :
    """
    geeft het volledige pad naar het PDF-bestand van het trainingsschema terug.
    """
    return os.path.join(os.path.dirname(__file__), "Trainingsschema-25-26.pdf")

def open_schema() :
    """
    Open het PDF-bestand met de standaard PDF-viewer van het systeem.
    Werkt op Linux, Windows en macOs.
    """

    import platform
    import subprocess

    path = get_schema_path()

    if platform.system() == "Darwin":            #macOs
        subprocess.call(("open", path))
    elif platform.system() == "Windows":         #Windows
        os.startfile(path)
    else:                                        #Linux en andere
        subprocess.call(("xdg-open", path))