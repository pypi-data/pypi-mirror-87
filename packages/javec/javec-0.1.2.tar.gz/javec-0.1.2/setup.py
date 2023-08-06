from setuptools import setup

with open('README.md', 'r') as f:
    long_description = f.read()

setup(name='javec',
      version='0.1.2',
      description='Just another virtual environment creator',
      url='https://github.com/BartlomiejF/JAVEC',
      author='Bartlomiej Fliszkiewicz',
      author_email='bartlomiej.fliszkiewicz.dev@gmail.com',
      license='MIT',
      packages=['javec'],
      zip_safe=False,
      entry_points={
        'console_scripts': ['javec=javec.argsHandler:handler']
        },
      long_description=long_description,
      include_package_data=True,
      )
