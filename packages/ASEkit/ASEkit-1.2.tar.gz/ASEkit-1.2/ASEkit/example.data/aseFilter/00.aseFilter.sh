#ASEkit Filter \
python3 /picb/humpopg-bigdata5/huangke/research/ASEtools/new/ASEkit/ASEkit/aseFilter.py Filter \
	--rawdir ./example.data/ \
   --totalreads 10 --fdr 0.05 --AIvalue 0.2 \
	--sample sample.info.txt \
    --outdir out

