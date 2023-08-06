import setuptools 

setuptools.setup(name='py-resilio-connect',
      version='2.1',
      description='Generate simple Resilio Connect Sync Jobs based on a csv file',
      url='https://github.com/ilanshamir/connect-scripts.git',
      author='Ilan Shamir',
      author_email='team@resilio.com',
      license='MIT',
      packages=setuptools.find_packages(),
      install_requires=[
         "requests",
      ],
      zip_safe=False)