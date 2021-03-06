from __future__ import print_function, division
import numpy as np
import healpy as hp
import matplotlib
import random
from os.path import join, normpath, basename, isdir
from os import listdir, mkdir
import pandas
import gc

def see_mapper(catalog_dir, nside, out_map):
    # create empty map
    hmap = np.zeros(hp.nside2npix(nside))
    npix = hp.nside2npix(nside)
    pix_seeing = np.zeros(npix)
    pix_totalcounts = np.zeros(npix)
    
    for cat in listdir(catalog_dir):
        if cat.endswith(".csv") and cat.startswith("with"):
            # read catalog, cols [ra,dec,psffwhm_i]
            c = pandas.read_csv(join(catalog_dir, cat), sep=',', header=0, dtype={'ra' : np.float64, 'dec' : np.float64, "psffwhm_i" : np.float64}, engine=None, usecols=[1,2,292])
            ra = c["ra"]
            dec = c["dec"]
            seeing = c["psffwhm_i"]

            # generate object pixel_IDs & pixel_counts
            theta = np.deg2rad(90.0 - dec)
            phi = np.deg2rad(ra)
            pix_IDs = np.array(hp.ang2pix(nside, theta, phi, nest=False))
            pix_counts = np.bincount(pix_IDs, minlength=npix)
            assert len(pix_counts) == npix, ("pixel numbers mismatched")

            # calculate "total" seeing in each pixel
            for (i, pix) in enumerate(pix_IDs):
                pix_seeing[pix] += seeing[i]
                pix_totalcounts[pix] += 1

            del c, ra, dec, seeing, pix_counts, pix_IDs
            gc.collect()

    pix_avg_seeing = pix_seeing/pix_totalcounts

    # map seeing
    hp.write_map(out_map, pix_avg_seeing) # CHANGE FILENAMES????

if __name__ == "__main__":
    catalog_dir = "/share/data1/SDSS_DR12_Photometry"
    nside = 256
    out_map = "/share/splinter/ug_hj/M101/seeing_map256.fits"
    see_mapper(catalog_dir, nside, out_map)
