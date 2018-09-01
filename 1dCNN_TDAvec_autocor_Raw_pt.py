
# coding: utf-8

# # 一次元CNNによる学習と識別性能評価（生データ&特徴データ）

# ---
#
# 引数：raw_tap.csv/raw_rest.csv/TDAvec_autocor_tap.csv/TDAvec_autocor_rest.csvがあるディレクトリまでのパス
#
# ---
#
# 入力：
# * raw_tap.csv/raw_rest.csv
# * TDAvec_autocor_tap.csv/TDAvec_autocor_rest.csv
#
# ---
#
# 出力：ACCURACYpt[loo][k_list]_1dCNN.csv　識別性能評価結果一覧
# k_listはk-分割交差検証法で用いた分割数
#
# ---
#
# 生データ（生データ or 生データに移動平均線を適用したデータ）と特徴抽出したデータを一次元CNNを用いて学習し，
# 交差検証法（k-分割交差検証，leave-one-out交差検証）を用いて識別性能評価を行う．
#
# ベクトル：ある時刻の各ボクセルの値のパターン
#

# In[1]:

import pandas as pd
import sys

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


# コマンドライン引数でraw_tap.csv/raw_rest.csv/TDAvec_autocor_tap.csv/TDAvec_autocor_rest.csvがあるディレクトリまでのパスを取得

# In[2]:

args = sys.argv
PATH = args[1]

# jupyter notebookのときはここで指定
# PATH = '../Data_block/analysis_by_programs/20170130ar/12ch/MAL5/'


# In[3]:

# RawDataディレクトリかMALディレクトリか識別用
DIRs = PATH.split("/")
DATA_NAME = DIRs[len(DIRs) - 2]

# k-分割交差検証用
k_list = [3, 5, 7]


# ## ONEdCNN_LOO関数

# 引数としてTrainingData関数で作成した教師データをX，ラベルをyで受け取る．
# 交差検証法の一つleave-one-out交差検証で識別精度評価を行う．
#
# * (1個をテストデータ，残りを教師データにして学習・評価) * すべてのデータ個
# * 得られたすべてのデータ個の評価結果（識別率）の平均を求めてパーセントに直す
# * 評価結果（識別率）をTrainingData関数に返す

# In[4]:

def ONEdCNN_LOO(X, y):

    # 識別率を格納する配列
    LOOscore = np.zeros(len(X))

    # ベクトルの長さを格納しておく
    bach_size = X.shape[1]


    # 1個をテストデータ，残りを教師データにして学習・評価
    # すべてのデータに対して行う
    for i in range(len(X)):

        print('----------- LOO ' + PATH + ' ' + str(i) + '回 / ' + str(len(X)) + ' ---------')

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


# ## ONEdCNN_kCV関数

# 引数としてTrainingData関数で作成した教師データをX，ラベルをy，データ分割数をkで受け取る．
# 交差検証法の一つk-分割交差検証で識別精度評価を行う．
#
# * 学習
# * (k分割し，1グループをテストデータ，残りグループを教師データにして評価) * k
# * 得られたk個の評価結果（識別率）の平均を求めてパーセントに直す
# * 評価結果（識別率）をTrainingData関数に返す

# In[5]:

def ONEdCNN_kCV(X, y, k):


    # 識別率を格納する配列
    kCVscore = np.zeros(k)

    # ベクトルの長さを格納しておく
    bach_size = X.shape[1]

    # 分割数
    kf = KFold(n_splits=k, shuffle=False)
    # 繰り返し回数
    i = 0

    for train_index, eval_index in kf.split(X):

        print('--------- kFold ' + PATH + ' ' + str(i) + ' / ' + str(k) + ' 回目 ---------')

        X_train, X_test = X[train_index], X[eval_index]
        y_train, y_test = y[train_index], y[eval_index]

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
        kCVscore[i] = score[1]

        i = i + 1


    # 評価結果（識別率）の平均を求める
    result = kCVscore.mean()

    # パーセントに直す
    result = round(result * 100, 1)

    print('k = ' + str(k) + '：' + str(kCVscore))

    return result



# ## TrainingData関数
# 引数として読み込みたいTapping/Restのそれぞれのファイル名をfile_tap/file_restで受け取る．
# * 機械学習にかけれるようにデータのベクトル化とラベルを作成
# * データとラベルを1dCNN_LOO関数，1dCNN_kCV関数に渡す
# * 帰ってきた識別率をまとめてmain関数に返す

# In[6]:

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
    results = pd.DataFrame({col_name : [result_LOO] })


    # 学習とk-分割交差検証

    print('k-hold Cross-Validation')

    # k_listに従って学習・評価
    for i in k_list:

        col_name = 'k = ' + str(i)

        #print(col_name)

        # SVM_CV関数
        result_CV = ONEdCNN_kCV(X, y, i)

        # 評価結果（識別率）をデータフレームに変換・格納
        result_CV = pd.DataFrame({col_name : [result_CV] })
        results = pd.concat([results, result_CV], axis = 1)

    return results




# ## main関数

# In[7]:

if __name__ == '__main__':

    # 生データの識別率

    print('--------- ' + DATA_NAME + ' ---------')
    raw_result = TrainingData('raw_rest.csv', 'raw_tap.csv')
    print('\n' + str(raw_result))


    # 特徴抽出データの識別率

    print('\n--------- Feature Extraction Data ---------')
    fe_result = TrainingData('TDAvec_autocor_rest.csv', 'TDAvec_autocor_tap.csv')
    print('\n' + str(fe_result))

    # 生データと特徴抽出データの識別率をまとめる
    result_cmp = pd.concat([raw_result, fe_result], axis = 0)

    # インデックス名をつける
    result_index = [DATA_NAME, 'TDAvec_autocor']
    result_cmp.index = result_index

    # csv書き出し
    PATH_RESULT = PATH + 'ACCURACYpt[loo]' + str(k_list) + '_1dCNN.csv'
    result_cmp.to_csv(PATH_RESULT, index = True)

    # #生データだけ？
    # # インデックス名をつける
    # raw_result_index = [DATA_NAME]
    # raw_result.index = raw_result_index
    #
    # # csv書き出し
    # PATH_RESULT = PATH + 'ACCURACYpt[loo]' + str(k_list) + '_Raw_1dCNN.csv'
    # raw_result.to_csv(PATH_RESULT, index = True)



# In[ ]:




# In[ ]:
