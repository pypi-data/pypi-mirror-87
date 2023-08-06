
import PIL
"""
package:
    获取放置于里面的静态文件
args:
    filename:文件名
"""

def where_data(filename):
    import os
    basepath = os.path.abspath(__file__)
    folder = os.path.dirname(basepath)
    data_path = os.path.join(folder, filename)
    return data_path
print(where_data("xes\\AIspeak.py"))