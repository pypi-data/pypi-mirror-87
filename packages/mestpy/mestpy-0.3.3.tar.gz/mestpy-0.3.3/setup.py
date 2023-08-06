from setuptools import setup, find_packages

setup(name='mestpy',
      version='0.3.3',
      description='Gauss-Jordan Elimination in Teaching, Work with docs of main professional educational program',
      packages=find_packages( include=['mestpy','mestpy.*']),
      install_requires = [ 
        'pandas >= 0.23.3', 
        'NumPy >= 1.14.5', 
		'doc2pdf >=0.1.7',
		'PyPDF2>=1.26.0',
		'python-docx>=0.8.10'
        ],
      extras_require = { 
        'interactive' :  ['jupyter']
		},
      author ='Mestnikov S.V.',
      author_email='mestsv@mail.ru',
      zip_safe=False)
