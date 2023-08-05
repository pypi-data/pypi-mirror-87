from setuptools import setup, find_packages


requirements = [
    "chevron==0.13.1"
]

with open('README.md') as f:
    long_desc = f.read()

setup(
    name='envsubst-mustache',
    version='0.0.1',
    description='GNU envsubst-like tool with a mustache templating system.',
    long_description=long_desc,
    author='David Volm',
    author_email='david@volminator.com',
    url='https://github.com/daxxog/envsubst-mustache',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.9',
        'Topic :: Text Processing :: Markup'
    ],
    license='Apache 2.0',
    install_requires=requirements,
    py_modules=['envsubst_mustache'],
    packages=find_packages("src"),
    package_dir={'': 'src'},
    entry_points={
        'console_scripts': [
            'envsubst-mustache = envsubst_mustache:main',
        ],
    },
)
