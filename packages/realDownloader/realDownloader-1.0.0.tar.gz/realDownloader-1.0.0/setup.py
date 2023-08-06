from setuptools import setup

setup(
    name="realDownloader",
    version="1.0.0",
    description="instant way to create a flask api for your databases",
    author="Mehdi YAHIA CHERIF",
    licence='GPL-3.0',
    classifiers=[
    "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
    "Programming Language :: Python :: 3" ,
    "Programming Language :: Python :: 3.7",
    ],
    packages=['downloader_folder'],
    include_package_data=True,
    install_requires=["sqlite3"],
    entry_points={
    "console_scripts":[
        "downloadFrom=downloader_folder.downloader:main",
    ]
    }
    )
    
    
