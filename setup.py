from setuptools import setup, find_packages

setup(
    name="realdoc_api",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'fastapi',
        'uvicorn',
        # Add other dependencies from requirements.txt
    ],
)
