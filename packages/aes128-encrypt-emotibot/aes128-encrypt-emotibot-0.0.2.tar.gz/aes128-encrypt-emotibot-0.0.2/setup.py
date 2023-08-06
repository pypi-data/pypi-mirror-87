import setuptools


with open('README.md', 'r', encoding='utf-8') as fh:
  long_description = fh.read()
  
  
setuptools.setup(
  name = 'aes128-encrypt-emotibot',
  version = '0.0.2',
  author = 'Emotibot',
  author_email = 'admin@emotibot.com',
  description = 'AES encrypt util',
  long_description = long_description,
  long_description_content_type = 'text/markdown',
  url='',
  packages=setuptools.find_packages(),
  classfiers=[
  'Programming Language :: Python :: 3',
  'License :: OSI Approved :: MIT License',
  'Operating System :: OS Independent',
  ],
  install_requires=['pycryptodomex'],

)
