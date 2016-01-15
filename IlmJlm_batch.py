from __future__ import print_function, division
import numpy as np
import healpy as hp
import matplotlib
import random
from os.path import join, normpath, basename, isdir
import os
import pandas
import gc

def main(nside, jobname, queue, l_max, bin_size, mask_fits, outfile_dir):
	multipole1 = np.arange(start=0, stop=l_max, step=bin_size)
	multipole2 = np.arange(start=bin_size, stop=(l_max + bin_size), step=bin_size)
	if not isdir(join(outfile_dir, "IJs")):
		os.mkdir(join(outfile_dir, "IJs"))
	for (i, l) in  enumerate(multipole1):
		shell_script = ["#!/bin/tcsh",
					"#PBS -q " + str(queue),
					"#PBS -N " + str(jobname),
					"#PBS -l nodes=1:ppn=1",
					"#PBS -l mem=50gb",
					"#PBS -l walltime=120:00:00",
					"",
					"source /share/splinter/sbalan/Projects/LauraPCL/envvars.csh",
					"", 
					"cd $PBS_O_WORKDIR",
					""]
		if l != 0:									
			shell_script.append("IlmJlm -m " + str(mask_fits) + " -O " + str(outfile_dir) + "IJs/IlmJlm_" + str(i).zfill(2) + ".dat -N " + str(nside) + " -l " + str(l) + " -L " + str(multipole2[i]))
		else:
			shell_script.append("IlmJlm -m " + str(mask_fits) + " -O " + str(outfile_dir) + "IJs/IlmJlm_" + str(i).zfill(2) + ".dat -N " + str(nside) + " -L " + str(multipole2[i]))

		shell_script.append("")

		F = str(outfile_dir) + str(l).zfill(3) + "-" + str(multipole2[i]).zfill(3) + ".sh"
		A = open(F, "w")
		T = "\n".join(shell_script)
		A.write(str(T))
		A.close()

		# os.system("qsub " + F)
		# os.system("sleep 1")

if __name__ == "__main__":
	nside = 512
	jobname = "PCL"
	queue = "compute"
	l_max = 1020
	bin_size = 10
	mask_fits = "/share/splinter/ug_hj/M101/Ebv0.4See1.55Air1.4VM200BrBa_512mask.fits"
	outfile_dir = "/share/splinter/ug_hj/M101/PCL/ebv_plus/" # check for ////
	main(nside, jobname, queue, l_max, bin_size, mask_fits, outfile_dir)
