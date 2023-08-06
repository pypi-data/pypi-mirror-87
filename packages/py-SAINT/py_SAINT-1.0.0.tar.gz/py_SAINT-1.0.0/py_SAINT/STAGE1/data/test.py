import os #line:1
from ..data import srdata #line:2
class TEST (srdata .SRData ):#line:5
    def __init__ (OO00OOO0OO0O0000O ,OOO00O0000O0O0O00 ,name ='TEST',train =True ,):#line:6
        super (TEST ,OO00OOO0OO0O0000O ).__init__ (OOO00O0000O0O0O00 ,name =name ,train =train )#line:9
    def _scan (O00000OO0O0O0OO0O ):#line:11
        O00OOOO0OO00000O0 ,OO0O00000O0000O00 =super (TEST ,O00000OO0O0O0OO0O )._scan ()#line:12
        print ('@@@',len (O00OOOO0OO00000O0 ),len (OO0O00000O0000O00 ))#line:13
        O00OOOO0OO00000O0 =O00OOOO0OO00000O0 [O00000OO0O0O0OO0O .begin -1 :O00000OO0O0O0OO0O .end ]#line:14
        OO0O00000O0000O00 =OO0O00000O0000O00 [O00000OO0O0O0OO0O .begin -1 :O00000OO0O0O0OO0O .end ]#line:15
        return O00OOOO0OO00000O0 ,OO0O00000O0000O00 #line:16
    def _set_filesystem (O000000OO0OO0O0O0 ,OOOOO00000O00OOO0 ):#line:18
        super (TEST ,O000000OO0OO0O0O0 )._set_filesystem (OOOOO00000O00OOO0 )#line:19
        O000000OO0OO0O0O0 .dir_hr =os .path .join (O000000OO0OO0O0O0 .apath ,'HR')#line:20
        O000000OO0OO0O0O0 .dir_lr =os .path .join (O000000OO0OO0O0O0 .apath ,'LR')#line:21
