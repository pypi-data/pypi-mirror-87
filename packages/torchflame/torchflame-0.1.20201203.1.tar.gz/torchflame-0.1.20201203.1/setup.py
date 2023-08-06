from setuptools import setup, find_packages

with open("README.rst", "r") as f:
    long_description = f.read()
setup(
    name='torchflame',
    packages=find_packages(),
    version='0.1.20201203.1',
    license='MIT',
    description='a small extension of pytorch writen and collected by Jewelry',
    long_description=long_description,
    author='Jewelry',
    author_email='3180105772@zju.edu.cn',
    classifiers=[],
    install_requires=['torch', 'torchvision', 'torch_optimizer', 'numpy', 'matplotlib', 'pandas', 'xlrd'],
    python_requires='>=3.6'
)
