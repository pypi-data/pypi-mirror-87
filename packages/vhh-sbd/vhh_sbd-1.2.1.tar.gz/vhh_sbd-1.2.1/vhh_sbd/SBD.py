from vhh_sbd.Video import Video, VideoDataset
from vhh_sbd.utils import *
from vhh_sbd.Configuration import Configuration
from vhh_sbd.Shot import Shot
from vhh_sbd.PreProcessing import PreProcessing
from vhh_sbd.Model import *
from matplotlib import pyplot as plt
from scipy.spatial import distance
from vhh_sbd.DeepSBD import CandidateSelection
import os
import cv2


class SBD(object):
    """
    Main class of shot boundary detection (sbd) package.
    """

    def __init__(self, config_file: str):
        """
        Constructor

        :param config_file: [required] path to configuration file (e.g. PATH_TO/config.yaml)
                                       must be with extension ".yaml"
        """
        #printCustom("INFO: create instance of sbd ... ", STDOUT_TYPE.INFO);

        if (config_file == ""):
            printCustom("No configuration file specified!", STDOUT_TYPE.ERROR)
            exit()

        self.config_instance = Configuration(config_file)
        self.config_instance.loadConfig()

        self.vid_instance = None
        self.pre_proc_instance = PreProcessing(self.config_instance)
        self.candidate_selection_instance = CandidateSelection(self.config_instance)
        self.net = None

        self.src_path = ""
        self.filename_l = ""

    def runOnSingleVideo(self, video_filename, max_recall_id=-1):
        """
        Method to run sbd on specified video.

        :param video_filename: This parameter must hold a valid video file path.
        :param max_recall_id: [required] integer value holding unique video id from VHH MMSI system
        """

        shot_boundaries_l = []
        self.src_path = self.config_instance.path_videos

        vid_name = video_filename.split('/')[-1]

        printCustom("--------------------------", STDOUT_TYPE.INFO)
        printCustom("Process video: " + str(vid_name) + " ... ", STDOUT_TYPE.INFO)

        # load video
        self.vid_instance = Video()
        self.vid_instance.load(video_filename)

        shot_boundaries_np = None
        if (self.config_instance.activate_candidate_selection == 1):
            # candidate selection
            printCustom("Process candidate selection: " + str(vid_name) + " ... ", STDOUT_TYPE.INFO)
            candidate_selection_result_np = self.candidate_selection_instance.run(video_filename)

            # shot boundary detection
            printCustom("Process shot boundary detection: " + str(vid_name) + " ... ", STDOUT_TYPE.INFO)
            shots_np = self.runWithCandidateSelection(candidate_selection_result_np)
            shot_boundaries_l.append(shots_np)
            shot_boundaries_np = np.squeeze(np.array(shot_boundaries_l))

        elif (self.config_instance.activate_candidate_selection == 0):
            # shot boundary detection
            printCustom("Process shot boundary detection: " + str(vid_name) + " ... ", STDOUT_TYPE.INFO)
            shot_boundaries_np = self.runWithoutCandidateSelection(self.src_path, vid_name)


        # convert shot boundaries to final shots
        final_shot_l = self.convertShotBoundaries2Shots(shot_boundaries_np)

        # export final results
        if (self.config_instance.save_final_results == 1):
            self.exportFinalResultsToCsv(final_shot_l, str(max_recall_id))

        return final_shot_l

    def runWithoutCandidateSelection(self, src_path, vid_name):
        """
        This method is used to run sbd without candidate selection mode.

        :param src_path: THis parameter must hold a valid path to the video file.
        :param vid_name: This parameter must hold a valid videofile name.
        :return: This method returns a numpy list with all detected shots in a video.
        """
        #printCustom("process shot detection ... ", STDOUT_TYPE.INFO);

        # load video
        trans = transforms.Compose([transforms.CenterCrop(self.config_instance.resize_dim[0]),
                                    transforms.ToTensor()
                                    ])
        self.vid_instance = VideoDataset(src_path + "/" + vid_name, transform=trans)

        # initial pre-trained model
        self.net = PyTorchModel(model_arch=self.config_instance.backbone_cnn, use_gpu=self.config_instance.use_gpu)

        results_l = []
        cnt = 0

        cap = cv2.VideoCapture(src_path + "/" + vid_name)
        cnt = cnt + 1
        ret, frame_prev = cap.read()
        if (ret == True):
            frame_prev = self.pre_proc_instance.applyTransformOnImg(frame_prev)

        number_of_frames = int(self.vid_instance.number_of_frames)

        while(ret == True):
            cnt = cnt + 1
            ret, frame_curr = cap.read()
            #print(cnt)
            #print(ret)
            #print(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            if (ret == True):
                frame_curr = self.pre_proc_instance.applyTransformOnImg(frame_curr)

                if (self.config_instance.debug_flag == 1):
                    if(cnt <= 500):
                        cv2.imwrite(self.config_instance.path_eval_results + vid_name + "_" + str(cnt) + ".png", frame_curr)

                feature_prev = self.net.getFeatures(frame_prev)
                feature_curr = self.net.getFeatures(frame_curr)
                result = self.calculateDistance(feature_prev, feature_curr)
                results_l.append(result)

                frame_prev = frame_curr
            else:
                break

        distances_np = np.array(results_l)

        # calculate thresholds
        shot_l = []
        if (self.config_instance.threshold_mode == 'adaptive'):
            window_size = self.config_instance.window_size
            alpha = self.config_instance.alpha
            beta = self.config_instance.beta

            thresholds = []
            for x in range(0, len(distances_np)):
                if(x % window_size == 0):
                    if (x % window_size == 0):
                            th = np.mean(distances_np[x:x + window_size]) + alpha + np.std(distances_np[x:x + window_size]) * beta
                thresholds.append(th)
            thresholds = np.array(thresholds)

            for i in range(0, len(distances_np)):
                #print("####################")
                #print(i)
                #print("th: " + str(thresholds[i]))
                #print("dist: " + str(distances_np[i]))
                if (distances_np[i] > thresholds[i]):
                    idx_curr = i + 1
                    idx_prev = i
                    print("cut at: " + str(i) + " -> " + str(i+1))
                    printCustom("Abrupt Cut detected: " + str(idx_prev) + ", " + str(idx_curr), STDOUT_TYPE.INFO)
                    shot_l.append([self.vid_instance.vidName, (idx_prev, idx_curr)])
                    
        elif (self.config_instance.threshold_mode == 'fixed'):
            for i in range(0, len(distances_np)):
                if (distances_np[i] > self.config_instance.threshold):
                    idx_curr = i + 1
                    idx_prev = i

                    # print("cut at: " + str(i) + " -> " + str(i+1))
                    # print(i)
                    # print(thresholds[i])
                    # print(distances_np[i])
                    printCustom("Abrupt Cut detected: " + str(idx_prev) + ", " + str(idx_curr), STDOUT_TYPE.INFO)
                    shot_l.append([self.vid_instance.vidName, (idx_prev, idx_curr)])

        # save raw results to file
        if (int(self.config_instance.save_raw_results) == 1):
            print("save raw results ... ")
            raw_results_l = []
            raw_results_l.append([1, number_of_frames, results_l])
            results_np = np.array(raw_results_l)
            if (self.config_instance.path_postfix_raw_results == 'csv'):
                self.exportRawResultsAsCsv_New(results_np)
            elif (self.config_instance.path_postfix_raw_results == 'npy'):
                self.exportRawResultsAsNumpy(results_np)

        if (len(shot_l) == 0):
            print("no cuts detected ... ")
            shot_l.append([self.vid_instance.vidName, (-1, -1)])

        # convert shot boundaries to shots
        shots_np = np.array(shot_l)

        return shots_np

    def runWithCandidateSelection(self, candidates_np):
        """
        This method is used to run sbd with candidate selection mode.

        :param candidates_np: THis parameter must hold a valid numpy list including all pre-selected candidates.
        :return: This method returns a numpy list with all detected shots in a video.
        """
        #printCustom("process shot detection ... ", STDOUT_TYPE.INFO);

        # initial pre-trained model
        self.net = PyTorchModel(model_arch=self.config_instance.backbone_cnn, use_gpu=self.config_instance.use_gpu)

        results_l = []
        shot_l = []
        for i in range(0, len(candidates_np)):
            start = candidates_np[i][0]
            end = candidates_np[i][1] - 1

            #print(start)
            #print(end)
            results_per_range = []
            for j in range(start+1, end):
                # print("-------------------")
                # print("process " + str(i))
                idx_curr = j
                idx_prev = j - 1

                frm_prev = self.vid_instance.getFrame(idx_prev)
                frm_curr = self.vid_instance.getFrame(idx_curr)

                if(len(frm_prev) == 0 or len(frm_curr) == 0):
                    break
                #print(idx_prev)
                #print(idx_curr)
                #print(frm_prev.shape)
                #print(frm_curr.shape)

                frm_trans_prev = self.pre_proc_instance.applyTransformOnImg(frm_prev)
                frm_trans_curr = self.pre_proc_instance.applyTransformOnImg(frm_curr)

                # print("process core part ... ")
                feature_prev = self.net.getFeatures(frm_trans_prev)
                feature_curr = self.net.getFeatures(frm_trans_curr)
                result = self.calculateDistance(feature_prev, feature_curr)

                if (int(self.config_instance.save_raw_results) == 1):
                    results_per_range.append(result)

                if(result >= self.config_instance.threshold):
                    printCustom("Abrupt Cut detected: " + str(idx_prev) + ", " + str(idx_curr), STDOUT_TYPE.INFO)
                    shot_l.append([self.vid_instance.vidName, (idx_prev, idx_curr)])

            if (int(self.config_instance.save_raw_results) == 1):
                results_l.append([start, end, results_per_range])

        # save raw results to file
        if (int(self.config_instance.save_raw_results) == 1):
            print("save raw results ... ")
            results_np = np.array(results_l)
            self.exportRawResultsAsCsv_New(results_np)

        # convert shot boundaries to shots
        shots_np = np.array(shot_l)

        return shots_np

    def exportFinalResultsToCsv(self, shot_l: list, name: str):
        """
        This method is used to export the final results to a csv file (semicolon seperated).
        :param shot_l: This parameter must hold a valid array list including the final results list.
        :param name: This parameter represents the name of the csv list.
        """
        printCustom("Export shot list to csv file ... ", STDOUT_TYPE.INFO)

        fp = open(self.config_instance.path_final_results + "/" + str(name) + ".csv", 'w')   # final_shots_"
        fp.write("vid_name;shot_id;start;end" + "\n")
        for shot in shot_l:
            tmp_str = shot.convert2String()
            fp.write(tmp_str + "\n")
        fp.close()

    def exportShotBoundariesResultsToCsv(self, shot_boundaries_np: np.ndarray, name: str):
        """
        This method is used to export the final results to a csv file (semicolon seperated).
        :param shot_l: This parameter must hold a valid array list including the final results list.
        :param name: This parameter represents the name of the csv list.
        """
        printCustom("Export shot list to csv file ... ", STDOUT_TYPE.INFO)

        fp = open("/data/share/maxrecall_vhh_mmsi/develop/videos/results/sbd/" + "/" + str(name) + "_sbd.csv", 'w')  # final_shots_"
        fp.write("shot_id;vid_name;start;end" + "\n")
        for i in range(0, len(shot_boundaries_np)):
            video_name = shot_boundaries_np[i][0]
            start, end = shot_boundaries_np[i][1]
            tmp_str = str(video_name) + ";" + str(start) + ";" + str(end)
            fp.write(tmp_str + "\n")
        fp.close()

    def exportRawResultsAsNumpy(self, results_np: np.ndarray):
        """
        This method is used to export the raw results to a numpy file.

        :param results_np: This parameter must hold a valid numpy list including the raw results.
        """
        np.save(self.config_instance.path_raw_results +
                  self.config_instance.path_prefix_raw_results +
                  str(self.vid_instance.vidName.split('.')[0]) + "." +
                  self.config_instance.path_postfix_raw_results,
                results_np)

    def exportRawResultsAsCsv_New(self, results_np: np.ndarray):
        """
        This method is used to export the raw results to a csv file.

        :param results_np: This parameter must hold a valid numpy list including the raw results.
        """
        # save raw results to file
        fp = open(self.config_instance.path_raw_results +
                  self.config_instance.path_prefix_raw_results +
                  str(self.vid_instance.vidName.split('.')[0]) + "." +
                  self.config_instance.path_postfix_raw_results, mode='w')

        for i in range(0, len(results_np)):
            start, end, distances_l = results_np[i]
            tmp_str = str(start) + ";" + str(end)
            for j in range(0, len(distances_l)):
                tmp_str = tmp_str + ";" + str(distances_l[j])
            fp.write(self.vid_instance.vidName.split('.')[0] + ";" + str(tmp_str) + "\n")
            # csv_writer.writerow(row);
        fp.close()

    def calculateDistance(self, x, y):
        """
        This method is used to calculate the distance between 2 feature vectors.

        :param x: This parameter represents a feature vector (one-dimensional)
        :param y: This parameter represents a feature vector (one-dimensional)
        :return: This method returns the similarity score of a specified distance metric.
        """
        dst = 0

        # initial pre-trained model
        if (self.config_instance.similarity_metric == "cosine"):
            dst = distance.cosine(x, y)
        elif (self.config_instance.similarity_metric == "euclidean"):
            dst = distance.euclidean(x, y)
        else:
            dst = None
            printCustom("No valid similarity metric selected!", STDOUT_TYPE.ERROR)
            exit()

        return dst

    def convertShotBoundaries2Shots(self, shot_boundaries_np: np.ndarray):
        """
        This method converts a list with detected shot boundaries to the final shots.

        :param shot_boundaries_np: This parameter must hold a numpy array with all detected shot boundaries.
        :return: This method returns a numpy list with the final shots.
        """
        # convert results to shot instances

        shot_l = []

        vidname_curr = shot_boundaries_np[0][0]
        start_curr, stop_curr = shot_boundaries_np[0][1]

        print("shot boundaries list: ")
        print(shot_boundaries_np)

        if (start_curr == -1 and stop_curr == -1):
            print("no shots detected ... ")
            shot = Shot(len(shot_boundaries_np), vidname_curr, 0, int(self.vid_instance.number_of_frames) - 1)
            shot_l.append(shot)
            return shot_l

        shot_start = 0
        shot_end = start_curr
        shot = Shot(1, vidname_curr, shot_start, shot_end)
        shot_l.append(shot)

        for i in range(1, len(shot_boundaries_np)):
            #print(i)
            start_prev, stop_prev = shot_boundaries_np[i-1][1]
            start_curr, stop_curr = shot_boundaries_np[i][1]
            vidname_curr = shot_boundaries_np[i][0]

            shot_start = int(stop_prev)
            shot_end = int(start_curr)
            shot = Shot(i + 1, vidname_curr, shot_start, shot_end)
            shot_l.append(shot)

        vidname_curr = shot_boundaries_np[-1][0]
        start_curr, stop_curr = shot_boundaries_np[-1][1]
        shot_start = int(stop_curr)
        shot_end = int(self.vid_instance.number_of_frames) - 1
        shot = Shot(len(shot_boundaries_np) + 1, vidname_curr, shot_start, shot_end)
        shot_l.append(shot)

        if(self.config_instance.debug_flag == 1):
            # print shot infos
            for i in range(0, len(shot_l)):
                shot_l[i].printShotInfo()

        return shot_l
