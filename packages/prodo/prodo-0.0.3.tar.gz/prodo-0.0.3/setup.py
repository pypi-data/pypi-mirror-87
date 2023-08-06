from setuptools import setup, find_packages

setup(
    name='prodo',
    version='0.0.3',
    author="Karishnu Poddar",
    author_email="karishnu@gmail.com",
    py_modules=['src/script'],
    package_dir = {'': '.'},
    install_requires=[
        'Click',
        'paramiko',
        'scp',
        'nbformat',
        'nbconvert',
        'ipython'
    ],
    entry_points='''
        [console_scripts]
        cuttle=script:cli
    ''',
)