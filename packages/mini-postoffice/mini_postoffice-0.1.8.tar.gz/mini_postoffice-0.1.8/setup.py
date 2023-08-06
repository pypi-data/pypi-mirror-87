from setuptools import setup, find_packages

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='mini_postoffice',
    version='0.1.8',
    description='small package for sending email',
    url='https://github.com/jryzj/mini_postoffice',
    author='Jerry Zang',
    author_email='2381002887@qq.com',
    license='MIT',
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Development Status :: 3 - Alpha'   
    ],
    keywords='email smtp tool ',
    #packages= ['mini_postoffice'],
    packages= find_packages(),
    install_requires=['chardet'],
    python_requires= '>=3',
)