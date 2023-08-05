from setuptools import setup, find_packages

setup(
    name='Digo',
    version='0.1.6',
    author='DiggerWorks',
    author_email='support@digger.works',
    packages=find_packages(),
    long_description=open('README.md').read(),
    keywords=['digo', 'ml'],
    install_requires=['azure-core', 'azure-storage-blob', 'Pillow', 'numpy', 'requests', 'psutil', 'nvgpu', 'argparse', 'inputimeout'],
    zip_safe=False
)