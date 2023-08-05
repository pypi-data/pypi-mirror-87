import os
from setuptools import setup, find_packages


def get_packages(package):
    """
    Return root package and all sub-packages.
    """
    return [dirpath
            for dirpath, dirnames, filenames in os.walk(package)
            if os.path.exists(os.path.join(dirpath, '__init__.py'))]


def get_package_data(package):
    """
    Return all files under the root package, that are not in a
    package themselves.
    """
    walk = [(dirpath.replace(package + os.sep, '', 1), filenames)
            for dirpath, dirnames, filenames in os.walk(package)
            if not os.path.exists(os.path.join(dirpath, '__init__.py'))]

    filepaths = []
    for base, filenames in walk:
        filepaths.extend([os.path.join(base, filename)
                          for filename in filenames])
    return {package: filepaths}


setup(
    name='bluedot_rest_framework',
    version='1.0.9',
    packages=get_packages('bluedot_rest_framework'),
    package_data=get_package_data('bluedot_rest_framework'),
    include_package_data=True,
    zip_safe=True,
    # install_requires=[
    #     'mongoengine',
    #     'djangorestframework'
    #     'django-rest-framework-mongoengine',
    #     'djangorestframework-jwt',
    #     'wechatpy',
    #     'pycryptodome',
    #     'oss2',
    #     'redis'
    # ],
)
