from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='affiliatelinkconverter',
    version='1.0.3',
    description='affiliate link converter package',
    url='',
    author='Manoj Sitapara',
    author_email='manojsitapara@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='affiliatelinkconverter',
    packages=find_packages(),
    install_requires=[
        'furl>=2.1.0',
        'unshortenit>=0.4.0'

    ]
)