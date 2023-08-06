from sys import platform
import os, sys
from setuptools import setup, Extension


with open("README.md", "r") as fh:
    long_description = fh.read()




setup(
  name = 'explainx',         # How you named your package folder (MyLib)
  packages = ['explainx'],   # Chose the same as "name"
  version = '2.404',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Explain and debug any black-box Machine Learning model.',   # Give a short description about your library
  long_description=long_description,
  long_description_content_type="text/markdown",
  author = 'explainx.ai',                   # Type in your name
  author_email = 'muddassar@explainx.ai',      # Type in your E-Mail
  url = 'https://github.com/explainX/explainx',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/explainX/explainx/archive/v2.40.zip',    # I explain this later on
  keywords = ['Explainable AI', 'Explainable Machine Learning', 'trust', "interpretability", "transparent"],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'jupyter_dash==0.2.1.post1',
          'dash_bootstrap_components==0.10.2',
          'dash==1.12.0',
          'dash_core_components==1.10.0',
          'dash_html_components==1.0.3',
          'plotly==4.5.1',
          'dash_table==4.7.0',
          'pandas==1.0.4',
          'numpy==1.18.1',
          'dash_bootstrap_components==0.10.2',
          'cvxopt==1.2.4',
           'scikit-learn==0.22.1',
          'scipy==1.4.1',
            'pandasql==0.7.3',
            'tqdm==4.47.0',
            'dash-editor-components==0.0.2',
            'shap==0.37.0',
            'dash_daq==0.5.0',
            'pytest',
            'pyrebase'

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
    package_data={"explainx":["lib/*", "tutorials/*", "datasets/*", "lib/shap/*","lib/shap/plots/*", "lib/shap/plots/resources/*",
                              "lib/shap/explainers/*",
                              "lib/shap/explainers/deep/*",
                              "lib/shap/explainers/other/*",
                              "lib/shap/benchmark/*",
                              "lib/apps/*",
                              "lib/apps/webapps/static/*",
                              "lib/assets/*",
                              "lib/frameworks/*",
                              "lib/models/*",
                              "lib/models/test/*",
                              "lib/modules/cohort_analysis/*",
                              "lib/modules/cohort_analysis/apps/*",
                              "lib/modules/cohort_analysis/assets/*",
                              "lib/modules/feature_interactions/*",
                              "lib/modules/feature_interactions/apps/*",
                              "lib/modules/feature_interactions/assets/*",
                              "lib/modules/local_explanation/*",
                              "lib/modules/local_explanation/apps/*",
                              "lib/modules/local_explanation/assets/*"

                              ]},
)
