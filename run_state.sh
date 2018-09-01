PATH_DATA="../Data_state/analysis_by_programs/"

DIRs=`ls -F ${PATH_DATA} | grep /`

dir="20171020rn/"

for image_method in 12ch 32ch mb
do

  PATH_MAL3="${PATH_DATA}${dir}${image_method}/MAL3/"

  echo "------------ ${PATH_MAL3} ---------------"

  python SVM_TDAvec_autocor_Raw_pt.py ${PATH_MAL3}
  python SVM_TDAvec_autocor_Raw_ts.py ${PATH_MAL3}


  PATH_MAL7="${PATH_DATA}${dir}${image_method}/MAL7/"

  echo "------------ ${PATH_MAL7} ---------------"

  python SVM_TDAvec_autocor_Raw_pt.py ${PATH_MAL7}
  python SVM_TDAvec_autocor_Raw_ts.py ${PATH_MAL7}



  echo "------------ ${PATH_MAL3} ---------------"

  python 1dCNN_TDAvec_autocor_Raw_ts.py ${PATH_MAL3}

  PATH_MAL7="${PATH_DATA}${dir}${image_method}/MAL7/"

  echo "------------ ${PATH_MAL} ---------------"

  python 1dCNN_TDAvec_autocor_Raw_ts.py ${PATH_MAL7}

done
