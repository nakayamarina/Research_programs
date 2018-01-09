PATH_DATA="../Data_block/"

DIRs=`ls -F ${PATH_DATA} | grep /`

for dir in $DIRs
do

  for image_method in 12ch 32ch mb
  do

    PATH_RAW="${PATH_DATA}${dir}${image_method}/RawData/"

    echo "------------ ${PATH_RAW} ---------------"
    python SVM_TDAvec_autocor.py ${PATH_RAW}

    PATH_MAL="${PATH_DATA}${dir}${image_method}/MAL5/"

    echo "------------ ${PATH_MAL} ---------------"
    python SVM_TDAvec_autocor.py ${PATH_MAL}

  done

done
