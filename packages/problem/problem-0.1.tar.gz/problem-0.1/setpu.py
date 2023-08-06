from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()

setup(name='problem',
    version='0.1',
    description='this is problem',
    long_description=readme(),
    url='https://github.com/yingkhun/problem',
    author='yingkhun',
    author_email='yingkhunn@gmail.com',
    license='yingkhun',
    install_requires=['time', 'datetime',],
    keywords='problem',
    packages=['problem']
)