import sys
import nilearn
from nilearn import plotting

if len(sys.argv) > 3:
    print("Plotting with background image..")
    plotting.plot_roi(sys.argv[1], bg_img=sys.argv[2], cmap='autumn', output_file=sys.argv[3])
else:
    plotting.plot_img(sys.argv[1], output_file=sys.argv[2])
