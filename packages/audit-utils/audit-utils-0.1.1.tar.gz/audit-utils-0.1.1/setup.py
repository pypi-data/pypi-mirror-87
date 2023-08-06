
import os
import setuptools

def readme():
    path = os.path.dirname(__file__)
    with open(os.path.join(path, 'README.rst')) as f:
        return f.read()

name = 'audit-utils'
description = 'DB Table Auditing Utilities'
version = '0.1.1'
author = 'Fictive Kin LLC'
email = 'hello@fictivekin.com'
classifiers = [
    'Development Status :: 3 - Alpha',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.8',
    'Topic :: Software Development',
]

if __name__ == "__main__":
    setuptools.setup(
        name=name,
        version=version,
        description=description,
        long_description=readme(),
        classifiers=classifiers,
        url='https://github.com/fictivekin/audit-utils',
        author=author,
        author_email=email,
        maintainer=author,
        maintainer_email=email,
        license='MIT',
        python_requires=">=3.8",
        packages=[
            'audit',
            'audit.models',
            'audit.utils',
        ],
        install_requires=[
            'alembic',
            'sqlalchemy',
        ],
    )
