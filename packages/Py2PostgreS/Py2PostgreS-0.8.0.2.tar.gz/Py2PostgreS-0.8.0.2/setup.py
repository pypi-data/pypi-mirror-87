from setuptools import setup

setup(name='Py2PostgreS',
      version='0.8.0.2',
      description='Py to postgreSQL',  # Small descriptions.
      author='Blahyi Andrii, Kushnirenko Mariia, Tochanenko Vladislav, Velychko Taisiia',  # Optional in test.PyPI.
      author_email='blagij00@gmail.com',  # Optional in test.PyPI.
      license='MIT',
      packages=['Py2PostgreS'],
      install_requires=["psycopg2",],
      zip_safe=False)
