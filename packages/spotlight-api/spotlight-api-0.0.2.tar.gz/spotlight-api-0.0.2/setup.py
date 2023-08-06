from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'Operating System :: Unix',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]
setup(
    name='spotlight-api',
    version='0.0.2',
    description='Allow you to monetize your Discord Bots while adding ads to them',
    Long_description=open('README.txt').read()+'\n\n'+open('CHANGELOG.txt').read(),
    url='https://spotlight.crossplay.xyz/',
    author='CR-Crossplay',
    author_email='discord.cr3861@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='discord bot',
    packages=find_packages(),
    install_requires=['discord','urllib3','requests']    
    )