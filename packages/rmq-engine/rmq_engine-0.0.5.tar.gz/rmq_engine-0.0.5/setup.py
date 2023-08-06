from setuptools import setup
from pathlib import Path

path = Path(__file__).resolve().parent
with open(path/'README.md', encoding='utf-8') as f:
    long_description = f.read()

with open(path/'VERSION') as version_file:
    version = version_file.read().strip()


setup(name='rmq_engine',
      version=version,
      description='Engine class for AMQP collect data froma a queue',
      url='http://gitlab.csn.uchile.cl/dpineda/rmq_engine',
      author='David Pineda Osorio',
      author_email='dpineda@csn.uchile.cl',
      license='MIT',
      packages=['rmq_engine'],
      keywords = ["amqp","data", "broker", "async",],
      install_requires=["data-amqp"],
      entry_points={
        },
      include_package_data=True,
      long_description=long_description,
      long_description_content_type='text/markdown',
      zip_safe=False)
