from setuptools import setup

setup(
    name='SHOU-urp-auto-evaluate',
    version='0.0.1',
    package_dir={'': 'project'},
    url='https://github.com/adminerest/SHOU-urp-auto-evaluate',
    license='GPL-3.0',
    author='@adminerest, @huobaolajiao, @spencercjh',
    author_email='',
    description='上海海洋大学urp自动评教程序',
    install_requires=[
        'beautifulsoup4',
        'requests',
        'Pillow',
        'certifi',
        'chardet',
        'idna',
        'soupsieve',
        'urllib3'
    ]
)
