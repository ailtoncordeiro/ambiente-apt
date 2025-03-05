import pandas as pd
from pm4py.objects.log.util import dataframe_utils
from pm4py.objects.conversion.log import converter as conversion_factory
from pm4py.objects.log.exporter.xes import exporter as xes_exporter

def convert_csv_to_xes(csv_filename, xes_filename):
    """Converte um arquivo CSV para o formato XES compatível com mineração de processos."""
    df = pd.read_csv(csv_filename)

    if df.empty:
        print(f"O arquivo {csv_filename} está vazio, não será convertido.")
        return

    # Definir atributos obrigatórios para o formato XES
    if "EventID" in df.columns:  # Para logs de segurança
        df["concept:name"] = df["EventID"].astype(str)  # Nome do evento
        df["time:timestamp"] = pd.to_datetime(df["TimeGenerated"])  # Timestamp

    elif "process" in df.columns:  # Para logs de processos
        df["concept:name"] = df["process"]  # Nome do processo
        df["time:timestamp"] = pd.to_datetime(df["timestamp"], unit="s")  # Timestamp

    else:
        print(f"Erro: Arquivo {csv_filename} não possui colunas reconhecidas!")
        return

    # Verifique se 'case:concept:name' está presente, se não, adicione-a
    if 'case:concept:name' not in df.columns:
        df['case:concept:name'] = 'default_case'

    # Organizar o DataFrame no formato esperado pelo PM4Py
    df = dataframe_utils.convert_timestamp_columns_in_df(df)
    df = df[["case:concept:name", "concept:name", "time:timestamp"]]  # Apenas colunas relevantes

    # Converter DataFrame para evento de log
    event_log = conversion_factory.apply(df)

    # Exportar para XES
    xes_exporter.apply(event_log, xes_filename)
    print(f"Arquivo {xes_filename} salvo com sucesso!")

# Converter logs para XES
convert_csv_to_xes("filtered_windows_logs.csv", "filtered_windows_logs.xes")
convert_csv_to_xes("process_logs.csv", "process_logs.xes")
