import setuptools
from suoran import load_content
from suoran.command.skeleton import zip

zip('skeleton')

setuptools.setup(
    name='suoran',
    version='0.0.10',
    description='extends sanic',
    long_description=load_content('readme.md'),
    long_description_content_type='text/markdown',
    url='https://github.com/chenshenchao/suoran',
    keywords='sanic suoran',
    license='MIT',
    author='chenshenchao',
    author_email='chenshenchao@outlook.com',
    platforms='any',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    packages=setuptools.find_packages(),
    install_requires=[
        'sanic>=20.9.0',
        'tortoise-orm>=0.16.16',
        'aiomysql>=0.0.20',
    ],
    entry_points={
        'console_scripts': 'suoran=suoran.command:luanch',
    },
)
