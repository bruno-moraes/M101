from __future__ import print_function, division
import numpy as np
import healpy as hp
import matplotlib
import random
from os.path import join, normpath, basename, isdir
from os import listdir, mkdir
import pandas
import gc

def mapper1(catalog_dir, nside, ra_col, dec_col, out_dir, sw=None, ew=None, weights=None):
    # create empty map
    hmap = np.zeros(hp.nside2npix(nside))
    npix = hp.nside2npix(nside)
    
    for cat in listdir(catalog_dir):
        if cat.endswith(".csv") and cat.startswith("with_header"):
            # read catalog
            c = pandas.read_csv(join(catalog_dir, cat), sep=',', header=0, dtype={ra_col : np.float64, dec_col : np.float64}, engine=None, usecols=[1,2,9,10,311])
            ra = c["ra"]
            dec = c["dec"]
            stripecuts = c["stripe"]
            cut1220 = stripecuts != 1220
            cut1188 = stripecuts != 1188
            cut1140 = stripecuts != 1140
            cut1100 = stripecuts != 1100
            cut1260 = stripecuts != 1260
            cut1300 = stripecuts != 1300
            cut1356 = stripecuts != 1356
            cut1374 = stripecuts != 1374
            cut1406 = stripecuts != 1406
            cut1458 = stripecuts != 1458
            cut1540 = stripecuts != 1540
            cut1600 = stripecuts != 1600
            cut1020 = stripecuts != 1020
            cut1062 = stripecuts != 1062

            cleancut = c["clean"] == True
            typecut = c["type"] == 3
            totalcut = cleancut & typecut & cut1220 & cut1188 & cut1140 & cut1100 & cut1260 & cut1300 & cut1356 & cut1374 & cut1406 & cut1458 & cut1540 & cut1600 & cut1020 & cut1062

            ra = ra[totalcut]
            dec = dec[totalcut]

            #print(str(cat) + ": table columns read") #see where errors are thrown

            # generate theta/phi vectors
            theta = np.deg2rad(90.0 - dec)
            phi = np.deg2rad(ra)
        
            # generate corresponding pixel_IDs
            pix_IDs = hp.ang2pix(nside, theta, phi, nest=False)
        
            # distribute galaxies according to pixel_ID, weights deal with potential systematics
            cmap = np.bincount(pix_IDs, weights=weights, minlength=npix)
            if weights is not None:
                assert len(weights) == len(pix_IDs), ("shape of weights must match shape of ra/dec data")
            assert len(cmap) == npix, ("pixel numbers mismatched")
        
            # sum to hmap
            hmap = cmap
        
            # assign filenames & write to file
            out_filename = "countmap_" + cat[:-4] + ".fits"
            hp.write_map(join(out_dir, out_filename), hmap)

            del c, ra, dec, cleancut, typecut, stripecuts, cut1220, cut1188, cut1140, cut1100, cut1260, cut1300, cut1356, cut1374, cut1406, cut1458, cut1540, cut1600, cut1020, cut1062
            gc.collect()

    return None

def main(catalog_dir, nside, ra_col, dec_col, out_dir, sw=None, ew=None, weights=None):
    
    # define map resolution, create map of zeros
    assert hp.isnsideok(nside), ("nside must be a power of 2")
    npix = hp.nside2npix(nside)
    hmap = np.zeros(npix)
    
    # create destination directory
    if not isdir(out_dir):
        mkdir(out_dir)
    else:
    	assert listdir(out_dir) == [], ("out_dir already exists/has content, choose a new destination directory")
    
    # create count maps
    mapper1(catalog_dir, nside, ra_col, dec_col, out_dir, sw, ew, weights)

    # merge count maps
    for cmap in listdir(out_dir):
        m = hp.read_map(join(out_dir, cmap))
        hmap += m

	# assign filename & write final map
    if not all(x == 0 for x in hmap):
        out_filename = basename(normpath(catalog_dir)) + "_" + str(nside) + "cmap.fits"
        hp.write_map(join(out_dir, out_filename), hmap)
    else:
        print("empty map")

    return None

if __name__ == "__main__":
    catalog_dir = "/share/data1/SDSS_DR12_Photometry"
    nside = 128
    ra_col = "ra"
    dec_col = "dec"
    out_dir = "/share/splinter/ug_hj/M101/128_SDSS_cuts3"
    sw = None
    ew = None
    weights = None
    main(catalog_dir, nside, ra_col, dec_col, out_dir, sw, ew, weights)