#!/bin/sh


set -e


PYTHONPATH=${PYTHONPATH}:${PWD}/release2.3/m2scorer/scripts
export PYTHONPATH


echo "Hello in here PYTHON is " $PYTHON

# echo "Hello in there, SEED is " $SEED
echo "Hello in there, WIDTH is " $WIDTH
# echo "Hello in there, POSWEIGHT is " $POSWEIGHT


# export SEED
export WIDTH
# export POSWEIGHT

TS=`date +"%F_%T%:::z"`
echo TS is ${TS}
DNAME=tagtests-${TS}
mkdir ${DNAME}
cd ${DNAME}
cp ../run-em-all.sh .

# for SEED in 1 2 3 4 5 6 7 ; do
for SEED in 5 ; do
# for CCWEIGHT in 0.25 0.5 0.75 ; do 
for CCWEIGHT in 0.25 ; do 
# for ERRPROB in -1.1 -1.3 -1.9 ; do 
for ERRPROB in -1.1 ; do 
    cd archive
    NAME=voc5_wid${WIDTH}_ccweight${CCWEIGHT}_seed${SEED}_errprob${ERRPROB}_python`basename ${PYTHON}`
    mkdir "${NAME}"
    cd "${NAME}"
    ln -snf ../../newer-inputs/* .
    cp ../../run-em-all.sh .
    time $PYTHON /usr/bin/scons -f ../../SConstruct data_directory="." vocabulary_size=5 width=${WIDTH} closed_class_weight=${CCWEIGHT} seed="${SEED}" error_probability="${ERRPROB}" > scons-run-log.txt 2> scons-run-stderr.txt
    cd ../..
done
done
done
