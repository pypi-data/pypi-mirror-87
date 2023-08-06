from distutils.core import setup
import setuptools

setup(
    name = "torrent",
    packages=setuptools.find_packages(),
    version="0",
    license='wtfpl',
    description="python data scharing",
    long_description="""
    python server utils
    alowes for:
    -   calling functions on other devices in the session
    -   comunication bewean clients
    """,
    author = 'Julian Wandhoven',                   # Type in your name
    author_email = 'julian.wandhoven@fgz.ch',

    url="https://github.com/JulianWww/torent",
    download_url="https://github.com/JulianWww/torent/archive/0.tar.gz",
    keywords=["data", "multicomputer", "userfriendly", "simple", ],
    install_requires=[
        "jpe_types"
    ],
    classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Internet :: Proxy Servers',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3.6' ,
    'Programming Language :: Python :: 3'],#Specify which pyhton versions that you want to support

)