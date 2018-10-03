
# coding: utf-8

# # 穴の種類を限定

# ---
#   
# 引数：提案手法でベクトル化したcsvファイル（大体 TDvec_autocor_tap_custom_(パラメータ)012dim.csv）があるディレクトリまでのパス  
#   
# ---
#   
# 入力：提案手法でベクトル化したcsvファイル
# 
# ---
#   
# 出力：  
# * TDAvec_autocor_tap_custom_(パラメータ).csv
# * TDAvec_autocor_rest_custom_(パラメータ).csv
# 
# ---  
# 
# 0-dim，1-dim，2-dimの穴の情報を含んだベクトルデータにおいて，穴の種類を選択しベクトル化し直す．
# 

# In[1]:

import numpy as np
import pandas as pd
import sys


# コマンドライン引数で提案手法でベクトル化したcsvファイルがあるディレクトリまでのパスを取得

# In[4]:

#args = sys.argv
#PATH = args[1]

# jupyter notebookのときはここで指定
PATH = '../Data_tappingState-2fe_Moter/analysis_by_programs/20171020rn/12ch/RawData/'

# ベクトル化する際の手法
PM = 'TDAvec_autocor'

# ベクトル化された際のきざみ時間
kizamiNumber = [100, 300]


# In[5]:


# ベクトル化する穴の種類
# 使わないもの（使う穴が2つの場合）
NotHole = 2
# or
# 使うもの（使う穴が1つの場合）
UseHole = 10
# を設定する．設定しない場合は10とかにする


# ## ReVec関数

# 引数として読み込みたいファイル名をfileで受け取る．  
# 条件に応じて再ベクトル化する（reVec）．  
# 出力ファイル用に条件を含んだファイルの名前を作成しておく（parameters）．  
# reVec，parametersを返す．

# In[6]:

def ReVec(file, kizamiNumber):
    
    # 読み込みたいファイルのパス
    PATH_file = PATH + file
    
    # csvファイル読み込み
    data = pd.read_csv(PATH_file, header = 0)
    
    # 条件に応じた穴の種類のベクトル抽出，出力ファイル用の名前作成
    if (NotHole == 0 and UseHole == 10) :

        reVec = data.iloc[:, kizamiNumber:kizamiNumber*3]
        
        parameters = str(kizamiNumber) + '_12dim'

    elif (NotHole == 1 and UseHole == 10) :

        reVec1 = data.iloc[:, 0:kizamiNumber]
        reVec2 = data.iloc[:, kizamiNumber*2:kizamiNumber*3]
        reVec = pd.concat([reVec1, reVec2], axis = 1)
        
        parameters = str(kizamiNumber) + '_02dim'

    elif (NotHole == 2 and UseHole == 10) :

        reVec = data.iloc[:, 0:kizamiNumber*2]
        
        parameters = str(kizamiNumber) + '_01dim'

    elif (UseHole == 0 and NotHole == 10) :  

        reVec = data.iloc[:, 0:kizamiNumber]
        
        parameters = str(kizamiNumber) + '_0dim'

    elif (UseHole == 1 and NotHole == 10) :

        reVec = data.iloc[:, kizamiNumber:kizamiNumber*2]
        
        parameters = str(kizamiNumber) + '_1dim'

    elif (UseHole == 2 and NotHole == 10) :

        reVec = data.iloc[:, kizamiNumber*2:kizamiNumber*3]
        parameters = str(kizamiNumber) + '_2dim'

    return reVec, parameters


# ## main関数

# In[9]:

if __name__ == '__main__':
    
    for kizami in range(len(kizamiNumber)):
        
        # ベクトル化し直すデータ
        ReVec_restData = 'TDAvec_autocor_rest_custom_' + str(kizamiNumber[kizami]) + '_012dim.csv'
        ReVec_tapData = 'TDAvec_autocor_tap_custom_' + str(kizamiNumber[kizami]) + '_012dim.csv'

        newRestVec, paraName = ReVec(ReVec_restData, kizamiNumber[kizami])
        newTapVec, paraName = ReVec(ReVec_tapData, kizamiNumber[kizami])

        # csv書き出し
        PATH_newRest = PATH + PM + '_rest_custom_' + paraName + '.csv'
        newRestVec.to_csv(PATH_newRest, index = False, header = True)
        print(PATH_newRest)

        PATH_newTap = PATH + PM + '_tap_custom_' + paraName + '.csv'
        newTapVec.to_csv(PATH_newTap, index = False, header = True)
        print(PATH_newTap)


# In[ ]:




# In[ ]:



