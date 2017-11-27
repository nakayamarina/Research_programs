
# coding: utf-8

# # 実験（ブロックデザイン）から得られたfMRIデータの前処理
# ----
# /VoxelディレクトリのY01.csv, Y02.csv, ... Y10.csvまでのデータには，指のタッピング運動時，またはレスト時に賦活しているとされる上位10ボクセルそれぞれのZ-score（賦活度合いみたいなもの）が記録されている．  
# 記録は以下の実験デザイン（ブロックデザインの場合）に従ってされている．  
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
#   
# 本研究では時系列データとして扱いたいため，rest，tappingをそれぞれまとめる．  
#   
# ----

# In[1]:

print('########## Preprocessing.py program excution ############')


# In[17]:

import glob
import sys
import pandas as pd
import matplotlib.pyplot as plt


# コマンドライン引数で/Voxelディレクトリまでのパスを取得

# In[6]:

#args = sys.argv
#PATH = args[1]

# jupyter notebookのときはここで指定
PATH = '../tameshi/20170130ar/mb/Voxel/'


# ## SplitRT関数

# * RestデータとTappingデータに分割
# * RestデータとTappingデータをcsvファイルで書き出し

# In[7]:

def SplitRT(brain):
    
    # 12ch or 32ch Head coil の場合
    if len(brain) == 120:
        
        # Rest，Tappingのデータ抽出用maskを作成
        # 行数0-119のうち　(行数 // 10) % 2　で割り切れるならRest，割り切れなければTapping
        # （除算は '//' としないと小数まで計算される）
        R_mask = (brain.index // 10) % 2 == 0
        T_mask = (brain.index // 10) % 2 == 1
        
        # mask適用
        rest_data = brain[R_mask]
        tap_data = brain[T_mask]
        
        # csv書き出し
        REST_PATH = PATH + '../rest_raw.csv'
        rest_data.to_csv(REST_PATH, index = False)
        TAP_PATH = PATH + '../tap_raw.csv'
        tap_data.to_csv(TAP_PATH, index = False)
        
        
    # 32ch Milti-band の場合
    elif len(brain) == 360:
        
        # 行数0-359のうち　(行数 // 30) % 2　で割り切れるならRest，割り切れなければTapping
        R_mask = (brain.index // 30) % 2 == 0
        T_mask = (brain.index // 30) % 2 == 1
        
        # mask適用
        rest_data = brain[R_mask]
        tap_data = brain[T_mask]

        # csv書き出し
        REST_PATH = PATH + '../rest_raw.csv'
        rest_data.to_csv(REST_PATH, index = False)
        TAP_PATH = PATH + '../tap_raw.csv'
        tap_data.to_csv(TAP_PATH, index = False)


# ## main関数 

# * fMRIデータ読み込み
# * 全ボクセルデータ連結
# * 全ボクセルデータをcsvで書き出し

# In[20]:

if __name__ == '__main__':
    
    # /Voxelディレクトリ内のcsvファイルのパスを取得
    csv_file = PATH + '*.csv'
    files = []
    files = glob.glob(csv_file)
    

    # 1つ目のファイルを読み込む
    
    # 列名
    row_name = "Voxel1"
    
    # 列名をつけてデータフレームとして読み込み（row_nameの後に','をつけることで1列だけ名前をつけることができる）
    brain = pd.read_csv(files[0], names=(row_name,))
    
    # 同様に2つ目以降のファイルをデータフレームとして読み込み，1つ目のデータフレームに横連結
    for i in range(1, len(files)):

        row_name = "Voxel" + str(i+1)
        data = pd.read_csv(files[i], names=(row_name,))
        
        brain = pd.concat([brain, data], axis = 1)
        
    
    # csv書き出し
    BRAIN_PATH = PATH + '../all_raw.csv'
    brain.to_csv(BRAIN_PATH, index = False)
        
    # SplitRTにbrainを引数として渡し，RestとTappingを分ける
    SplitRT(brain)
    
    

