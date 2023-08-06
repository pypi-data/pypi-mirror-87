#coding=GBK
from distutils.core import setup
setup(
    name='muchenMath2', # 对外我们模块的名字
    version='1.0', # 版本号
    description='这是第一个对外发布的模块，里面只有数学方法，用于测试哦', #描述
    author='muchen', # 作者
    author_email='1070086888@qq.com',
    py_modules=['muchenMath2.demo1','muchenMath2.demo2']       # 要发布的模块
)
