#!/usr/bin/env python
# copy_exif_data_to_framegrabs.py v1 2023-03-15

"""copy_exif_data_to_framegrabs.py  last modified 2023-03-15

~/git/copy-exif-meta/copy_exif_data_to_framegrabs.py -f framegrabs/*.jpg -m *.MP4
"""

import sys
import argparse
import os

# commands will be printed in the format of:
#exiftool -TagsFromFile GX011548_seastar_then_blacktail_comber_w_bg_good.MP4 framegrabs/GX011548.MP4__00_00_152022-12-18-21h25m16s734.jpg

def main(argv, wayout):
	if not len(argv):
		argv.append('-h')
	parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, description=__doc__)
	parser.add_argument('-f','--framegrabs', nargs="*", help="framegrabs/*.jpg")
	parser.add_argument('-m','--movies', nargs="*", help="*.MP4")
	args = parser.parse_args(argv)

	gx_to_file = {} # key is first 8 letters, value is full filename of movie

	for moviefile in args.movies:
		# GX number is always first 8
		gxn = os.path.basename(moviefile)[0:8]
		gx_to_file[gxn] = moviefile

	print("#!/bin/bash", file=wayout)
	for framegrab in args.framegrabs:
		fgxn = os.path.basename(framegrab)[0:8]
		original_moviefile = gx_to_file.get(fgxn,None)
		if original_moviefile is None: # if None, then not in folder, so skip
			continue
		exifline = "exiftool -TagsFromFile {} {}".format( original_moviefile, framegrab )
		print(exifline, file=wayout)

if __name__ == "__main__":
	main(sys.argv[1:], sys.stdout)
