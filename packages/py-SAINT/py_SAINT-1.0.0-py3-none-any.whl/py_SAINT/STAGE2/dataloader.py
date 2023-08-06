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
def _O00OO0O00OOOOO00O (OOO00000OO0OO00O0 ,OO000O0OOOOO0000O ,OO00OOO0O00OO0OO0 ,OO0O0000OO0O0O0O0 ,OO00O00O00OOOO00O ,OOO0000OO0OOOO0OO ,O0OO00OO0000O0OOO ,OOOOOOO0O0O0000O0 ):#line:29
    global _use_shared_memory #line:30
    _use_shared_memory =True #line:31
    _set_worker_signal_handlers ()#line:32
    torch .set_num_threads (1 )#line:34
    torch .manual_seed (OOO0000OO0OOOO0OO )#line:35
    while True :#line:36
        OO0O0OO0OOOO000OO =OO000O0OOOOO0000O .get ()#line:37
        if OO0O0OO0OOOO000OO is None :#line:38
            break #line:39
        O00OO00OO0O0000O0 ,OOO00OO00O000000O =OO0O0OO0OOOO000OO #line:40
        try :#line:42
            OO0OO00000OOOO0O0 =0 #line:43
            if len (OO00O00O00OOOO00O )>1 and OOO00000OO0OO00O0 .train :#line:44
                OO0OO00000OOOO0O0 =random .randrange (0 ,len (OO00O00O00OOOO00O ))#line:45
                OOO00000OO0OO00O0 .set_scale (OO0OO00000OOOO0O0 )#line:46
            OOOOO0O00OOOO00O0 =OO0O0000OO0O0O0O0 ([OOO00000OO0OO00O0 [OOO0OOOO00OO00OOO ]for OOO0OOOO00OO00OOO in OOO00OO00O000000O ])#line:49
            OOOOO0O00OOOO00O0 .append (OO0OO00000OOOO0O0 )#line:50
        except Exception :#line:52
            OO00OOO0O00OO0OO0 .put ((O00OO00OO0O0000O0 ,ExceptionWrapper (sys .exc_info ())))#line:53
        else :#line:54
            OO00OOO0O00OO0OO0 .put ((O00OO00OO0O0000O0 ,OOOOO0O00OOOO00O0 ))#line:55
class _O000OO0000O00OOOO (_DataLoaderIter ):#line:57
    def __init__ (OOO0O0O0000O00000 ,O00O0OO000O000O0O ):#line:58
        OOO0O0O0000O00000 .dataset =O00O0OO000O000O0O .dataset #line:59
        OOO0O0O0000O00000 .scale =O00O0OO000O000O0O .scale #line:60
        OOO0O0O0000O00000 .collate_fn =O00O0OO000O000O0O .collate_fn #line:61
        OOO0O0O0000O00000 .batch_sampler =O00O0OO000O000O0O .batch_sampler #line:62
        OOO0O0O0000O00000 .num_workers =O00O0OO000O000O0O .num_workers #line:63
        OOO0O0O0000O00000 .pin_memory =O00O0OO000O000O0O .pin_memory and torch .cuda .is_available ()#line:64
        OOO0O0O0000O00000 .timeout =O00O0OO000O000O0O .timeout #line:65
        OOO0O0O0000O00000 .done_event =threading .Event ()#line:66
        OOO0O0O0000O00000 .sample_iter =iter (OOO0O0O0000O00000 .batch_sampler )#line:68
        if OOO0O0O0000O00000 .num_workers >0 :#line:70
            OOO0O0O0000O00000 .worker_init_fn =O00O0OO000O000O0O .worker_init_fn #line:71
            OOO0O0O0000O00000 .index_queues =[multiprocessing .Queue ()for _OOO000000O0OO0O00 in range (OOO0O0O0000O00000 .num_workers )]#line:74
            OOO0O0O0000O00000 .worker_queue_idx =0 #line:75
            OOO0O0O0000O00000 .worker_result_queue =multiprocessing .SimpleQueue ()#line:76
            OOO0O0O0000O00000 .batches_outstanding =0 #line:77
            OOO0O0O0000O00000 .worker_pids_set =False #line:78
            OOO0O0O0000O00000 .shutdown =False #line:79
            OOO0O0O0000O00000 .send_idx =0 #line:80
            OOO0O0O0000O00000 .rcvd_idx =0 #line:81
            OOO0O0O0000O00000 .reorder_dict ={}#line:82
            OO000OO000000OOOO =torch .LongTensor (1 ).random_ ()[0 ]#line:84
            OOO0O0O0000O00000 .workers =[multiprocessing .Process (target =_O00OO0O00OOOOO00O ,args =(OOO0O0O0000O00000 .dataset ,OOO0O0O0000O00000 .index_queues [OOO00000O00OOO0O0 ],OOO0O0O0000O00000 .worker_result_queue ,OOO0O0O0000O00000 .collate_fn ,OOO0O0O0000O00000 .scale ,OO000OO000000OOOO +OOO00000O00OOO0O0 ,OOO0O0O0000O00000 .worker_init_fn ,OOO00000O00OOO0O0 ))for OOO00000O00OOO0O0 in range (OOO0O0O0000O00000 .num_workers )]#line:99
            if OOO0O0O0000O00000 .pin_memory or OOO0O0O0000O00000 .timeout >0 :#line:101
                OOO0O0O0000O00000 .data_queue =queue .Queue ()#line:102
                if OOO0O0O0000O00000 .pin_memory :#line:103
                    O0OOOO0O0O00OO0O0 =torch .cuda .current_device ()#line:104
                else :#line:105
                    O0OOOO0O0O00OO0O0 =None #line:107
                OOO0O0O0000O00000 .worker_manager_thread =threading .Thread (target =_worker_manager_loop ,args =(OOO0O0O0000O00000 .worker_result_queue ,OOO0O0O0000O00000 .data_queue ,OOO0O0O0000O00000 .done_event ,OOO0O0O0000O00000 .pin_memory ,O0OOOO0O0O00OO0O0 ))#line:111
                OOO0O0O0000O00000 .worker_manager_thread .daemon =True #line:112
                OOO0O0O0000O00000 .worker_manager_thread .start ()#line:113
            else :#line:114
                OOO0O0O0000O00000 .data_queue =OOO0O0O0000O00000 .worker_result_queue #line:115
            for OO00O0O000OO0OOO0 in OOO0O0O0000O00000 .workers :#line:117
                OO00O0O000OO0OOO0 .daemon =True #line:118
                OO00O0O000OO0OOO0 .start ()#line:119
            _update_worker_pids (id (OOO0O0O0000O00000 ),tuple (OOOO0O0000O0O000O .pid for OOOO0O0000O0O000O in OOO0O0O0000O00000 .workers ))#line:121
            _set_SIGCHLD_handler ()#line:122
            OOO0O0O0000O00000 .worker_pids_set =True #line:123
            for _OOO0O0OO00O00O0OO in range (2 *OOO0O0O0000O00000 .num_workers ):#line:126
                OOO0O0O0000O00000 ._put_indices ()#line:127
class MSDataLoader (DataLoader ):#line:129
    def __init__ (OOO0OO00O00O0O0O0 ,O000OO0OOOO0O0OO0 ,OO000OO00O000O000 ,batch_size =1 ,shuffle =False ,sampler =None ,batch_sampler =None ,collate_fn =default_collate ,pin_memory =False ,drop_last =False ,timeout =0 ,worker_init_fn =None ):#line:134
        super (MSDataLoader ,OOO0OO00O00O0O0O0 ).__init__ (OO000OO00O000O000 ,batch_size =batch_size ,shuffle =shuffle ,sampler =sampler ,batch_sampler =batch_sampler ,num_workers =O000OO0OOOO0O0OO0 .n_threads ,collate_fn =collate_fn ,pin_memory =pin_memory ,drop_last =drop_last ,timeout =timeout ,worker_init_fn =worker_init_fn )#line:141
        OOO0OO00O00O0O0O0 .scale =O000OO0OOOO0O0OO0 .scale #line:143
    def __iter__ (O000O00O0000O0OO0 ):#line:145
        return _O000OO0000O00OOOO (O000O00O0000O0OO0 )#line:146
