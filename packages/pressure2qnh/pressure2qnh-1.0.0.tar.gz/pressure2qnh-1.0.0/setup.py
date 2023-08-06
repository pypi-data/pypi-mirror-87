from distutils.core import setup
import os.path

setup(
  name = 'pressure2qnh',         # How you named your package folder (MyLib)
  packages = ['pressure2qnh'],   # Chose the same as "name"
  version = '1.0.0',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Correcting station pressure to qnh',   # Give a short description about your library
  long_description='plese read in: https://github.com/kanutsanun-b/pressure2qnh',
  author = 'Kanutsanun Bouking',                   # Type in your name
  author_email = 'kanutsanun.b@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/kanutsanun-b/pressure2qnh',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/kanutsanun-b/pressure2qnh/archive/1.0.0.zip',    # I explain this later on
  keywords = ['pressure', 'qnh', 'Raspberry Pi','kanutsanun bouking'],   # Keywords that define your package best
  install_requires=[
      'numpy'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
  ],
)
