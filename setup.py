from setuptools import setup, Extension, find_packages

with open("README.md", "r") as fh:
    readme = fh.read()

setup(
    name = 'filesystempro',
    version = '2.1.0.0',
    url = 'https://github.com/hbisneto/FileSystemPro',
    license = 'MIT License',
    
    author = 'Heitor Bisneto',
    author_email = 'heitor.bardemaker@live.com',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'Intended Audience :: End Users/Desktop',
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
    description = u'FileSystemPro is a powerful toolkit designed to handle file and directory operations with ease and efficiency across various operating systems.',
    install_requires = [
        'requests',
        'psutil',
    ],
    long_description = readme,
    long_description_content_type = "text/markdown",
    keywords = ['Compression', 'Console', 'Device', 
                'Directory',
                'File', 'FileSystem', 
                'Linux', 
                'macOS', 
                'System', 
                'Terminals', 
                'Watcher', 'Windows', 'Wrapper'
    ],
    packages=find_packages(),
    platforms = 'any',
    python_requires= '>=3.8',
)