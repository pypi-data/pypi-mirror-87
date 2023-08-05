from setuptools import setup

with open('README.md','r') as fh:
    long_description = fh.read()

setup(
    name = 'SCoinAPI',
    version = '1.1.2',
    description = "The light package for the SCU blockchain in the IOTA system.",
    py_modules = ['SCoinAPI'],
    package_dir = {'' : 'src/SCoinAPI'},
    long_description = long_description,
    long_description_content_type='text/markdown',
    install_requires = ["requests>=2.23.0",],
    url = 'https://github.com/sefx5ever/SCoinAPI.git',
    author = 'Wyne Tan',
    author_email = 'sefx5ever@gmail.com',
)

# 創建 whl 檔 【python setup.py bdist_wheel】