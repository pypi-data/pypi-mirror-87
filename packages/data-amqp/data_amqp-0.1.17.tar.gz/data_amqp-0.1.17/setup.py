from setuptools import setup, find_packages

from pathlib import Path

path = Path(__file__).resolve().parent

with open(path/'README.md', encoding='utf-8') as f:
    long_description = f.read()

with open(path/'VERSION') as version_file:
    version = version_file.read().strip()

setup(name='data_amqp',
      version=version,
      description='DataDBS for RabbitMQP',
      url='http://www.gitlab.com/dpineda/data_amqp',
      author='David Pineda Osorio',
      author_email='dpineda@csn.uchile.cl',
      license='GPLv3',
      packages=["data_amqp"],
      install_requires=["networktools","data_geo","pika","datadbs", "tasktools"],
      package_dir={'data_amqp': 'data_amqp'},
      package_data={
          'data_amqp': ['../doc', '../docs', '../requeriments.txt']},
      long_description=long_description,
      long_description_content_type='text/markdown',
      zip_safe=False)
