
# coding: utf-8

# # 各ボクセルごとの時間遅れτを求める
# ### 自己相関関数が最初に極小値をとる時刻
# ---
#
# 引数：raw_tap.csv/raw_rest.csvがあるディレクトリまでのパス
#
# ---
#
# 入力：raw_tap.csv/raw_rest.csv
#
# ---
#
# 出力：TAUautocor.csv　rest, tappingの各ボクセルの時間遅れτをまとめたもの
#
# ---
#
# Preprocessing_block.pyでまとめた，
#
# * tapping時の複数ボクセル（tap_raw.csv）
# * rest時の複数ボクセル（rest_raw.csv）
#
# の時系列特性を得るために3次元空間に写像する．
# 時系列データにおいて，ある時刻tの値をx軸，t+τ（時間遅れ）の値をy軸，t+2*τの値をz軸に写像すると，
# 特徴的な軌道を描くとされている（カオス理論）．
# 時間遅れτの求め方はいくつかあるが，このプログラムでは時系列データ（各ボクセルのデータ）の自己相関関数が最初に極小値をとる時刻をτとする．

# In[186]:

print('########## TAUautocor.py program excution ############')


# In[187]:

import numpy as np
from scipy import signal
import sys
import pandas as pd


# コマンドライン引数でraw_tap.csv/raw_rest.csvがあるディレクトリまでのパスを取得

# In[209]:

args = sys.argv
PATH = args[1]

# jupyter notebookのときはここで指定
#PATH = '../Data_block/analysis_by_programs/20170130ar/mb/MAL5/'


# ## autocor関数
# 引数としてmain関数で読み込んだデータをdataで受け取る．
# Rest, Tappingの各ボクセルごとの自己相関関数が最初に極小値をとる時刻を調べる --> csvファイルで書き出し

# In[210]:

def autocor(data):

    # 求めた値を入れる
    TAUs = []

    # ボクセル（列）の数だけ繰り返す
    for i in range(len(data.columns)):

        # i番目のボクセルデータ抽出
        voxel = data.iloc[:, i]

        # 自己相関関数
        x = np.correlate(voxel, voxel, mode = 'full')

        # 極小値のインデックス一覧
        first_min = signal.argrelmin(x)

        # 「最初に極小値をとるときの値」なので最初の値をTAUsに追加
        TAUs.append(first_min[0][0])

        print(i)

    return TAUs


# ## main関数
#
# * tap_raw.csv/rest_raw.csv読み込み
# * autcor関数呼び出し

# In[211]:

if __name__ == '__main__':

    # 読み込みたいファイルのパス
    PATH_rest = PATH + 'raw_rest.csv'
    PATH_tap = PATH + 'raw_tap.csv'

    # csvファイル読み込み
    rest = pd.read_csv(PATH_rest, header = 0)
    tap = pd.read_csv(PATH_tap, header = 0)



    # In[212]:

    tau_rest = autocor(rest)


    # In[213]:

    tau_tap = autocor(tap)


    # In[214]:

    # RestとTappingの各ボクセルごとの時間遅れTAUを整形
    TAUs = pd.DataFrame({'TAU_Rest':tau_rest, 'TAU_Tap':tau_tap})


    # In[215]:

    # csv書き出し
    PATH_TAU = PATH + 'TAUautocor.csv'
    TAUs.to_csv(PATH_TAU, index = False)


    # In[ ]:
