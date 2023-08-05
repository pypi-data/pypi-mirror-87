from distutils.core import setup
setup(
  name = 'groupingsentences',         # How you named your package folder (MyLib)
  packages = ['groupingsentences'],   # Chose the same as "name"
  version = '0.18',      # Start with a small number and increase it with every change you make
  license='apache-2.0',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'groupingsentences',   # Give a short description about your library
  author = 'Gary App',                   # Type in your name
  author_email = 'garyapphub@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/garyapphub/GroupingSentences.git',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/garyapphub/GroupingSentences/archive/v_01_8.tar.gz',    # I explain this later on
  keywords = ['grouping', 'sentences', 'KEYWORDS'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'validators',
          'jieba',
          'xlrd',
          'xlwt',
          'xmind',
          'sklearn',
          'numpy',
          'distance',
          'gensim',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: Apache Software License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
  ],
)