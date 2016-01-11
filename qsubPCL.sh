#!/bin/tcsh
#PBS -q compute
#PBS -N Cl.cmod
#PBS -l nodes=1:ppn=1
#PBS -l mem=50gb
#PBS -l walltime=120:00:00
#PBS -M zcaphjo@ucl.ac.uk

source /share/splinter/sbalan/Projects/LauraPCL/envvars.csh

cd $PBS_O_WORKDIR

Alm2Cl -I /share/splinter/ug_hj/M101/cmod256_map_alms.fits -O /share/splinter/ug_hj/M101/cmodVMBrBa_256_Cls.dat -P -m /share/splinter/ug_hj/M101/cmod_V_M_Br_Ba_mask256.fits -o -R /share/splinter/ug_hj/M101/cmodVMBrBa_IJs.dat -T /share/splinter/ug_hj/M101/cmod_cutmap256.fits -N 256 -L 513
