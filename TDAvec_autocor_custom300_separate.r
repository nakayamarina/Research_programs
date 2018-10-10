# TDAによる特徴抽出とベクトル化（穴の種類やきざみ時間変更可）

# ---

# 引数：raw_tap.csv/raw_rest.csv, 時間遅れτのcsvファイルがあるディレクトリまでのパス

# ---

# 入力：raw_tap.csv/raw_rest.csv, 時間遅れτのcsvファイル(TAUautocre.csv)

# ---

# 出力：
# * TDAvec_autocor_tap_custom_(パラメータ).csv：前処理をしたTapping時のデータの特徴抽出を行ったもの
# * TDAvec_autocor_rest_custom_(パラメータ).csv：前処理をしたRest時のデータの特徴抽出を行ったもの
#
# 場合に応じて
# * TDAvec_autocor_attractor/voxel[ボクセル番号]-[区切り番号]_Tapping.png
# * TDAvec_autocor_attractor/voxel[ボクセル番号]-[区切り番号]_Rest.png
# * TDAvec_autocor_barcode/voxel[ボクセル番号]-[区切り番号]_Tapping.png
# * TDAvec_autocor_barcode/voxel[ボクセル番号]-[区切り番号]_Rest.png


# ---

# 穴の種類を変更することは可能だが，ここでやると処理時間がかかるのでpythonの再ベクトル化プログラムでやる（ReVectrize_ProposedMethod.py)

# 前処理（Preprocessing_block.py, MovingAverageLine.py）をした

# * Tapping時のデータ（raw_tap.csv or MAL区間_tap.csv）
# * Rest時のデータ（raw_rest.csv or MAL区間_rest.csv）

# の特徴抽出をTDAを用いて行う．

# separateがついたプログラムでは，1ボクセルの1時系列データをいくつかに区切る．

# (1) 3次元空間への写像
# Tapping時とRest時の各ボクセルの時間遅れτを用いて
# 各ボクセルの時系列データにおいてある時刻tの値，t+τの値，t+2*τの値で3次元データとし，アトラクタ図形を得る

# (2) TDA適用
# 3次元データに対してTDAのPersistent Homology適用しバーコードダイアグラムを得る

# (3) ベクトル化
# 穴の数をkizamiNumber(TDAvec関数の変数)回数えることでベクトル化する

if (!require(package = "TDA")) {
  install.packages(pkgs = "TDA")
}

if (!require(package = "scatterplot3d")) {
  install.packages(pkgs = "scatterplot3d")
}

library(TDA)
library(scatterplot3d)

print('################ TDAvec_autocor.r excution ###################')

# コマンドライン引数でraw_tap.csv/raw_rest.csv, TAUautocor.csvがあるディレクトリまでのパスを取得

#PATH <- '../Data_block/analysis_by_orograms/20170130ar/12ch/RawData/
PATH = commandArgs(trailingOnly=TRUE)[1]

# 12ch,32chの場合の1タスクあたりのスキャン数
scan <- 96
# 32chMBの場合の1タスクあたりのスキャン数
scanMB <- 296

# 時系列データを分割する際の1区切りあたりのスキャン枚数
# 12ch,32ch 24scanの場合約72秒，4区切り
separate <- 24
# 32chMBの場合 74scanの場合約74秒，４区切り
separateMB <- 74

# TDAvec関数で使うripsDiagのmaxsxaleの値設定
ms<- 2

# BettiNumberCount関数で使う穴を数える回数
kizamiNumber <- 300

# アトラクタ図，バーコードを出力する(1) or しない (0)
# 出力する場合の保存ディレクトリ名
atrct_output <- 1
barcode_output <- 1
atrctName <- 'TDAvec_autocor_attractor_sep'
barcodeName <- 'TDAvec_autocor_barcode_sep'

# ベクトル化する穴の種類
# 使わないもの（使う穴が2つの場合）
NotHole <- 10
# or
# 使うもの（使う穴が1つの場合）
UseHole <- 10
# 設定する．設定しない場合は10とかにする

# どういう設定かをPatternに数字として格納
# パラメータがわかるcsvファイル名用文字列
if (NotHole == 0 && UseHole == 10){
  
  Pattern <- 1
  parameters <- paste(kizamiNumber, "_", "12dim", sep="")
  
} else if (NotHole == 1 && UseHole == 10) {
  
  Pattern <- 2
  parameters <- paste(kizamiNumber, "_", "02dim", sep="")
  
} else if (NotHole == 2 && UseHole == 10) {
  
  Pattern <- 3
  parameters <- paste(kizamiNumber, "_", "01dim", sep="")
  
} else if (UseHole == 0 && NotHole == 10) {
  
  Pattern <- 4
  parameters <- paste(kizamiNumber, "_", "0dim", sep="")
  
} else if (UseHole == 1 && NotHole == 10) {
  
  Pattern <- 5
  parameters <- paste(kizamiNumber, "_", "1dim", sep="")
  
} else if (UseHole == 2 && NotHole == 10) {
  
  Pattern <- 6
  parameters <- paste(kizamiNumber, "_", "2dim", sep="")
  
} else {
  
  Pattern <- 7
  parameters <- paste(kizamiNumber, "_", "012dim", sep="")
  
}


# main関数

# * raw_tap.csv/raw_reset.csv読み込み
# * TDAvec_autocor_tap.csv/TDAvec_autocor_rest.csv書き出し

main <- function(){
  
  # 読み込みたいファイルのパス
  PATH_rest <- paste(PATH, 'raw_rest.csv', sep = "")
  PATH_tap <- paste(PATH, 'raw_tap.csv', sep = "")
  PATH_tau <- paste(PATH, 'TAUautocor.csv', sep = "")
  
  # csvファイルの読み込み
  rest <- read.csv(PATH_rest)
  tap <- read.csv(PATH_tap)
  taus <- read.csv(PATH_tau)
  
  if(nrow(rest) == scan){
    scan_num <- scan
    sep_num <- separate
  } else if(nrow(rest) == scanMB){
    scan_num <- scanMB
    sep_num <- separateMB
  }
  
  # このプログラムでの出力ファイルをを保存するディレクトリ名・パス
  newDIR <- paste(PATH, 'separate', sep_num, sep="")
  newPATH <- paste(newDIR, '/', sep="")
  
  # すでに存在する場合は何もせず，存在していない場合はディレクトリ作成
  if(!file.exists(newPATH)) {
    dir.create(newDIR)
  }
  
  # ベクトル化したデータを格納する配列
  restVec <- c()
  tapVec <- c()
  
  # ボクセルの数だけ繰り返す
  for(i in 1:nrow(taus)){
    
    # 区切りごとに繰り返す
    for(j in 1:(scan_num/sep_num)){
    
      messe <- paste('----- excution voxel.', i, ' - ', j, '/', (scan_num/sep_num), '区切り ---')
      print(messe)
      
      # i番目のボクセルのj区切り目のデータ
      
      voxel_rest <- rest[(((j-1) * sep_num)+1):(j * sep_num), i]
      voxel_tap <- tap[(((j-1) * sep_num)+1):(j * sep_num), i]
      
      # i番目のボクセルの時間遅れτ
      tau_rest <- taus[i, 1]
      tau_tap <- taus[i, 2]
      
      attractor_rest <- Attractor(voxel_rest, tau_rest, i, j, sep_num, "Rest", newPATH)
      attractor_tap <- Attractor(voxel_tap, tau_tap, i, j,  sep_num, "Tapping", newPATH)
      
      restVec <- rbind(restVec, TDAvec(attractor_rest, i, j, sep_num, "Rest", newPATH))
      tapVec <- rbind(tapVec, TDAvec(attractor_tap, i, j, sep_num, "Tapping", newPATH))
    
}
    
  }
  
  
  # csv書き出し
  PATH_restVec <- paste(newPATH, 'TDAvec_autocor_rest_custom_', parameters, '.csv', sep = "")
  write.csv(as.data.frame(restVec), PATH_restVec, quote = FALSE, row.names = FALSE)
  
  PATH_tapVec <- paste(newPATH, 'TDAvec_autocor_tap_custom_', parameters, '.csv', sep = "")
  write.csv(as.data.frame(tapVec), PATH_tapVec, quote = FALSE, row.names = FALSE)
  
}


# Attractor関数
# 引数としてi番目のボクセルデータをVoxel，時間遅れτをtau，何番目のボクセルかをvoxel_no，何区切りめかをsep_no, 1区切りのscan数をsep_num, RestかTappingかをtask, パスをnewPATHで受けとる
# * 時間遅れτを使って，ある時刻tの値，t+τの値，t+2*τの値で3次元データを作る
# * 3次元データを返す

Attractor <- function(voxel, tau, voxel_no, sep_no, sep_num, task, newPATH){
  
  # データをずらすことで長さが変わるので注意！
  
  # 元データ
  x <- voxel[1:(length(voxel) - (2*tau))]
  # 元データからτ分ずらしたデータ
  y <- voxel[(1 + tau):(length(voxel) - (tau))]
  # 元データから2*τ分ずらしたデータ
  z <- voxel[(1 + (2*tau)):length(voxel)]
  
  # 3次元データとして結合
  xyz <- cbind(x, y, z)
  
  # アトラクタ図を出力する場合
  if (atrct_output == 1){
    
    # 出力するアトラクタ図を保存するのディレクトリ名・パス
    DIR_attractor <- paste(newPATH, atrctName, sep_num, sep="")
    PATH_attractor <- paste(DIR_attractor, '/', sep="")
    
    # すでに存在する場合は何もせず，存在していない場合はディレクトリ作成
    if(!file.exists(PATH_attractor)) {
      dir.create(DIR_attractor)
    }
    
    # この後にplotするアトラクタ図のタイトル
    graph_name <- paste("Mapping to 3dim space : ", task, "-voxel", voxel_no, "-", sep_no, sep="")
    
    # この後に出力するpngファイル名
    PATH_graph <- paste(PATH_attractor, "voxel", voxel_no, "-", sep_no, '_', task, '.png', sep="")
    
    # 3次元データをplot，出力
    png(PATH_graph)
    scatterplot3d(xyz, xlab = "x = t", ylab = "y = t + τ", zlab = "z = t + 2*τ", pch = 16, type="o", main = graph_name)
    dev.off()
    
    print(PATH_graph)
    
  }
  
  return (xyz)
  
}

# TDAvec関数
# 引数としてi番目のボクセルデータを3次元データにしたものをattractor，何番目のボクセルかをvoxel_no，何区切りめかをsep_no, 1区切りのscan数をsep_num, RestかTappingかをtask, パスをnewPATHで受けとる
# * ripsDiagで3次元データにTDAのPersistent Homologyを適用
# * 各次の穴情報それぞれに対してBattiNumberCount関数を使って穴の数を数え，横結合することでベクトル化
# * ベクトル化したデータを返す

TDAvec <- function(attractor, voxel_no, sep_no, sep_num, task, newPATH){
  
  # TDAのPersistent Homologyを適用
  tda <- ripsDiag(X = attractor, maxdimension = 2, maxscale = ms)
  
  if (barcode_output == 1){
    
    # バーコードを保存するディレクトリ名・パス
    DIR_tda <- paste(newPATH, barcodeName, sep_num, sep="")
    PATH_tda <- paste(DIR_tda, '/', sep="")
    
    # すでに存在する場合は何もせず，存在していない場合はディレクトリ作成
    if(!file.exists(PATH_tda)) {
      dir.create(DIR_tda)
    }
    
    # この後でplotするバーコードのタイトル
    barcode_name <- paste("Barcode Diagram (TDA) : ", task, "-voxel", voxel_no, "-", sep_no, '_', sep="")
    
    # この後で出力するpngファイル名
    PATH_barcode <- paste(PATH_tda, "voxel", voxel_no, "-", sep_no, '_', task, '.png', sep="")
    
    # バーコードをplot，出力
    png(PATH_barcode)
    plot(tda$diagram, barcode = TRUE, main = barcode_name)
    dev.off()
    
    print(PATH_barcode)
    
  }
  
  # 穴情報を抽出
  df_tda <- as.data.frame(tda$diagram[, 1:3])
  
  # 各次の穴情報を分割
  zeroDim <- subset(df_tda, df_tda$dimension == 0)
  oneDim <- subset(df_tda, df_tda$dimension == 1)
  twoDim <- subset(df_tda, df_tda$dimension == 2)
  
  
  # 各次の穴の数を数え横結合することでベクトル化
  
  if (Pattern == 1){
    
    tdaVec <- c(BettiNumberCount(oneDim), BettiNumberCount(twoDim))
    
  } else if (Pattern == 2) {
    
    tdaVec <- c(BettiNumberCount(zeroDim), BettiNumberCount(twoDim))
    
  } else if (Pattern == 3) {
    
    tdaVec <- c(BettiNumberCount(zeroDim), BettiNumberCount(oneDim))
    
  } else if (Pattern == 4) {
    
    tdaVec <- c(BettiNumberCount(zeroDim))
    
  } else if (Pattern == 5) {
    
    tdaVec <- c(BettiNumberCount(oneDim))
    
  } else if (Pattern == 6) {
    
    tdaVec <- c(BettiNumberCount(twoDim))
    
  } else if (Pattern == 7) {
    
    tdaVec <- c(BettiNumberCount(zeroDim), BettiNumberCount(oneDim), BettiNumberCount(twoDim))
    
  }
  
  return(tdaVec)
  
}

# BettiNumberCount関数
# 引数として各次の穴情報をholeで受け取る
# * 穴を数える回数（kizamiNumber）などのパラメータを決める
# * 穴情報はそれぞれの穴発生時の直径（Birth），穴消滅時の直径（Death）が記録されており，ある時刻timeの時の穴の数を数える
# * 1×kizamiNumberのデータを返す

BettiNumberCount <- function(hole){
  
  
  # 穴をkizamiNumber回数えるために時間幅を求める
  # もともとの時間はms，kizamiNumberで割ることでどれぐらいずつ時刻timeをずらせばいいかわかる
  kizamiWidth <- ms/kizamiNumber
  
  # 時刻
  time <- 0
  
  # 穴を数えた回数
  k <- 0
  
  # kizamiNumber回数えた結果を格納する配列
  bettiNumbers <- c()
  
  # 穴が発生していればTrue
  if(nrow(hole) >= 1){
    
    # kizamiNumber回穴の数を数えるまでループ
    while(k != kizamiNumber){
      
      # 時刻timeの時の穴の数
      bettiCount <- 0
      
      # 発生したそれぞれの穴に対して調べる
      for(j in 1:nrow(hole)){
        
        # 時刻timeがある穴の発生時間中（Birth <= time <= Death）であればbettiCountに1足す
        if((hole$Birth[j] <= time) && (time <= hole$Death[j])){
          
          bettiCount = bettiCount + 1
          
        }
        
      }
      
      # bettiCountを配列に格納
      bettiNumbers <- c(bettiNumbers, bettiCount)
      
      # 時刻timeをずらす
      time = time + kizamiWidth
      
      # 穴の数を数えたのでkに1足す
      k = k + 1
      
    }
    
  } else {
    
    # そもそも穴が発生していなければ0をkizamiNumber個格納
    bettiNumbers <- numeric(kizamiNumber)
    
  }
  
  return(bettiNumbers)
  
}

# Execute main function
main()
