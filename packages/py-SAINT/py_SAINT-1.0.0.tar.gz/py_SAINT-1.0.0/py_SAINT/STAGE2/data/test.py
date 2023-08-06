import os #line:1
from ..data import srdata #line:2
class TEST (srdata .SRData ):#line:4
    def __init__ (O0OOOO000000000OO ,O0O0O000O00O0O000 ,name ='TEST',train =True ,):#line:5
        super (TEST ,O0OOOO000000000OO ).__init__ (O0O0O000O00O0O000 ,name =name ,train =train )#line:8
    def _scan (OOO0OO0O0O000OO0O ):#line:10
        OOO0O0OOOOO0OO0OO ,O00000OOOOOO00OOO =super (TEST ,OOO0OO0O0O000OO0O )._scan ()#line:11
        print ('@@@',len (OOO0O0OOOOO0OO0OO ),len (O00000OOOOOO00OOO ))#line:13
        OOO0O0OOOOO0OO0OO =OOO0O0OOOOO0OO0OO [OOO0OO0O0O000OO0O .begin -1 :OOO0OO0O0O000OO0O .end ]#line:14
        O00000OOOOOO00OOO =O00000OOOOOO00OOO [OOO0OO0O0O000OO0O .begin -1 :OOO0OO0O0O000OO0O .end ]#line:15
        return OOO0O0OOOOO0OO0OO ,O00000OOOOOO00OOO #line:16
    def _set_filesystem (OOO00OOO00O0OO0OO ,O0O0O00OOO0OOO0OO ):#line:18
        super (TEST ,OOO00OOO00O0OO0OO )._set_filesystem (O0O0O00OOO0OOO0OO )#line:19
        OOO00OOO00O0OO0OO .dir_hr =os .path .join (OOO00OOO00O0OO0OO .apath ,'HR')#line:20
        OOO00OOO00O0OO0OO .dir_lr =os .path .join (OOO00OOO00O0OO0OO .apath ,'LR')#line:21
