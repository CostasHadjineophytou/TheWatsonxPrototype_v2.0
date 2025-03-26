from setuptools import setup, find_packages

setup(
    name="WatsonxPrototype",
    version="2.0",
    packages=find_packages(),
    install_requires=[
        'python-dotenv',
        'Pillow',
        'ibm-watson',
        'ibm-watson-machine-learning',
        'ibm-cloud-sdk-core',
        'requests',
        'pygame'  # for audio playback
    ],
    python_requires='>=3.8',
    entry_points={
        'console_scripts': [
            'watsonx-prototype=main:main',
        ],
    },
    include_package_data=True,
    package_data={
        'frontend': ['assets/images/*'],
    }
) 