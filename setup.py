from setuptools import setup

with open("README.md", "r") as fh:
    readme = fh.read()

setup(name='filesystem',
    version='0.0.0.10',
    url='https://github.com/hbisneto/FileSystem',
    license='MIT License',
    author='Heitor Bisneto',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='heitor.bardemaker@live.com',
    keywords= ['FileSystem', 'Linux', 'macOS', 'Windows', 'File', 'System'],
    description=u'FileSystem is designed to identify the operating system (OS) on which it`s running and define the paths to various user directories based on the OS.',
    packages=['filesystem', 'filesystem/wrapper'],
    install_requires=[''],)