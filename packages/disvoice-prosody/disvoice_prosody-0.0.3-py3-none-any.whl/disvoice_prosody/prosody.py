
# -*- coding: utf-8 -*-
"""
Created on Jul 21 2017, Modified Apr 10 2018.

@author: J. C. Vasquez-Correa, T. Arias-Vergara, J. S. Guerrero
"""

from scipy.io.wavfile import read
import os
import sys
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams["font.family"] = "Times New Roman"
from matplotlib import cm
import math
import pysptk
try:
    from .prosody_functions import V_UV, E_cont, logEnergy, F0feat, energy_cont_segm, polyf0, energy_feat, dur_seg, duration_feat, E_cont
except:
    from prosody_functions import V_UV, E_cont, logEnergy, F0feat, energy_cont_segm, polyf0, energy_feat, dur_seg, duration_feat, E_cont

import scipy.stats as st
import uuid
from sklearn.metrics import mean_squared_error
import pandas as pd
import torch
from tqdm import tqdm
path_praat_script=os.path.dirname(os.path.abspath(__file__))
path_app = os.path.dirname(os.path.abspath(__file__))
sys.path.append(path_app+'/../')


class Prosody:
    """
    Compute prosody features from continuous speech based on duration, fundamental frequency and energy.
    Static or dynamic matrices can be computed:
    Static matrix is formed with 103 features and include

    1-6     F0-contour:                                                       Avg., Std., Max., Min., Skewness, Kurtosis

    7-12    Tilt of a linear estimation of F0 for each voiced segment:        Avg., Std., Max., Min., Skewness, Kurtosis

    13-18   MSE of a linear estimation of F0 for each voiced segment:         Avg., Std., Max., Min., Skewness, Kurtosis

    19-24   F0 on the first voiced segment:                                   Avg., Std., Max., Min., Skewness, Kurtosis

    25-30   F0 on the last voiced segment:                                    Avg., Std., Max., Min., Skewness, Kurtosis

    31-34   energy-contour for voiced segments:                               Avg., Std., Skewness, Kurtosis

    35-38   Tilt of a linear estimation of energy contour for V segments:     Avg., Std., Skewness, Kurtosis

    39-42   MSE of a linear estimation of energy contour for V segment:       Avg., Std., Skewness, Kurtosis

    43-48   energy on the first voiced segment:                               Avg., Std., Max., Min., Skewness, Kurtosis

    49-54   energy on the last voiced segment:                                Avg., Std., Max., Min., Skewness, Kurtosis

    55-58   energy-contour for unvoiced segments:                             Avg., Std., Skewness, Kurtosis

    59-62   Tilt of a linear estimation of energy contour for U segments:     Avg., Std., Skewness, Kurtosis

    63-66   MSE of a linear estimation of energy contour for U segments:      Avg., Std., Skewness, Kurtosis

    67-72   energy on the first unvoiced segment:                             Avg., Std., Max., Min., Skewness, Kurtosis

    73-78   energy on the last unvoiced segment:                              Avg., Std., Max., Min., Skewness, Kurtosis

    79      Voiced rate:                                                      Number of voiced segments per second

    80-85   Duration of Voiced:                                               Avg., Std., Max., Min., Skewness, Kurtosis

    86-91   Duration of Unvoiced:                                             Avg., Std., Max., Min., Skewness, Kurtosis

    92-97   Duration of Pauses:                                               Avg., Std., Max., Min., Skewness, Kurtosis

    98-103  Duration ratios:                                                 Pause/(Voiced+Unvoiced), Pause/Unvoiced, Unvoiced/(Voiced+Unvoiced),Voiced/(Voiced+Unvoiced), Voiced/Puase, Unvoiced/Pause

    Dynamic matrix is formed with 13 features computed for each voiced segment and contains


    1-6. Coefficients of 5-degree Lagrange polynomial to model F0 contour

    7-12. Coefficients of 5-degree Lagrange polynomial to model energy contour

    13. Duration of the voiced segment

    Dynamic prosody features are based on
    Najim Dehak, "Modeling Prosodic Features With Joint Factor Analysis for Speaker Verification", 2007

    Script is called as follows

    >>> python prosody.py <file_or_folder_audio> <file_features> <static (true or false)> <plots (true or false)> <format (csv, txt, npy, kaldi, torch)>

    Examples command line:

    >>> python prosody.py "../audios/001_ddk1_PCGITA.wav" "prosodyfeaturesAst.txt" "true" "true" "txt"
    >>> python prosody.py "../audios/001_ddk1_PCGITA.wav" "prosodyfeaturesUst.csv" "true" "true" "csv"
    >>> python prosody.py "../audios/001_ddk1_PCGITA.wav" "prosodyfeaturesUdyn.pt" "false" "true" "torch"

    >>> python prosody.py "../audios/" "prosodyfeaturesst.txt" "true" "false" "txt"
    >>> python prosody.py "../audios/" "prosodyfeaturesst.csv" "true" "false" "csv"
    >>> python prosody.py "../audios/" "prosodyfeaturesdyn.pt" "false" "false" "torch"
    >>> python prosody.py "../audios/" "prosodyfeaturesdyn.csv" "false" "false" "csv"

    Examples directly in Python

    >>> prosody=Prosody()
    >>> file_audio="../audios/001_ddk1_PCGITA.wav"
    >>> features1=prosody.extract_features_file(file_audio, static=True, plots=True, fmt="npy")
    >>> features2=prosody.extract_features_file(file_audio, static=True, plots=True, fmt="dataframe")
    >>> features3=prosody.extract_features_file(file_audio, static=False, plots=True, fmt="torch")
    >>> prosody.extract_features_file(file_audio, static=False, plots=False, fmt="kaldi", kaldi_file="./test")

    >>> path_audio="../audios/"
    >>> features1=prosody.extract_features_path(path_audio, static=True, plots=False, fmt="npy")
    >>> features2=prosody.extract_features_path(path_audio, static=True, plots=False, fmt="csv")
    >>> features3=prosody.extract_features_path(path_audio, static=False, plots=True, fmt="torch")
    >>> prosody.extract_features_path(path_audio, static=False, plots=False, fmt="kaldi", kaldi_file="./test.ark")

    """

    def __init__(self):
        self.pitch_method="praat"
        self.size_frame=0.02
        self.step=0.01
        self.thr_len=0.14
        self.minf0=60
        self.maxf0=350
        self.PATH = os.path.dirname(os.path.abspath(__file__))
        self.voice_bias=-0.2
        self.P=5
        self.namefeatf0=["F0avg", "F0std", "F0max", "F0min", 
            "F0skew", "F0kurt", "F0tiltavg", "F0mseavg", 
            "F0tiltstd", "F0msestd", "F0tiltmax", "F0msemax", 
            "F0tiltmin", "F0msemin","F0tiltskw", "F0mseskw", 
            "F0tiltku", "F0mseku", "1F0mean", "1F0std", 
            "1F0max", "1F0min", "1F0skw", "1F0ku", "lastF0avg", 
            "lastF0std", "lastF0max", "lastF0min", "lastF0skw", "lastF0ku"]
        self.namefeatEv=["avgEvoiced", "stdEvoiced", "skwEvoiced", "kurtosisEvoiced", 
            "avgtiltEvoiced", "stdtiltEvoiced", "skwtiltEvoiced", "kurtosistiltEvoiced", 
            "avgmseEvoiced", "stdmseEvoiced", "skwmseEvoiced", "kurtosismseEvoiced", 
            "avg1Evoiced", "std1Evoiced", "max1Evoiced", "min1Evoiced", "skw1Evoiced", 
            "kurtosis1Evoiced", "avglastEvoiced", "stdlastEvoiced", "maxlastEvoiced", 
            "minlastEvoiced", "skwlastEvoiced",  "kurtosislastEvoiced"]    
        self.namefeatEu=["avgEunvoiced", "stdEunvoiced", "skwEunvoiced", "kurtosisEunvoiced", 
            "avgtiltEunvoiced", "stdtiltEunvoiced", "skwtiltEunvoiced", "kurtosistiltEunvoiced", 
            "avgmseEunvoiced", "stdmseEunvoiced", "skwmseEunvoiced", "kurtosismseEunvoiced", 
            "avg1Eunvoiced", "std1Eunvoiced", "max1Eunvoiced", "min1Eunvoiced", "skw1Eunvoiced", 
            "kurtosis1Eunvoiced", "avglastEunvoiced", "stdlastEunvoiced", "maxlastEunvoiced", 
            "minlastEunvoiced", "skwlastEunvoiced",  "kurtosislastEunvoiced"]  

        self.namefeatdur=["Vrate", "avgdurvoiced", "stddurvoiced", "skwdurvoiced", "kurtosisdurvoiced", "maxdurvoiced", "mindurvoiced", 
            "avgdurunvoiced", "stddurunvoiced", "skwdurunvoiced", "kurtosisdurunvoiced", "maxdurunvoiced", "mindurunvoiced", 
            "avgdurpause", "stddurpause", "skwdurpause", "kurtosisdurpause", "maxdurpause", "mindurpause", 
            "PVU", "PU", "UVU", "VVU", "VP", "UP"]
        self.head_st=self.namefeatf0+self.namefeatEv+self.namefeatEu+self.namefeatdur

        self.namef0d=["f0coef"+str(i) for i in range(6)]
        self.nameEd=["Ecoef"+str(i) for i in range(6)]
        self.head_dyn=self.namef0d+self.nameEd+["Voiced duration"]
        
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
    
    def get_dict(feat_mat, IDs):
        uniqueids=np.unique(IDs)
        df={}
        for k in uniqueids:
            p=np.where(IDs==k)[0]
            featid=feat_mat[p,:]
            df[str(k)]=featid
        return df

    def save_dict_kaldimat(dict_feat, temp_file):
        ark_scp_output='ark:| copy-feats --compress=true ark:- ark,scp:'+temp_file+'.ark,'+temp_file+'.scp'
        with kaldi_io.open_or_fd(ark_scp_output,'wb') as f:
            for key,mat in dict_feat.items():
                kaldi_io.write_mat(f, mat, key=key)

    def multi_find(s, r):
        """
        Internal function used to decode the Formants file generated by Praat.
        """
        s_len = len(s)
        r_len = len(r)
        _complete = []
        if s_len < r_len:
            n = -1
        else:
            for i in range(s_len):
                # search for r in s until not enough characters are left
                if s[i:i + r_len] == r:
                    _complete.append(i)
                else:
                    i = i + 1
        return(_complete)

    def praat_vuv(audio_filaname, resultsp, resultst, time_stepF0=0, minf0=75, maxf0=600, maxVUVPeriod=0.02, averageVUVPeriod=0.01):
        """
        runs vuv_praat script to obtain pitch and voicing decisions for a wav file.
        It writes the results into two text files, one for the pitch and another
        for the voicing decisions. These results can then be read using the function
        read_textgrid_trans and decodeF0

        :param audio_filaname: Full path to the wav file
        :param resultsp: Full path to the resulting file with the pitch
        :param resultst: Full path to the resulting file with the voiced/unvoiced decisions
        :param time_stepF0: time step to compute the pitch, default value is 0 and Praat will use 0.75 / minf0
        :param minf0: minimum frequency for the pitch in Hz, default is 75Hz
        :param maxf0: maximum frequency for the pitch in Hz, default is 600
        :param maxVUVPeriod: maximum interval that considered part of a larger voiced interval, default 0.02
        :param averageVUVPeriod: half of this value will be taken to be the amount to which a voiced interval will extend                             beyond its initial and final points, default is 0.01
        :returns: nothing
        """
        command='praat '+path_praat_script+'/vuv_praat.praat '
        command+=audio_filaname+' '+resultsp +' '+  resultst+' '
        command+=str(minf0)+' '+str(maxf0)+' '
        command+=str(time_stepF0)+' '+str(maxVUVPeriod)+' '+str(averageVUVPeriod)
        os.system(command)

    def praat_formants(audio_filename, results_filename,sizeframe,step, n_formants=5, max_formant=5500):
        """
        runs FormantsPraat script to obtain the formants for a wav file.
        It writes the results into a text file.
        These results can then be read using the function decodeFormants.

        :param audio_filaname: Full path to the wav file, string
        :param results_filename: Full path to the resulting file with the formants
        :param sizeframe: window size
        :param step: time step to compute formants
        :param n_formants: number of formants to look for
        :param max_formant: maximum frequencyof formants to look for
        :returns: nothing
        """
        command='praat '+path_praat_script+'/FormantsPraat.praat '
        command+=audio_filename + ' '+results_filename+' '
        command+=str(n_formants)+' '+ str(max_formant) + ' '
        command+=str(float(sizeframe)/2)+' '
        command+=str(float(step))
        os.system(command) #formant extraction praat

    def read_textgrid_trans(file_textgrid, data_audio, fs, win_trans=0.04):
        """
        This function reads a text file with the text grid with voiced/unvoiced
        decisions then finds the onsets (unvoiced -> voiced) and
        offsets (voiced -> unvoiced) and then reads the audio data to returns
        lists of segments of lenght win_trans around these transitions.

        :param file_textgrid: The text file with the text grid with voicing decisions.
        :param data_audio: the audio signal.
        :param fs: sampling frequency of the audio signal.
        :param win_trans: the transition window lenght, default 0.04
        :returns segments: List with both onset and offset transition segments.
        :returns segments_onset: List with onset transition segments
        :returns segments_offset: List with offset transition segments
        """
        segments=[]
        segments_onset=[]
        segments_offset=[]
        prev_trans=""
        prev_line=0
        with open(file_textgrid) as fp:
            for line in fp:
                line = line.strip('\n')
                if line=='"V"' or line == '"U"':
                    transVal=int(float(prev_line)*fs)-1
                    segment=data_audio[int(transVal-win_trans*fs):int(transVal+win_trans*fs)]
                    segments.append(segment)
                    if prev_trans=='"V"' or prev_trans=="":
                        segments_onset.append(segment)
                    elif prev_trans=='"U"':
                        segments_offset.append(segment)
                    prev_trans=line
                prev_line=line
        return segments,segments_onset,segments_offset

    def decodeF0(fileTxt,len_signal=0, time_stepF0=0):
        """
        Reads the content of a pitch file created with praat_vuv function.
        By default it will return the contents of the file in two arrays,
        one for the actual values of pitch and the other with the time stamps.
        Optionally the lenght of the signal and the time step of the pitch
        values can be provided to return an array with the full pitch contour
        for the signal, with padded zeros for unvoiced segments.

        :param fileTxt: File with the pitch, which can be generated using the function praat_vuv
        :param len_signal: Lenght of the audio signal in
        :param time_stepF0: The time step of pitch values. Optional.
        :returns pitch: Numpy array with the values of the pitch.
        :returns time_voiced: time stamp for each pitch value.
        """
        if os.stat(fileTxt).st_size==0:
            return np.array([0]), np.array([0])
        pitch_data=np.loadtxt(fileTxt)
        if len(pitch_data.shape)>1:
            time_voiced=pitch_data[:,0] # First column is the time stamp vector
            pitch=pitch_data[:,1] # Second column
        elif len(pitch_data.shape)==1: # Only one point of data
            time_voiced=pitch_data[0] # First datum is the time stamp
            pitch=pitch_data[1] # Second datum is the pitch value
        if len_signal>0:
            n_frames=int(len_signal/time_stepF0)
            t=np.linspace(0.0,len_signal,n_frames)
            pitch_zeros=np.zeros(int(n_frames))
            if len(pitch_data.shape)>1:
                for idx,time_p in enumerate(time_voiced):
                    argmin=np.argmin(np.abs(t-time_p))
                    pitch_zeros[argmin]=pitch[idx]
            else:
                argmin=np.argmin(np.abs(t-time_voiced))
                pitch_zeros[argmin]=pitch
            return pitch_zeros, t
        else:
            return pitch, time_voiced

    def decodeFormants(fileTxt):
        """
        Read the praat textgrid file for formants and return the array
        
        :param fileTxt: File with the formants, which can be generated using the
                        function praat_formants
        :returns F1: Numpy array containing the values for the first formant
        :returns F2: Numpy array containing the values for the second formant
        """
        fid=open(fileTxt)
        datam=fid.read()
        end_line1=multi_find(datam, '\n')
        F1=[]
        F2=[]
        ji=10
        while (ji<len(end_line1)-1):
            line1=datam[end_line1[ji]+1:end_line1[ji+1]]
            cond=(line1=='3' or line1=='4' or line1=='5')
            if (cond):
                F1.append(float(datam[end_line1[ji+1]+1:end_line1[ji+2]]))
                F2.append(float(datam[end_line1[ji+3]+1:end_line1[ji+4]]))
            ji=ji+1
        F1=np.asarray(F1)
        F2=np.asarray(F2)
        return F1, F2
    
    def plot_pros(self, data_audio,fs,F0,segmentsV, segmentsU, F0_features):
        """Plots of the prosody features

        :param data_audio: speech signal.
        :param fs: sampling frequency
        :param F0: contour of the fundamental frequency
        :param segmentsV: list with the voiced segments
        :param segmentsU: list with the unvoiced segments
        :param F0_features: vector with f0-based features
        :returns: plots of the prosody features.
        """
        plt.figure(figsize=(6,6))
        plt.subplot(211)
        ax1=plt.gca()
        t=np.arange(len(data_audio))/float(fs)
        colors = cm.get_cmap('Accent', 5)
        ax1.plot(t, data_audio, 'k', label="speech signal", alpha=0.5, color=colors.colors[4])
        ax1.set_ylabel('Amplitude', fontsize=12)
        ax1.set_xlabel('Time (s)', fontsize=12)
        ax1.set_xlim([0, t[-1]])
        ax2 = ax1.twinx()
        fsp=len(F0)/t[-1]
        t2=np.arange(len(F0))/fsp
        ax2.plot(t2, F0, color=colors.colors[0], linewidth=2,label=r"Real $F_0$", alpha=0.5)
        ax2.set_ylabel(r'$F_0$ (Hz)', color=colors.colors[0], fontsize=12)
        ax2.tick_params('y', colors=colors.colors[0])

        p0=np.where(F0!=0)[0]
        f0avg=np.nanmean(np.where(F0!=0,F0,np.nan))
        f0std=np.std(F0[p0])

        ax2.plot([t2[0], t2[-1]], [f0avg, f0avg], color=colors.colors[2], label=r"Avg. $F_0$")
        ax2.fill_between([t2[0], t2[-1]], y1= [f0avg+f0std, f0avg+f0std], y2=[f0avg-f0std, f0avg-f0std], color=colors.colors[2], alpha=0.2, label=r"Avg. $F_0\pm$ SD.")
        F0rec=polyf0(F0, fs)
        ax2.plot(t2,F0rec, label=r"estimated $F_0$", c=colors.colors[1], linewidth=2.0)
        plt.text(t2[2], np.max(F0)-5, r"$F_0$ SD.="+str(np.round(f0std, 1))+" Hz")
        plt.text(t2[2], np.max(F0)-20, r"$F_0$ tilt.="+str(np.round(F0_features[6], 1))+" Hz")

        plt.legend(ncol=2, loc=8)

        plt.subplot(212)
        size_frameS=0.02*float(fs)
        size_stepS=0.01*float(fs)

        logE=energy_cont_segm([data_audio], fs,size_frameS, size_stepS)
        Esp=len(logE[0])/t[-1]
        t2=np.arange(len(logE[0]))/float(Esp)
        plt.plot(t2, logE[0], color='k', linewidth=2.0)
        plt.xlabel('Time (s)', fontsize=12)
        plt.ylabel('Energy (dB)', fontsize=12)
        plt.xlim([0, t[-1]])
        plt.grid(True)
        plt.tight_layout()
        plt.show()

        plt.figure(figsize=(6,3))
        Ev=energy_cont_segm(segmentsV, fs, size_frameS, size_stepS)
        Eu=energy_cont_segm(segmentsU, fs, size_frameS, size_stepS)

        plt.plot([np.mean(Ev[j]) for j in range(len(Ev))], label="Voiced energy")
        plt.plot([np.mean(Eu[j]) for j in range(len(Eu))], label="Unvoiced energy")

        plt.xlabel("Number of segments")
        plt.ylabel("Energy (dB)")
        plt.legend()
        plt.grid()
        plt.tight_layout()
        plt.show()


    def extract_features_file(self, audio, static=True, plots=False, fmt="npy", kaldi_file=""):
        """Extract the prosody features from an audio file

        :param audio: .wav audio file.
        :param static: whether to compute and return statistic functionals over the feature matrix, or return the feature matrix computed over frames
        :param plots: timeshift to extract the features
        :param fmt: format to return the features (npy, dataframe, torch, kaldi)
        :param kaldi_file: file to store kaldi features, only valid when fmt=="kaldi"
        :returns: features computed from the audio file.

        >>> prosody=Prosody()
        >>> file_audio="../audios/001_ddk1_PCGITA.wav"
        >>> features1=prosody.extract_features_file(file_audio, static=True, plots=True, fmt="npy")
        >>> features2=prosody.extract_features_file(file_audio, static=True, plots=True, fmt="dataframe")
        >>> features3=prosody.extract_features_file(file_audio, static=False, plots=True, fmt="torch")
        >>> prosody.extract_features_file(file_audio, static=False, plots=False, fmt="kaldi", kaldi_file="./test")
        """
        if static:
            features=self.prosody_static(audio, plots)
            if fmt=="npy" or fmt=="txt":
                return features
            elif fmt=="dataframe" or fmt=="csv":
                df={}
                for e, k in enumerate(self.head_st):
                    #print(feat_v.shape, len(head_st), e, k)
                    df[k]=[features[e]]
                return pd.DataFrame(df)
            elif fmt=="torch":
                feat_t=torch.from_numpy(features)
                return feat_t
            elif fmt=="kaldi":
                raise ValueError("Kaldi is only supported for dynamic features")
            else:
                raise ValueError("format"+ fmt+" is not supported" )


        else:
            features=self.prosody_dynamic(audio)
            if fmt=="npy" or fmt=="txt":
                return features
            elif fmt=="dataframe" or fmt=="csv":
                df={}
                for e, k in enumerate(self.head_dyn):
                    df[k]=features[:,e]
                return pd.DataFrame(df)
            elif fmt=="torch":
                feat_t=torch.from_numpy(features)
                return feat_t
            elif fmt=="kaldi":
                name_all=audio.split('/')
                dictX={name_all[-1]:features}
                save_dict_kaldimat(dictX, kaldi_file)
            else:
                raise ValueError("format"+ fmt+" is not supported" )


    def prosody_static(self, audio, plots):
        """Extract the static prosody features from an audio file

        :param audio: .wav audio file.
        :param plots: timeshift to extract the features
        :returns: array with the 103 prosody features

        >>> prosody=Prosody()
        >>> file_audio="../audios/001_ddk1_PCGITA.wav"
        >>> features=prosody.prosody_static(file_audio, plots=True)

        """
        fs, data_audio=read(audio)
        data_audio=data_audio-np.mean(data_audio)
        data_audio=data_audio/float(np.max(np.abs(data_audio)))
        size_frameS=self.size_frame*float(fs)
        size_stepS=self.step*float(fs)
        thr_len_pause=self.thr_len*float(fs)
        overlap=size_stepS/size_frameS
        nF=int((len(data_audio)/size_frameS/overlap))-1

        if self.pitch_method == 'praat':
            name_audio=audio.split('/')
            temp_uuid='prosody'+name_audio[-1][0:-4]
            if not os.path.exists(self.PATH+'/../tempfiles/'):
                os.makedirs(self.PATH+'/../tempfiles/')
            temp_filename_f0=self.PATH+'/../tempfiles/tempF0'+temp_uuid+'.txt'
            temp_filename_vuv=self.PATH+'/../tempfiles/tempVUV'+temp_uuid+'.txt'
            praat_vuv(audio, temp_filename_f0, temp_filename_vuv, time_stepF0=self.step, minf0=self.minf0, maxf0=self.maxf0)

            F0,_=decodeF0(temp_filename_f0,len(data_audio)/float(fs),self.step)
            os.remove(temp_filename_f0)
            os.remove(temp_filename_vuv)
        elif self.pitch_method == 'rapt':
            data_audiof=np.asarray(data_audio*(2**15), dtype=np.float32)
            F0=pysptk.sptk.rapt(data_audiof, fs, int(size_stepS), min=self.minf0, max=self.maxf0, voice_bias=self.voice_bias, otype='f0')

        segmentsV=V_UV(F0, data_audio, fs, type_seg="Voiced", size_stepS=size_stepS)
        segmentsUP=V_UV(F0, data_audio, fs, type_seg="Unvoiced", size_stepS=size_stepS)

        segmentsP=[]
        segmentsU=[]
        for k in range(len(segmentsUP)):
            eu=logEnergy(segmentsUP[k])
            if (len(segmentsUP[k])>thr_len_pause):
                segmentsP.append(segmentsUP[k])
            else:
                segmentsU.append(segmentsUP[k])

        F0_features=F0feat(F0)
        energy_featuresV=energy_feat(segmentsV, fs, size_frameS, size_stepS)
        energy_featuresU=energy_feat(segmentsU, fs, size_frameS, size_stepS)
        duration_features=duration_feat(segmentsV, segmentsU, segmentsP, data_audio, fs)

        if plots:
            self.plot_pros(data_audio,fs,F0,segmentsV, segmentsU, F0_features)

        features=np.hstack((F0_features, energy_featuresV, energy_featuresU, duration_features))
        
        return features


    def prosody_dynamic(self,audio):
        """Extract the dynamic prosody features from an audio file

        :param audio: .wav audio file.
        :returns: array (N,13) with the prosody features extracted from an audio file.  N= number of voiced segments

        >>> prosody=Prosody()
        >>> file_audio="../audios/001_ddk1_PCGITA.wav"
        >>> features=prosody.prosody_dynamic(file_audio)

        """
        fs, data_audio=read(audio)
        data_audio=data_audio-np.mean(data_audio)
        data_audio=data_audio/float(np.max(np.abs(data_audio)))
        size_frameS=self.size_frame*float(fs)
        size_stepS=self.step*float(fs)
        thr_len_pause=self.thr_len*float(fs)
        overlap=size_stepS/size_frameS
        nF=int((len(data_audio)/size_frameS/overlap))-1

        if self.pitch_method == 'praat':
            name_audio=audio.split('/')
            temp_uuid='prosody'+name_audio[-1][0:-4]
            if not os.path.exists(self.PATH+'/../tempfiles/'):
                os.makedirs(self.PATH+'/../tempfiles/')
            temp_filename_f0=self.PATH+'/../tempfiles/tempF0'+temp_uuid+'.txt'
            temp_filename_vuv=self.PATH+'/../tempfiles/tempVUV'+temp_uuid+'.txt'
            praat_vuv(audio, temp_filename_f0, temp_filename_vuv, time_stepF0=self.step, minf0=self.minf0, maxf0=self.maxf0)

            F0,_=decodeF0(temp_filename_f0,len(data_audio)/float(fs),self.step)
            os.remove(temp_filename_f0)
            os.remove(temp_filename_vuv)
        elif self.pitch_method == 'rapt':
            data_audiof=np.asarray(data_audio*(2**15), dtype=np.float32)
            F0=pysptk.sptk.rapt(data_audiof, fs, int(size_stepS), min=self.minf0, max=self.maxf0, voice_bias=self.voice_bias, otype='f0')


        #Find pitch contour of EACH voiced segment
        pitchON = np.where(F0!=0)[0]
        dchange = np.diff(pitchON)
        change = np.where(dchange>1)[0]
        iniV = pitchON[0]

        featvec = []
        iniVoiced = (pitchON[0]*size_stepS)+size_stepS#To compute energy
        seg_voiced=[]
        f0v=[]
        Ev=[]
        for indx in change:
            finV = pitchON[indx]+1
            finVoiced = (pitchON[indx]*size_stepS)+size_stepS#To compute energy
            VoicedSeg = data_audio[int(iniVoiced):int(finVoiced)]#To compute energy
            temp = F0[iniV:finV]
            tempvec = []
            if len(VoicedSeg)>int(size_frameS): #Take only segments greater than frame size
                seg_voiced.append(VoicedSeg)
                #Compute duration
                dur = len(VoicedSeg)/float(fs)
                tempvec.append(dur)
                #Pitch coefficients
                x = np.arange(0,len(temp))
                z = np.poly1d(np.polyfit(x,temp,self.P))
                f0v.append(temp)
                tempvec.extend(z.coeffs)
                #Energy coefficients
                temp = E_cont(VoicedSeg,size_frameS,size_stepS,overlap)
                Ev.append(temp)
                x = np.arange(0,len(temp))
                z = np.poly1d(np.polyfit(x,temp,self.P))
                tempvec.extend(z.coeffs)
                featvec.append(tempvec)
            iniV= pitchON[indx+1]
            iniVoiced = (pitchON[indx+1]*size_stepS)+size_stepS#To compute energy

        #Add the last voiced segment
        finV = (pitchON[len(pitchON)-1])
        finVoiced = (pitchON[len(pitchON)-1]*size_stepS)+size_stepS#To compute energy
        VoicedSeg = data_audio[int(iniVoiced):int(finVoiced)]#To compute energy
        temp = F0[iniV:finV]
        tempvec = []

        if len(VoicedSeg)>int(size_frameS): #Take only segments greater than frame size
            #Compute duration
            dur = len(VoicedSeg)/float(fs)
            tempvec.append(dur)
            x = np.arange(0,len(temp))
            z = np.poly1d(np.polyfit(x,temp,self.P))
            tempvec.extend(z.coeffs)
            #Energy coefficients
            temp = E_cont(VoicedSeg,size_frameS,size_stepS,overlap)
            x = np.arange(0,len(temp))
            z = np.poly1d(np.polyfit(x,temp,self.P))
            tempvec.extend(z.coeffs)
            #Compute duration
            featvec.append(tempvec)

        return np.asarray(featvec)

    def extract_features_path(self, path_audio, static=True, plots=False, fmt="npy", kaldi_file=""):
        """Extract the prosody features for audios inside a path

        :param path_audio: directory with (.wav) audio files inside, sampled at 16 kHz
        :param static: whether to compute and return statistic functionals over the feature matrix, or return the feature matrix computed over frames
        :param plots: timeshift to extract the features
        :param fmt: format to return the features (npy, dataframe, torch, kaldi)
        :param kaldi_file: file to store kaldifeatures, only valid when fmt=="kaldi"
        :returns: features computed from the audio file.

        >>> prosody=Prosody()
        >>> path_audio="../audios/"
        >>> features1=prosody.extract_features_path(path_audio, static=True, plots=False, fmt="npy")
        >>> features2=prosody.extract_features_path(path_audio, static=True, plots=False, fmt="csv")
        >>> features3=prosody.extract_features_path(path_audio, static=False, plots=True, fmt="torch")
        >>> prosody.extract_features_path(path_audio, static=False, plots=False, fmt="kaldi", kaldi_file="./test.ark")
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
        print("python prosody.py <file_or_folder_audio> <file_features> <static (true, false)> <plots (true,  false)> <format (csv, txt, npy, kaldi, torch)>")
        sys.exit()

    prosody=Prosody()
    script_manager(sys.argv, prosody)
