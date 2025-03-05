import win32evtlog
import psutil
import time
import pandas as pd
import signal
import threading

"""
Falhas de autenticação e logins suspeitos:

- 4624 (Login bem-sucedido)
- 4625 (Falha de login)
- 4776 (Falha na autenticação NTLM)
- 4648 (Login usando credenciais explícitas)


Eventos SMB (compartilhamento de arquivos na rede)

- 5140 (Um recurso SMB foi acessado)
- 5145 (Tentativa de acesso a um arquivo compartilhado)


Eventos SSH (se houver logs habilitados para OpenSSH no Windows)

- 22 (Porta padrão do SSH, pode verificar tentativas de conexão)
- Analisar logs do Microsoft-Windows-OpenSSH/Operational se habilitado


Escalada de Privilégios e Execução de Código:

- 4673 (Uso de privilégios elevados)
- 4674 (Uma operação sensível foi tentada)
- 4688 (Criação de um novo processo)
- 4697 (Um serviço foi instalado)

"""


# Eventos de interesse
SECURITY_EVENTS = {4624, 4625, 4648, 4673, 4674, 4688, 4697, 4776}
SMB_EVENTS = {5140, 5145}
SSH_EVENTS = {22}
ALL_EVENTS = SECURITY_EVENTS | SMB_EVENTS | SSH_EVENTS

windows_logs = []
process_logs = []
running = True  # Variável para controle de execução

def get_filtered_windows_logs(log_type="Security"):
    """ Captura apenas eventos relacionados à segurança, SMB e escalada de privilégios. """
    global running, windows_logs
    server = "localhost"
    flags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ
    log_handle = win32evtlog.OpenEventLog(server, log_type)

    try:
        while running:
            events_chunk = win32evtlog.ReadEventLog(log_handle, flags, 0)
            if not events_chunk:
                break
            for event in events_chunk:
                if event.EventID in ALL_EVENTS:
                    windows_logs.append({
                        "EventID": event.EventID,
                        "TimeGenerated": event.TimeGenerated.Format(),
                        "SourceName": event.SourceName,
                        "Message": event.StringInserts
                    })
            time.sleep(1)
            print('coletando windows_logs')
    except Exception as e:
        print(f"Erro ao capturar eventos: {e}")
    finally:
        win32evtlog.CloseEventLog(log_handle)

def monitor_processes():
    """ Captura processos em execução. """
    global running, process_logs
    try:
        while running:
            for proc in psutil.process_iter(attrs=['pid', 'name', 'username']):
                if not running:
                    break
                try:
                    process_logs.append({
                        "timestamp": time.time(),
                        "process": proc.info['name'],
                        "pid": proc.info['pid'],
                        "user": proc.info['username']
                    })
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            time.sleep(1)
            print('coletando process_logs')
    except Exception as e:
        print(f"Erro ao monitorar processos: {e}")

def save_logs():
    """ Salva os logs quando o programa finaliza. """
    if windows_logs:
        df_win = pd.DataFrame(windows_logs)
        df_win.to_csv("filtered_windows_logs.csv", index=False)
        print("Logs filtrados do Windows salvos.")

    if process_logs:
        df_proc = pd.DataFrame(process_logs)
        df_proc.to_csv("process_logs.csv", index=False)
        print("Logs de processos salvos.")

def stop_execution(signum, frame):
    """ Finaliza a coleta de logs corretamente ao pressionar Ctrl+C. """
    global running
    print("\nParando a coleta de logs...")
    running = False

if __name__ == "__main__":
    signal.signal(signal.SIGINT, stop_execution)

    t1 = threading.Thread(target=get_filtered_windows_logs, daemon=True)
    t2 = threading.Thread(target=monitor_processes, daemon=True)

    t1.start()
    t2.start()

    try:
        while running:
            time.sleep(1)
    except KeyboardInterrupt:
        stop_execution(None, None)

    save_logs()
    print("Coleta finalizada.")
