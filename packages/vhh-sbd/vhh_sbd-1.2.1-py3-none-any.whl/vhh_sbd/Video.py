import numpy as np
import cv2
import datetime
from vhh_sbd.utils import *
from PIL import Image


class Video(object):
    """
    This class represents on video and contains properties such as dimensions, length, format, video name ... .
    """

    def __init__(self):
        """
        Constructor.
        """
        #printCustom("create instance of video class ... ", STDOUT_TYPE.INFO);
        self.vidFile = ''
        self.vidName = ""
        self.frame_rate = 0
        self.channels = 0
        self.height = 0
        self.width = 0
        self.format = ''
        self.length = 0
        self.number_of_frames = 0
        self.vid = None
        self.convert_to_gray = False
        self.convert_to_hsv = False

    def load(self, vidFile: str):
        """
        This method is used to load a video of a specified storage.

        :param vidFile: This parameter must hold a valid video file path.
        """
        #printCustom("load video information ... ", STDOUT_TYPE.INFO);
        self.vidFile = vidFile
        if(self.vidFile == ""):
            printCustom("ERROR: you must add a video file path!", STDOUT_TYPE.ERROR)
            exit(1)
        self.vidName = self.vidFile.split('/')[-1]
        self.vid = cv2.VideoCapture(self.vidFile)

        if(self.vid.isOpened() == False):
            printCustom("ERROR: not able to open video file!", STDOUT_TYPE.ERROR)
            exit(1)

        status, frm = self.vid.read()

        self.channels = frm.shape[2]
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.frame_rate = self.vid.get(cv2.CAP_PROP_FPS)
        self.format = self.vid.get(cv2.CAP_PROP_FORMAT)
        self.number_of_frames = self.vid.get(cv2.CAP_PROP_FRAME_COUNT)

        self.vid.release()

    def printVIDInfo(self):
        """
        This method is used to print all video properties.
        """
        print("---------------------------------")
        print("Video information")
        print("filename: " + str(self.vidFile))
        print("format: " + str(self.format))
        print("fps: " + str(self.frame_rate))
        print("channels: " + str(self.channels))
        print("width: " + str(self.width))
        print("height: " + str(self.height))
        print("nFrames: " + str(self.number_of_frames))
        print("---------------------------------")

    def getFrame(self, frame_id: int) -> np.ndarray:
        """
        This method is used to return one frame specified with a given frame index.

        :param frame_id: This parameter must hold a valid integer frame index.
        :return: This method returns a numpy frame with a specified index (position).
        """
        self.vid.open(self.vidFile)
        if(frame_id >= self.number_of_frames):
            print("ERROR: frame idx out of range!")
            return []

        #print("Read frame with id: " + str(frame_id));
        time_stamp_start = datetime.datetime.now().timestamp()

        self.vid.set(cv2.CAP_PROP_POS_FRAMES, frame_id)
        status, frame_np = self.vid.read()
        self.vid.release()

        if(status == True):
            if(self.convert_to_gray == True):
                frame_np = cv2.cvtColor(frame_np, cv2.COLOR_BGR2GRAY)
                #print(frame_gray_np.shape);
            if (self.convert_to_hsv == True):
                frame_np = cv2.cvtColor(frame_np, cv2.COLOR_BGR2HSV);
                h, s, v = cv2.split(frame_np)

        time_stamp_end = datetime.datetime.now().timestamp()
        time_diff = time_stamp_end - time_stamp_start
        #print("time: " + str(round(time_diff, 4)) + " sec");

        return frame_np

    def getNumberOfBatches(self) -> int:
        batch_size = 64;
        nBatches = int(self.number_of_frames / batch_size) + 1
        return nBatches;

    def getFrameBatch(self, batch_id: int) -> np.ndarray:
        self.vid.open(self.vidFile);
        if(batch_id >= self.getNumberOfBatches()):
            print("ERROR: batch idx out of range!");
            return [];

        batch_np = []

        for j in range(0, 64):
            frm_id = batch_id * 64 + j;
            frame_np = self.getFrame(frm_id)
            if(len(frame_np) == 0):
                break;
            batch_np.append(frame_np)

        batch_np = np.array(batch_np)
        return batch_np;
      #data: np.ndarray, labels: np.ndarray) -> float:

import torch
from torch.utils import data

class VideoDataset(data.Dataset):

    def __init__(self, vidFile: str, transform=None):
        # printCustom("create instance of video class ... ", STDOUT_TYPE.INFO);
        self.vidFile = '';
        self.vidName = "";
        self.frame_rate = 0;
        self.channels = 0;
        self.height = 0;
        self.width = 0;
        self.format = '';
        self.length = 0;
        self.number_of_frames = 0;
        self.vid = None;
        self.convert_to_gray = False;
        self.convert_to_hsv = False;

        self.transform = transform;

        # printCustom("load video information ... ", STDOUT_TYPE.INFO);
        self.vidFile = vidFile;
        if (self.vidFile == ""):
            printCustom("ERROR: you must add a video file path!", STDOUT_TYPE.ERROR);
            exit(1);
        self.vidName = self.vidFile.split('/')[-1]
        self.vid = cv2.VideoCapture(self.vidFile);

        if (self.vid.isOpened() == False):
            printCustom("ERROR: not able to open video file!", STDOUT_TYPE.ERROR);
            exit(1);

        status, frm = self.vid.read();

        self.channels = frm.shape[2];
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT);
        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH);
        self.frame_rate = self.vid.get(cv2.CAP_PROP_FPS);
        self.format = self.vid.get(cv2.CAP_PROP_FORMAT);
        self.number_of_frames = self.vid.get(cv2.CAP_PROP_FRAME_COUNT);

        self.vid.release();

    def __len__(self):
        return int(self.number_of_frames)

    def __getitem__(self, frame_id: int):

        self.vid.open(self.vidFile);
        if(frame_id >= self.number_of_frames):
            print("ERROR: frame idx out of range!");
            return [];

        #print("Read frame with id: " + str(frame_id));
        time_stamp_start = datetime.datetime.now().timestamp();

        self.vid.set(cv2.CAP_PROP_POS_FRAMES, frame_id);
        status, frame_np = self.vid.read();
        self.vid.release();

        frame_np = Image.fromarray(frame_np.astype('uint8'))

        time_stamp_end = datetime.datetime.now().timestamp();
        time_diff = time_stamp_end - time_stamp_start;
        #print("time: " + str(round(time_diff, 4)) + " sec");

        if(self.transform != None):
            frame_np = self.transform(frame_np);

        return frame_np;