from setuptools import setup

setup(name='gym_snake',
      version='0.1.6',
      description='Gym Snake Env',
      url='https://github.com/boangri/gym-snake',
      author='Boris Gribovskiy',
      packages=['gym_snake'],
      author_email='xinu@yandex.ru',
      license='MIT License',
      install_requires=['gym', 'numpy', 'pygame'],
      python_requires='>=3.6'
      )
