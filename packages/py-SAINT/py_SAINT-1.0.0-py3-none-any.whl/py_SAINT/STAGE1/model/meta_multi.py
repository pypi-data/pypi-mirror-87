import torch #line:1
import torch .nn as nn #line:2
import torch .nn .functional as F #line:3
def make_model (args ,parent =False ):#line:5
    return MSR_RDN (args )#line:6
def get_org_mask (dim ):#line:9
    OO0OOOO0OOO00O0O0 =dim [1 ]+1 #line:10
    O0O0OO0O0O0OO00O0 =dim [3 ]*OO0OOOO0OOO00O0O0 #line:11
    O0O0OOO0O00O0OO0O =torch .LongTensor (list (range (0 ,O0O0OO0O0O0OO00O0 )))#line:12
    O0OOO0OO00000O0OO =O0O0OOO0O00O0OO0O [::dim [3 ]]#line:13
    for O00O0OO0OOO00O00O in range (dim [3 ]-1 ):#line:14
        O0OOO0OO00000O0OO =torch .cat ((O0OOO0OO00000O0OO ,O0O0OOO0O00O0OO0O [O00O0OO0OOO00O00O +1 :][::dim [3 ]]))#line:15
    return O0OOO0OO00000O0OO #line:16
class RDB_Conv (nn .Module ):#line:18
    def __init__ (self ,inChannels ,growRate ,kSize =3 ):#line:19
        super (RDB_Conv ,self ).__init__ ()#line:20
        OO0OO000000OOO0O0 =inChannels #line:21
        OOO0OO0000OOO0O00 =growRate #line:22
        self .conv =nn .Sequential (*[nn .Conv2d (OO0OO000000OOO0O0 ,OOO0OO0000OOO0O00 ,kSize ,padding =(kSize -1 )//2 ,stride =1 ),nn .ReLU ()])#line:26
    def forward (self ,x ):#line:28
        OOOOOOO0O0000OOO0 =self .conv (x )#line:29
        return torch .cat ((x ,OOOOOOO0O0000OOO0 ),1 )#line:30
class RDB (nn .Module ):#line:33
    def __init__ (self ,growRate0 ,growRate ,nConvLayers ,kSize =3 ):#line:34
        super (RDB ,self ).__init__ ()#line:35
        O0O00000O00O0OO00 =growRate0 #line:36
        O0O0OOOO000O0OOO0 =growRate #line:37
        OO00OOO00000000OO =nConvLayers #line:38
        OO0O0O0000O0OOOO0 =[]#line:40
        for O00000O00OOOO0O0O in range (OO00OOO00000000OO ):#line:41
            OO0O0O0000O0OOOO0 .append (RDB_Conv (O0O00000O00O0OO00 +O00000O00OOOO0O0O *O0O0OOOO000O0OOO0 ,O0O0OOOO000O0OOO0 ))#line:42
        self .convs =nn .Sequential (*OO0O0O0000O0OOOO0 )#line:43
        self .LFF =nn .Conv2d (O0O00000O00O0OO00 +OO00OOO00000000OO *O0O0OOOO000O0OOO0 ,O0O00000O00O0OO00 ,1 ,padding =0 ,stride =1 )#line:46
    def forward (self ,x ):#line:48
        return self .LFF (self .convs (x ))+x #line:49
class GenWeights (nn .Module ):#line:51
    def __init__ (self ,inpC =64 ,kernel_size =3 ,outC =32 ):#line:52
        super (GenWeights ,self ).__init__ ()#line:53
        self .kernel_size =kernel_size #line:54
        self .outC =outC #line:55
        self .inpC =inpC #line:56
        self .meta_block =nn .Sequential (nn .Conv2d (1 ,32 ,3 ,padding =(3 -1 )//2 ,stride =1 ),nn .ReLU (inplace =True ),nn .Conv2d (32 ,64 ,3 ,padding =(3 -1 )//2 ,stride =1 ),nn .ReLU (inplace =True ),nn .Conv2d (64 ,64 ,3 ,padding =(3 -1 )//2 ,stride =1 ),nn .ReLU (inplace =True ),nn .Conv2d (64 ,64 ,3 ,padding =(3 -1 )//2 ,stride =1 ),nn .ReLU (inplace =True ),nn .Conv2d (64 ,64 ,3 ,padding =(3 -1 )//2 ,stride =1 ))#line:67
    def forward (self ,x ):#line:68
        O0000OOOOOOOO000O =self .meta_block (x )#line:69
        return O0000OOOOOOOO000O #line:70
class MSR_RDN (nn .Module ):#line:73
    def __init__ (self ,args ):#line:74
        super (MSR_RDN ,self ).__init__ ()#line:75
        O00OO0OOOOOOO0000 =args .G0 #line:76
        OO00O000O0OO0OOO0 =args .RDNkSize #line:77
        self .D ,O000OO0O00O00OO0O ,O00OOOOO0000O000O ={'A':(20 ,6 ,32 ),'B':(16 ,8 ,64 ),'C':(6 ,8 ,32 ),'D':(2 ,8 ,32 )}[args .RDNconfig ]#line:85
        self .SFENet1 =nn .Conv2d (3 ,O00OO0OOOOOOO0000 ,OO00O000O0OO0OOO0 ,padding =(OO00O000O0OO0OOO0 -1 )//2 ,stride =1 )#line:88
        self .SFENet2 =nn .Conv2d (O00OO0OOOOOOO0000 ,O00OO0OOOOOOO0000 ,OO00O000O0OO0OOO0 ,padding =(OO00O000O0OO0OOO0 -1 )//2 ,stride =1 )#line:89
        self .RDBs =nn .ModuleList ()#line:92
        for OOOO0OO00OOO00OO0 in range (self .D ):#line:93
            self .RDBs .append (RDB (growRate0 =O00OO0OOOOOOO0000 ,growRate =O00OOOOO0000O000O ,nConvLayers =O000OO0O00O00OO0O ))#line:96
        self .GFF =nn .Sequential (*[nn .Conv2d (self .D *O00OO0OOOOOOO0000 ,O00OO0OOOOOOO0000 ,1 ,padding =0 ,stride =1 ),nn .Conv2d (O00OO0OOOOOOO0000 ,O00OO0OOOOOOO0000 ,OO00O000O0OO0OOO0 ,padding =(OO00O000O0OO0OOO0 -1 )//2 ,stride =1 )])#line:102
        self .GW =GenWeights ()#line:103
    def forward (self ,inp_x ,dist ):#line:110
        O000O00000OO0O0O0 =self .SFENet1 (inp_x )#line:111
        OO000000O0O00O00O =self .SFENet2 (O000O00000OO0O0O0 )#line:112
        OO0O0OOO0OO0O0O00 =[]#line:113
        for OOOOOO00O00O000O0 in range (self .D ):#line:114
            OO000000O0O00O00O =self .RDBs [OOOOOO00O00O000O0 ](OO000000O0O00O00O )#line:115
            OO0O0OOO0OO0O0O00 .append (OO000000O0O00O00O )#line:116
        OO000000O0O00O00O =self .GFF (torch .cat (OO0O0OOO0OO0O0O00 ,1 ))#line:117
        OO000000O0O00O00O +=O000O00000OO0O0O0 #line:118
        for OOOOOO00O00O000O0 in range (int (dist .size (1 ))):#line:123
            if OOOOOO00O00O000O0 ==0 :#line:124
                OOOO0OOOO0O0O0O00 =self .GW (dist [:,[OOOOOO00O00O000O0 ],:,:]).view (OO000000O0O00O00O .size (0 ),1 ,64 ,3 ,3 )#line:125
            else :#line:126
                OOOO0OOOO0O0O0O00 =torch .cat ((OOOO0OOOO0O0O0O00 ,self .GW (dist [:,[OOOOOO00O00O000O0 ],:,:]).view (OO000000O0O00O00O .size (0 ),1 ,64 ,3 ,3 )),1 )#line:127
        OO00O0OOOOO0OOO0O =nn .functional .unfold (OO000000O0O00O00O ,3 ,padding =1 )#line:128
        O0O0OO0OOOO0O0000 =OO00O0OOOOO0OOO0O .transpose (1 ,2 ).matmul (OOOO0OOOO0O0O0O00 .view (OOOO0OOOO0O0O0O00 .size (0 ),OOOO0OOOO0O0O0O00 .size (1 ),-1 ).transpose (1 ,2 )).transpose (1 ,2 )#line:130
        O0O0OO0OOOO0O0000 =O0O0OO0OOOO0O0000 .view (-1 ,dist .size (1 ),OO000000O0O00O00O .size (2 ),OO000000O0O00O00O .size (3 ))#line:131
        return O0O0OO0OOOO0O0000 #line:134
