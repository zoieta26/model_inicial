import FreeSimpleGUI as sg
from controllers.controlador_principal import ControladorPrincipal

if __name__ == "__main__":
    sg.theme("Reddit")
    sistema = ControladorPrincipal()
    sistema.iniciar()
