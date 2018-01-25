#!/bin/bash

set -xe

LASTDIR=$(ls -td generated/*/ | head -1)
cd $LASTDIR

source=graph.dot

filename="${source%%.*}"
target=$filename.without_alones.dot
gvpr -c "N[$.degree==0]{delete(root, $)}" ${source} > ${target}
dot $target -Tpdf -o dot_$filename.pdf
#sfdp -x -Goverlap=scale $target -Tpdf -o sfdp_scaled_$filename.pdf
#circo $target -Tpdf -o circo_$filename.pdf
twopi $target -Tpdf -o twopi_$filename.pdf
#fdp $target -Tpdf -o fdp_$filename.pdf

python ../plotLog.py log.txt
python ../plot_graph_stats.py ${target}
python ../pyveplot_hiveplot.py ${target} 0 3
for i in {3..50}
do
    python ../pyveplot_hiveplot.py ${target} 1 ${i}
done

for f in *.svg
do
    convert ${f} ${f}.png
done
