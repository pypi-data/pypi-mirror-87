import numpy as np
from vhh_stc.Video import Video
import os
from vhh_stc.Models import loadModel
from vhh_stc.CustomTransforms import ToGrayScale
import torch
from PIL import Image
from torch.autograd import Variable
from torch.utils import data
from torchvision import transforms
from vhh_stc.utils import *
from vhh_stc.Configuration import Configuration
import cv2
import json


class STC(object):
    """
        Main class of shot type classification (stc) package.
    """

    def __init__(self, config_file: str):
        """
        Constructor

        :param config_file: [required] path to configuration file (e.g. PATH_TO/config.yaml)
                                       must be with extension ".yaml"
        """
        print("create instance of stc ... ")

        if (config_file == ""):
            printCustom("No configuration file specified!", STDOUT_TYPE.ERROR)
            exit()

        self.config_instance = Configuration(config_file)
        self.config_instance.loadConfig()

        if (self.config_instance.debug_flag == True):
            self.debug_results = "./debug_results/"
            if not os.path.exists(self.debug_results):
                os.mkdir(self.debug_results)
        else:
            if not os.path.exists(self.config_instance.path_final_results):
                os.mkdir(self.config_instance.path_final_results)

    def runOnSingleVideo(self, shots_per_vid_np=None, max_recall_id=-1):
        """
        Method to run stc classification on specified video.

        :param shots_per_vid_np: [required] numpy array representing all detected shots in a video
                                 (e.g. sid | movie_name | start | end )
        :param max_recall_id: [required] integer value holding unique video id from VHH MMSI system
        """

        print("run stc classifier on single video ... ")

        if (type(shots_per_vid_np) == None):
            print("ERROR: you have to set the parameter shots_per_vid_np!")
            exit()

        if (max_recall_id == -1 or max_recall_id == 0):
            print("ERROR: you have to set a valid max_recall_id [1-n]!")
            exit()

        shots_np = shots_per_vid_np

        if (len(shots_np) == 0):
            print("ERROR: there must be at least one shot in the list!")
            exit()

        with open(self.config_instance.path_pre_trained_model + "/" + "/experiment_notes.json", 'r') as json_file:
            param_dict = json.load(json_file)

        model_arch = param_dict['expNet']
        classes = param_dict['classes']
        pre_trained_weights = self.config_instance.path_pre_trained_model + "/best_model.pth"

        #model = self.loadStcModel(self.config_instance.path_pre_trained_model, classes=self.config_instance.class_names)
        model = loadModel(model_arch=model_arch, classes=classes, pre_trained_path=pre_trained_weights)

        if (self.config_instance.debug_flag == True):
            num_shots = 3
        else:
            num_shots = len(shots_np)

        vid_name = shots_np[0][0]
        vid_instance = Video()
        vid_instance.load(os.path.join(self.config_instance.path_videos, vid_name))

        # prepare transformation for cnn model
        preprocess = transforms.Compose([
            transforms.ToPILImage(),
            transforms.Resize((int(vid_instance.height), vid_instance.width)),
            transforms.CenterCrop((int(vid_instance.height), int(vid_instance.height))),
            transforms.Resize(self.config_instance.resize_dim),
            transforms.ToTensor(),
            transforms.Normalize((self.config_instance.mean_values[0],
                                  self.config_instance.mean_values[1],
                                  self.config_instance.mean_values[2]),
                                 (self.config_instance.std_dev[0],
                                  self.config_instance.std_dev[1],
                                  self.config_instance.std_dev[2]))
        ])

        frame_cnt = 0
        results_stc_l = []
        for i, shot in enumerate(vid_instance.getFramesByShots(shots_np, preprocess_pytorch=preprocess)):
            if (i >= num_shots):
                break

            shot_tensors = shot["Tensors"]
            shot_id = int(shot["sid"])
            start = int(shot["start"])
            stop = int(shot["end"])

            # run classifier
            class_name, nHits, all_preds_np = self.runModel(model, shot_tensors)

            if(self.config_instance.save_raw_results == 1):
                #print("save intermediate/raw results ... ")

                # prepare folder structure
                video_raw_result_path = os.path.join(self.config_instance.path_raw_results, str(vid_name.split('.')[0]))
                createFolder(video_raw_result_path)
                shot_result_path = os.path.join(video_raw_result_path, str(shot_id))
                createFolder(shot_result_path)

                # save class distribution
                indices, distr = np.unique(all_preds_np, return_counts=True)
                class_distr_per_shot = np.zeros(len(self.config_instance.class_names)).astype('uint8')
                class_distr_per_shot[indices] = distr
                #names = self.config_instance.class_names[indices]
                #print(names)
                plotClassDistribution(file_name=shot_result_path + "/class_distr_" + str(shot_id),
                                      file_extension="pdf",
                                      class_distr_name=self.config_instance.class_names,
                                      class_distr_data=class_distr_per_shot)

                # save predicition per frame for whole video
                raw_results_per_frame_csv = "results_per_frame.csv"
                for r in range(0, len(all_preds_np)):
                    frame_cnt = frame_cnt + 1
                    entries_l = [frame_cnt, all_preds_np[r], self.config_instance.class_names[all_preds_np[r]]]
                    csvWriter(dst_folder=video_raw_result_path, name=raw_results_per_frame_csv, entries_list=entries_l)

                # save n frames of each shot in separate folders
                n = self.config_instance.number_of_frames_per_shot
                shot_frames_np = np.array(shot_tensors)
                number_of_frames = len(shot_frames_np.shape)
                center_idx = int(number_of_frames / 2)
                a = center_idx - n
                if(a <= 0): a = 0
                if(a >= len(shot_frames_np)): a = len(shot_frames_np)
                b = center_idx + n
                if (b <= 0): b = 0
                if (b >= len(shot_frames_np)): b = len(shot_frames_np)

                for j in range(a, b):
                    #print(shot_frames_np[j].transpose(1, 2, 0).shape)
                    cv2.imwrite(shot_result_path + "/" + str(shot_id) + "_ " + str(j) + ".png",
                                shot_frames_np[j].transpose(1, 2, 0))

            # prepare results
            print(str(vid_name) + ";" + str(shot_id) + ";" + str(start) + ";" + str(stop) + ";" + str(class_name))
            results_stc_l.append([str(vid_name) + ";" + str(shot_id) + ";" + str(start) + ";" + str(stop) + ";" + str(class_name)])

        results_stc_np = np.array(results_stc_l)

        # export results
        self.exportStcResults(str(max_recall_id), results_stc_np)

    def runModel(self, model, tensor_l):
        """
        Method to calculate stc predictions of specified model and given list of tensor images (pytorch).

        :param model: [required] pytorch model instance
        :param tensor_l: [required] list of tensors representing a list of frames.
        :return: predicted class_name for each tensor frame,
                 the number of hits within a shot,
                 frame-based predictions for a whole shot
        """

        input_batch = tensor_l

        # prepare pytorch dataloader
        dataset = data.TensorDataset(input_batch)  # create your datset

        inference_dataloader = data.DataLoader(dataset, batch_size=self.config_instance.batch_size)  # create your dataloader

        preds_l = []
        for i, inputs in enumerate(inference_dataloader):
            input_batch = inputs[0]
            input_batch = Variable(input_batch)

            # move the input and model to GPU for speed if available
            if torch.cuda.is_available():
                input_batch = input_batch.to('cuda')
                model.to('cuda')

            model.eval()
            with torch.no_grad():
                output = model(input_batch)
                preds = output.argmax(1, keepdim=True)
                preds_l.extend(preds.detach().cpu().numpy().flatten())

        preds_np = np.array(preds_l).flatten()
        indices, distr = np.unique(preds_np, return_counts=True)
        tmp_idx = np.zeros(len(self.config_instance.class_names)).astype('int')
        tmp_idx[indices] = distr
        idx = tmp_idx.argmax(0)
        class_name = self.config_instance.class_names[idx]
        nHits = tmp_idx[idx]

        return class_name, nHits, preds_np

    def loadSbdResults(self, sbd_results_path):
        """
        Method for loading shot boundary detection results as numpy array

        .. note::
            Only used in debug_mode.

        :param sbd_results_path: [required] path to results file of shot boundary detection module (vhh_sbd)
        :return: numpy array holding list of detected shots.
        """

        # open sbd results
        fp = open(sbd_results_path, 'r')
        lines = fp.readlines()
        lines = lines[1:]

        lines_n = []
        for i in range(0, len(lines)):
            line = lines[i].replace('\n', '')
            line_split = line.split(';')
            lines_n.append([line_split[0], os.path.join(line_split[1]), line_split[2], line_split[3]])
        lines_np = np.array(lines_n)
        #print(lines_np.shape)

        return lines_np

    def exportStcResults(self, fName, stc_results_np: np.ndarray):
        """
        Method to export stc results as csv file.

        :param fName: [required] name of result file.
        :param stc_results_np: numpy array holding the shot type classification predictions for each shot of a movie.
        """

        print("export results to csv!")

        if (len(stc_results_np) == 0):
            print("ERROR: numpy is empty")
            exit()

        # open stc resutls file
        if (self.config_instance.debug_flag == True):
            fp = open(self.debug_results + "/" + fName + ".csv", 'w')
        else:
            fp = open(self.config_instance.path_final_results + "/" + fName + ".csv", 'w')
        header = "vid_name;shot_id;start;end;stc"
        fp.write(header + "\n")

        for i in range(0, len(stc_results_np)):
            tmp_line = str(stc_results_np[i][0])
            for c in range(1, len(stc_results_np[i])):
                tmp_line = tmp_line + ";" + stc_results_np[i][c]
            fp.write(tmp_line + "\n")




