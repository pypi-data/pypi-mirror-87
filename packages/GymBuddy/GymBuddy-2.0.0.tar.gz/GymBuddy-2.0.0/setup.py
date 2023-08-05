from setuptools import setup, find_packages,find_namespace_packages
import GymBuddyApp

setup(

    name = 'GymBuddy',
    version = '2.0.0',
    packages= find_namespace_packages(),
    url = 'https://github.com/CTKogstrom/GymBuddyApp',
    install_requires= ['asgiref==3.2.10','certifi==2020.6.20','cycler==0.10.0','Django==3.1.2','django-crispy-forms==1.9.2','kiwisolver==1.2.0','matplotlib==3.3.2','numpy==1.19.2','Pillow==7.2.0','pyparsing==2.4.7','python-dateutil==2.8.1','pytz==2020.1','six==1.15.0','sqlparse==0.3.1','testresources==2.0.1'],

    package_data= {'': ['*.html','*.json','*.css','*.jpg','*.png','*.zip','*.txt','README.md', '*.sqlite3'],
                   },
    entry_points={
        "console_scripts":['launch= GymBuddyApp.manage:main']
    },
    python_requires='>=3.6',
)
