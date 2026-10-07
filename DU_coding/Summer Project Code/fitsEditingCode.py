import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits  # We use fits to open the actual data file




all_data, all_headers = fits.getdata("Mosaic.fits",header=True)
starMask_data = all_data[414:419,592:602]
starMask_data = np.copy(all_data)

for i in range(len(starMask_data)):
    for j in range(len(starMask_data[0])):
        starMask_data[i,j] = 0
        if i >= 414 and i <= 419 and j >= 592 and j <= 602:
            starMask_data[i,j] = all_data[i,j]
        elif j >= 477 and j <= 504 and i >= 281 and i <= 303:
            starMask_data[i,j] = all_data[i,j]
        elif j >= 499 and j <= 518 and i >= 207 and i <= 224:
                starMask_data[i,j] = all_data[i,j]
        elif j >= 600 and j <= 612 and i >= 227 and i <= 239:
                starMask_data[i,j] = all_data[i,j]
        elif j >= 447 and j <= 457 and i >= 458 and i <= 468:
                starMask_data[i,j] = all_data[i,j]
        elif j >= 825 and j <= 846 and i >= 525 and i <= 545:
                starMask_data[i,j] = all_data[i,j]
        elif j >= 769 and j <= 781 and i >= 406 and i <= 416:
                starMask_data[i,j] = all_data[i,j]
        elif j >= 880 and j <= 898 and i >= 256 and i <= 272:
                starMask_data[i,j] = all_data[i,j]
        elif j >= 953 and j <= 968 and i >= 331 and i <= 342:
                starMask_data[i,j] = all_data[i,j]
        elif j >= 224 and j <= 238 and i >= 663 and i <= 675:
                starMask_data[i,j] = all_data[i,j]
        elif j >= 152 and j <= 171 and i >= 638 and i <= 654:
                starMask_data[i,j] = all_data[i,j]
        elif j >= 133 and j <= 143 and i >= 689 and i <= 698:
                starMask_data[i,j] = all_data[i,j]
        elif j >= 170 and j <= 183 and i >= 736 and i <= 747:
                starMask_data[i,j] = all_data[i,j]
        elif j >= 167 and j <= 184 and i >= 795 and i <= 811:
                starMask_data[i,j] = all_data[i,j]
fits.writeto("B_19_02_09_starMask.fits",starMask_data, overwrite=True)

#header["NCOMBINE"] = 8
#psf_data = all_data[254:274,878:898] #put y then x values
#fits.writeto("B_19_02_09_PSF.fits",psf_data,overwrite=True)
#fits.writeto("B_19_02_09_galfit.fits", data, header, overwrite=True)p