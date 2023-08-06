def nitrogen_utils():
    txt = '''\
import os
import shutil
import math


def get_cpu_num():
    """Get n_cpu, return NUM_CPU if user specified, else os.cpu_count()"""
    n_cpu = os.getenv('NUM_CPU')
    all_cpu = os.cpu_count()-1 if os.cpu_count() > 1 else 1

    if not n_cpu:
        n_cpu = all_cpu
    else:
        n_cpu = int(n_cpu)
        if n_cpu > all_cpu:
            n_cpu = all_cpu

    limit = os.getenv('CPU')
    if limit:
        n_cpu = math.ceil(int(limit)*2/3)

    print(f'n_cpu:{n_cpu}, limit:{limit}')
    return n_cpu


def create_workdir(dir_name='workdir'):
    stashpath = os.getenv('STASHPATH')
    if stashpath:
        # xbcp
        workdir = os.path.join(stashpath, dir_name)
    else:
        # local
        workdir = os.path.join('/home/', dir_name)

    if os.path.exists(workdir):
        shutil.rmtree(workdir)
    os.mkdir(workdir)
    return workdir


def get_env_param(env_str, default_value=None, type_func=str):
    value = os.getenv(env_str)
    if (value == True or value == False) and type_func == eval:
        return value
    if value:
        value = type_func(value)
    else:
        value = default_value
    print('ENV:', env_str, '| VALUE:', value, '| TYPE:', type(value))
    return value


def get_datafile(datapath, file_ext, get_all=False):
    file_list = [i for i in os.listdir(datapath) if i.endswith(file_ext)]
    if not file_list:
        return
    else:
        if get_all:
            return file_list
        else:
            return file_list[0]

'''
    return txt
