import sys #line:1
import threading #line:2
import queue #line:3
import random #line:4
import collections #line:5
import torch #line:7
import torch .multiprocessing as multiprocessing #line:8
from torch ._C import _set_worker_signal_handlers ,_update_worker_pids ,_remove_worker_pids ,_error_if_any_worker_fails #line:11
from torch .utils .data .dataloader import DataLoader #line:12
from torch .utils .data .dataloader import _DataLoaderIter #line:13
from torch .utils .data .dataloader import ExceptionWrapper #line:15
from torch .utils .data .dataloader import _use_shared_memory #line:16
from torch .utils .data .dataloader import _worker_manager_loop #line:17
from torch .utils .data .dataloader import numpy_type_map #line:18
from torch .utils .data .dataloader import default_collate #line:19
from torch .utils .data .dataloader import pin_memory_batch #line:20
from torch .utils .data .dataloader import _SIGCHLD_handler_set #line:21
from torch .utils .data .dataloader import _set_SIGCHLD_handler #line:22
if sys .version_info [0 ]==2 :#line:24
    import Queue as queue #line:25
else :#line:26
    import queue #line:27
def _O000O0OOO0O0O000O (OO0O0000OO0OO00O0 ,O00O000OO0O0000OO ,O000OO0O00OO0OOO0 ,OO000O0O000O00OO0 ,OOO00OO00000O0OO0 ,OOO0O0OOO0OOOO0O0 ,OOOOOO0OOO0OOO0OO ,O0OO000O0000OOOO0 ):#line:29
    global _use_shared_memory #line:30
    _use_shared_memory =True #line:31
    _set_worker_signal_handlers ()#line:32
    torch .set_num_threads (1 )#line:34
    torch .manual_seed (OOO0O0OOO0OOOO0O0 )#line:35
    while True :#line:36
        OO00OOO0O00OOO000 =O00O000OO0O0000OO .get ()#line:37
        if OO00OOO0O00OOO000 is None :#line:38
            break #line:39
        OO000O00OO00OOO00 ,O00000O000OOOOOO0 =OO00OOO0O00OOO000 #line:40
        try :#line:42
            OOOO00O00OOO00O00 =0 #line:43
            if len (OOO00OO00000O0OO0 )>1 and OO0O0000OO0OO00O0 .train :#line:44
                OOOO00O00OOO00O00 =random .randrange (0 ,len (OOO00OO00000O0OO0 ))#line:45
                OO0O0000OO0OO00O0 .set_scale (OOOO00O00OOO00O00 )#line:46
            O0O000OO00O00000O =OO000O0O000O00OO0 ([OO0O0000OO0OO00O0 [O000OO0OO00O0OO00 ]for O000OO0OO00O0OO00 in O00000O000OOOOOO0 ])#line:49
            O0O000OO00O00000O .append (OOOO00O00OOO00O00 )#line:50
        except Exception :#line:52
            O000OO0O00OO0OOO0 .put ((OO000O00OO00OOO00 ,ExceptionWrapper (sys .exc_info ())))#line:53
        else :#line:54
            O000OO0O00OO0OOO0 .put ((OO000O00OO00OOO00 ,O0O000OO00O00000O ))#line:55
class _OOOOOOOO0OOOO0000 (_DataLoaderIter ):#line:57
    def __init__ (O00O0OOO00OOOO000 ,OOOOO0OOO00O0O00O ):#line:58
        O00O0OOO00OOOO000 .dataset =OOOOO0OOO00O0O00O .dataset #line:59
        O00O0OOO00OOOO000 .scale =OOOOO0OOO00O0O00O .scale #line:60
        O00O0OOO00OOOO000 .collate_fn =OOOOO0OOO00O0O00O .collate_fn #line:61
        O00O0OOO00OOOO000 .batch_sampler =OOOOO0OOO00O0O00O .batch_sampler #line:62
        O00O0OOO00OOOO000 .num_workers =OOOOO0OOO00O0O00O .num_workers #line:63
        O00O0OOO00OOOO000 .pin_memory =OOOOO0OOO00O0O00O .pin_memory and torch .cuda .is_available ()#line:64
        O00O0OOO00OOOO000 .timeout =OOOOO0OOO00O0O00O .timeout #line:65
        O00O0OOO00OOOO000 .done_event =threading .Event ()#line:66
        print ("_MSDataLodaerIter--len(dataset)",len (OOOOO0OOO00O0O00O .dataset ))#line:67
        O00O0OOO00OOOO000 .sample_iter =iter (O00O0OOO00OOOO000 .batch_sampler )#line:68
        if O00O0OOO00OOOO000 .num_workers >0 :#line:70
            O00O0OOO00OOOO000 .worker_init_fn =OOOOO0OOO00O0O00O .worker_init_fn #line:71
            O00O0OOO00OOOO000 .index_queues =[multiprocessing .Queue ()for _O00OOOOO0OO000O00 in range (O00O0OOO00OOOO000 .num_workers )]#line:74
            O00O0OOO00OOOO000 .worker_queue_idx =0 #line:75
            O00O0OOO00OOOO000 .worker_result_queue =multiprocessing .SimpleQueue ()#line:76
            O00O0OOO00OOOO000 .batches_outstanding =0 #line:77
            O00O0OOO00OOOO000 .worker_pids_set =False #line:78
            O00O0OOO00OOOO000 .shutdown =False #line:79
            O00O0OOO00OOOO000 .send_idx =0 #line:80
            O00O0OOO00OOOO000 .rcvd_idx =0 #line:81
            O00O0OOO00OOOO000 .reorder_dict ={}#line:82
            O0000OO000O0O000O =torch .LongTensor (1 ).random_ ()[0 ]#line:84
            O00O0OOO00OOOO000 .workers =[multiprocessing .Process (target =_O000O0OOO0O0O000O ,args =(O00O0OOO00OOOO000 .dataset ,O00O0OOO00OOOO000 .index_queues [O000O00O0O00O00OO ],O00O0OOO00OOOO000 .worker_result_queue ,O00O0OOO00OOOO000 .collate_fn ,O00O0OOO00OOOO000 .scale ,O0000OO000O0O000O +O000O00O0O00O00OO ,O00O0OOO00OOOO000 .worker_init_fn ,O000O00O0O00O00OO ))for O000O00O0O00O00OO in range (O00O0OOO00OOOO000 .num_workers )]#line:99
            if O00O0OOO00OOOO000 .pin_memory or O00O0OOO00OOOO000 .timeout >0 :#line:101
                O00O0OOO00OOOO000 .data_queue =queue .Queue ()#line:102
                if O00O0OOO00OOOO000 .pin_memory :#line:103
                    OO00O00O00O0O0OO0 =torch .cuda .current_device ()#line:104
                else :#line:105
                    OO00O00O00O0O0OO0 =None #line:107
                O00O0OOO00OOOO000 .worker_manager_thread =threading .Thread (target =_worker_manager_loop ,args =(O00O0OOO00OOOO000 .worker_result_queue ,O00O0OOO00OOOO000 .data_queue ,O00O0OOO00OOOO000 .done_event ,O00O0OOO00OOOO000 .pin_memory ,OO00O00O00O0O0OO0 ))#line:111
                O00O0OOO00OOOO000 .worker_manager_thread .daemon =True #line:112
                O00O0OOO00OOOO000 .worker_manager_thread .start ()#line:113
            else :#line:114
                O00O0OOO00OOOO000 .data_queue =O00O0OOO00OOOO000 .worker_result_queue #line:115
            for OO00OOO0000000O0O in O00O0OOO00OOOO000 .workers :#line:117
                OO00OOO0000000O0O .daemon =True #line:118
                OO00OOO0000000O0O .start ()#line:119
            _update_worker_pids (id (O00O0OOO00OOOO000 ),tuple (OO0O0O0000O0000OO .pid for OO0O0O0000O0000OO in O00O0OOO00OOOO000 .workers ))#line:121
            _set_SIGCHLD_handler ()#line:122
            O00O0OOO00OOOO000 .worker_pids_set =True #line:123
            for _OO0000O0O0O0000O0 in range (2 *O00O0OOO00OOOO000 .num_workers ):#line:126
                O00O0OOO00OOOO000 ._put_indices ()#line:127
class MSDataLoader (DataLoader ):#line:129
    def __init__ (O00OOO0OOO0O0OO00 ,O0OOOO0O0O000O0O0 ,OOOOO00O0O0O0000O ,batch_size =1 ,shuffle =False ,sampler =None ,batch_sampler =None ,collate_fn =default_collate ,pin_memory =False ,drop_last =False ,timeout =0 ,worker_init_fn =None ):#line:134
        super (MSDataLoader ,O00OOO0OOO0O0OO00 ).__init__ (OOOOO00O0O0O0000O ,batch_size =batch_size ,shuffle =shuffle ,sampler =sampler ,batch_sampler =batch_sampler ,num_workers =O0OOOO0O0O000O0O0 .n_threads ,collate_fn =collate_fn ,pin_memory =pin_memory ,drop_last =drop_last ,timeout =timeout ,worker_init_fn =worker_init_fn )#line:141
        O00OOO0OOO0O0OO00 .scale =O0OOOO0O0O000O0O0 .scale #line:143
    def __iter__ (OO0OOOOO00O000O0O ):#line:145
        return _OOOOOOOO0OOOO0000 (OO0OOOOO00O000O0O )#line:146
