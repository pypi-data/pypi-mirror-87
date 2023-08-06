from setuptools import setup, find_packages
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='fb_waba_manager',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    version='v0.0.4',
    license='MIT',
    description='Helper to handle with facebook\'s waba',
    author='Gabriel Rodrigues dos Santos',
    author_email='gabrielr@take.net',
    url='https://github.com/chr0m1ng/fb-waba-manager',
    keywords=['facebook', 'graph api', 'waba'],
    install_requires=[
        'requests'
    ],
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        # "3 - Alpha", "4 - Beta" or "5 - Production/Stable"
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8'
    ]
)
