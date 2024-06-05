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
    # dataframe final = tabela em memória para guardar os conteúdos dos arquivos
    df = []
    
    for file in excel_files:
        try:
            # LOAD FILE ------------------------
            # ler cada arquivo individualmente
            df_temp = pd.read_excel(file)  
            
            # LOAD FILENAME ---------------------
            # pega nome do arquivo
            file_name = os.path.basename(file)
            
            # CRIA COLUNA---------------------------
            # cria uma nova coluna country
            if 'brasil' in file_name.lower():
                df_temp['country'] = 'br'
            elif 'france' in file_name.lower():
                df_temp['country'] = 'fr'
            elif 'italian' in file_name.lower():
                df_temp['country'] = 'it'
            
            # CRIA COLUNA---------------------------------------------------------------
            df_temp['campaign'] = df_temp['utm_link'].str.extract(r'utm_campaign=(.*)')
            
            # ADCIONA AO DATAFRAME FINAL --------------------------------------------
            # guarda os dados tratados para o dataframe final
            if isinstance(df_temp, pd.DataFrame):  # verificar se é um DataFrame
                df.append(df_temp)  # usar append
            
            # test print
            print(df_temp)  
            
        except Exception as e:
            print(f"Erro ao ler o arquivo {file} : {e}")
            
# CRIAÇÃO DO ARQUIVO .xlsx COM AS TRANSFORMAÇÕES     
if df:
    # concatena todas tabelas salvas do df final
    result = pd.concat(df, ignore_index=True)
    
    # caminho de saída
    out_file = os.path.join('src', 'data', 'ready', 'clean.xlsx')  # usar os.path.join
    
    # configura o motor de escrita
    writer = pd.ExcelWriter(out_file, engine='xlsxwriter')
    
    # coloca os dados para o motor de excel configurado
    result.to_excel(writer, index=False)
    
    # salva o arquivo de excel
    writer.close()  # usar writer.close()
    
else:
    print("Nenhum arquivo encontrado")