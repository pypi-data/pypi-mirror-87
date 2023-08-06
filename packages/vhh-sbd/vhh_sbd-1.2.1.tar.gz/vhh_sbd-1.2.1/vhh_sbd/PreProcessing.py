from vhh_sbd.utils import *
import cv2
import numpy as np
from vhh_sbd.Configuration import Configuration


class PreProcessing(object):
    """
    This class is used to pre-process frames.
    """

    def __init__(self, config_instance: Configuration):
        """
        Constructor

        :param config_instance: object instance of type Configuration
        """
        printCustom("create instance of preprocessing ... ", STDOUT_TYPE.INFO)
        self.config_instance = config_instance

    def applyTransformOnImg(self, image: np.ndarray) -> np.ndarray:
        """
        This method is used to apply the configured pre-processing methods on a numpy frame.

        :param image: This parameter must hold a valid numpy image (WxHxC).
        :return: This methods returns the preprocessed numpy image.
        """
        image_trans = image

        # convert to grayscale image
        if(int(self.config_instance.flag_convert2Gray) == 1):
            image_trans = self.convertRGB2Gray(image_trans)

        # crop image
        if (int(self.config_instance.flag_crop) == 1):
            image_trans = self.crop(image_trans, (image_trans.shape[0], image_trans.shape[0]))

        # resize image
        if(self.config_instance.flag_downscale == 1):
            dim = self.config_instance.resize_dim
            image_trans = self.resize(image_trans, dim)

        # apply histogram equalization
        if(self.config_instance.opt_histogram_equ == 'classic'):
            image_trans = self.classicHE(image_trans)
        elif(self.config_instance.opt_histogram_equ == 'clahe'):
            image_trans = self.claHE(image_trans)
        #elif(self.config_instance.opt_histogram_equ == 'none'):
        #    image_trans

        return image_trans

    def applyTransformOnImgSeq(self, img_seq: np.ndarray) -> np.ndarray:
        #printCustom("NOT IMPLEMENTED YET", STDOUT_TYPE.INFO);
        img_seq_trans_l = []
        for i in range(0, len(img_seq)):
            img_seq_trans_l.append(self.applyTransformOnImg(img_seq[i]))
        img_seq_trans = np.array(img_seq_trans_l)
        return img_seq_trans

    def convertRGB2Gray(self, img: np.ndarray):
        """
        This method is used to convert a RBG numpy image to a grayscale image.

        :param img: This parameter must hold a valid numpy image.
        :return: This method returns a grayscale image (WxHx1).
        """
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img_gray_3channels = cv2.cvtColor(img_gray, cv2.COLOR_GRAY2RGB)
        #img_gray = np.expand_dims(img_gray, axis=-1)
        return img_gray_3channels

    def crop(self, img: np.ndarray, dim: tuple):
        """
        This method is used to crop a specified region of interest from a given image.

        :param img: This parameter must hold a valid numpy image.
        :param dim: This parameter must hold a valid tuple including the crop dimensions.
        :return: This method returns the cropped image.
        """
        crop_w, crop_h = dim

        crop_h_1 = 0
        crop_h_2 = 0
        crop_w_1 = 0
        crop_w_2 = 0

        img_h = img.shape[0]
        img_w = img.shape[1]

        crop_w_1 = int(img_w / 2) - int(crop_w / 2)
        if (crop_w_1 < 0):
            crop_w_1 = 0

        crop_w_2 = int(img_w / 2) + int(crop_w / 2)
        if (crop_w_2 >= img_w):
            crop_w_2 = img_w

        crop_h_1 = int(img_h / 2) - int(crop_h / 2)
        if (crop_h_1 < 0):
            crop_h_1 = 0

        crop_h_2 = int(img_h / 2) + int(crop_h / 2)
        if (crop_h_2 >= img_h):
            crop_h_2 = img_h

        img_crop = img[crop_h_1:crop_h_2, crop_w_1:crop_w_2]
        return img_crop

    def resize(self, img: np.ndarray, dim: tuple):
        """
        This method is used to resize a image.

        :param img: This parameter must hold a valid numpy image.
        :param dim: This parameter must hold a valid tuple including the resize dimensions.
        :return: This method returns the resized image.
        """
        img_resized = cv2.resize(img, dim)
        return img_resized

    def classicHE(self, img: np.ndarray):
        """
        This method is used to calculate the classic histogram equalization.

        :param img: This parameter must hold a valid numpy image.
        :return: This method returns the pre-processed image.
        """
        # classic histogram equalization
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img_che = cv2.equalizeHist(gray)
        img_che = cv2.cvtColor(img_che, cv2.COLOR_GRAY2RGB)
        return img_che

    def claHE(self, img: np.ndarray):
        """
        This method is used to calculate the Contrast Limited Adaptive Histogram Equalization.

        :param img: This parameter must hold a valid numpy image.
        :return: This method returns the pre-processed image.
        """
        # contrast Limited Adaptive Histogram Equalization
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        clahe = cv2.createCLAHE()
        img_clahe = clahe.apply(gray)
        img_clahe = cv2.cvtColor(img_clahe, cv2.COLOR_GRAY2RGB)
        return img_clahe

