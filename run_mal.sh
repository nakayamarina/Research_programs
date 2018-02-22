PATH_DATA="../Data_block/analysis_by_programs/"

DIRs=`ls -F ${PATH_DATA} | grep /`

for dir in $DIRs
do

  for image_method in 12ch 32ch mb
  do

    PATH_RAW="${PATH_DATA}${dir}${image_method}/RawData/"

    echo "------------ ${PATH_RAW} ---------------"
    python MovingAverageLine.py ${PATH_RAW}

    python TAUautocor.py ${PATH_RAW}

    Rscript TDAvec_autocor.r ${PATH_RAW}

    python SVM_TDAvec_autocor_Raw_ts.py ${PATH_RAW}
    python SVM_TDAvec_autocor_Raw_pt.py ${PATH_RAW}

    PATH_MAL="${PATH_DATA}${dir}${image_method}/MAL3/"

    echo "------------ ${PATH_MAL} ---------------"
    python TAUautocor.py ${PATH_MAL}

    Rscript TDAvec_autocor.r ${PATH_MAL}

    python SVM_TDAvec_autocor_Raw_ts.py ${PATH_MAL}
    python SVM_TDAvec_autocor_Raw_pt.py ${PATH_MAL}



    PATH_MAL="${PATH_DATA}${dir}${image_method}/MAL5/"

    echo "------------ ${PATH_MAL} ---------------"
    python TAUautocor.py ${PATH_MAL}

    Rscript TDAvec_autocor.r ${PATH_MAL}

    python SVM_TDAvec_autocor_Raw_ts.py ${PATH_MAL}
    python SVM_TDAvec_autocor_Raw_pt.py ${PATH_MAL}



    PATH_MAL="${PATH_DATA}${dir}${image_method}/MAL10/"

    echo "------------ ${PATH_MAL} ---------------"
    python TAUautocor.py ${PATH_MAL}

    Rscript TDAvec_autocor.r ${PATH_MAL}

    python SVM_TDAvec_autocor_Raw_ts.py ${PATH_MAL}




  done

done
