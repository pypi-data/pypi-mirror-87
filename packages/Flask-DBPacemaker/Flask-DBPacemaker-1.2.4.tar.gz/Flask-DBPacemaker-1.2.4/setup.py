from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="Flask-DBPacemaker",
    version="1.2.4",
    author="Ron Chang",
    author_email="ron.hsien.chang@gmail.com",
    description="Hook db connection when you're running a long term sleep crawler assignment.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Ron-Chang/flask_dbpacemaker",
    packages=find_packages(),
    license='MIT',
    python_requires='>=3.6',
    exclude_package_date={'':['.gitignore', 'dev', 'test', 'setup.py']},
    install_requires=[
        'SQLAlchemy>=1.2.10',
        'Flask>=1.0.2',
        'Flask-APScheduler>=1.11.0',
        'Flask-SQLAlchemy>=2.3.2'
    ]
)
