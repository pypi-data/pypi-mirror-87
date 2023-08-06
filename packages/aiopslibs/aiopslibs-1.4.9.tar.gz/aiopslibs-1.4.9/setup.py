from setuptools import setup

exec(open('aiopslibs/version.py').read())

with open('README.md') as f:
    long_description = f.read()

setup(
  name = 'aiopslibs',         # How you named your package folder
  packages = ['aiopslibs'],   # Chose the same as "name"
  version = __version__,     # pylint: disable=undefined-variable
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  long_description=long_description,
  long_description_content_type='text/markdown',  # This is important!
  author = 'Avanade',                   # Type in your name
  author_email = 'j.kibassa.maliba@avanade.com',      # Type in your E-Mail
  url = 'https://dev.azure.com/galliatools/Data_Science_Human-in-the-Loop/_git/AI_Ops_Libs',   # Provide either the link to your github or to your website
  #download_url = 'https://github.com/RaaLabs/TSIClient/archive/v_0.7.tar.gz',    # If you create releases through Github, then this is important
  keywords = ['Pytorch', 'Deep Learning', 'Neural Network'],   # Keywords that define your package best
  install_requires=['pandas'],
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