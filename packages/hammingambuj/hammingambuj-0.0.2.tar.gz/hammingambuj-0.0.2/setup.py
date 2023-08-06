from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 8',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='hammingambuj',
    version='0.0.2',
    description='Hamming code generation and error detection',
    Long_description=open('README.txt').read()+ '\n\n'+ open('CHANGELOG.txt').read(),
    url='',
    author='Ambuj Dubey',
    author_email='ambujdubey2426@gmail.com',
    License='MIT',
    classifiers=classifiers,
    keywords='hamming code',
    packages=['hammingambuj'],
    install_requires=['']
)
