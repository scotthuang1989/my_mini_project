import numpy as np
import cv2


class CoverMatcher(object):
    """
    class for matching features
    """
    def __init__(self, descriptor, cover_paths, ratio=0.7,
                 min_matches=40, use_hamming=True):
        self.descriptor = descriptor
        self.cover_paths = cover_paths
        self.ratio = ratio
        self.min_matches = min_matches
        self.distance_method = "BruteForce"

        if use_hamming:
            self.distance_method += "-Hamming"

    def search(self, queryKps, queryDescs):
        results = {}

        for cover_path in self.cover_paths:
            cover = cv2.imread(cover_path)
            gray = cv2.cvtColor(cover, cv2.COLOR_BGR2GRAY)
            (kps, descs) = self.descriptor.describe(gray)

            score = self.match(queryKps, queryDescs, kps, descs)
            results[cover_path] = score

        if len(results) > 0:
            results = sorted([(v, k) for (k, v) in results.items() if v > 0],
                             reverse=True)

        return results

    def match(self, kpsA, featuresA, kpsB, featuresB):
        matcher = cv2.DescriptorMatcher_create(self.distance_method)

        raw_matches = matcher.knnMatch(featuresB, featuresA, 2)
        matches = []

        for m in raw_matches:
            if len(m) == 2 and m[0].distance < m[1].distance * self.ratio:
                matches.append((m[0].trainIdx, m[0].queryIdx))

        if len(matches) > self.min_matches:
            ptsA = np.float32([kpsA[i] for (i, _) in matches])
            ptsB = np.float32([kpsB[j] for (_, j) in matches])
            (_, status) = cv2.findHomography(ptsA, ptsB, cv2.RANSAC, 4.0)

            return float(status.sum())/ status.size

        return -1.0
