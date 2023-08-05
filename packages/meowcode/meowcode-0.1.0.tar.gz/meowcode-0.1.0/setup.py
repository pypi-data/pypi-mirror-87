from setuptools import setup, find_packages

setup(
  name='meowcode',
  version='0.1.0',
  keywords=('meowcode'),
  license='MIT',
  author='riven',
  url='https://gitee.com/KittenTech/pylib_meowcode',
  author_email='riven@kittenbot.cc',
  packages=find_packages(exclude=('tests')),
  install_requires=['pyserial','usb'],
  description="Lib for meowcode, build over ampy from adafruit",
  platform='any'
)

