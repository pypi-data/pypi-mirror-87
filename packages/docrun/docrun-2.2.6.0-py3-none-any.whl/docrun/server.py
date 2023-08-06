#!/usr/bin/env python
import sys
import os
import traceback
import subprocess
import threading
import time
import json
import asyncio
import websockets

try:
    from lang import *
except Exception as e:
    try:
        from .lang import *
    except Exception as ee:
        from docrun.lang import *
        pass
    pass

try:
    import psutil
except Exception as e:
    pass

import jupyter_client



port = 5595 
server_address   = "127.0.0.1"

WEB_SOCKET       = None

INFO       = {}
LANG_VER   = {}
GV = {
    # 'status_python3'     : 'idle',
    # 'status_in_python3'  : 'done',

    # 'status_matlab'      : 'idle',
    # 'status_in_matlab'   : 'done',

    # 'status_ir'           : 'idle',
    # 'status_in_ir'        : 'done',
}

KE = {
    # 'python3'     : None,
    # 'rscript'     : None,
    # 'matlab'      : None,
}
MA = {
    # 'python3'     : None,
    # 'rscript'     : None,
    # 'matlab'      : None,
}
TH = {
}

INFO['Kernels'] = jupyter_client.kernelspec.find_kernel_specs()

async def request_processing(websocket, path ):

    def msg_stdin(lang='python3'):
        async def task():
            print("stdin thread started")
            sys.stdout.flush()
            while True:
                try:
                    time.sleep(0.001)
                    if not GV['status_in_'+lang] in ['ready']:
                        time.sleep(0.05)
                        continue
                    #print("waiting for stdin msg",GV['status_in_'+lang])
                    sys.stdout.flush()
                    msg = KE[lang].get_stdin_msg()
                    cont = msg['content']
                    cont['name'] = 'stdin'
                    #print( 'stdin message:', cont )

                    await GV['websocket'].send(json.dumps(cont) )

                    # KE[lang].input('999')
                    #print("request frontend to return an input")
                    sys.stdout.flush()
                    GV['status_in_'+lang] = 'waiting'
                    pass
                except Exception as e:
                    print("iopub error:", e)
                    traceback.print_exc()
                    pass
                pass
            pass
        new_loop = asyncio.new_event_loop()
        asyncio.set_event_loop( new_loop )
        loop = asyncio.get_event_loop()
        loop.run_until_complete( asyncio.gather( task() ) )
        loop.run_forever()
        pass

    def msg_control(lang='python3'):
        async def task():
            print("control thread started")
            sys.stdout.flush()
            while True:
                try:
                    time.sleep(0.001)
                    msg = KE[lang].get_control_msg()
                    cont = msg.get('content')
                    #print( 'control message:', cont )
                    await GV['websocket'].send(json.dumps(cont) )

                    sys.stdout.flush()
                except Exception as e:
                    print("control msg processing error:", e)
                    traceback.print_exc()
                    pass

                pass
            pass
        new_loop = asyncio.new_event_loop()
        asyncio.set_event_loop( new_loop )
        loop = asyncio.get_event_loop()
        loop.run_until_complete( asyncio.gather( task() ) )
        loop.run_forever()
        pass

    def msg_shell(lang='python3'):
        async def task():
            print("shell thread started")
            sys.stdout.flush()
            while True:
                try:
                    time.sleep(0.001)
                    if GV['status_'+lang] in ['idle']:
                        #print("idle wait")
                        #sys.stdout.flush()
                        time.sleep(0.05)
                        continue
                    sys.stdout.flush()
                    msg = KE[lang].get_shell_msg()
                    cont = msg.get('content')
                    #print( 'shell message:', cont )
                    # if cont.get('status') == 'ok':

                    time.sleep(0.5)
                    GV['status_'+lang] = 'idle'
                    GV['status_in_'+lang] = 'done'

                    #await GV['websocket'].send(json.dumps(cont) )

                    sys.stdout.flush()
                    pass

                except Exception as e:
                    print("shell msg processing error:", e)
                    traceback.print_exc()
                    pass

                pass
            pass
        new_loop = asyncio.new_event_loop()
        asyncio.set_event_loop( new_loop )
        loop = asyncio.get_event_loop()
        loop.run_until_complete( asyncio.gather( task() ) )
        loop.run_forever()
        pass

    def msg_iopub(lang='python3'):
        async def task():
            print("iopub thread started")
            sys.stdout.flush()
            while True:
                try:
                    time.sleep(0.001)
                    if GV['status_'+lang] in ['idle']:
                        #print("idle wait")
                        sys.stdout.flush()
                        time.sleep(0.1)
                        #continue
                    if GV['status_'+lang] == 'busy':
                        GV['status_'+lang] = 'processing'


                    #print("waiting for iopub msg",GV['status_'+lang])
                    sys.stdout.flush()
                    msg = KE[lang].get_iopub_msg()
                    cont = msg.get('content')
                    #print( 'iopub message:', cont )
                    await GV['websocket'].send(json.dumps(cont) )

                    sys.stdout.flush()
                    # GV['status_'+lang] = ( cont.get('execution_state') or
                    #                        GV['status_'+lang] )
                    # if GV['status_'+lang] == 'idle': # set stdin to done
                    #     GV['status_in_'+lang] = 'done'
                except Exception as e:
                    print("iopub error:", e)
                    traceback.print_exc()
                    pass

                pass
            pass
        new_loop = asyncio.new_event_loop()
        asyncio.set_event_loop( new_loop )
        loop = asyncio.get_event_loop()
        loop.run_until_complete( asyncio.gather( task() ) )
        loop.run_forever()
        pass

    def start_kernel(lang="python3"):
        print("try start kernel",lang)
        sys.stdout.flush()
        MA[lang], KE[lang] = jupyter_client.manager.start_new_kernel(
            kernel_name = lang
        )

        # if lang == 'python3':
        #     exe_dir   = os.path.dirname( os.path.dirname( __file__ ) )
        #     lib_dir   = os.path.join( exe_dir,'..','Lib' )
        #     KE[lang].execute( "import sys\nsys.path.insert(0,'"+lib_dir+"')\n",
        #                       silent=True,
        #                       allow_stdin=False,
        #     )
        print(lang, "kernel started")
        sys.stdout.flush()


        pass

    async def request():
        #print("\nsocket loop started")
        GV['websocket'] = websocket
        while True:
            try:
                res = json.loads( await websocket.recv() )
                #print('get input request: ',res)
                mtype  = res.get('type')
                lang   = res.get('language')

                if mtype == "info_kernels":
                    #print("web request kernels")
                    for name in INFO['Kernels']:
                        INFO['Kernels'][name] = jupyter_client.kernelspec.get_kernel_spec(name).display_name
                        pass
                    await websocket.send('{"name":"kernels","kernels":'+json.dumps(INFO['Kernels'])+'}')
                    continue

                lang = res.get('language')
                if not lang or not INFO['Kernels'].get(lang):
                    await websocket.send('{"name":"none_kernel","language":"'+lang+'"}')
                    await websocket.send('{"execution_state":"idle"}')
                    continue
                    pass
                if mtype == 'operate':
                    oper = res.get('operation')
                    if oper == "restart": # try  stop kernel
                        print("try to restart kernel for", lang)
                        MA[lang].restart_kernel()
                        continue
                    elif oper == "interrupt": # try  stop kernel
                        print("try to interrupt kernel for", lang)
                        MA[lang].interrupt_kernel()
                        continue
                    elif oper == "stop": # try  stop kernel
                        print("try to stop kernel for", lang)
                        MA[lang].shutdown_kernel()
                        INFO['KERNEL_STATUS_'+lang] = lt("Stoped")
                        continue
                    elif oper == "readmore": # try  stop kernel
                        #print("more should read from iopub", lang)
                        GV['status_in_'+lang] = 'processing'
                        continue
                    print("unknown operation:",oper)
                    continue
                elif mtype == 'input': 
                    if not KE[lang]:
                        #print("input request back, but no kernel exists, just abort")
                        continue
                    instr = res.get('input')
                    #print("send input str",instr, "as input. mark stdin ready")
                    KE[lang].input(instr)
                    GV['status_in_'+lang] = 'ready'
                    continue
                elif mtype == 'evaluate':
                    #print("normal input code")
                    instr = res.get('code')
                    if not MA.get(lang):
                        print( lt("Kernel {0} is not started. Try start...",lang) )
                        try:
                            start_kernel(lang)
                        except Exception as e:
                            errs = "start kernel failed for: {0}".format(e)
                            print(errs)
                            await websocket.send(
                                '{"name":"kernel-start-error","text":"'+errs+'"}')
                            traceback.print_exc()
                            continue
                            pass
                        GV['status_'+lang] = 'idle'
                        GV['status_in_'+lang] = 'done'
                        TH[lang] = {}
                        TH[lang]['iopub'] = threading.Thread(
                            target=msg_iopub, args=([lang]))
                        TH[lang]['iopub'].start()

                        TH[lang]['stdin']=threading.Thread(
                            target=msg_stdin, args=([lang]) )
                        TH[lang]['stdin'].start()

                        TH[lang]['shell']=threading.Thread(
                            target=msg_shell, args=([lang]) )
                        TH[lang]['shell'].start()

                        # TH[lang]['control']=threading.Thread(
                        #     target=msg_control, args=([lang]) )
                        # TH[lang]['control'].start()

                        time.sleep(0.001)
                        pass
                    while not KE[lang]:
                        #print("wait for kernel to be ready")
                        time.sleep(0.05)
                        continue
                    if not MA[lang].is_alive():
                        print("kernel is not alive. Try restart")
                        MA[lang].restart_kernel()
                        pass
                    while not MA[lang].is_alive():
                        #print("wait for kernel to be alive")
                        time.sleep(0.05)
                        continue
                        pass
                    try:
                        #print("send input to kernel",KE[lang] )
                        KE[lang].execute( instr,
                                          silent=False,
                                          store_history=False,
                                          allow_stdin=True,
                        )
                        INFO['KERNEL_STATUS_'+lang] = lt("running")
                        GV['status_'+lang]      = 'msgexec'
                        GV['status_in_'+lang]   = 'ready'
                    except Exception as e:
                        print("kernel execution error:",e)
                        traceback.print_exc()
                        pass
                    pass
                else:
                    print('unknown request message:', res)
                    continue
                pass
            except Exception as e:
                print("request loop error:",e)
                traceback.print_exc()
                GV['status_'+lang] = 'idle'
                if GV['status_in_'+lang] == 'waiting':
                    GV['status_in_'+lang] = 'done'
                    MA[lang].shutdown_kernel()
                    INFO['KERNEL_STATUS_'+lang] = lt("Stoped")
                    pass
                break
            pass
        pass



    request_task = asyncio.create_task( request() )
    await request_task

    pass

def run_server(): # in non-main thread
    #print("kernels : ", INFO['Kernels'])
    print("starting server on port",port )
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop( loop )
    loop = asyncio.get_event_loop()

    try:
        server = websockets.serve(request_processing, server_address, port)
        loop.run_until_complete( server )
        loop.run_forever()
    except Exception as e:
        print("quit with error:", e)
        pass
    #print("task assigned")
    pass

def stop_server(lang='python'):
    print("try stop server",)
    pass

#run_server()

def check_parent_pid():
    if not psutil: return
    while True:
        if not psutil.pid_exists( INFO['parent_pid'] ):
            print("no parent found. Quiting...")
            os._exit(1)
            pass
        time.sleep(0.05)
        pass

    pass
            

if __name__  == "__main__":
    #print('run server with argv:',sys.argv)
    try:
        INFO['parent_pid'] = int(sys.argv[-1])
        check = threading.Thread(target=check_parent_pid)
        check.start()
    except:
        INFO['parent_pid'] = -1
        print("not launched by parent process in manner")
        pass
    run_server()

