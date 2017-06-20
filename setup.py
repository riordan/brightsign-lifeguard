from setuptools import setup

setup(name='brightsignlifeguard',
      version='0.1',
      description='tools for working with Brightsign show pools (shard/unshard)',
      url='http://github.com/riordan/brightsign-lifeguard',
      author='David Riordan',
      author_email='dr@daveriordan.com',
      license='Apache-2.0',
      packages=['brightsignlifeguard'],
      install_requires=["copyfile==0.1.1"],
      entry_points={
        'console_scripts': [
            'lifeguardIn=brightsignlifeguard.lifeguardIn:guardIn',
            'lifeguardOut=brightsignlifeguard.lifeguardOut:guardOut',
        ],
    },
      zip_safe=False)
