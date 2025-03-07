from pm4py.objects.log.importer.xes import importer as xes_importer
from pm4py.algo.discovery.alpha import algorithm as alpha_miner
from pm4py.visualization.petri_net import visualizer as pn_visualizer
from pm4py.algo.conformance.tokenreplay import algorithm as token_replay

logs_names = ['filtered_windows_logs', 'process_logs']

for logN in logs_names:
    # Carregar o log XES
    log = xes_importer.apply(f"{logN}.xes")
    print(f"Log carregado com {len(log)} eventos!")

    # Descobrir a rede de Petri usando Alpha Miner
    net, initial_marking, final_marking = alpha_miner.apply(log)

    # Visualizar o modelo descoberto
    gviz = pn_visualizer.apply(net, initial_marking, final_marking)
    pn_visualizer.view(gviz)

    # Salva a visualização em um arquivo PNG
    gviz.render(filename=f'{logN}_output', format='png')


    # Calcular conformidade
    replayed_traces = token_replay.apply(log, net, initial_marking, final_marking)

    # Exibir resultado de conformidade
    #print(replayed_traces)

    with open(f'{logN}_conformidade.txt', 'w') as arquivo:
    # Escreva o conteúdo da variável no arquivo
        arquivo.write(str(replayed_traces))