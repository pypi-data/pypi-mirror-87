from setuptools import setup
import os

"""
说明:
1. py_modules 只能指定一个文件
2. packages 配置包地址,默认不包含包的子包
3.打包模块给别人安装

```
python3 setup.py build
python setup.py sdist
dist/mypk1-1.0.zip
解压后使用
python setup.py install即可
```
4.发布模块到本地环境

在项目根目录下
```
python setup.py install
```

https://www.cnblogs.com/maociping/p/6633948.html

"""

this_directory = os.path.abspath(os.path.dirname(__file__))

# 读取文件内容
def read_file(filename):
    with open(os.path.join(this_directory, filename), encoding='utf-8') as f:
        long_description = f.read()
    return long_description

# 指定要安装的package
def get_packages(package):
    """Return root package and all sub-packages."""
    return [dirpath
            for dirpath, dirnames, filenames in os.walk(package)
            if os.path.exists(os.path.join(dirpath, '__init__.py'))]

# 获取依赖
def read_requirements(filename):
    return [line.strip() for line in read_file(filename).splitlines()
            if not line.startswith('#')]

my_packages = []
my_packages.extend(get_packages("package1"))
my_packages.extend(get_packages("package2"))
print("my_packages:", my_packages)

my_requirements = read_requirements('requirements.txt')
print("my_requirements:", my_requirements)


setup(
    name='mypk1',
    version="0.0.1",
    author='yangzhi',
    author_email='y.zhisky@163.com',
    url='http://www.zhim.top',
    license='MIT Licence',
    description='Project documentation with Markdown.',
    long_description=read_file('README.md'), # 读取的Readme文档内容
    long_description_content_type="text/markdown",  # 指定包文档格式为markdown
    platforms="any",
    packages=my_packages,
    # 包含非python脚本文件,搭配MANIFEST.in使用
    include_package_data=True,
    # 需要安装的依赖
    install_requires=my_requirements,
    python_requires='>=3.5',
    # 添加这个选项，在windows下Python目录的scripts下生成exe文件, 注意：模块与函数之间是冒号:
    entry_points={'console_scripts': [
        'test1 = package1.test2:cli',
        'test4 = package2.test4:main1',
    ]},
    # 程序的所属分类列表
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3 :: Only',
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        'Topic :: Documentation',
        'Topic :: Text Processing',
    ],
    # 此项需要，否则卸载时报windows error
    zip_safe=False,
)
