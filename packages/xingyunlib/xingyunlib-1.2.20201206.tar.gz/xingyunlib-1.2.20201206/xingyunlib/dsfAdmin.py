from pkg_resources import find_distributions
from sys import executable,exit
sys.executable
_path = executable.split("python.exe")[0]+"lib\\site-packages"
_res = find_distributions(_path)
_list=[]
_down_from=['https://pypi.tuna.tsinghua.edu.cn/simple', 'https://pypi.douban.com/simple','https://mirrors.aliyun.com/pypi/simple/', 'http://pypi.mirrors.ustc.edu.cn/simple/']
for _item in _res:
    _item=_item.hashcmp
    v=list(_item)
    v[0]=str(v[0])
    _item=tuple(v)
    del v
    _list.append(_item)

# for x in _list:
#     print(x)
# exit()
def pip_cmd(cmd):
    import os,sys

    if "linux" in sys.platform:
        mit="sudo apt-get"
    elif "darwin" in sys.platform:
        mit=f"sudo {sys.executable} -m pip"
    elif "win" in sys.platform:
        mit=f"{sys.executable} -m pip"
    os.system(f"{mit} {cmd}")

def get_interpreter():
    import sys
    return sys.executable

def get_packages():
    return _list

def look_for_package(pakage, ver=False):
    Ls = get_packages()
    for x in Ls:
        if x[2] == pakage and((not ver) or (ver==x[0])):
            return x
    return False
# print(look_for_package('pycparser','2.20'))#'2.20', -1, 'pycparser'
# exit()
def upgrade(pakage):
    # import os
    # if type(pakage) != type(" "):
    #     pakage = "".join(pakage)
    pip_cmd(f"install --upgrade {pakage} -i {_down_from[1]}")


def install(pakage, interpreter=None):
    # import os
    # if type(pakage) != type(" "):
    #     pakage = " ".join(pakage)
    # if interpreter == None:
    #     interpreter = get_interpreter()
    print(pakage)
    pip_cmd(f"install {pakage} -i {_down_from[1]}")
# upgrade("xingyunlib")

def dump_pip_list(filename):
    pip_cmd(f"freeze > {filename}")

# dump_pip_list("free.txt")
def load_pip_list(filename, interpreter=None):
    pip_cmd(f"install -r {filename}")
# load_pip_list("free.txt")

def get_all_pakages():
    return
# print(find_packages("xingyunlib"))
# exit()
exit()