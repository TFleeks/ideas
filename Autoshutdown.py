import PySimpleGUI as sg
import os
import platform
import threading
import time

def shutdown_after_delay(tempo_em_segundos):
    time.sleep(tempo_em_segundos)
    sistema = platform.system()
    if sistema == "Windows":
        os.system("shutdown /s /t 0")
    elif sistema == "Linux" or sistema == "Darwin":  # Darwin é o nome do kernel do macOS
        os.system("sudo shutdown -h now")

def show_confirmation_window(tempo_em_segundos):
    layout_confirmacao = [
        [sg.Text(f"O computador será desligado em {tempo_em_segundos} segundos. Confirmar desligamento?")],
        [sg.Button("OK"), sg.Button("Cancelar")]
    ]
    
    window_confirmacao = sg.Window("Confirmação de Desligamento", layout_confirmacao, keep_on_top=True)

    event, values = window_confirmacao.read(timeout=600000)  # 10 minutos = 600000 ms
    if event == "OK":
        shutdown_after_delay(0)  # Executa o desligamento imediatamente
    elif event == "Cancelar" or event == sg.WIN_CLOSED:
        pass
    else:
        shutdown_after_delay(0)  # Tempo esgotado, executa o desligamento

    window_confirmacao.close()

sg.theme("reddit")

# layout principal
interface = [
    [sg.Text("Qual é o tempo em horas para desligar o computador? ")],
    [sg.Input(key="Tempo")],
    [sg.Button("Executar")],
    [sg.Text("", key="Resultado", size=(30, 1))]  # Campo para exibir o resultado ou erro
]

# criar a janela principal
window = sg.Window("SleepDownload", layout=interface)

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break
    elif event == "Executar":
        tempo_digitado = values["Tempo"]
        if tempo_digitado.isdigit():  # Verifica se o input é um número
            tempo_em_horas = int(tempo_digitado)
            tempo_em_segundos = tempo_em_horas * 3600
            window["Resultado"].update(f"O computador será desligado em {tempo_em_segundos} segundos.")

            # Exibe a janela de confirmação em uma nova thread para não bloquear a janela principal
            threading.Thread(target=show_confirmation_window, args=(tempo_em_segundos,), daemon=True).start()
        else:
            window["Resultado"].update("Por favor, insira um número válido.")

window.close()
