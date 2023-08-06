from vhh_sbd.utils import *
import numpy as np
import torch
from torchvision import models, transforms
from torch.autograd import Variable
from PIL import Image


class PyTorchModel(object):
    """
    This class is needed to create a specified cnn model architecture and extract the the features.
    """

    def __init__(self, model_arch, use_gpu: bool=False):
        """
        Constructor.
        :param model_arch: This parameter must hold a string containing a valid model architecture name.
        """
        printCustom("create instance of PyTorchModel ... ", STDOUT_TYPE.INFO)
        self.model_arch = model_arch
        if(self.model_arch == "squeezenet"):
            self.model = models.squeezenet1_0(pretrained=True)
        elif (self.model_arch == "vgg16"):
            self.model = models.vgg16(pretrained=True)
        else:
            self.model_arch = None
            printCustom("No valid backbone cnn network selected!", STDOUT_TYPE.ERROR)
            exit()

        self.normalize = transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])

        self.use_gpu = use_gpu and torch.cuda.is_available()
        device = "GPU" if self.use_gpu else "CPU"
        printCustom(f"PyTorchModel created for inference on " + device, STDOUT_TYPE.INFO)

    def getFeatures(self, frm: np.ndarray):
        """
        This method is used to extract features.
        :param frm: THis parameter must hold a valid numpy image.
        :return: This method returns a flattened numpy array representing the visual features.
        """
        # print("calculate features ... ")
        try:
            image = Image.fromarray(frm.astype('uint8'))
            loader = transforms.Compose([transforms.ToTensor()])
            image = loader(image).float()
            image = self.normalize(image)

            image = Variable(image, requires_grad=True)
            image = image.unsqueeze(0)  # this is for VGG, may not be needed for ResNet

            # do inference on CPU or GPU depending on CUDA availability
            if self.use_gpu:
                self.model.features = self.model.features.cuda()
                inputs = image.cuda()
            else:
                self.model.features = self.model.features.cpu()
                inputs = image.cpu()

            self.model.features.eval()

            with torch.no_grad():
                outputs = self.model.features(inputs)
                outputs_flatten = outputs.view(outputs.size(0), -1)
                #print(outputs_flatten.size())
        except:
            print("+++++++++++++++++++++++++++++")
            exit(1)

        return outputs_flatten.cpu().detach().numpy()
