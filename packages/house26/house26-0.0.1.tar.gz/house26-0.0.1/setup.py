import setuptools
with open('README.md', 'r') as f:
    long_description = f.read()

setuptools.setup(
    name = 'house26', #模块名
    version = '0.0.1', #版本号
    author = 'suxiawei',
    author_email = '773979910@qq.com',
    description = 'just test',
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    url = 'https://www.baidu.com/', #项目地址，一般是代码托管的网站
    packages = setuptools.find_packages(),
    install_requires = ['pandas'], #依赖项（可不设置）
    classifiers = [
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ]
)
