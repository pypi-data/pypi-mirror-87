from distutils.core import setup
setup(
  name = 'nfer-sandbox-cli',        
  packages = ['nfer-sandbox-cli'],  
  version = '0.1',      
  license='MIT',  
  description = 'STUB : Arbit Package Name for Nfer Sandbox CLI',   
  author = 'nference@nference.net',         
  author_email = 'nference@nference.net', 
  url = 'https://github.com/maneckshaw71/nfer-sandbox-cli',  
  download_url = 'https://github.com/maneckshaw71/nfer-sandbox-cli/archive/0.1.tar.gz',
  keywords = ['Sensoriant', 'Sandbox', 'Confidential-Computing'],   
  install_requires=[ 
          'requests',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9'
  ],
)
