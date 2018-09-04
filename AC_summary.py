
# coding: utf-8

# # 識別率をまとめる

# 指定したcsvファイルに記録されている識別率をまとめる
#
# ---
#
# 引数：各被験者のRawDataディレクトリまでのパス
#
# ---
#
# 入力：まとめたい識別率が記録されたcsvファイルまでのパス
#
# ---
#
# 出力：Result[日付]ディレクトリ
# * 各被験者，各ヘッドコイルの従来手法や提案手法の識別率をまとめたcsvファイル
# * 全被験者の各ヘッドコイルの従来手法や提案手法の平均識別率を算出したcsvファイル

# In[254]:

import numpy as np
import pandas as pd
import sys
import os
from statistics import mean, median,variance,stdev

# .pyで実行するときは%matplotlib inlineをコメントアウト！！！！
import matplotlib.pyplot as plt
#get_ipython().magic('matplotlib inline')


# In[255]:

args = sys.argv
PATH = args[1]

# jupyter notebookのときはここで指定
# PATH = '../Data_block/analysis_by_programs/'


# In[275]:

DIR_sub = ['20170130ar/', '20170130hm/', '20170130ms/', '20170130ns/', '20170202dt/', '20170202tsk/']
DIR_ch = ['12ch/', '32ch/', 'mb/']
DIR_data = 'RawData/'

# ------ 書き換え --------- #

date = '0905'

CV = 'ACCURACY[loo]'
PM = '012dim300'
ML = '1dCNN'

# 一つ目は従来手法なので機械学習はSVMのまま
input_csv = ['ACCURACY[loo]_RAWpt_SVM.csv', 'ACCURACY[loo]_RAWts_1dCNN.csv', 'ACCURACY[loo]_TDAvecAutocor012dim300_1dCNN.csv']

# 出力csvファイルの列名
method_col = ['SPM', 'RAW data', 'TDA Data(' + PM + ')']

# ------------------------ #

# 出力csvファイルの行明
coil_index = ['12ch head coil(12ch)', '32ch head coil(32ch)', '32ch head coil multi-band(32chMB)']

# Result[日付]のディレクトリ名・パス
DIR_result = PATH + '../Result' + str(date)
PATH_result = DIR_result + '/'

# すでに存在する場合は何もせず，存在していない場合はディレクトリ作成
if not os.path.exists(DIR_result):
    os.mkdir(DIR_result)


# ## Main関数

# In[276]:

if __name__ == '__main__':

    acTab = AcSumarry()

    # グラフ出力する場合
    AcBar(acTab)


# ## AcSumarry関数
# 識別率を表としてまとめてcsvファイルに出力

# In[258]:

def AcSumarry():

    ############### 各被験者，各ヘッドコイルの従来手法や提案手法の識別率をまとめる

    all_ac = pd.DataFrame(index = [], columns = method_col)

    for s in range(len(DIR_sub)):

        ac_sub = []

        for c in range(len(DIR_ch)):

            ac_ch = []

            for i in range(len(input_csv)):

                # 各csvファイルへのパス作成，読み込み
                PATH_ac = PATH + DIR_sub[s] + DIR_ch[c] + DIR_data + input_csv[i]
                ac_method = pd.read_csv(PATH_ac, index_col = 0, header = 0)

                ac_ch.append(ac_method.iloc[0,0])

            ac_sub.append(ac_ch)


        # データフレームのac_allに結合できるようデータフレーム化，同様の列名をつける
        ac_sub_df = pd.DataFrame(ac_sub)
        ac_sub_df.columns = method_col
        ac_sub_df.index = coil_index

        # ac_allに結合
        all_ac = pd.concat([all_ac, ac_sub_df])


    # csv書き出し
    PATH_acAll = PATH + '../Result' + date + '/' + CV + '_' + PM + '_' + ML + '_all.csv'
    all_ac.to_csv(PATH_acAll)




    ############## 全被験者の各ヘッドコイルの従来手法や提案手法の平均識別率を算出したcsvファイル

    all_mean = pd.DataFrame(index = [], columns = method_col)

    for c in range(len(DIR_ch)):

        mean_method = []

        for i in range(len(input_csv)):

            mean_method.append(mean(all_ac.loc[coil_index[c], method_col[i]]))

        # データフレームのac_allに結合できるようデータフレーム化（転置しておく），同様の列名をつける
        mean_method_df = pd.DataFrame(mean_method).T
        mean_method_df.columns = method_col

        # all_meanに結合
        all_mean = pd.concat([all_mean, mean_method_df])

    # 行明をつける
    all_mean.index = coil_index

    # csv書き出し
    PATH_acMean = PATH + '../Result' + date + '/' + CV + '_' + PM + '_' + ML + '_mean.csv'
    all_mean.to_csv(PATH_acMean)

    return all_mean


# ## AcBar関数

# 棒グラフにして出力

# In[259]:

def AcBar(acTab):

    plt.figure()

    acTab.plot.bar(color = ['silver', 'lightblue', 'firebrick'],
               width = 0.8, figsize = (16,9), rot = 0, fontsize = 15, legend='reverse',
               yticks = [10,20,30,40,50,60,70,80,90,100])

    PATH_graph = PATH + '../Result' + date + '/' + CV + '_' + PM + '_' + ML + '_mean.png'
    plt.savefig(PATH_graph)

    plt.close('all')


# In[ ]:
