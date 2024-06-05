import pandas as pd
import os
import glob

# Caminho para ler os arquivos
folder_path = 'src\\data\\raw'

# lista todos ler os arquivos
excel_files = glob.glob(os.path.join(folder_path , '*.xlsx'))

if not excel_files:
    print("Nenhum arquivo encontrado")
else:
    # dataframe = tabela em memória para guardar os conteúdos dos arquivos
    df = []
    
    for file in excel_files:
        try:
            df_temp = pd.read_excel(file)  # ler cada arquivo individualmente
            print(df_temp)  # imprimir o conteúdo do arquivo
            df.append(df_temp)  # adicionar ao dataframe principal
        except Exception as e:
            print(f"Erro ao ler o arquivo {file} : {e}")