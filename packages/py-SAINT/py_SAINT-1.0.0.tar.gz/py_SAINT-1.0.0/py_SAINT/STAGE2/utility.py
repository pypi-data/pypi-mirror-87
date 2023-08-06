import os #line:1
import math #line:2
import time #line:3
import datetime #line:4
from functools import reduce #line:5
import matplotlib #line:7
matplotlib .use ('Agg')#line:8
import matplotlib .pyplot as plt #line:9
import numpy as np #line:11
import scipy .misc as misc #line:12
import pickle #line:13
import torch #line:14
import torch .optim as optim #line:15
import torch .optim .lr_scheduler as lrs #line:16
class timer ():#line:18
    def __init__ (O0O0OOOOO000O0OO0 ):#line:19
        O0O0OOOOO000O0OO0 .acc =0 #line:20
        O0O0OOOOO000O0OO0 .tic ()#line:21
    def tic (O0000OO0O00000O00 ):#line:23
        O0000OO0O00000O00 .t0 =time .time ()#line:24
    def toc (O00O0000O000O0000 ):#line:26
        return time .time ()-O00O0000O000O0000 .t0 #line:27
    def hold (O00OO000OO0O0OOOO ):#line:29
        O00OO000OO0O0OOOO .acc +=O00OO000OO0O0OOOO .toc ()#line:30
    def release (O00OO00O00O00O00O ):#line:32
        OOO0000OO000O0000 =O00OO00O00O00O00O .acc #line:33
        O00OO00O00O00O00O .acc =0 #line:34
        return OOO0000OO000O0000 #line:36
    def reset (OO0OO0000OOO0OO0O ):#line:38
        OO0OO0000OOO0OO0O .acc =0 #line:39
class checkpoint ():#line:41
    def __init__ (O0OOO00O0OO0OOO0O ,OO00OO0O0OO0OO00O ):#line:42
        O0OOO00O0OO0OOO0O .args =OO00OO0O0OO0OO00O #line:43
        O0OOO00O0OO0OOO0O .ok =True #line:44
        O0OOO00O0OO0OOO0O .log =torch .Tensor ()#line:45
        O00O00O0O0OO00O0O =datetime .datetime .now ().strftime ('%Y-%m-%d-%H:%M:%S')#line:46
        if OO00OO0O0OO0OO00O .load =='.':#line:48
            if OO00OO0O0OO0OO00O .save =='.':OO00OO0O0OO0OO00O .save =O00O00O0O0OO00O0O #line:49
            O0OOO00O0OO0OOO0O .dir =OO00OO0O0OO0OO00O .save #line:50
        else :#line:51
            O0OOO00O0OO0OOO0O .dir ='../experiment/'+OO00OO0O0OO0OO00O .load #line:52
            if not os .path .exists (O0OOO00O0OO0OOO0O .dir ):#line:53
                OO00OO0O0OO0OO00O .load ='.'#line:54
            else :#line:55
                O0OOO00O0OO0OOO0O .log =torch .load (O0OOO00O0OO0OOO0O .dir +'/psnr_log.pt')#line:56
                print ('Continue from epoch {}...'.format (len (O0OOO00O0OO0OOO0O .log )))#line:57
        if OO00OO0O0OO0OO00O .reset :#line:59
            os .system ('rm -rf '+O0OOO00O0OO0OOO0O .dir )#line:60
            OO00OO0O0OO0OO00O .load ='.'#line:61
        def _OO0OO00O0OO0000OO (OO0OO0O00OOO0OOO0 ):#line:63
            if not os .path .exists (OO0OO0O00OOO0OOO0 ):os .makedirs (OO0OO0O00OOO0OOO0 )#line:64
        _OO0OO00O0OO0000OO (O0OOO00O0OO0OOO0O .dir )#line:66
        _OO0OO00O0OO0000OO (O0OOO00O0OO0OOO0O .dir +'/model')#line:67
        _OO0OO00O0OO0000OO (O0OOO00O0OO0OOO0O .dir +'/results')#line:68
        OO00O000O0000O00O ='a'if os .path .exists (O0OOO00O0OO0OOO0O .dir +'/log.txt')else 'w'#line:70
        O0OOO00O0OO0OOO0O .log_file =open (O0OOO00O0OO0OOO0O .dir +'/log.txt',OO00O000O0000O00O )#line:71
        with open (O0OOO00O0OO0OOO0O .dir +'/config.txt',OO00O000O0000O00O )as O0OO000OOOO00O0OO :#line:72
            O0OO000OOOO00O0OO .write (O00O00O0O0OO00O0O +'\n\n')#line:73
            for OOO00O0OO000O0O00 in vars (OO00OO0O0OO0OO00O ):#line:74
                O0OO000OOOO00O0OO .write ('{}: {}\n'.format (OOO00O0OO000O0O00 ,getattr (OO00OO0O0OO0OO00O ,OOO00O0OO000O0O00 )))#line:75
            O0OO000OOOO00O0OO .write ('\n')#line:76
    def save (O00OO0O0OO0O0O0O0 ,OO000O0O0O00O0OO0 ,O0O0000O00OOO0O00 ,is_best =False ):#line:78
        OO000O0O0O00O0OO0 .model .save (O00OO0O0OO0O0O0O0 .dir ,O0O0000O00OOO0O00 ,is_best =is_best )#line:79
        OO000O0O0O00O0OO0 .loss .save (O00OO0O0OO0O0O0O0 .dir )#line:80
        OO000O0O0O00O0OO0 .loss .plot_loss (O00OO0O0OO0O0O0O0 .dir ,O0O0000O00OOO0O00 )#line:81
        O00OO0O0OO0O0O0O0 .plot_psnr (O0O0000O00OOO0O00 )#line:83
        torch .save (O00OO0O0OO0O0O0O0 .log ,os .path .join (O00OO0O0OO0O0O0O0 .dir ,'psnr_log.pt'))#line:84
        torch .save (OO000O0O0O00O0OO0 .optimizer .state_dict (),os .path .join (O00OO0O0OO0O0O0O0 .dir ,'optimizer.pt'))#line:88
    def save_train (OOOOO000OOO0O0O0O ,O0OOO0OOO0000OOO0 ,O00O0OO0OO00OOOO0 ):#line:90
        O0OOO0OOO0000OOO0 .model .save (OOOOO000OOO0O0O0O .dir ,O00O0OO0OO00OOOO0 )#line:91
        torch .save (OOOOO000OOO0O0O0O .log ,os .path .join (OOOOO000OOO0O0O0O .dir ,'psnr_log.pt'))#line:92
        torch .save (O0OOO0OOO0000OOO0 .optimizer .state_dict (),os .path .join (OOOOO000OOO0O0O0O .dir ,'optimizer.pt'))#line:96
    def add_log (OOOOO0O0O00OOOO00 ,O0OOO0000O00OOO0O ):#line:98
        OOOOO0O0O00OOOO00 .log =torch .cat ([OOOOO0O0O00OOOO00 .log ,O0OOO0000O00OOO0O ])#line:99
    def write_log (O00000O0O000OOO0O ,O0OO0O000O000OO0O ,refresh =False ):#line:101
        print (O0OO0O000O000OO0O )#line:102
        O00000O0O000OOO0O .log_file .write (O0OO0O000O000OO0O +'\n')#line:103
        if refresh :#line:104
            O00000O0O000OOO0O .log_file .close ()#line:105
            O00000O0O000OOO0O .log_file =open (O00000O0O000OOO0O .dir +'/log.txt','a')#line:106
    def done (O0O0O000000000OOO ):#line:108
        O0O0O000000000OOO .log_file .close ()#line:109
    def plot_psnr (O000O00OO00OO0O00 ,OOOO0000OOO0000O0 ):#line:111
        OOOOO0O0OO0O0OOO0 =np .linspace (1 ,OOOO0000OOO0000O0 ,OOOO0000OOO0000O0 )#line:112
        OO0OOO00O0O0OOO0O ='SR on {}'.format (O000O00OO00OO0O00 .args .data_test )#line:113
        OOOO00OOOOOOO00OO =plt .figure ()#line:114
        plt .title (OO0OOO00O0O0OOO0O )#line:115
        for OOOO0000O0O0O0OO0 ,OO00O00O0O0O00O00 in enumerate (O000O00OO00OO0O00 .args .scale ):#line:116
            plt .plot (OOOOO0O0OO0O0OOO0 ,O000O00OO00OO0O00 .log [:,OOOO0000O0O0O0OO0 ].numpy (),label ='Scale {}'.format (OO00O00O0O0O00O00 ))#line:121
        plt .legend ()#line:122
        plt .xlabel ('Epochs')#line:123
        plt .ylabel ('PSNR')#line:124
        plt .grid (True )#line:125
        plt .savefig ('{}/test_{}.pdf'.format (O000O00OO00OO0O00 .dir ,O000O00OO00OO0O00 .args .data_test ))#line:126
        plt .close (OOOO00OOOOOOO00OO )#line:127
    def save_results (O00OO00O0000O0OO0 ,O0OO00OO0OO000000 ,O0O000000O0O000OO ,O0OO0OO0000O000OO ):#line:129
        OOOO00000O0OOOOO0 =('SR','LR','HR','NUM')#line:131
        if not os .path .isdir ('{}/results/raw/'.format (O00OO00O0000O0OO0 .dir )):#line:132
            os .mkdir ('{}/results/raw/'.format (O00OO00O0000O0OO0 .dir ))#line:133
        if not os .path .isdir ('{}/results/img/'.format (O00OO00O0000O0OO0 .dir )):#line:134
            os .mkdir ('{}/results/img/'.format (O00OO00O0000O0OO0 .dir ))#line:135
        for OO0O0O0OOOO0000O0 ,OOO0OO0O0O0O0000O in zip (O0O000000O0O000OO ,OOOO00000O0OOOOO0 ):#line:136
            O0000OOO0OO0O000O =np .clip (OO0O0O0OOOO0000O0 [0 ][0 ],-1024 ,4000 ).round ().astype ('int16')#line:139
            O00O0OO000OO0OOO0 ='{}/results/raw/{}_x{}_'.format (O00OO00O0000O0OO0 .dir ,O0OO00OO0OO000000 ,O0OO0OO0000O000OO )#line:144
            OOO00O0O0OO0O0OO0 ='{}/results/img/{}_x{}_'.format (O00OO00O0000O0OO0 .dir ,O0OO00OO0OO000000 ,O0OO0OO0000O000OO )#line:145
            pickle .dump (O0000OOO0OO0O000O ,open ('{}{}.pt'.format (O00O0OO000OO0OOO0 ,OOO0OO0O0O0O0000O ),'wb'))#line:146
def quantize (O00OO00O0O00O000O ,OO00O0O000OO0OO00 ):#line:151
    O0O0OOOO00O0OOO00 =255 /OO00O0O000OO0OO00 #line:152
    return O00OO00O0O00O000O .mul (O0O0OOOO00O0OOO00 ).clamp (0 ,255 ).round ().div (O0O0OOOO00O0OOO00 )#line:153
def calc_psnr (OO00OO0OO0OOOOOOO ,OO000O000OOOOO0O0 ,O0000O0OO0O0OO0OO ,O00O000O00000OO00 ):#line:155
    print (OO000O000OOOOO0O0 .shape ,O0000O0OO0O0OO0OO .shape )#line:157
    O00OOOO000O000O00 =OO000O000OOOOO0O0 [0 ]/4000 #line:158
    O0000OO0OOO000OOO =O0000O0OO0O0OO0OO [0 ]/4000 #line:159
    O00OOOO000O000O00 =np .clip (O00OOOO000O000O00 ,O0000OO0OOO000OOO .min (),O0000OO0OOO000OOO .max ())#line:160
    OOOOO0000OO00OOO0 =1 #line:164
    for O00OOOOOO00OOO0OO in O0000OO0OOO000OOO .shape :#line:165
        OOOOO0000OO00OOO0 =OOOOO0000OO00OOO0 *O00OOOOOO00OOO0OO #line:166
    O0000OO0O0OO000OO =np .square ((O00OOOO000O000O00 -O0000OO0OOO000OOO )).sum ()/OOOOO0000OO00OOO0 #line:167
    if O0000OO0O0OO000OO ==0.0 :#line:168
        print ('same_vol')#line:169
        return 0 #line:170
    OO000OOOOOO00OOO0 =10 *np .log10 (1 /O0000OO0O0OO000OO )#line:171
    return OO000OOOOOO00OOO0 #line:173
def make_optimizer (OO0OOO0OO00O00000 ,OO000O000O0O0OOO0 ):#line:175
    O00OOOO0O0OOOO0OO =filter (lambda OOOOOO00OO0O0O0OO :OOOOOO00OO0O0O0OO .requires_grad ,OO000O000O0O0OOO0 .parameters ())#line:176
    if OO0OOO0OO00O00000 .optimizer =='SGD':#line:178
        OOOO0OOO00O0O0OO0 =optim .SGD #line:179
        O0O00OOO0OO0000OO ={'momentum':OO0OOO0OO00O00000 .momentum }#line:180
    elif OO0OOO0OO00O00000 .optimizer =='ADAM':#line:181
        OOOO0OOO00O0O0OO0 =optim .Adam #line:182
        O0O00OOO0OO0000OO ={'betas':(OO0OOO0OO00O00000 .beta1 ,OO0OOO0OO00O00000 .beta2 ),'eps':OO0OOO0OO00O00000 .epsilon }#line:186
    elif OO0OOO0OO00O00000 .optimizer =='RMSprop':#line:187
        OOOO0OOO00O0O0OO0 =optim .RMSprop #line:188
        O0O00OOO0OO0000OO ={'eps':OO0OOO0OO00O00000 .epsilon }#line:189
    O0O00OOO0OO0000OO ['lr']=OO0OOO0OO00O00000 .lr #line:191
    O0O00OOO0OO0000OO ['weight_decay']=OO0OOO0OO00O00000 .weight_decay #line:192
    return OOOO0OOO00O0O0OO0 (O00OOOO0O0OOOO0OO ,**O0O00OOO0OO0000OO )#line:194
def make_scheduler (O0O0O0O0O00O0OOOO ,O0OO0OO000OOO0OOO ):#line:196
    if O0O0O0O0O00O0OOOO .decay_type =='step':#line:197
        OOO0O00000OO0OOO0 =lrs .StepLR (O0OO0OO000OOO0OOO ,step_size =O0O0O0O0O00O0OOOO .lr_decay ,gamma =O0O0O0O0O00O0OOOO .gamma )#line:202
    elif O0O0O0O0O00O0OOOO .decay_type .find ('step')>=0 :#line:203
        O0O0O00O000OO00OO =O0O0O0O0O00O0OOOO .decay_type .split ('_')#line:204
        O0O0O00O000OO00OO .pop (0 )#line:205
        O0O0O00O000OO00OO =list (map (lambda OO0O000OOO0000OOO :int (OO0O000OOO0000OOO ),O0O0O00O000OO00OO ))#line:206
        OOO0O00000OO0OOO0 =lrs .MultiStepLR (O0OO0OO000OOO0OOO ,milestones =O0O0O00O000OO00OO ,gamma =O0O0O0O0O00O0OOOO .gamma )#line:211
    return OOO0O00000OO0OOO0 #line:213
