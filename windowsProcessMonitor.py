import win32evtlog
import psutil
import time
import pandas as pd
import signal
import threading

# Listas para armazenar os logs em memória
windows_logs = []
process_logs = []
running = True  # Variável de controle para encerrar as threads

def get_windows_logs(log_type="Security"):
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
                windows_logs.append({
                    "EventID": event.EventID,
                    "TimeGenerated": event.TimeGenerated.Format(),
                    "SourceName": event.SourceName,
                    "Message": event.StringInserts
                })
            time.sleep(1)  # Evita sobrecarga do sistema
    except Exception as e:
        print(f"Erro ao capturar eventos: {e}")
    finally:
        win32evtlog.CloseEventLog(log_handle)

def monitor_processes():
    global running, process_logs
    try:
        while running:
            for proc in psutil.process_iter(attrs=['pid', 'name', 'username']):
                if not running:
                    break  # Sai do loop se o programa for encerrado
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
    except Exception as e:
        print(f"Erro ao monitorar processos: {e}")

def save_logs():
    """Salva os logs em disco quando o programa termina."""
    if windows_logs:
        df_win = pd.DataFrame(windows_logs)
        df_win.to_csv("windows_logs.csv", index=False)
        print("Logs do Windows salvos.")

    if process_logs:
        df_proc = pd.DataFrame(process_logs)
        df_proc.to_csv("process_logs.csv", index=False)
        print("Logs de processos salvos.")

def stop_execution(signum, frame):
    """Função chamada ao pressionar Ctrl+C para salvar os logs antes de sair."""
    global running
    print("\nParando a coleta de logs...")
    running = False  # Para os loops das threads

if __name__ == "__main__":
    # Captura o Ctrl+C para encerrar corretamente
    signal.signal(signal.SIGINT, stop_execution)

    t1 = threading.Thread(target=get_windows_logs, daemon=True)
    t2 = threading.Thread(target=monitor_processes, daemon=True)

    t1.start()
    t2.start()

    # Mantém o programa rodando até o usuário pressionar Ctrl+C
    try:
        while running:
            time.sleep(1)  # Aguarda a interrupção
    except KeyboardInterrupt:
        stop_execution(None, None)

    save_logs()  # Salva os logs antes de finalizar
    print("Coleta finalizada.")
