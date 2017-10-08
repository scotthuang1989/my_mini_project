import numpy as np
import cv2


class CoverDescriptor(object):
    """
    class for creating descriptor from image
    """
    def __init__(self, use_sift=False):
        self.use_sift = use_sift

    def describe(self, image):
        if self.use_sift:
            descriptor = cv2.xfeatures2d.SIFT_create()
        else:
            descriptor = cv2.BRISK_create()
        kps, descs = descriptor.detectAndCompute(image, None)
        kps = np.float32([kp.pt for kp in kps])
        return (kps, descs)
