
# coding: utf-8

# # 各ボクセルごとの自己相関関数が最初に極小値をとる値を調べる
# ---
#
# 引数：tap_raw.csv/rest_raw.csvがあるディレクトリまでのパス
#
# ---
#
# 入力：tap_raw.csv/rest_raw.csv
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
# 時間遅れτの求め方はいくつかあるが，このプログラムでは時系列データ（各ボクセルのデータ）の自己相関関数が最初に極小値をとる値をτとする．

# In[102]:

print('########## TAUautocor.py program excution ############')


# In[111]:

import numpy as np
from scipy import signal
import sys
import pandas as pd


# コマンドライン引数でtap_raw.csv/rest_raw.csvがあるディレクトリまでのパスを取得

# In[167]:

args = sys.argv
PATH = args[1]

# jupyter notebookのときはここで指定
#PATH = '../tameshi/20170130ar/mb/'


# ## autocor関数
#
# * Rest, Tappingの各ボクセルごとの自己相関関数が最初に極小値をとる値を調べる --> csvファイルで書き出し

# In[168]:

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

# In[169]:

if __name__ == '__main__':

    # 読み込みたいファイルのパス
    rest_PATH = PATH + 'rest_raw.csv'
    tap_PATH = PATH + 'tap_raw.csv'

    # csvファイル読み込み
    rest = pd.read_csv(rest_PATH, header = 0)
    tap = pd.read_csv(tap_PATH, header = 0)



# In[170]:

rest_tau = autocor(rest)


# In[171]:

tap_tau = autocor(tap)


# In[172]:

# RestとTappingの各ボクセルごとの時間遅れTAUを整形
TAUs = pd.DataFrame({'Rest_TAU':rest_tau, 'Tap_TAU':tap_tau})


# In[173]:

# csv書き出し
TAU_PATH = PATH + 'TAUautcor.csv'
TAUs.to_csv(TAU_PATH, index = False)
