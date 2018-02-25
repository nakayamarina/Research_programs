PATH_DATA="../Data_state/analysis_by_programs/"

dir="20171020rn/"

for image_method in 12ch 32ch mb
do

  PATH_RAW="${PATH_DATA}${dir}${image_method}/RawData/"


  PATH_MAL="${PATH_DATA}${dir}${image_method}/MAL5/"



  echo "------------ ${PATH_RAW} ---------------"

  python 1dCNN_TDAvec_autocor_Raw_ts.py ${PATH_RAW}



  echo "------------ ${PATH_MAL} ---------------"

  python 1dCNN_TDAvec_autocor_Raw_ts.py ${PATH_MAL}




done
