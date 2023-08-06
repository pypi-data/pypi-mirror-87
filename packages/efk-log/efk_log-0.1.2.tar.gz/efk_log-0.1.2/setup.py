import setuptools
import os.path as os_path

this_directory = os_path.abspath(os_path.dirname(__file__))


# 读取文件内容
def read_file(filename):
    with open(os_path.join(this_directory, filename), encoding='utf-8') as f:
        long_description = f.read()
    return long_description


setuptools.setup(
    name='efk_log',
    version='0.1.2',
    packages=setuptools.find_packages(include=('*',)),
    url='https://github.com/zip-data/efk-log.git',
    license='MIT',
    author='lishulong',
    author_email='lishulong.never@gmail.com',
    description='Python Json Log IO Operator',
    long_description=read_file('efk_log/readme.md'),
    # https://use-python.readthedocs.io/zh_CN/latest/packaging_and_sharing.html
    include_package_data=True,
    long_description_content_type="text/markdown",
    install_requires=[],
    zip_safe=False,
    classifiers=[
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        'Programming Language :: Python :: Implementation :: CPython',
        "Topic :: Software Development :: Libraries :: Python Modules",
        'Topic :: Utilities',
    ]
)
