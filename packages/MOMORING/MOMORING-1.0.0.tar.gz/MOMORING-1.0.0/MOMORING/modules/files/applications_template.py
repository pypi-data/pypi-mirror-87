def get_applications_template(project_name):
    txt = '''\
from momo_PJ_name.utils.nitrogen_utils import get_cpu_num, get_env_param
import os


def func_on_nitrogen():
    datapath = os.environ.get('DATAPATH')
    savedpath = os.environ.get('SAVEDPATH')
    
    num_cpu = get_cpu_num()
    
    param = get_env_param('PARAM', default_value='value', type_func=str)

'''
    return txt.replace('momo_PJ_name', project_name)
