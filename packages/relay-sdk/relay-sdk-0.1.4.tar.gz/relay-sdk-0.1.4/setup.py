from os import path

import setuptools

long_description_file = path.join(
    path.abspath(path.dirname(__file__)),
    'README.rst',
)
with open(long_description_file, encoding='utf-8') as fp:
    long_description = fp.read()

setuptools.setup(
    name='relay-sdk',
    use_scm_version={
        'relative_to': __file__,
    },
    author='Puppet, Inc.',
    author_email='relay@puppet.com',
    description='SDK for interacting with Puppet Relay',
    long_description=long_description,
    long_description_content_type='text/x-rst',
    url='https://github.com/puppetlabs/relay-sdk-python',
    packages=setuptools.find_packages('src'),
    package_dir={'': 'src'},
    python_requires='>=3.8',
    setup_requires=[
        'setuptools_scm',
    ],
    install_requires=[
        'asgiref>=3.2.7',
        'hypercorn>=0.9.5',
        'requests>=2.23',
    ],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
    ],
)
