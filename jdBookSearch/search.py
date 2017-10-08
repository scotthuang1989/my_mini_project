from __future__ import print_function
from searchEngine.coverdescriptor import CoverDescriptor
from searchEngine.covermatcher import CoverMatcher
import argparse
import glob
import csv
import cv2
import os
import pandas as pd

ap = argparse.ArgumentParser()
ap.add_argument("-d", "--db", required = True,
                help = "path to the book database")
ap.add_argument("-c", "--covers", required = True,
                help = "path to the directory that contains our book covers")
ap.add_argument("-q", "--query", required = True,
                help = "path to t  he query book cover")
ap.add_argument("-s", "--sift", type = int, default = 1,
                help = "whether or not SIFT should be used")
args = vars(ap.parse_args())

db = {}

# create book name to cover file mapping.
# key is full path of cover image, value is book name
# for line in csv.reader(open(args["db"])):
#     db[line[2]] =line[0]
book_info_df = pd.read_csv("jdBookData/jdbookexporter.csv")
for index in book_info_df.index:
    db[book_info_df.loc[index,"image_location"]] = book_info_df.loc[index,"book_name"]

use_sift = args['sift'] > 0
use_hamming = args['sift'] == 0
ratio = 0.7
min_matches = 40

if use_sift:
    min_matches = 50

cover_descriptor = CoverDescriptor(use_sift=use_sift)
cover_matcher = CoverMatcher(cover_descriptor, glob.glob(args['covers'] + "/*.jpg"),
                             ratio=ratio, min_matches=min_matches,
                             use_hamming=use_hamming)
query_image = cv2.imread(args["query"])
gray = cv2.cvtColor(query_image, cv2.COLOR_BGR2GRAY)
queryKps, queryDescs = cover_descriptor.describe(gray)

results = cover_matcher.search(queryKps, queryDescs)
cv2.imshow("Query", query_image)

if len(results) == 0:
    print("I could not find a match for that cover!")
    cv2.waitKey(0)
else:
    for (i, (score, cover_path)) in enumerate(results):
        image_base_name = os.path.basename(cover_path)
        for (k, v) in db.items():
            if image_base_name in k:
                print("The book name is: {}(with score: {})".format(v, score))
                break
