from setuptools import setup
import pathlib

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.rst").read_text()

setup(
  name = 'AuthGG',
  packages = ['AuthGG'],
  version = '0.7',
  license='MIT',
  description = 'Identity made simple for developers.',
  author = 'razu',                   # Type in your name
  long_description=README,
  long_description_content_type = "text/markdown",
  author_email = 'support@xyris.org',      # Type in your E-Mail
  url = 'https://github.com/rqzu/AuthGG',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/rqzu/AuthGG/archive/main.tar.gz',    # I explain this later on
  keywords = ['auth', 'authgg', 'AuthGG'],   # Keywords that define your package best
  install_requires=[
          'requests',
      ],
  classifiers=[
    'Development Status :: 4 - Beta',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3.6',
  ],
)