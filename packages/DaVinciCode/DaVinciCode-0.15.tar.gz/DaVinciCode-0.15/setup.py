from distutils.core import setup
setup(
  name = 'DaVinciCode',         # How you named your package folder (MyLib)
  packages = ['DaVinciCode'],   # Chose the same as "name"
  version = '0.15',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'ML-Viz',   # Give a short description about your library
  author = 'Dhruv Mangtani',                   # Type in your name
  author_email = 'dhruv.mangtani@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/1dividedby0/DaVinciCode',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/1dividedby0/DaVinciCode/archive/v_02.tar.gz',    # I explain this later on
  keywords = ['visualization', 'ML', 'pipeline'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'pandas',
          'numpy',
          'plotly',
          'dash',
          'jupyter-dash',
          'sklearn',
          'mlflow',
          'xgboost'
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
  ],
)