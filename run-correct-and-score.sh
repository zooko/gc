#!/bin/sh

# closed class weights or pos weights

for POSWEIGHT in 0.1 0.25 0.5 0.75 ; do for ERRPROB in -1.7 -1.5 -1.3 ; do for WIDTH in 5 10 ; do for VOCSIZE in 5 10 20 ; do
    ( PATH=${PATH}:/home/ubuntu/BackOffTrigramModel/bin/:/home/ubuntu/srilm/bin/:/home/ubuntu/srilm/bin/i686-m64/ PYTHONPATH=/home/ubuntu/BackOffTrigramModel/src/Python/:/home/ubuntu/release2.3/m2scorer/scripts/ time /usr/bin/python /usr/bin/scons -f ../SConstruct data_directory="." seed=${SEED} vocabulary_size=${VOCSIZE} pos_weight=${POSWEIGHT} error_probability=${ERRPROB} width=${WIDTH} --debug=explain ) >> scons-seed${SEED}.stdout 2>> scons-seed${SEED}.stderr
done; done ; done ; done
