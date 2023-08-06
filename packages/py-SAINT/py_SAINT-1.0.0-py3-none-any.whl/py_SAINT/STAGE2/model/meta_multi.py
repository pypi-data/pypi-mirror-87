from ..model import common #line:4
import torch #line:6
import torch .nn as nn #line:7
def make_model (args ,parent =False ):#line:10
    return RDN3D (args )#line:11
class RDB_Conv (nn .Module ):#line:13
    def __init__ (self ,inChannels ,growRate ,kSize =3 ):#line:14
        super (RDB_Conv ,self ).__init__ ()#line:15
        O00OO0000OOO00O00 =inChannels #line:16
        OO0O0O0OOOOO00O00 =growRate #line:17
        self .conv =nn .Sequential (*[nn .Conv3d (O00OO0000OOO00O00 ,OO0O0O0OOOOO00O00 ,(3 ,3 ,1 ),padding =(1 ,1 ,0 ),stride =1 ),nn .ReLU ()])#line:21
    def forward (self ,x ):#line:23
        OO0O00OOOOO0O0OO0 =self .conv (x )#line:24
        return torch .cat ((x ,OO0O00OOOOO0O0OO0 ),1 )#line:25
class RDB (nn .Module ):#line:28
    def __init__ (self ,growRate0 ,growRate ,nConvLayers ,kSize =3 ):#line:29
        super (RDB ,self ).__init__ ()#line:30
        O00O00OOO0OO00O0O =growRate0 #line:31
        OOO0O0000OO000000 =growRate #line:32
        O00OO0OOO0O00O00O =nConvLayers #line:33
        OO00O0O0000O0O00O =[]#line:35
        for O0OOOOOO000O00OOO in range (O00OO0OOO0O00O00O ):#line:36
            OO00O0O0000O0O00O .append (RDB_Conv (O00O00OOO0OO00O0O +O0OOOOOO000O00OOO *OOO0O0000OO000000 ,OOO0O0000OO000000 ))#line:37
        self .convs =nn .Sequential (*OO00O0O0000O0O00O )#line:38
        self .LFF =nn .Conv3d (O00O00OOO0OO00O0O +O00OO0OOO0O00O00O *OOO0O0000OO000000 ,O00O00OOO0OO00O0O ,1 ,padding =0 ,stride =1 )#line:41
    def forward (self ,x ):#line:43
        return self .LFF (self .convs (x ))+x #line:44
class RDN3D (nn .Module ):#line:47
    def __init__ (self ,args ):#line:48
        super (RDN3D ,self ).__init__ ()#line:49
        O0O000O0O00OO00OO =args .scale [0 ]#line:50
        OO0O00O000O0000OO =64 #line:51
        O000OO000000OO0OO =args .RDNkSize #line:52
        self .D ,O00O0OO0OOO0O000O ,O0OO000OO0O0000OO ={'A':(20 ,6 ,32 ),'B':(16 ,8 ,64 ),'C':(4 ,6 ,12 ),'D':(5 ,4 ,12 )}[args .RDNconfig ]#line:60
        self .SFENet1 =nn .Conv3d (2 ,OO0O00O000O0000OO ,(3 ,3 ,1 ),padding =(1 ,1 ,0 ),stride =1 )#line:63
        self .SFENet2 =nn .Conv3d (OO0O00O000O0000OO ,OO0O00O000O0000OO ,(3 ,3 ,1 ),padding =(1 ,1 ,0 ),stride =1 )#line:64
        self .RDBs =nn .ModuleList ()#line:67
        for O0O00O0O0O0000O00 in range (self .D ):#line:68
            self .RDBs .append (RDB (growRate0 =OO0O00O000O0000OO ,growRate =O0OO000OO0O0000OO ,nConvLayers =O00O0OO0OOO0O000O ))#line:71
        self .GFF =nn .Sequential (*[nn .Conv3d (self .D *OO0O00O000O0000OO ,OO0O00O000O0000OO ,1 ,padding =0 ,stride =1 ),nn .Conv3d (OO0O00O000O0000OO ,OO0O00O000O0000OO ,(3 ,3 ,1 ),padding =(1 ,1 ,0 ),stride =1 )])#line:77
        self .UPNet =nn .Sequential (*[nn .Conv3d (OO0O00O000O0000OO ,1 ,(3 ,3 ,1 ),padding =(1 ,1 ,0 ),stride =1 )])#line:82
    def forward (self ,x ):#line:84
        O0O00O0OO0000O0O0 =self .SFENet1 (x )#line:85
        OOOO0O000O000OO00 =self .SFENet2 (O0O00O0OO0000O0O0 )#line:86
        OOO0OO0O0OO0000OO =[]#line:88
        for O00O0O0000O000000 in range (self .D ):#line:89
            OOOO0O000O000OO00 =self .RDBs [O00O0O0000O000000 ](OOOO0O000O000OO00 )#line:90
            OOO0OO0O0OO0000OO .append (OOOO0O000O000OO00 )#line:91
        OOOO0O000O000OO00 =self .GFF (torch .cat (OOO0OO0O0OO0000OO ,1 ))#line:93
        OOOO0O000O000OO00 +=O0O00O0OO0000O0O0 #line:94
        return self .UPNet (OOOO0O000O000OO00 )+x .mean (1 ).view (x .size (0 ),-1 ,x .size (2 ),x .size (3 ),x .size (4 ))#line:96
