
# coding: utf-8

# # 一次元CNNによる学習と識別性能評価（提案手法）

# ---
#
# 引数：提案手法でベクトル化したcsvファイルがあるディレクトリまでのパス
#
# ---
#
# 入力：提案手法でベクトル化したcsvファイル
#
# ---
#
# 出力：ACCURACY[loo]_(ファイル名)_SVM.csv 識別性能評価
#
# ---
#
# 提案手法でベクトル化したデータを1dCNNで学習，交差検証法(leave-one-out交差検証法)を用いて識別性能評価を行う．

# In[10]:

import pandas as pd
import sys

# matplotlib inline部分は.pyの時にはコメントアウトしないとエラー出る！

import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
# get_ipython().magic('matplotlib inline')
import matplotlib.pyplot as plt
from keras.layers.convolutional import Conv1D, UpSampling1D
from keras.layers.pooling import MaxPooling1D
from keras.utils import np_utils

from sklearn.model_selection import KFold
from sklearn.model_selection import train_test_split


# コマンドライン引数で提案手法でベクトル化したcsvファイルがあるディレクトリまでのパスを取得

# In[11]:


args = sys.argv
PATH = args[1]

# jupyter notebookのときはここで指定
# PATH = '../Data_block/analysis_by_programs/20170130ar/12ch/RawData/'

# 機械学習するデータ（提案手法でベクトル化したcsvファイル）
ML_restData = 'TDAvec_autocor_rest_custom_300_012dim.csv'
ML_tapData = 'TDAvec_autocor_tap_custom_300_012dim.csv'

# 出力するデータの行名，ファイル名
outputIndex = 'TDAvec_autocor(300, 012dim) + 1dCNN'
outputFile = 'TDAvecAutocor012dim300'


# ## ONEdCNN_LOO関数

# 引数としてTrainingData関数で作成した教師データをX，ラベルをyで受け取る．
# 交差検証法の一つleave-one-out交差検証で識別精度評価を行う．
#
# * (1個をテストデータ，残りを教師データにして学習・評価) * すべてのデータ個
# * 得られたすべてのデータ個の評価結果（識別率）の平均を求めてパーセントに直す
# * 評価結果（識別率）をTrainingData関数に返す

# In[12]:

def ONEdCNN_LOO(X, y):

    # 識別率を格納する配列
    LOOscore = np.zeros(len(X))

    # ベクトルの長さを格納しておく
    bach_size = X.shape[1]


    # 1個をテストデータ，残りを教師データにして学習・評価
    # すべてのデータに対して行う
    for i in range(len(X)):

        print('------ ' + str(i) + ' / ' + str(len(X)) + '回 -----')

        # テストデータ
        X_test = X[i]
        y_test = y[i]

        # テストデータとして使用するデータを除いた教師データを作成
        X_train = np.delete(X, i, 0)
        y_train = np.delete(y, i, 0)


        # （データ数, ベクトルの長さ，1）という形にリシェイプする
        X_train = np.reshape(X_train, (-1, bach_size, 1))
        X_test = np.reshape(X_test, (-1, bach_size, 1))

        # ダミー変数に変換
        y_train = np_utils.to_categorical(y_train, 2)
        y_test = np_utils.to_categorical(y_test ,2)

        # 1次元CNNのインスタンスを作成
        # 参考文献（Time series classification via TDA）に従ってパラメータを設定
        # 1st Conv1d : kernel_number = 7, kernel_size = 6
        # 1st MacPooling : kernel_number = 7
        # 2nd Conv1d : kernel_number = 7, kernel_size = 2
        # 2nd MacPooling : kernel_number = 3
        # Flattenで1次元に
        model = Sequential()
        model.add(Conv1D(7, 6, padding='same', input_shape=(bach_size, 1)))
        model.add(Activation('relu'))
        model.add(MaxPooling1D(7, padding='same'))
        model.add(Conv1D(7, 2, padding='same', activation='relu'))
        model.add(MaxPooling1D(3, padding='same'))

        model.add(Flatten())
        model.add(Dense(units=2, activation='softmax'))
        model.compile(loss='mse', optimizer='adam', metrics=["accuracy"])

        # 学習
        history = model.fit(X_train, y_train, epochs=100)

        # 評価結果（識別率）を格納
        score = model.evaluate(X_test, y_test)
        LOOscore[i] = score[1]



    # 評価結果（識別率）の平均を求める
    result = LOOscore.mean()

    # パーセントに直す
    result = round(result * 100, 1)

    print(str(LOOscore) + '\n')

    return result


# ## TrainingData関数
# 引数として読み込みたいTapping/Restのそれぞれのファイル名をfile_tap/file_restで受け取る．
# * 機械学習にかけれるようにデータのベクトル化とラベルを作成
# * データとラベルを1dCNN_LOO関数，1dCNN_kCV関数に渡す
# * 帰ってきた識別率をまとめてmain関数に返す

# In[13]:

def TrainingData(file_rest, file_tap):

    # 読み込みたいファイルのパス
    PATH_rest = PATH + file_rest
    PATH_tap = PATH + file_tap

    # csvファイル読み込み
    rest = pd.read_csv(PATH_rest, header = 0)
    tap = pd.read_csv(PATH_tap, header = 0)

    # RestとTappingのデータをまとめる
    all_data = pd.concat([rest, tap], axis = 0)

    # ベクトル化
    X = all_data.as_matrix()

    # ラベル作成
    label_rest = np.zeros(len(rest.index))
    label_tap = np.ones(len(tap.index))

    y = np.r_[label_rest, label_tap]


    # 学習とleave-one-out交差検証

    print('leave-one-out')

    col_name = 'leave-one-out'

    #print(col_name)

    # SVM_LOO関数
    result_LOO = ONEdCNN_LOO(X, y)

    # 評価結果（識別率）をデータフレームに変換・格納
    ac = pd.DataFrame({col_name : [result_LOO] })

    return ac




# ## main関数

# In[14]:

if __name__ == '__main__':


    # 識別率を算出

    print('\n--------- ' + outputIndex + ' Data ---------')
    PS_result = TrainingData(ML_restData, ML_tapData)
    print('\n' + str(PS_result))

    # インデックス名をつける
    result_index = [outputIndex]
    PS_result.index = result_index

    # csv書き出し
    PATH_RESULT = PATH + 'ACCURACY[loo]_' + outputFile + '_1dCNN.csv'
    PS_result.to_csv(PATH_RESULT, index = True)



# In[ ]:




# In[ ]:
