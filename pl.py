#!/usr/bin/python2
#-*- encoding: UTF-8 -*-
#encoding: UTF-8

import psutil
import sys
from texttable import Texttable
import cmdw
MAX_LENGTH = cmdw.getWidth() - 4
if not sys.platform == 'win32':
    MAX_LENGTH = MAX_LENGTH - 4
from make_colors import make_colors
import colorama
colorama.init()
import time
import os
import math
import traceback
import random
import cmdw
from debug import * 

def convert_size(size_bytes):
    if (size_bytes == 0):
        return '0B'
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return '%s %s' % (s, size_name[i])

def makeTable(data_search, data_filter = None, sorted = False, tail = None, show_cpu = False):
    debug(data_search = data_search)
    #random_choices = ['white','grey', 'blue', 'cyan', 'green', 'red', 'magenta', 'yellow',]
    #print "tail =", tail
    if tail and not sorted:
        data_search1 = {}
        data_filter1 = {}
        data_search_keys = data_search.keys()[-int(tail):]
        data_filter_keys = data_filter.keys()[-int(tail):]
        for i in data_search_keys:
            data_search1.update({i:data_search.get(i)})
        for i in data_filter_keys:
            data_filter1.update({i:data_filter.get(i)})
        data_search = data_search1
        data_filter = data_filter1
    elif tail and sorted:
        data_search = data_search[-int(tail):]
        data_filter = data_filter[-int(tail):]
    if MAX_LENGTH <= (220 / 2):
        number = 1
        if not sorted:
            for i in data_search:
                name = data_search.get(i).get('name')
                pid = data_search.get(i).get('pid')
                exe =  data_search.get(i).get('exe')
                cmd = " ".join(data_search.get(i).get('cmd'))
                mem = convert_size(data_search.get(i).get('mem'))
                cpu = data_search.get(i).get('cpu')
                print "NAME :", make_colors(str(name), 'lightcyan', color_type= 'colorama')
                print "PID  :", make_colors(str(pid), 'lightyellow', color_type= 'colorama')
                print "EXE  :", make_colors(str(exe), 'lightred', color_type= 'colorama')
                print "MEM  :", make_colors(str(mem), 'lightgreen', color_type= 'colorama')
                print "CMD  :", make_colors(str(cmd), 'lightblue', color_type= 'colorama')
                print "CPU  :", make_colors(str(cmd), 'lightcyan', color_type= 'colorama')
                print "-" * MAX_LENGTH
                number += 1
            if data_filter:
                for i in data_filter:
                    name = data_filter.get(i).get('name')
                    pid = data_filter.get(i).get('pid')
                    exe =  data_filter.get(i).get('exe')
                    cmd = " ".join(data_filter.get(i).get('cmd'))
                    cpu = data_filter.get(i).get('cpu')
                    mem = convert_size(data_filter.get(i).get('mem'))
                    print "NAME :", make_colors(str(name), 'lightcyan', color_type= 'colorama')
                    print "PID  :", make_colors(str(pid), 'lightyellow', color_type= 'colorama')
                    print "EXE  :", make_colors(str(exe), 'lightred', color_type= 'colorama')
                    print "MEM  :", make_colors(str(mem), 'lightgreen', color_type= 'colorama')
                    print "CMD  :", make_colors(str(cmd), 'lightblue', color_type= 'colorama')
                    print "CPU  :", make_colors(str(cmd), 'lightcyan', color_type= 'colorama')
                    print "-" * MAX_LENGTH
                    number += 1
        else:
            for i in data_search:
                name = i[1].get('name')
                pid = i[1].get('pid')
                exe = i[1].get('exe')
                cpu = i[1].get('cpu')
                cmd = " ".join(i[1].get('cmd'))
                mem = convert_size(i[1].get('mem'))
                print "NAME :", make_colors(str(name), 'lightcyan', color_type= 'colorama')
                print "PID  :", make_colors(str(pid), 'lightyellow', color_type= 'colorama')
                print "EXE  :", make_colors(str(exe), 'lightred', color_type= 'colorama')
                print "MEM  :", make_colors(str(mem), 'lightgreen', color_type= 'colorama')
                print "CMD  :", make_colors(str(cmd), 'lightblue', color_type= 'colorama')
                print "CPU  :", make_colors(str(cmd), 'lightcyan', color_type= 'colorama')
                print "-" * MAX_LENGTH
                number += 1
            if data_filter:
                for i in data_filter:
                    name = i[1].get('name')
                    pid = i[1].get('pid')
                    exe =  i[1].get('exe')
                    cpu =  i[1].get('cpu')
                    cmd = " ".join(i[1].get('cmd'))
                    mem = convert_size(i[1].get('mem'))
                    print "NAME :", make_colors(str(name), 'lightcyan', color_type= 'colorama')
                    print "PID  :", make_colors(str(pid), 'lightyellow', color_type= 'colorama')
                    print "EXE  :", make_colors(str(exe), 'lightred', color_type= 'colorama')
                    print "MEM  :", make_colors(str(mem), 'lightgreen', color_type= 'colorama')
                    print "CMD  :", make_colors(str(cmd), 'lightblue', color_type= 'colorama')
                    print "CPU  :", make_colors(str(cmd), 'lightcyan', color_type= 'colorama')
                    print "-" * MAX_LENGTH                    
                    number += 1
    else:
        table = Texttable()
        if show_cpu:
            table.header(['No','Name','PID','EXE', 'Mem', 'CPU %', 'CMD'])
            table.set_cols_align(["l", "l", "l", "l", "c", "c", "c"])
            table.set_cols_valign(["t", "m", "m", "m", "m", "m", "b"])
            if sys.platform == 'win32':
                table.set_cols_width([
                        int(MAX_LENGTH * 0.02),
                        int(MAX_LENGTH * 0.1),
                        int(MAX_LENGTH * 0.03),
                        int(MAX_LENGTH * 0.24),
                        int(MAX_LENGTH * 0.05),
                        int(MAX_LENGTH * 0.03),
                        int(MAX_LENGTH * 0.44),
                    ])
            else:
                table.set_cols_width([
                        int(MAX_LENGTH * 0.03),
                        int(MAX_LENGTH * 0.1),
                        int(MAX_LENGTH * 0.04),
                        int(MAX_LENGTH * 0.25),
                        int(MAX_LENGTH * 0.05),
                        int(MAX_LENGTH * 0.03),
                        int(MAX_LENGTH * 0.42),
                    ])
        else:
            table.header(['No','Name','PID','EXE', 'Mem', 'CMD'])
            table.set_cols_align(["l", "l", "l", "l", "c", "c"])
            table.set_cols_valign(["t", "m", "m", "m", "m", "b"])
            if sys.platform == 'win32':
                table.set_cols_width([
                        int(MAX_LENGTH * 0.02),
                        int(MAX_LENGTH * 0.1),
                        int(MAX_LENGTH * 0.03),
                        int(MAX_LENGTH * 0.28),
                        int(MAX_LENGTH * 0.05),
                        int(MAX_LENGTH * 0.44),
                    ])
            else:
                table.set_cols_width([
                        int(MAX_LENGTH * 0.03),
                        int(MAX_LENGTH * 0.1),
                        int(MAX_LENGTH * 0.04),
                        int(MAX_LENGTH * 0.28),
                        int(MAX_LENGTH * 0.05),
                        int(MAX_LENGTH * 0.42),
                    ])
            
        sys.dont_write_bytecode = True
        number = 1
        #print "sorted =", sorted
        if not sorted:
            for i in data_search:
                name = data_search.get(i).get('name')
                pid = data_search.get(i).get('pid')
                exe =  data_search.get(i).get('exe')
                cpu =  data_search.get(i).get('cpu')
                cmd = " ".join(data_search.get(i).get('cmd'))
                mem = convert_size(data_search.get(i).get('mem'))
                time = data_search.get(i).get('time')
                
                try:
                    table.add_row([
                        str(number),
                        name,
                        str(pid),
                        exe,
                        mem,
                        cpu, 
                        cmd
                    ])
                    #table.add_row([
                        #str(number),
                        #make_colors(name, 'lightyellow', color_type= 'colorama'),
                        #make_colors(str(pid), 'lightblue', color_type= 'colorama'),
                        #make_colors(exe, 'lightgreen', color_type= 'colorama'),
                        #make_colors(cmd, 'lightcyan', color_type= 'co2lorama')
                        #])
                except:
                    if show_cpu:
                        table.add_row([
                            str(number),
                            unicode(name).encode(sys.stdout.encoding, errors='replace'),
                            unicode(str(pid)).encode(sys.stdout.encoding, errors='replace'),
                            unicode(exe).encode(sys.stdout.encoding, errors='replace'),
                            unicode(mem).encode(sys.stdout.encoding, errors='replace'),
                            unicode(cpu).encode(sys.stdout.encoding, errors='replace'),
                            unicode(cmd).encode(sys.stdout.encoding, errors='replace'), 
                        ])
                    else:
                        table.add_row([
                            str(number),
                            unicode(name).encode(sys.stdout.encoding, errors='replace'),
                            unicode(str(pid)).encode(sys.stdout.encoding, errors='replace'),
                            unicode(exe).encode(sys.stdout.encoding, errors='replace'),
                            unicode(mem).encode(sys.stdout.encoding, errors='replace'),
                            unicode(cmd).encode(sys.stdout.encoding, errors='replace'), 
                        ])
                number += 1
            if data_filter:
                for i in data_filter:
                    name = data_filter.get(i).get('name')
                    pid = data_filter.get(i).get('pid')
                    exe =  data_filter.get(i).get('exe')
                    cpu =  data_filter.get(i).get('cpu')
                    cmd = " ".join(data_filter.get(i).get('cmd'))
                    mem = convert_size(data_filter.get(i).get('mem'))
                    time = data_filter.get(i).get('time')
                    
                    try:
                        table.add_row([
                                str(number),
                                name,
                                str(pid),
                                exe,
                                mem,
                                cpu, 
                                cmd
                            ])
                    except:
                        if show_cpu:
                            table.add_row([
                                    str(number),
                                    unicode(name).encode(sys.stdout.encoding, errors='replace'),
                                    unicode(str(pid)).encode(sys.stdout.encoding, errors='replace'),
                                    unicode(exe).encode(sys.stdout.encoding, errors='replace'),
                                    unicode(mem).encode(sys.stdout.encoding, errors='replace'),
                                    unicode(cpu).encode(sys.stdout.encoding, errors='replace'),
                                    unicode(cmd).encode(sys.stdout.encoding, errors='replace'), 
                            ])
                        else:
                            table.add_row([
                                    str(number),
                                    unicode(name).encode(sys.stdout.encoding, errors='replace'),
                                    unicode(str(pid)).encode(sys.stdout.encoding, errors='replace'),
                                    unicode(exe).encode(sys.stdout.encoding, errors='replace'),
                                    unicode(mem).encode(sys.stdout.encoding, errors='replace'),
                                    unicode(cmd).encode(sys.stdout.encoding, errors='replace'), 
                            ])            
            #if sys.stdout.encoding != 'cp850':
                #sys.stdout = codecs.getwriter('utf-8')(sys.stdout, 'strict')
            #if sys.stderr.encoding != 'cp850':
                #sys.stderr = codecs.getwriter('utf-8')(sys.stderr, 'strict')
                number += 1
        else:
            for i in data_search:
                name = i[1].get('name')
                pid = i[1].get('pid')
                exe = i[1].get('exe')
                cpu = i[1].get('cpu')
                cmd = " ".join(i[1].get('cmd'))
                mem = convert_size(i[1].get('mem'))
                
                try:
                    table.add_row([
                        str(number),
                        name,
                        str(pid),
                        exe,
                        mem,
                        cpu, 
                        cmd
                    ])
                    #table.add_row([
                        #str(number),
                        #make_colors(name, 'lightyellow', color_type= 'colorama'),
                        #make_colors(str(pid), 'lightblue', color_type= 'colorama'),
                        #make_colors(exe, 'lightgreen', color_type= 'colorama'),
                        #make_colors(cmd, 'lightcyan', color_type= 'co2lorama')
                        #])
                except:
                    if show_cpu:
                        table.add_row([
                            str(number),
                            unicode(name).encode(sys.stdout.encoding, errors='replace'),
                            unicode(str(pid)).encode(sys.stdout.encoding, errors='replace'),
                            unicode(exe).encode(sys.stdout.encoding, errors='replace'),
                            unicode(mem).encode(sys.stdout.encoding, errors='replace'),
                            unicode(cpu).encode(sys.stdout.encoding, errors='replace'),
                            unicode(cmd).encode(sys.stdout.encoding, errors='replace'), 
                        ])
                    else:
                        table.add_row([
                            str(number),
                            unicode(name).encode(sys.stdout.encoding, errors='replace'),
                            unicode(str(pid)).encode(sys.stdout.encoding, errors='replace'),
                            unicode(exe).encode(sys.stdout.encoding, errors='replace'),
                            unicode(mem).encode(sys.stdout.encoding, errors='replace'),
                            unicode(cmd).encode(sys.stdout.encoding, errors='replace'), 
                        ])
                number += 1
            if data_filter:
                for i in data_filter:
                    name = i[1].get('name')
                    pid = i[1].get('pid')
                    exe =  i[1].get('exe')
                    cpu =  i[1].get('cpu')
                    cmd = " ".join(i[1].get('cmd'))
                    mem = convert_size(i[1].get('mem'))
                
                    try:
                        table.add_row([
                                str(number),
                                name,
                                str(pid),
                                exe,
                                mem,
                                cpu, 
                                cmd
                            ])
                    except:
                        if show_cpu:
                            table.add_row([
                                    str(number),
                                    unicode(name).encode(sys.stdout.encoding, errors='replace'),
                                    unicode(str(pid)).encode(sys.stdout.encoding, errors='replace'),
                                    unicode(exe).encode(sys.stdout.encoding, errors='replace'),
                                    unicode(mem).encode(sys.stdout.encoding, errors='replace'),
                                    unicode(cpu).encode(sys.stdout.encoding, errors='replace'),
                                    unicode(cmd).encode(sys.stdout.encoding, errors='replace'), 
                            ])
                        else:
                            table.add_row([
                                    str(number),
                                    unicode(name).encode(sys.stdout.encoding, errors='replace'),
                                    unicode(str(pid)).encode(sys.stdout.encoding, errors='replace'),
                                    unicode(exe).encode(sys.stdout.encoding, errors='replace'),
                                    unicode(mem).encode(sys.stdout.encoding, errors='replace'),
                                    unicode(cmd).encode(sys.stdout.encoding, errors='replace'), 
                            ])            
            #if sys.stdout.encoding != 'cp850':
                #sys.stdout = codecs.getwriter('utf-8')(sys.stdout, 'strict')
            #if sys.stderr.encoding != 'cp850':
                #sys.stderr = codecs.getwriter('utf-8')(sys.stderr, 'strict')
                number += 1
        print table.draw()
    return data_search, data_filter, number

def sort_dict(myDict, value_sort_name, reverse = False):
    dicts = myDict.items()
    dicts.sort(key=lambda (k,d): (d[value_sort_name]), reverse = reverse)
    return dicts

def get_memory_full_info(pid, separted = True, process_instance = None, tab = 1):
    random_colors = ['yellow', 'green', 'blue', 'cyan', 'magenta', 'white', 'red']
    lens = []
    pid = int(pid)
    try:
        if not process_instance:
            p = psutil.Process(pid)
            mem = p.memory_full_info()
        else:
            mem = process_instance.memory_full_info()
    except:
        return ()
    for i in mem._fields:
        lens.append(len(i))
    MAX = max(lens)
    
    print "\t" * (tab - 1) + make_colors("MEMORY DETAILS:", 'yellow', ['bold'])
    print "\t" * tab + "RSS" + " " * (MAX - len("RSS")) + " = " + make_colors(convert_size(mem.rss), "yellow")
    print "\t" * tab + "VMS" + " " * (MAX - len("VMS")) + " = " + make_colors(convert_size(mem.vms), "green")
    if sys.platform == 'win32':
        print "\t" * tab + "NUM PAGE FAULTS" + " " * (MAX - len("NUM PAGE FAULTS")) + " = " + make_colors(convert_size(mem.num_page_faults), "magenta")
        print "\t" * tab + "WSET" + " " * (MAX - len("WSET")) + " = " + make_colors(convert_size(mem.wset), "cyan")
        print "\t" * tab + "PEAK WSET" + " " * (MAX - len("PEAK WSET")) + " = " + make_colors(convert_size(mem.peak_wset), "red")
        print "\t" * tab + "PAGED POOL" + " " * (MAX - len("PAGED POOL")) + " = " + make_colors(convert_size(mem.paged_pool), "blue")
        print "\t" * tab + "PEAK PAGED POOL" + " " * (MAX - len("PEAK PAGED POOL")) + " = " + make_colors(convert_size(mem.peak_paged_pool), "red")
        print "\t" * tab + "NONPAGED POOL" + " " * (MAX - len("NONPAGED POOL")) + " = " + make_colors(convert_size(mem.nonpaged_pool), "green")
        print "\t" * tab + "PEAK NONPAGED POOL" + " " * (MAX - len("PEAK NONPAGED POOL")) + " = " + make_colors(convert_size(mem.peak_nonpaged_pool), "red")
        print "\t" * tab + "PAGEFILE" + " " * (MAX - len("PAGEFILE")) + " = " + make_colors(convert_size(mem.pagefile), "yellow")
        print "\t" * tab + "PEAK PAGEFILE" + " " * (MAX - len("PEAK PAGEFILE")) + " = " + make_colors(convert_size(mem.peak_pagefile), "red")
        print "\t" * tab + "PRIVATE" + " " * (MAX - len("PRIVATE")) + " = " + make_colors(convert_size(mem.private), "white")
    else:
        print "\t" * tab + "PSS" + " " * (MAX - len("PSS")) + " = " + make_colors(convert_size(mem.pss), "white")
        print "\t" * tab + "SHARED" + " " * (MAX - len("SHARED")) + " = " + make_colors(convert_size(mem.shared), "white")
        print "\t" * tab + "SWAP" + " " * (MAX - len("SHARED")) + " = " + make_colors(convert_size(mem.swap), "white")
        print "\t" * tab + "TEXT" + " " * (MAX - len("TEXT")) + " = " + make_colors(convert_size(mem.text), "white")
        print "\t" * tab + "LIB" + " " * (MAX - len("LIB")) + " = " + make_colors(convert_size(mem.lib), "white")
        print "\t" * tab + "DATA" + " " * (MAX - len("DATA")) + " = " + make_colors(convert_size(mem.data), "white")
        print "\t" * tab + "DIRTY" + " " * (MAX - len("DIRTY")) + " = " + make_colors(convert_size(mem.dirty), "white")
        print "\t" * tab + "DIRTY" + " " * (MAX - len("DIRTY")) + " = " + make_colors(convert_size(mem.dirty), "white")
    print "\t" * tab + "USS" + " " * (MAX - len("USS")) + " = " + make_colors(convert_size(mem.uss), "magenta")
    if separted:
        print "-" * (MAX + 15)
    return mem

def get_child(pid, separated = True, process_instance = None, memory_detail = False, tab = 2, kill = False):
    if not process_instance:
        childs = psutil.Process(int(pid)).children()
        print make_colors("CHILDS PROCESS DETAILS:", 'yellow', ['bold'])
        for i in childs:
            print "\t" * tab + "Name   :", make_colors(str(i.name()), 'yellow')
            print "\t" * tab + "PID    :", make_colors(str(i.pid), 'white', 'red')
            print "\t" * tab + "EXE    :", make_colors(str(i.exe()), 'white', 'green')
            print "\t" * tab + "MEM    :", make_colors(convert_size(i.memory_info().vms), 'white', 'blue')
            if str(i.name()) == str(" ".join(i.cmdline())):
                print "\t" * tab + "CMD    :"
            else:
                print "\t" * tab + "CMD    :", make_colors(str(" ".join(i.cmdline())), 'white', 'blue')
            if kill:
                i.terminate()
            try:
                print "\t" * tab + "STATUS :", make_colors(str(i.status().upper()), 'white', 'yellow', ['bold', 'blink'])
            except:
                print "\t" * tab + "STATUS :", make_colors("TERMINATED !!!", 'white', 'red', ['bold', 'blink'])
            try:
                pid = i.pid
                if memory_detail:
                    get_memory_full_info(pid, False, tab = 2)
            except:
                print make_colors("PROCESS TERMINATED !!!", 'white', 'red', ['bold', 'blink'])
            if separated:
                print "+" * 100            
                
    else:
        childs = process_instance.children()
        print make_colors("CHILDS PROCESS DETAILS:", 'yellow', ['bold'])
        for i in childs:
            print "\t" * tab + "Name   :", make_colors(str(i.name()), 'yellow')
            print "\t" * tab + "PID    :", make_colors(str(i.pid), 'white', 'red')
            print "\t" * tab + "EXE    :", make_colors(str(i.exe()), 'white', 'green')
            print "\t" * tab + "MEM    :", make_colors(convert_size(i.memory_info().vms), 'white', 'blue')
            if str(i.name()) == str(" ".join(i.cmdline())):
                print "\t" * tab + "CMD    :"
            else:
                print "\t" * tab + "CMD    :", make_colors(str(" ".join(i.cmdline())), 'white', 'blue')
            if kill:
                i.terminate()
            try:
                print "\t" * tab + "STATUS :", make_colors(str(i.status().upper()), 'white', 'yellow', ['bold', 'blink'])
            except:
                print "\t" * tab + "STATUS :", make_colors("TERMINATED !!!", 'white', 'red', ['bold', 'blink'])
            try:
                pid = i.pid
                if memory_detail:
                    get_memory_full_info(pid, False, tab = 2)
            except:
                print make_colors("PROCESS TERMINATED !!!", 'white', 'red', ['bold', 'blink'])
            if separated:
                print "+" * 100                        
    

def ps(pfilter = None, sort = None, reverse = False, show_all = False, show_cpu = False):
    list_process = {}
    list_filter = {}
    n = 1
    for process in psutil.process_iter():
        #debug(process = process)
        name, exe, cmd, mem = "", "", [], ()
        try:
            name = process.name()
            cmd = process.cmdline()
            exe = process.exe()
            pid = process.pid
            if show_cpu:
                cpu = process.cpu_percent(interval = 0.116)
            else:
                cpu = 0.0
            #debug(cpu = cpu)
            mem = process.memory_full_info().vms
            time = process._create_time
            if pfilter and isinstance(pfilter, list):
                for i in pfilter:
                    if show_all == False and os.path.basename(__file__) in " ".join(cmd):
                        pass
                    else:
                        if str(i).strip().lower() in str(name).lower():
                            list_filter.update({
                                n: {
                                    'name': name,
                                    'cmd': cmd,
                                    'exe': exe,
                                    'pid': pid,
                                    'cpu': cpu,
                                    'mem': mem,
                                    'time': time,
                                    },
                            })
                    n += 1
            if pfilter:
                if name in pfilter or str(pid) in pfilter:
                    pass
                elif show_all == False and os.path.basename(__file__) in " ".join(cmd):
                    pass
                else:
                    list_process.update({
                        n: {
                            'name': name,
                            'cmd': cmd,
                            'exe': exe,
                            'pid': pid,
                            'cpu': cpu,
                            'mem': mem,
                            'time': time,
                            },
                    })                    
            else:
                if show_all == False and os.path.basename(__file__) in " ".join(cmd):
                    pass
                else:
                    list_process.update({
                            n: {
                                'name': name,
                                'cmd': cmd,
                                'exe': exe,
                                'pid': pid,
                                'cpu': cpu,
                                'mem': mem,
                                'time': time,
                                },
                        })                
            n += 1
        except (psutil.AccessDenied, psutil.ZombieProcess):
            pass
        except psutil.NoSuchProcess:
            continue

    if sort:
        return sort_dict(list_process, sort, reverse),  sort_dict(list_filter, sort, reverse)
    else:
        return list_process, list_filter

def kill(kills, always_kill = False):
    list_process, list_filter = ps()
    #print "-" * 100
    ver = 0
    for i in kills:
        if str(i).isdigit():
            for n in list_process:
                if int(i) == list_process.get(n).get('pid'):
                    p = psutil.Process(int(i))
                    p.terminate()
                    print "Name   :", make_colors(str(list_process.get(n).get('name')), 'yellow')
                    print "PID    :", make_colors(str(list_process.get(n).get('pid')), 'white', 'red')
                    print "EXE    :", make_colors(str(list_process.get(n).get('exe')), 'white', 'green')
                    print "MEM    :", make_colors(convert_size(list_process.get(n).get('mem')), 'white', 'blue')
                    if str(list_process.get(n).get('name')) == str(" ".join(list_process.get(n).get('cmd'))):
                        print "CMD    :"
                    else:
                        print "CMD    :", make_colors(str(" ".join(list_process.get(n).get('cmd'))), 'white', 'blue')                    
                    if p.is_running():
                        print "STATUS :", make_colors("RUNNING !", 'white', 'red', ['bold', 'blink'])
                        if always_kill:
                            while 1:
                                if p.is_running():
                                    print make_colors("Re-Terminating .....", 'red', attrs= ['bold', 'blink'])
                                    p.terminate()
                                    time.sleep(1)
                                else:
                                    print "Name   :", make_colors(str(list_process.get(n).get('name')), 'yellow')
                                    print "PID    :", make_colors(str(list_process.get(n).get('pid')), 'white', 'red')
                                    print "EXE    :", make_colors(str(list_process.get(n).get('exe')), 'white', 'green')
                                    if str(list_process.get(n).get('name')) == str(" ".join(list_process.get(n).get('cmd'))):
                                        print "CMD    :"
                                    else:
                                        print "CMD    :", make_colors(str(" ".join(list_process.get(n).get('cmd'))), 'white', 'blue')                                
                                    print "STATUS :", make_colors("TERMINATED / KILLED", 'white', 'red', ['bold', 'blink'])
                                    break
                    else:
                        try:
                            print "STATUS :", make_colors(p.status().title(), 'white', 'red', ['bold', 'blink'])
                        except:
                            print "STATUS :", make_colors("TERMINATED !!!", 'white', 'red', ['bold', 'blink'])
                    print "-" * 100
        else:
            for n in list_process:
                if str(i) == list_process.get(n).get('name'):
                    ver += 1
                    p = psutil.Process(list_process.get(n).get('pid'))
                    p.terminate()
                    print "Name   :", make_colors(str(list_process.get(n).get('name')), 'yellow')
                    print "PID    :", make_colors(str(list_process.get(n).get('pid')), 'white', 'red')
                    print "EXE    :", make_colors(str(list_process.get(n).get('exe')), 'white', 'green')
                    print "MEM    :", make_colors(convert_size(list_process.get(n).get('mem')), 'white', 'blue')
                    if str(list_process.get(n).get('name')) == str(" ".join(list_process.get(n).get('cmd'))):
                        print "CMD    :"
                    else:
                        print "CMD    :", make_colors(str(" ".join(list_process.get(n).get('cmd'))), 'white', 'blue')                    
                    if p.is_running():
                        print "STATUS :", make_colors("RUNNING !", 'white', 'red', ['bold', 'blink'])
                        if always_kill:
                            while 1:
                                if p.is_running():
                                    print make_colors("Re-Terminating .....", 'red', attrs= ['bold', 'blink'])
                                    p.terminate()
                                    time.sleep(1)
                                else:
                                    print "Name   :", make_colors(str(list_process.get(n).get('name')), 'yellow')
                                    print "PID    :", make_colors(str(list_process.get(n).get('pid')), 'white', 'red')
                                    print "EXE    :", make_colors(str(list_process.get(n).get('exe')), 'white', 'green')
                                    print "MEM    :", make_colors(convert_size(list_process.get(n).get('mem')), 'white', 'blue')
                                    if str(list_process.get(n).get('name')) == str(" ".join(list_process.get(n).get('cmd'))):
                                        print "CMD    :"
                                    elif str(list_process.get(n).get('exe')) == str(" ".join(list_process.get(n).get('cmd'))):
                                        print "CMD    :"
                                    else:
                                        print "CMD    :", make_colors(str(" ".join(list_process.get(n).get('cmd'))), 'white', 'blue')                                
                                    print "STATUS :", make_colors("TERMINATED / KILLED", 'white', 'red', ['bold', 'blink'])
                                    break
                    else:
                        try:
                            print "STATUS :", make_colors(p.status().upper(), 'white', 'red', ['bold', 'blink'])
                        except:
                            print make_colors("TERMINATED !!!", 'white', 'red', ['bold', 'blink'])
                    print "-" * 100
                else:
                    if str(i) in list_process.get(n).get('name'):
                        ver += 1
                        p = psutil.Process(list_process.get(n).get('pid'))
                        p.terminate()
                        print "Name   :", make_colors(str(list_process.get(n).get('name')), 'yellow')
                        print "PID    :", make_colors(str(list_process.get(n).get('pid')), 'white', 'red')
                        print "EXE    :", make_colors(str(list_process.get(n).get('exe')), 'white', 'green')
                        print "MEM    :", make_colors(convert_size(list_process.get(n).get('mem')), 'white', 'blue')
                        if str(list_process.get(n).get('name')) == str(" ".join(list_process.get(n).get('cmd'))):
                            print "CMD    :"
                        else:
                            print "CMD    :", make_colors(str(" ".join(list_process.get(n).get('cmd'))), 'white', 'blue')                    
                        if p.is_running():
                            print "STATUS :", make_colors("RUNNING !", 'white', 'red', ['bold', 'blink'])
                            if always_kill:
                                while 1:
                                    if p.is_running():
                                        print make_colors("Re-Terminating .....", 'red', attrs= ['bold', 'blink'])
                                        p.terminate()
                                        time.sleep(1)
                                    else:
                                        print "Name   :", make_colors(str(list_process.get(n).get('name')), 'yellow')
                                        print "PID    :", make_colors(str(list_process.get(n).get('pid')), 'white', 'red')
                                        print "EXE    :", make_colors(str(list_process.get(n).get('exe')), 'white', 'green')
                                        print "MEM    :", make_colors(convert_size(list_process.get(n).get('mem')), 'white', 'blue')
                                        if str(list_process.get(n).get('name')) == str(" ".join(list_process.get(n).get('cmd'))):
                                            print "CMD    :"
                                        elif str(list_process.get(n).get('exe')) == str(" ".join(list_process.get(n).get('cmd'))):
                                            print "CMD    :"
                                        else:
                                            print "CMD    :", make_colors(str(" ".join(list_process.get(n).get('cmd'))), 'white', 'blue')                                
                                        print "STATUS :", make_colors("TERMINATED / KILLED", 'white', 'red', ['bold', 'blink'])
                                        break
                        else:
                            try:
                                print "STATUS :", make_colors(p.status().upper(), 'white', 'red', ['bold', 'blink'])
                            except:
                                print make_colors("TERMINATED !!!", 'white', 'red', ['bold', 'blink'])
                        print "-" * 100
        if ver == 0:
            print "STATUS :", make_colors("NOT FOUND !!!", 'white', 'red', ['bold', 'blink'])

def search(query, kill = False, fast = False, memory_detail = False, child_detail = False, kill_recursive = False):
    list_process, list_filter = ps()
    ver = 0
    if fast:
        list_process1, list_filter1 = ps(query, 'time')
        for p in list_filter1[-len(query):]:
            try:
                x = psutil.Process(p[1].get('pid'))
            except:
                pass
            print "Name   :", make_colors(str(p[1].get('name')), 'yellow')
            print "PID    :", make_colors(str(p[1].get('pid')), 'white', 'red')
            print "EXE    :", make_colors(str(p[1].get('exe')), 'white', 'green')
            print "MEM    :", make_colors(convert_size(p[1].get('mem')), 'white', 'blue')
            if str(p[1].get('name')) == str(" ".join(p[1].get('cmd'))):
                print "CMD    :"
            elif str(p[1].get('exe')) == str(" ".join(p[1].get('cmd'))):
                print "CMD    :"                    
            else:
                print "CMD    :", make_colors(str(" ".join(p[1].get('cmd'))), 'white', 'blue')
            if kill:
                try:
                    x.terminate()
                except:
                    pass
            try:
                STATUS = x.status()
            except:
                STATUS = "TERMINATED !!!"                    
            print "STATUS : " + make_colors(STATUS.upper(), 'white', 'red', ['bold', 'blink'])
            #print make_colors(STATUS.upper(), 'white', 'red', ['bold', 'blink'])
            if memory_detail:
                get_memory_full_info(p[1].get('pid'), False)
            if child_detail:
                get_child(p[1].get('pid'), False, memory_detail= memory_detail, tab = 1, kill = kill_recursive)
            print "-" * MAX_LENGTH        
        #print "list_process =", list_process[-len(query):]
        #print "list_filter  =", list_filter[-len(query):]
        #print "-" * 200
    else:
        for i in query:
            if str(i).isdigit():
                for n in list_process:
                    if int(i) == list_process.get(n).get('pid'):
                        p = psutil.Process(int(i))
                        print "Name   :", make_colors(str(list_process.get(n).get('name')), 'yellow')
                        print "PID    :", make_colors(str(list_process.get(n).get('pid')), 'white', 'red')
                        print "EXE    :", make_colors(str(list_process.get(n).get('exe')), 'white', 'green')
                        print "MEM    :", make_colors(convert_size(list_process.get(n).get('mem')), 'white', 'blue')
                        if str(list_process.get(n).get('name')) == str(" ".join(list_process.get(n).get('cmd'))):
                            print "CMD    :"
                        elif str(list_process.get(n).get('exe')) == str(" ".join(list_process.get(n).get('cmd'))):
                            print "CMD    :"                    
                        else:
                            print "CMD    :", make_colors(str(" ".join(list_process.get(n).get('cmd'))), 'white', 'blue')
                        if kill:
                            p.terminate()                        
                        try:
                            STATUS = p.status()
                        except:
                            STATUS = "TERMINATED !!!"                    
                        print "STATUS : " + make_colors(STATUS.upper(), 'white', 'red', ['bold', 'blink'])
                        #print make_colors(STATUS.upper(), 'white', 'red', ['bold', 'blink'])
                        if memory_detail:
                            get_memory_full_info(list_process.get(n).get('pid'), False)
                        if child_detail:
                            get_child(list_process.get(n).get('pid'), True, process_instance= p, memory_detail= memory_detail, tab = 1, kill = kill_recursive)
                        print "-" * MAX_LENGTH
            else:
                for n in list_process:
                    if str(i).lower() == list_process.get(n).get('name').lower():
                        ver += 1
                        try:
                            p = psutil.Process(list_process.get(n).get('pid'))
                            print "Name   :", make_colors(str(list_process.get(n).get('name')), 'yellow')
                            print "PID    :", make_colors(str(list_process.get(n).get('pid')), 'white', 'red')
                            print "EXE    :", make_colors(str(list_process.get(n).get('exe')), 'white', 'green')
                            print "MEM    :", make_colors(convert_size(list_process.get(n).get('mem')), 'white', 'blue')
                            if str(list_process.get(n).get('name')) == str(" ".join(list_process.get(n).get('cmd'))):
                                print "CMD    :"
                            elif str(list_process.get(n).get('exe')) == str(" ".join(list_process.get(n).get('cmd'))):
                                print "CMD    :"
                            else:
                                print "CMD    :", make_colors(str(" ".join(list_process.get(n).get('cmd'))), 'white', 'blue')
                            if kill:
                                p.terminate()                            
                            try:
                                STATUS = p.status()
                            except:
                                STATUS = "TERMINATED !!!"                    
                            print "STATUS :", make_colors(STATUS.upper(), 'white', 'red', ['bold', 'blink'])
                            if memory_detail:
                                get_memory_full_info(list_process.get(n).get('pid'), False)
                            if child_detail:
                                get_child(list_process.get(n).get('pid'), True, memory_detail= memory_detail, tab = 1, kill = kill_recursive) 
                            print "-" * MAX_LENGTH
                        except psutil.NoSuchProcess:
                            pass
                        except:
                            traceback.format_exc()
                    else:
                        if str(i).lower() in list_process.get(n).get('name').lower():
                            ver += 1
                            try:
                                p = psutil.Process(list_process.get(n).get('pid'))
                                print "Name   :", make_colors(str(list_process.get(n).get('name')), 'yellow')
                                print "PID    :", make_colors(str(list_process.get(n).get('pid')), 'white', 'red')
                                print "EXE    :", make_colors(str(list_process.get(n).get('exe')), 'white', 'green')
                                print "MEM    :", make_colors(convert_size(list_process.get(n).get('mem')), 'white', 'blue')
                                if str(list_process.get(n).get('name')) == str(" ".join(list_process.get(n).get('cmd'))):
                                    print "CMD    :"
                                elif str(list_process.get(n).get('exe')) == str(" ".join(list_process.get(n).get('cmd'))):
                                    print "CMD    :"
                                else:
                                    print "CMD    :", make_colors(str(" ".join(list_process.get(n).get('cmd'))), 'white', 'blue')
                                if kill:
                                    p.terminate()                                
                                try:
                                    STATUS = p.status()
                                except:
                                    STATUS = "TERMINATED !!!"                    
                                print "STATUS :", make_colors(STATUS.upper(), 'white', 'red', ['bold', 'blink'])
                                if memory_detail:
                                    get_memory_full_info(list_process.get(n).get('pid'), False)
                                if child_detail:
                                    get_child(list_process.get(n).get('pid'), True, memory_detail= memory_detail, tab = 1, kill = kill_recursive)
                                print "-" * MAX_LENGTH
                            except psutil.NoSuchProcess:
                                pass
                            except:
                                traceback.format_exc()
                if ver == 0:
                    for n in list_process:
                        if not sys.platform == 'win32':
                            n_check = list_process.get(n).get('exe')
                        else:
                            n_check = list_process.get(n).get('exe')[0]
                        if str(i) == n_check.lower():
                            #print "XXX =", list_process.get(n).get('exe')[0].lower()
                            ver += 1
                            p = psutil.Process(list_process.get(n).get('pid'))
                            if kill:
                                p.terminate()
                            try:
                                STATUS = p.status()
                            except:
                                STATUS = "TERMINATED !!!"                        
                            print "Name   :", make_colors(str(list_process.get(n).get('name')), 'yellow')
                            print "PID    :", make_colors(str(list_process.get(n).get('pid')), 'white', 'red')
                            print "EXE    :", make_colors(str(list_process.get(n).get('exe')), 'white', 'green')
                            print "MEM    :", make_colors(convert_size(list_process.get(n).get('mem')), 'white', 'blue')
                            if str(list_process.get(n).get('name')) == str(" ".join(list_process.get(n).get('cmd'))):
                                print "CMD    :"
                            elif str(list_process.get(n).get('exe')) == str(" ".join(list_process.get(n).get('cmd'))):
                                print "CMD    :"
                            else:
                                print "CMD    :", make_colors(str(" ".join(list_process.get(n).get('cmd'))), 'white', 'blue')                    
                            print "STATUS :", make_colors(STATUS.upper(), 'white', 'red', ['bold', 'blink'])
                            if memory_detail:
                                get_memory_full_info(list_process.get(n).get('pid'), False)
                            if child_detail:
                                get_child(list_process.get(n).get('pid'), True, memory_detail= memory_detail, tab = 1, kill = kill_recursive)
                            print "-" * MAX_LENGTH
                        else:
                            if str(i) in list_process.get(n).get('exe').lower():
                                ver += 1
                                p = psutil.Process(list_process.get(n).get('pid'))
                                if kill:
                                    p.terminate()
                                try:
                                    STATUS = p.status()
                                except:
                                    STATUS = "TERMINATED !!!"                        
                                print "Name   :", make_colors(str(list_process.get(n).get('name')), 'yellow')
                                print "PID    :", make_colors(str(list_process.get(n).get('pid')), 'white', 'red')
                                print "EXE    :", make_colors(str(list_process.get(n).get('exe')), 'white', 'green')
                                print "MEM    :", make_colors(convert_size(list_process.get(n).get('mem')), 'white', 'blue')
                                if str(list_process.get(n).get('name')) == str(" ".join(list_process.get(n).get('cmd'))):
                                    print "CMD    :"
                                elif str(list_process.get(n).get('exe')) == str(" ".join(list_process.get(n).get('cmd'))):
                                    print "CMD    :"
                                else:
                                    print "CMD    :", make_colors(str(" ".join(list_process.get(n).get('cmd'))), 'white', 'blue')                    
                                print "STATUS :", make_colors(STATUS.upper(), 'white', 'red', ['bold', 'blink'])
                                if memory_detail:
                                    get_memory_full_info(list_process.get(n).get('pid'), False)
                                if child_detail:
                                    get_child(list_process.get(n).get('pid'), True, memory_detail= memory_detail, tab = 1, kill = kill_recursive)  
                                print "-" * MAX_LENGTH
                if ver == 0:
                    print make_colors("NOT FOUND !", 'white', 'red', ['bold', 'blink'])

def restart(query):
    import subprocess
    list_process, list_filter = ps()
    ver = 0
    for i in query:
        if str(i).isdigit():
            for n in list_process:
                if int(i) == list_process.get(n).get('pid'):
                    cmd = []
                    p = psutil.Process(int(i))
                    p.terminate()
                    print "Name   :", make_colors(str(list_process.get(n).get('name')), 'yellow')
                    print "PID    :", make_colors(str(list_process.get(n).get('pid')), 'white', 'red')
                    print "EXE    :", make_colors(str(list_process.get(n).get('exe')), 'white', 'green')
                    print "MEM    :", make_colors(convert_size(list_process.get(n).get('mem')), 'white', 'blue')
                    if str(list_process.get(n).get('name')) == str(" ".join(list_process.get(n).get('cmd'))):
                        print "CMD    :"
                    elif str(list_process.get(n).get('exe')) == str(" ".join(list_process.get(n).get('cmd'))):
                        print "CMD    :"                    
                    else:
                        print "CMD    :", make_colors(str(" ".join(list_process.get(n).get('cmd'))), 'white', 'blue')
                    try:
                        STATUS = p.status()
                    except:
                        STATUS = "TERMINATED !!!"                    
                    print "STATUS :", make_colors(STATUS.upper(), 'white', 'red', ['bold', 'blink'])
                    print "+" * 100
                    while 1:
                        try:
                            p.status()
                        except:
                            a = subprocess.Popen([list_process.get(n).get('exe')] + cmd, stderr=subprocess.PIPE, shell=True)
                            p1 = psutil.Process(int(a.pid))
                            print "Name   :", make_colors(str(list_process.get(n).get('name')), 'yellow')
                            print "PID    :", make_colors(str(a.pid), 'white', 'red')
                            print "EXE    :", make_colors(str(list_process.get(n).get('exe')), 'white', 'green')
                            print "MEM    :", make_colors(convert_size(p1.memory_full_info().vms), 'white', 'blue')
                            print "CMD    :", " ".join(cmd)
                            print "STATUS :", make_colors("STARTED", 'white', 'red', ['bold', 'blink'])
                            try:
                                x = p.status()
                                if x == 'running':
                                    break
                                if not a.poll():
                                    break
                            except:
                                if not a.poll():
                                    break
                                else:
                                    pass
                            (out, err) = a.communicate()
                            if err:
                                print "STATUS1:", make_colors("ERROR", 'white', 'red', ['bold', 'blink'])
                                print make_colors("ERROR: ", 'white','red',['bold','blink']) + make_colors(str(err), 'white','yellow',['bold'])
                            break
                    print "-" * 100
        else:
            for n in list_process:
                if str(i).lower() == list_process.get(n).get('name').lower():
                    cmd = []
                    ver += 1
                    p = psutil.Process(list_process.get(n).get('pid'))
                    p.terminate()
                    print "Name   :", make_colors(str(list_process.get(n).get('name')), 'yellow')
                    print "PID    :", make_colors(str(list_process.get(n).get('pid')), 'white', 'red')
                    print "EXE    :", make_colors(str(list_process.get(n).get('exe')), 'white', 'green')
                    print "MEM    :", make_colors(convert_size(list_process.get(n).get('mem')), 'white', 'blue')
                    if str(list_process.get(n).get('name')) == str(" ".join(list_process.get(n).get('cmd'))):
                        print "CMD    :"
                    elif str(list_process.get(n).get('exe')) == str(" ".join(list_process.get(n).get('cmd'))):
                        print "CMD    :"
                    else:
                        print "CMD    :", make_colors(str(" ".join(list_process.get(n).get('cmd'))), 'white', 'blue')
                    try:
                        STATUS = p.status()
                    except:
                        STATUS = "TERMINATED !!!"                    
                    print "STATUS :", make_colors(STATUS.upper(), 'white', 'red', ['bold', 'blink'])
                    print "+" * 100
                    while 1:
                        try:
                            p.status()
                        except:
                            a = subprocess.Popen([list_process.get(n).get('exe')] + cmd, stderr=subprocess.PIPE, shell=True)
                            p1 = psutil.Process(int(a.pid))
                            print "Name   :", make_colors(str(list_process.get(n).get('name')), 'yellow')
                            print "PID    :", make_colors(str(a.pid), 'white', 'red')
                            print "EXE    :", make_colors(str(list_process.get(n).get('exe')), 'white', 'green')
                            print "MEM    :", make_colors(convert_size(p1.memory_full_info().vms), 'white', 'blue')
                            print "CMD    :", " ".join(cmd)
                            print "STATUS :", make_colors("STARTED", 'white', 'red', ['bold', 'blink'])
                            try:
                                x = p.status()
                                if x == 'running':
                                    break
                                if not a.poll():
                                    break
                            except:
                                if not a.poll():
                                    break
                                else:
                                    pass
                            (out, err) = a.communicate()
                            if err:
                                print "STATUS1:", make_colors("ERROR", 'white', 'red', ['bold', 'blink'])
                                print make_colors("ERROR: ", 'white','red',['bold','blink']) + make_colors(str(err), 'white','yellow',['bold'])
                            break
                    print "-" * 100
                else:
                    if str(i).lower() in list_process.get(n).get('name').lower():
                        cmd = []
                        ver += 1
                        p = psutil.Process(list_process.get(n).get('pid'))
                        p.terminate()
                        print "Name   :", make_colors(str(list_process.get(n).get('name')), 'yellow')
                        print "PID    :", make_colors(str(list_process.get(n).get('pid')), 'white', 'red')
                        print "EXE    :", make_colors(str(list_process.get(n).get('exe')), 'white', 'green')
                        print "MEM    :", make_colors(convert_size(list_process.get(n).get('mem')), 'white', 'blue')
                        if str(list_process.get(n).get('name')) == str(" ".join(list_process.get(n).get('cmd'))):
                            print "CMD    :"
                        elif str(list_process.get(n).get('exe')) == str(" ".join(list_process.get(n).get('cmd'))):
                            print "CMD    :"
                        else:
                            print "CMD    :", make_colors(str(" ".join(list_process.get(n).get('cmd'))), 'white', 'blue')
                        try:
                            STATUS = p.status()
                        except:
                            STATUS = "TERMINATED !!!"                    
                        print "STATUS :", make_colors(STATUS.upper(), 'white', 'red', ['bold', 'blink'])
                        print "+" * 100
                        while 1:
                            try:
                                p.status()
                            except:
                                a = subprocess.Popen([list_process.get(n).get('exe')] + cmd, stderr=subprocess.PIPE, shell=True)
                                p1 = psutil.Process(int(a.pid))
                                print "Name   :", make_colors(str(list_process.get(n).get('name')), 'yellow')
                                print "PID    :", make_colors(str(a.pid), 'white', 'red')
                                print "EXE    :", make_colors(str(list_process.get(n).get('exe')), 'white', 'green')
                                print "MEM    :", make_colors(convert_size(p1.memory_full_info().vms), 'white', 'blue')
                                print "CMD    :", " ".join(cmd)
                                print "STATUS :", make_colors("STARTED", 'white', 'red', ['bold', 'blink'])
                                try:
                                    x = p.status()
                                    if x == 'running':
                                        break
                                    if not a.poll():
                                        break
                                except:
                                    if not a.poll():
                                        break
                                    else:
                                        pass
                                (out, err) = a.communicate()
                                if err:
                                    print "STATUS1:", make_colors("ERROR", 'white', 'red', ['bold', 'blink'])
                                    print make_colors("ERROR: ", 'white','red',['bold','blink']) + make_colors(str(err), 'white','yellow',['bold'])
                                break
                        print "-" * 100
            if ver == 0:
                for n in list_process:
                    if str(i) == list_process.get(n).get('exe')[0].lower():
                        cmd = []
                        ver += 1
                        p = psutil.Process(list_process.get(n).get('pid'))
                        p.terminate()
                        try:
                            STATUS = p.status()
                        except:
                            STATUS = "TERMINATED !!!"                        
                        print "Name   :", make_colors(str(list_process.get(n).get('name')), 'yellow')
                        print "PID    :", make_colors(str(list_process.get(n).get('pid')), 'white', 'red')
                        print "EXE    :", make_colors(str(list_process.get(n).get('exe')), 'white', 'green')
                        print "MEM    :", make_colors(convert_size(list_process.get(n).get('mem')), 'white', 'blue')
                        if str(list_process.get(n).get('name')) == str(" ".join(list_process.get(n).get('cmd'))):
                            print "CMD    :"
                        elif str(list_process.get(n).get('exe')) == str(" ".join(list_process.get(n).get('cmd'))):
                            print "CMD    :"
                        elif str(list_process.get(n).get('exe')) in str(" ".join(list_process.get(n).get('cmd'))):
                            print "CMD    :"
                        else:
                            print "CMD    :", make_colors(str(" ".join(list_process.get(n).get('cmd'))), 'white', 'blue')                    
                            cmd = list_process.get(n).get('cmd')
                        print "STATUS :", make_colors(STATUS.upper(), 'white', 'red', ['bold', 'blink'])
                        print "+" * 100
                        while 1:
                            try:
                                p.status()
                            except:
                                a = subprocess.Popen([list_process.get(n).get('exe')] + cmd, stderr=subprocess.PIPE, shell=True)
                                p1 = psutil.Process(int(a.pid))
                                print "Name   :", make_colors(str(list_process.get(n).get('name')), 'yellow')
                                print "PID    :", make_colors(str(a.pid), 'white', 'red')
                                print "EXE    :", make_colors(str(list_process.get(n).get('exe')), 'white', 'green')
                                print "MEM    :", make_colors(convert_size(p1.memory_full_info().vms), 'white', 'blue')
                                print "CMD    :", " ".join(cmd)
                                print "STATUS :", make_colors("STARTED", 'white', 'red', ['bold', 'blink'])
                                try:
                                    x = p.status()
                                    if x == 'running':
                                        break
                                    if not a.poll():
                                        break
                                except:
                                    if not a.poll():
                                        break
                                    else:
                                        pass
                                (out, err) = a.communicate()
                                if err:
                                    print "STATUS1:", make_colors("ERROR", 'white', 'red', ['bold', 'blink'])
                                    print make_colors("ERROR: ", 'white','red',['bold','blink']) + make_colors(str(err), 'white','yellow',['bold'])
                                break
                        print "-" * 100
                    else:
                        if str(i) in list_process.get(n).get('exe').lower():
                            cmd = []
                            ver += 1
                            p = psutil.Process(list_process.get(n).get('pid'))
                            p.terminate()
                            try:
                                STATUS = p.status()
                            except:
                                STATUS = "TERMINATED !!!"                        
                            print "Name   :", make_colors(str(list_process.get(n).get('name')), 'yellow')
                            print "PID    :", make_colors(str(list_process.get(n).get('pid')), 'white', 'red')
                            print "EXE    :", make_colors(str(list_process.get(n).get('exe')), 'white', 'green')
                            print "MEM    :", make_colors(convert_size(list_process.get(n).get('mem')), 'white', 'blue')
                            if str(list_process.get(n).get('name')) == str(" ".join(list_process.get(n).get('cmd'))):
                                print "CMD    :"
                            elif str(list_process.get(n).get('exe')) == str(" ".join(list_process.get(n).get('cmd'))):
                                print "CMD    :"
                            elif str(list_process.get(n).get('exe')) in str(" ".join(list_process.get(n).get('cmd'))):
                                print "CMD    :"
                            else:
                                print "CMD    :", make_colors(str(" ".join(list_process.get(n).get('cmd'))), 'white', 'blue')                    
                                cmd = list_process.get(n).get('cmd')
                            print "STATUS :", make_colors(STATUS.upper(), 'white', 'red', ['bold', 'blink'])
                            print "+" * 100
                            while 1:
                                try:
                                    p.status()
                                except:
                                    a = subprocess.Popen([list_process.get(n).get('exe')] + cmd, stderr=subprocess.PIPE, shell=True)
                                    p1 = psutil.Process(int(a.pid))
                                    print "Name   :", make_colors(str(list_process.get(n).get('name')), 'yellow')
                                    print "PID    :", make_colors(str(a.pid), 'white', 'red')
                                    print "EXE    :", make_colors(str(list_process.get(n).get('exe')), 'white', 'green')
                                    print "MEM    :", make_colors(convert_size(p1.memory_full_info().vms), 'white', 'blue')
                                    print "CMD    :", " ".join(cmd)
                                    print "STATUS :", make_colors("STARTED", 'white', 'red', ['bold', 'blink'])
                                    try:
                                        x = p.status()
                                        if x == 'running':
                                            break
                                        if not a.poll():
                                            break
                                    except:
                                        if not a.poll():
                                            break
                                        else:
                                            pass
                                    (out, err) = a.communicate()
                                    if err:
                                        print "STATUS1:", make_colors("ERROR", 'white', 'red', ['bold', 'blink'])
                                        print make_colors("ERROR: ", 'white','red',['bold','blink']) + make_colors(str(err), 'white','yellow',['bold'])
                                    break
                            print "-" * 100
            if ver == 0:
                print make_colors("NOT FOUND !", 'white', 'red', ['bold', 'blink'])

def usage():
    help = """
    pl.py -f xporcess1 xporcess2
    pl.py --filter xporcess1.exe xporcess2.exe
    pl.py -f 9939 9877
    pl.py -k killprocess
    pl.py --kill killprocess.exe
    pl.py --kill 9919
    
Options:
    -h --help      Show this help
    -f --filter    filter process, this will show at end
    -k --kill      list process and kill process
    -v --version   this version
    
"""
    import argparse
    parse = argparse.ArgumentParser(formatter_class= argparse.RawTextHelpFormatter, version= '1.0')
    parse.add_argument('-f', '--filter', help = 'Filter', action = 'store', nargs = '*')
    parse.add_argument('-k', '--kill', help = 'Kill process with name or PID', action = 'store', nargs = '*')
    parse.add_argument('-K', '--always-kill', help = 'Kill process with name or PID', action = 'store', nargs = '*')
    parse.add_argument('-s', '--sort-by', help = 'Sort list by [name, pid, exe, mem, cmd]', action = 'store', type = str)
    parse.add_argument('-t', '--sort-time', help = 'Sort list by time of start/creation', action = 'store_true')
    parse.add_argument('-m', '--sort-mem', help = 'Sort list by Private Memory usage', action = 'store_true')
    parse.add_argument('-p', '--sort-pid', help = 'Sort list by PID', action = 'store_true')
    parse.add_argument('-w', '--sort-cpu-percent', help = 'Sort list by CPU Load Percent', action = 'store_true')
    parse.add_argument('-e', '--sort-exe', help = 'Sort list by Exe Name', action = 'store_true')
    parse.add_argument('-n', '--sort-name', help = 'Sort list by Name', action = 'store_true')
    parse.add_argument('-T', '--tail', help = 'Sort list by time and show last of N', action = 'store', type = int)
    parse.add_argument('-x', '--search', help = 'search by input [name, pid, mem] for mem which approaching', action = 'store', nargs = '*')
    parse.add_argument('-X', '--search-kill', help = 'search by input [name, pid, mem] for mem which approaching then kill', action = 'store', nargs = '*')
    parse.add_argument('-z', '--fast', help = 'search by the last of list process', action = 'store_true')
    parse.add_argument('-r', '--reverse', help = 'List reverse', action = 'store_true')
    parse.add_argument('-rr', '--recursive', help = 'Recursive process and child', action = 'store_true')
    parse.add_argument('-R', '--restart', help = 'Restart process', action = 'store', nargs='*')
    parse.add_argument('-a', '--all', help = 'Show all list include this', action = 'store_true')
    parse.add_argument('-c', '--childs', help = 'Show all Childs process of process', action = 'store_true')
    parse.add_argument('-M', '--memory-details', help = 'Show all memory details of process', action = 'store_true')
    parse.add_argument('-d', '--details', help = 'Show all details of process', action = 'store_true')
    parse.add_argument('-C', '--show-cpu-percent', help = 'Show CPU Load Percent', action = 'store_true')
    parse.add_argument('-MM', '--memory-detail', help = 'Show all memory detail of one process by given pid or correct name', action = 'store', type = int)
    args = parse.parse_args()
    #print "args.filter =", args.filter
    #if len(sys.argv) == 1:
        #p, p1 = ps()
        #makeTable(p, p1)
    #else:
    SORTED = False
    sorting = args.sort_by
    if args.search:
        search(args.search, False, args.fast, args.details, args.childs, args.recursive)
    elif args.restart:
        restart(args.restart)
    elif args.search_kill:
        search(args.search_kill, True, args.fast, args.details, args.childs, args.recursive)
    elif args.memory_detail:
        get_memory_full_info(args.memory_detail, True)
    else:
        if args.sort_time:
            sorting = 'time'
            SORTED = True
        if args.sort_cpu_percent:
            sorting = 'cpu'
            SORTED = True
        if args.sort_mem:
            sorting = 'mem'
            SORTED = True
        if args.sort_pid:
            sorting = 'pid'
            SORTED = True
        if args.sort_exe:
            sorting = 'exe'
            SORTED = True
        if args.sort_name:
            sorting = 'name'
            SORTED = True
        if args.sort_by:
            SORTED = True
        if args.kill:
            kill(args.kill)
        if args.always_kill:
            kill(args.always_kill, True)
        if args.filter:
            if sorting == 'cpu' or args.show_cpu_percent:
                p, p1 = ps(args.filter, sorting, args.reverse, args.all, True)
            else:
                p, p1 = ps(args.filter, sorting, args.reverse, args.all)
            try:
                if sorting == 'cpu' or args.show_cpu_percent:
                    makeTable(p, p1, SORTED, args.tail, True)
                else:
                    makeTable(p, p1, SORTED, args.tail)
            except:
                if os.getenv('DEBUG') or os.getenv('debug'):
                    traceback.format_exc(print_msg= True)
                else:
                    traceback.format_exc(print_msg= False)
                pass
        else:
            if not args.kill and not args.always_kill and not args.search and not args.search_kill:
                if sorting == 'cpu' or args.show_cpu_percent:
                    p, p1 = ps(args.filter, sorting, args.reverse, args.all, True)
                else:
                    p, p1 = ps(args.filter, sorting, args.reverse, args.all)
                try:
                    if sorting == 'cpu' or args.show_cpu_percent:
                        makeTable(p, p1, SORTED, args.tail, True)
                    else:
                        makeTable(p, p1, SORTED, args.tail)
                except:
                    if os.getenv('DEBUG') or os.getenv('debug'):
                        traceback.format_exc(print_msg= True)
                    else:
                        traceback.format_exc(print_msg= False)
                    parse.print_help()
        
if __name__ == '__main__':
    #p, p1 = ps()
    #makeTable(p)
    usage()
    #query = ['python', 'fmedia']
    #search(query, False, True)
    