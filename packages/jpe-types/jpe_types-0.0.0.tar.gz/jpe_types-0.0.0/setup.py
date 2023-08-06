from distutils.core import setup

setup(
    name = "jpe_types",
    packages=["jpe_types/paralel",
              "jpe_types"],
    version=0,
    license='wtfpl',
    description="slitly improved python types",
    long_description="""
    Threading
    -   adds thread inharitance and return posibility
    -   logging filteter for thread inheritance
    -   a thread and a lock in the same class to make it slitly easyer to work with threads
    """,
    author = 'Julian Wandhoven',                   # Type in your name
    author_email = 'julian.wandhoven@fgz.ch',

    url="https://github.com/JulianWww/jpe_types",
    download_url="https://github.com/JulianWww/jpe_types/archive/0.tar.gz",
    keywords=["dtypes", "jpe", "utils", "paralel", "logging"],
    classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3.6' ,
    'Programming Language :: Python :: 3'],#Specify which pyhton versions that you want to support
)