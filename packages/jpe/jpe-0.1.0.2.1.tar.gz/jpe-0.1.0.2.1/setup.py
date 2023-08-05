from distutils.core import setup
setup(
  name = 'jpe',         # How you named your package folder (MyLib)
  packages = ['jpe',
              'jpe/crono',
              "jpe/errors",
              "jpe/math",
              "jpe/math/linalg",
              "jpe/random",
              "jpe/utils/unicode",
              "jpe/utils/copy"],   # Chose the same as "name"
  version = '0.1.0.2.1',      # Start with a small number and increase it with every change you make
  license='wtfpl',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'help files for my code',   # Give a short description about your library
  author = 'Julian Wandhoven',                   # Type in your name
  author_email = 'julian.wandhoven@fgz.ch',      # Type in your E-Mail
  url = 'https://github.com/JulianWww/jpe',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/JulianWww/jpe/archive/v0.1.0.1d.tar.gz',    # I explain this later on
  keywords = ['utils', 'linalg'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'numpy'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3.6' ,
    'Programming Language :: Python :: 3',#Specify which pyhton versions that you want to support
  ],
  scrips = ["jpe.math.Jmath.py"]
)


#upload twine upload dist/*
