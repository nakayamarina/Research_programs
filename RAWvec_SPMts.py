
# coding: utf-8

# # RAW dataから新しいベクトル生成
# ### M1seminner2の考察より
# ---
#
# 引数：all_raw.csvがあるディレクトリまでのパス
#
# ---
#
# 入力：all_raw.csv
#
# ---
#
# 出力：RAWvec_SPMts_rest.csv/RAWvec_SPMts_tap.csv　以下に従ってベクトル化したもの
#
# ---
#
# Preprocessing_block.pyでまとめた，
#
# * Tapping/Rest時の10ボクセルのデータ（all_raw.csv）
#
# を時系列，各ボクセルの値のパターンを考慮してベクトル化する．
#
# 前から voxel.1, voxel.2, ... , voxel.10
# rest    [ (01~10scan), (01~10scan), ... , (01~10scan) ]
# tapping [ (11~20scan), (11~20scan), ... , (11~20scan) ]
# rest    [ (21~30scan), (21~30scan), ... , (21~30scan) ]
# ...
#
# ( )には，1ブロック分を入れる（以下参照）
# ※ただし，pythonは0始まりなので注意
#
#
# [12ch or 32ch Head coil]
#
# 120 scan（360s）
# TR 3s / 1scan
#
# 1-10:	Rest
# 11-20:  Tapping
# 21-30:	Rest
# 31-40:  Tapping
# 41-50:	Rest
# 51-60:  Tapping
# 61-70:	Rest
# 71-80:  Tapping
# 81-90:	Rest
# 91-100:  Tapping
# 101-110: Rest
# 111-120:  Tapping
#
# [32ch Multi-band]
#
# 360 scan（360s）
# TR 1s / 1scan
#
# 1-30:	Rest
# 31-60:  Tapping
# 61-90:	Rest
# 91-120:  Tapping
# 121-150: Rest
# 151-180: Tapping
# 181-210: Rest
# 211-240: Tapping
# 241-270: Rest
# 271-300: Tapping
# 301-330: Rest
# 331-360: Tapping

# In[61]:

print('########## RAWvec_SPMts.py program excution ############')


# In[62]:

import numpy as np
from scipy import signal
import sys
import pandas as pd


# コマンドライン引数でraw_tap.csv/raw_rest.csvがあるディレクトリまでのパスを取得

# In[73]:

args = sys.argv
PATH = args[1]

# jupyter notebookのときはここで指定
#PATH = '../Data_block/analysis_by_programs/20170130ar/mb/RawData/'


# ## RAWvec関数
# 引数としてmain関数で読み込んだデータをdataで受け取る．
# RAWvec_SPMts_rest.csv/RAWvec_SPMts_tap.csvを書き出す．

# In[77]:

def RAWvec(data):

    # 生成したベクトルを格納する用
    restVec = []
    tapVec = []

    # 1ブロックあたりのscan数をnumber_scanに格納
    if len(data) == 120:
        number_scan = 10

    if len(data) == 360:
        number_scan = 30


    for task in range(int(len(data) / number_scan)):

        # 1ブロックの始まり
        bf = task * number_scan
        # 1ブロックの終わり
        be = bf + number_scan

        # 各ボクセルの1ブロックを取得,配列変換
        newVec = np.array(data[bf:be].T)

        # 2次元配列になっているので1次元配列変換
        newVec = np.ravel(newVec)

        # rest
        if task % 2 == 0:

            # 結合
            restVec.append(newVec)
            print("Rest : " + str(bf) + "~" + str(be-1))

        # tap
        else :

            #結合
            tapVec.append(newVec)
            print("Tapping : " + str(bf) + "~" + str(be-1))


    # DataFrame型に直しておく
    restVec = pd.DataFrame(restVec)
    tapVec = pd.DataFrame(tapVec)

    # csv書き出し
    PATH_REST = PATH + 'RAWvec_SPMts_rest.csv'
    restVec.to_csv(PATH_REST, index = False)

    PATH_TAP = PATH + 'RAWvec_SPMts_tap.csv'
    tapVec.to_csv(PATH_TAP, index = False)

    return


# ## main関数
#
# * all_raw.csv読み込み
# * RAWvec関数呼び出し
# * RAWvec_SPMts_rest.csv/RAWvec_SPMts_tap.csvの書き出し

# In[78]:

if __name__ == '__main__':

    # 読み込みたいファイルのパス
    PATH_raw = PATH + 'all_raw.csv'

    # csvファイル読み込み
    rawdata = pd.read_csv(PATH_raw, header = 0)



# In[79]:

RAWvec(rawdata)


# In[ ]:
