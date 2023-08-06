from vhh_sbd.utils import *
import yaml


class Configuration(object):
    """
    This class is needed to read the configuration parameters specified in the configuration.yaml file.
    The instance of the class is holding all parameters during runtime.

    .. note::
       e.g. ./config/config_vhh_test.yaml

        the yaml file is separated in multiple sections
        config['Development']
        config['PreProcessing']
        config['SbdCore']
        config['Evaluation']

        whereas each section should hold related and meaningful parameters.
    """

    def __init__(self, config_file: str):
        """
        Constructor

        :param config_file: [required] path to configuration file (e.g. PATH_TO/config.yaml)
                                       must be with extension ".yaml"
        """
        printCustom("create instance of configuration ... ", STDOUT_TYPE.INFO)

        self.config_file = config_file

        self.debug_flag = -1
        self.use_gpu = False

        self.resize_dim = None
        self.flag_convert2Gray = -1
        self.flag_crop = -1
        self.flag_downscale = -1
        self.opt_histogram_equ = None

        self.activate_candidate_selection = -1

        self.save_raw_results = -1
        self.path_postfix_raw_results = None
        self.path_prefix_raw_results = None
        self.path_raw_results = None

        self.save_final_results = -1
        self.path_prefix_final_results = None
        self.path_postfix_final_results = None
        self.path_final_results = None

        self.path_videos = None
        self.threshold = 0.0
        self.alpha = 0.0
        self.beta = 0.0
        self.threshold_mode = None
        self.window_size = None
        self.backbone_cnn = None
        self.similarity_metric = None

        self.pretrained_model = None

        self.path_eval_results = None
        self.path_raw_results_eval = None
        self.save_eval_results = -1
        self.path_gt_data = None

    def loadConfig(self):
        """
        Method to load configurables from the specified configuration file
        """

        fp = open(self.config_file, 'r')
        config = yaml.load(fp, Loader=yaml.BaseLoader)

        developer_config = config['Development']
        pre_processing_config = config['PreProcessing']
        sbd_core_config = config['SbdCore']
        candidate_selection_config = config['CandidateSelection']
        evaluation_config = config['Evaluation']

        # developer_config section
        self.debug_flag = int(developer_config['DEBUG_FLAG'])

        if int(developer_config['USE_GPU']) == 1:
            self.use_gpu = True

        # pre-processing section
        self.resize_dim = (int(pre_processing_config['RESIZE_DIM'].split(',')[0]),
                           int(pre_processing_config['RESIZE_DIM'].split(',')[1]))
        self.flag_convert2Gray = int(pre_processing_config['CONVERT2GRAY'])
        self.flag_crop = int(pre_processing_config['CROP'])
        self.flag_downscale = int(pre_processing_config['DOWNSCALE'])
        self.opt_histogram_equ = pre_processing_config['HISTOGRAM_EQU']

        # sbd_core_config section
        self.activate_candidate_selection = int(sbd_core_config['CANDIDATE_SELECTION'])
        self.save_raw_results = int(sbd_core_config['SAVE_RAW_RESULTS'])
        self.path_postfix_raw_results = sbd_core_config['POSTFIX_RAW_RESULTS']
        self.path_prefix_raw_results = sbd_core_config['PREFIX_RAW_RESULTS']
        self.path_raw_results = sbd_core_config['PATH_RAW_RESULTS']

        self.save_final_results = int(sbd_core_config['SAVE_FINAL_RESULTS'])
        self.path_prefix_final_results = sbd_core_config['PREFIX_FINAL_RESULTS']
        self.path_postfix_final_results = sbd_core_config['POSTFIX_FINAL_RESULTS']
        self.path_final_results = sbd_core_config['PATH_FINAL_RESULTS']

        self.path_videos = sbd_core_config['PATH_VIDEOS']
        self.threshold_mode = sbd_core_config['THRESHOLD_MODE']
        self.window_size = int(sbd_core_config['WINDOW_SIZE'])
        self.threshold = float(sbd_core_config['THRESHOLD'])
        self.alpha = float(sbd_core_config['ALPHA'])
        self.beta = float(sbd_core_config['BETA'])
        self.backbone_cnn = sbd_core_config['BACKBONE_CNN']
        self.similarity_metric = sbd_core_config['SIMILARITY_METRIC']

        # candidate_selection_config
        self.pretrained_model = candidate_selection_config['PATH_PRETRAINED_MODEL']

        # evaluation section
        self.path_raw_results_eval = evaluation_config['PATH_RAW_RESULTS']
        self.path_eval_results = evaluation_config['PATH_EVAL_RESULTS']
        self.save_eval_results = int(evaluation_config['SAVE_EVAL_RESULTS'])
        self.path_gt_data = evaluation_config['PATH_GT_ANNOTATIONS']
