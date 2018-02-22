PATH_DATA="../Data_block/analysis_by_programs/"

DIRs=`ls -F ${PATH_DATA} | grep /`

for dir in $DIRs
do

  for image_method in 12ch 32ch mb
  do

    rm "${PATH_DATA}${dir}${image_method}/MAL5/ACCURACY[loo][[3, 5, 7].csv"
    rm "${PATH_DATA}${dir}${image_method}/MAL5/ACCURACY[loo][3, 5, 7].csv"
    rm "${PATH_DATA}${dir}${image_method}/MAL5/ACCURACY[loo][20]_Raw.csv"


  done

done
