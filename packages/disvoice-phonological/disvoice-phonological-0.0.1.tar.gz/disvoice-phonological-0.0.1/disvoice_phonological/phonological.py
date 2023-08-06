
# -*- coding: utf-8 -*-
"""
Created on Jun 24 2020

@author: J. C. Vasquez-Correa
"""
import os
import sys

import numpy as np
import pandas as pd
from phonet.phonet import Phonet
from phonet.phonet import Phonological as phon
import scipy.stats as st
import matplotlib.pyplot as plt
plt.rcParams["font.family"] = "Times New Roman"

path_app = os.path.dirname(os.path.abspath(__file__))
sys.path.append(path_app+'/../')

import torch
from tqdm import tqdm

class Phonological:
    """
    Compute phonological features from continuous speech files.

    18 descriptors are computed, bases on 18 different phonological classes from the phonet toolkit 
    https://phonet.readthedocs.io/en/latest/?badge=latest

    It computes the phonological log-likelihood ratio features from phonet

    Static or dynamic matrices can be computed:

    Static matrix is formed with 108 features formed with (18 descriptors) x (6 functionals: mean, std, skewness, kurtosis, max, min)

    Dynamic matrix is formed with the 18 descriptors computed for frames of 25 ms with a time-shift of 10 ms.


    Script is called as follows

    >>> python phonological.py <file_or_folder_audio> <file_features> <static (true or false)> <plots (true or false)> <format (csv, txt, npy, kaldi, torch)>

    Examples command line:

    >>> python phonological.py "../audios/001_ddk1_PCGITA.wav" "phonologicalfeaturesAst.txt" "true" "true" "txt"
    >>> python phonological.py "../audios/001_ddk1_PCGITA.wav" "phonologicalfeaturesUst.csv" "true" "true" "csv"
    >>> python phonological.py "../audios/001_ddk1_PCGITA.wav" "phonologicalfeaturesUdyn.pt" "false" "true" "torch"

    >>> python phonological.py "../audios/" "phonologicalfeaturesst.txt" "true" "false" "txt"
    >>> python phonological.py "../audios/" "phonologicalfeaturesst.csv" "true" "false" "csv"
    >>> python phonological.py "../audios/" "phonologicalfeaturesdyn.pt" "false" "false" "torch"
    >>> python phonological.py "../audios/" "phonologicalfeaturesdyn.csv" "false" "false" "csv"

    Examples directly in Python

    >>> phonological=Phonological()
    >>> file_audio="../audios/001_ddk1_PCGITA.wav"
    >>> features1=phonological.extract_features_file(file_audio, static=True, plots=True, fmt="npy")
    >>> features2=phonological.extract_features_file(file_audio, static=True, plots=True, fmt="dataframe")
    >>> features3=phonological.extract_features_file(file_audio, static=False, plots=True, fmt="torch")
    >>> phonological.extract_features_file(file_audio, static=False, plots=False, fmt="kaldi", kaldi_file="./test")

    """

    def __init__(self):
        phonolist=phon()
        self.head_dyn=phonolist.get_list_phonological_keys()
        self.statistics=["mean", "std", "skewness", "kurtosis", "max", "min"]
        self.head_st=[]
        for j in self.head_dyn:
            for l in self.statistics:
                self.head_st.append(j+"_"+l)
        self.phon=Phonet(["all"])
        
    def script_manager(args, feature_method):

        audio=args[1]
        file_features=args[2]
        if args[3]=="false" or args[3]=="False":
            static=False
        elif args[3]=="true" or args[3]=="True":
            static=True
        else:
            raise ValueError(args[3] +" is not a valid argument for <static>. It should be only True or False")

        if args[4]=="false" or args[4]=="False":
            plots=False
        elif args[4]=="true" or args[4]=="True":
            plots=True
        else:
            raise ValueError(args[4] +" is not a valid argument for <plots>. It should be only True or False")

        if args[5]=="npy" or args[5]=="csv" or args[5]=="txt" or args[5]=="torch" or args[5]=="kaldi":
            fmt=args[5]
        else:
            raise ValueError(args[5]+ " is not a valid argument for <format>. It should be only csv, txt, npy, kaldi, or torch")

        if audio.find('.wav')!=-1 or audio.find('.WAV')!=-1:
            if fmt=="kaldi":
                feature_method.extract_features_file(audio, static=static, plots=plots, fmt=fmt, kaldi_file=file_features)
            else:
                features=feature_method.extract_features_file(audio, static=static, plots=plots, fmt=fmt)
                if fmt=="npy":
                    np.save(file_features, features)
                elif fmt=="txt":
                    np.savetxt(file_features, features)
                elif fmt=="csv":
                    features.to_csv(file_features)
                elif fmt=="torch":
                    torch.save(features, file_features)
                else:
                    raise ValueError("Not valid output format")
        else:
            if fmt=="kaldi":
                feature_method.extract_features_path(audio, static=static, plots=plots, fmt=fmt, kaldi_file=file_features)
            else:
                features=feature_method.extract_features_path(audio, static=static, plots=plots, fmt=fmt)
                if fmt=="npy":
                    np.save(file_features, features)
                elif fmt=="txt":
                    np.savetxt(file_features, features)
                elif fmt=="csv":
                    features.to_csv(file_features)
                elif fmt=="torch":
                    torch.save(features, file_features)
                else:
                    raise ValueError("Not valid output format")
                    
    def save_dict_kaldimat(dict_feat, temp_file):
        ark_scp_output='ark:| copy-feats --compress=true ark:- ark,scp:'+temp_file+'.ark,'+temp_file+'.scp'
        with kaldi_io.open_or_fd(ark_scp_output,'wb') as f:
            for key,mat in dict_feat.items():
                kaldi_io.write_mat(f, mat, key=key)

    def extract_features_file(self, audio, static=True, plots=False, fmt="npy", kaldi_file=""):
        """Extract the phonological features from an audio file

        :param audio: .wav audio file.
        :param static: whether to compute and return statistic functionals over the feature matrix, or return the feature matrix computed over frames
        :param plots: timeshift to extract the features
        :param fmt: format to return the features (npy, dataframe, torch, kaldi)
        :param kaldi_file: file to store kaldi features, only valid when fmt=="kaldi"
        :returns: features computed from the audio file.

        >>> phonological=Phonological()
        >>> file_audio="../audios/001_ddk1_PCGITA.wav"
        >>> features1=phonological.extract_features_file(file_audio, static=True, plots=True, fmt="npy")
        >>> features2=phonological.extract_features_file(file_audio, static=True, plots=True, fmt="dataframe")
        >>> features3=phonological.extract_features_file(file_audio, static=False, plots=True, fmt="torch")
        >>> phonological.extract_features_file(file_audio, static=False, plots=False, fmt="kaldi", kaldi_file="./test")

        >>> phonological=Phonological()
        >>> path_audio="../audios/"
        >>> features1=phonological.extract_features_path(path_audio, static=True, plots=False, fmt="npy")
        >>> features2=phonological.extract_features_path(path_audio, static=True, plots=False, fmt="csv")
        >>> features3=phonological.extract_features_path(path_audio, static=False, plots=True, fmt="torch")
        >>> phonological.extract_features_path(path_audio, static=False, plots=False, fmt="kaldi", kaldi_file="./test.ark")

        """

        
        df=self.phon.get_PLLR(audio, plot_flag=plots)

        keys=df.keys().tolist()
        keys.remove('time')

        if static:
            dff={}
            feat_vec=[]
            
            functions=[np.mean, np.std, st.skew, st.kurtosis, np.max, np.min]

            for j in keys:
                for l, function in zip(self.statistics, functions):

                    if (fmt=="npy") or (fmt=="txt") or (fmt=="torch"):
                        feat_vec.append(function(df[j]))
                    elif fmt=="dataframe" or fmt=="csv":

                        feat_name=j+"_"+l

                        dff[feat_name]=[function(df[j])]
            if fmt=="npy" or fmt=="txt":
                return np.hstack(feat_vec)
            elif fmt=="dataframe" or fmt=="csv":
                return pd.DataFrame(dff)
            elif fmt=="torch":
                feat_t=torch.from_numpy(np.hstack(feat_vec))
            elif fmt=="kaldi":
                raise ValueError("Kaldi is only supported for dynamic features")
            else:
                raise ValueError(fmt+" is not supported")

        else:
            
            if fmt=="npy" or fmt=="txt":
                featmat=np.stack([df[k] for k in keys], axis=1)
                print(featmat.shape)
                return featmat
            elif fmt=="dataframe" or fmt=="csv":
                return df
            elif fmt=="torch":
                featmat=np.stack([df[k] for k in keys], axis=1)
                return torch.from_numpy(featmat)
            elif fmt=="kaldi":
                featmat=np.stack([df[k] for k in keys], axis=1)
                name_all=audio.split('/')
                dictX={name_all[-1]:feat_mat}
                save_dict_kaldimat(dictX, kaldi_file)
            else:
                raise ValueError(fmt+" is not supported")



    def extract_features_path(self, path_audio, static=True, plots=False, fmt="npy", kaldi_file=""):
        """Extract the phonological features for audios inside a path
        
        :param path_audio: directory with (.wav) audio files inside, sampled at 16 kHz
        :param static: whether to compute and return statistic functionals over the feature matrix, or return the feature matrix computed over frames
        :param plots: timeshift to extract the features
        :param fmt: format to return the features (npy, dataframe, torch, kaldi)
        :param kaldi_file: file to store kaldifeatures, only valid when fmt=="kaldi"
        :returns: features computed from the audio file.

        >>> phonological=Phonological()
        >>> path_audio="../audios/"
        >>> features1=phonological.extract_features_path(path_audio, static=True, plots=False, fmt="npy")
        >>> features2=phonological.extract_features_path(path_audio, static=True, plots=False, fmt="csv")
        >>> features3=phonological.extract_features_path(path_audio, static=False, plots=True, fmt="torch")
        >>> phonological.extract_features_path(path_audio, static=False, plots=False, fmt="kaldi", kaldi_file="./test.ark")
        """

        hf=os.listdir(path_audio)
        hf.sort()

        pbar=tqdm(range(len(hf)))
        ids=[]

        Features=[]
        for j in pbar:
            pbar.set_description("Processing %s" % hf[j])
            audio_file=path_audio+hf[j]
            feat=self.extract_features_file(audio_file, static=static, plots=plots, fmt="npy")
            Features.append(feat)
            if static:
                ids.append(hf[j])
            else:
                ids.append(np.repeat(hf[j], feat.shape[0]))
        
        Features=np.vstack(Features)
        ids=np.hstack(ids)
        if fmt=="npy" or fmt=="txt":
            return Features
        elif fmt=="dataframe" or fmt=="csv":
            if static:
                df={}
                for e, k in enumerate(self.head_st):
                    df[k]=Features[:,e]
            else:
                df={}
                for e, k in enumerate(self.head_dyn):
                    df[k]=Features[:,e]
            df["id"]=ids
            return pd.DataFrame(df)
        elif fmt=="torch":
            return torch.from_numpy(Features)
        elif fmt=="kaldi":
            if static:
                raise ValueError("Kaldi is only supported for dynamic features")
            else:
                dictX=get_dict(Features, ids)
                save_dict_kaldimat(dictX, kaldi_file)
        else:
            raise ValueError(fmt+" is not supported")


if __name__=="__main__":

    if len(sys.argv)!=6:
        print("python phonological.py <file_or_folder_audio> <file_features> <static (true, false)> <plots (true,  false)> <format (csv, txt, npy, kaldi, torch)>")
        sys.exit()

    phonological=Phonological()
    script_manager(sys.argv, phonological)
