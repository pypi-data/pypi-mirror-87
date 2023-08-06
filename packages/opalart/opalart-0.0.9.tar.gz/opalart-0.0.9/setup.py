from setuptools import setup, find_packages

setup(name='opalart',
      version='0.0.9',
      url='https://gitlab.com/Shifty/opalart.git',
      license='GPL',
      author='Daniel Preston',
      author_email='prestondj.2001@yahoo.com',
      description='Asynchronous hentai scraper.',
      packages=find_packages(),
      long_description=open('README.md').read(),
      long_description_content_type='text/markdown',
      zip_safe=False)
