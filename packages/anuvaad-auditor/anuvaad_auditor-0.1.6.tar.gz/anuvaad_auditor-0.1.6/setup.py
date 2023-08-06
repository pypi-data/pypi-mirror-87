from distutils.core import setup

long_description = "A package to standardize and manage errors in anuvaad dataflow pipeline by EkStep \n" \
                   "This package also acts as an auditor for the anuvaad data flow pipeline by EkStep \n" \
                   "Visit the following repo for more details: https://github.com/project-anuvaad/anuvaad-em"

setup(
  name = 'anuvaad_auditor',         # How you named your package folder
  packages = ['anuvaad_auditor'],   # Chose the same as "name"
  version = '0.1.6',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'A package to standardize and manage audit details and errors in anuvaad dataflow pipeline',   # Give a short description about your library
  author = 'Vishal Mahuli',                   # Type in your name
  author_email = 'vishal.mahuli@tarento.com',      # Type in your E-Mail
  url = 'https://www.tarento.com',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/project-anuvaad/anuvaad-em/archive/16.0.0.tar.gz',    # Release source.tar.gz asset
  keywords = ['ANUVAAD', 'ERROR', 'MANAGER', 'TARENTO', 'EKSTEP', 'SUVAAS', 'AUDIT', 'LOG', 'INDEX'],   # Keywords that define your package best
  long_description=long_description,
  install_requires=[            # Packages to be explicitly installed ONLY. (No inbuilt py packages)
          'kafka-python',
          'uuid',
          'datetime',
          'elasticsearch',
  ],
  classifiers=[
    'Development Status :: 4 - Beta',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3.7',      #Specify which pyhton versions that you want to support
  ],
)