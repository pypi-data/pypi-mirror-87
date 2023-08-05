'''
setup.py is the Akasia setup file.
'''

from setuptools import setup

setup(
    version='1.3.0',
    license="MIT License",
    name='Akasia',
    author='Robrecht De Rouck',
    author_email='Robrecht.De.Rouck@gmail.com',
    maintainer='RIERIUS',
    maintainer_email='riderius.help@gmail.com',
    project_urls={
        "Source": "https://github.com/RIDERIUS/Akasia"},
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: Implementation :: CPython",
        "Environment :: Console",
        "Intended Audience :: Developers",
    ],
    python_requires=">=3.8",
    py_modules=['akasia'],
    entry_points={
        'console_scripts': ['akasia = akasia:main', ], },
    description='A fork tiny python text-based web browser Asiakas.',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    install_requires=[
        "certifi==2020.11.8",
        "chardet==3.0.4",
        "html2text==2020.1.16",
        "idna==2.10",
        "requests==2.25.0",
        "urllib3==1.26.2"
    ]
)
