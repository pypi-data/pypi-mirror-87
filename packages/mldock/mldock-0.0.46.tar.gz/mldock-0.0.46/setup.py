import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mldock", # Replace with your own username
    version="0.0.46",
    author="SheldonGrant",
    author_email="sheldz.shakes.williams@gmail.com",
    description="Global Machine learning helpers for docker based development. Build, train and deploy on cloud with docker",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SheldonGrant/locative-ml-global-helpers",
    packages=setuptools.find_packages(where='.'),
    package_data={
        'mldock': [
            'api/*.sh',
            'platform_helpers/gcp/*.sh',
            'platform_helpers/gcp/__init__.py',
            'platform_helpers/environment.py',
            'platform_helpers/gcp/storage.py',
            'templates/sagemaker/tests/container_health/*.py',
            'templates/sagemaker/src/',
            'templates/sagemaker/src/*.py',
            'templates/sagemaker/src/utils',
            'templates/sagemaker/src/utils/*py',
            'templates/sagemaker/src/container',
            'templates/sagemaker/src/container/config.json',
            'templates/sagemaker/src/container/*.sh',
            'templates/sagemaker/src/container/Dockerfile',
            'templates/sagemaker/src/container/ __init__.py',
            'templates/sagemaker/src/container/training/__init__.py',
            'templates/sagemaker/src/container/training/train',
            'templates/sagemaker/src/container/prediction/*.py',
            'templates/sagemaker/src/container/prediction/serve',
            'templates/sagemaker/src/container/prediction/nginx.conf',
            'templates/sagemaker/src/container/local_test/*.sh',
            'templates/sagemaker/src/container/local_test/test_dir/output/.gitkeep',
            'templates/sagemaker/src/container/local_test/test_dir/model/.gitkeep',
            'templates/sagemaker/src/container/local_test/test_dir/input/config/*.json',
            'templates/sagemaker/src/container/local_test/test_dir/input/data/training/',
            'templates/bare/tests/container_health/*.py',
            'templates/bare/service/docker-compose.yml',
            'templates/bare/src/',
            'templates/bare/src/env.py',
            'templates/bare/src/prediction.py',
            'templates/bare/src/trainer.py',
            'templates/bare/src/container',
            'templates/bare/src/container/config.json',
            'templates/bare/src/container/*.sh',
            'templates/bare/src/container/Dockerfile',
            'templates/bare/src/container/ __init__.py',
            'templates/bare/src/container/training/',
            'templates/bare/src/container/training/*.sh',
            'templates/bare/src/container/training/startup.py',
            'templates/bare/src/container/training/cleanup.py',
            'templates/bare/src/container/training/train.py',
            'templates/bare/src/container/prediction/',
            'templates/bare/src/container/prediction/serve.py',
            'templates/bare/src/container/prediction/startup.py',
            'templates/bare/src/container/prediction/wsgi.py',
            'templates/bare/src/container/prediction/predictor.py',
            'templates/bare/src/container/prediction/*.sh',
            'templates/bare/src/container/prediction/nginx.conf',
            'templates/bare/src/container/local_test/*.sh',
            'templates/bare/src/container/local_test/test_dir/output/.gitkeep',
            'templates/bare/src/container/local_test/test_dir/model/.gitkeep',
            'templates/bare/src/container/local_test/test_dir/input/config/*.json',
            'templates/bare/src/container/local_test/test_dir/input/data/training/'
        ]
    },
    setup_requires=['setuptools>=39.1.0'],
    extras_require={
        'ai-platform': ['future', 'google-cloud-storage', 'google-api-python-client'],
        'cli': ['click', 'docker', 'future'],
        'sagemaker': ['future', 'boto3']
    },
    entry_points="""
        [console_scripts]
        mldock=mldock.__main__:cli
    """,
    keywords=["docker", "machine learning", "ml", "ml services", "MLaaS"],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6"
    ],
    python_requires='>=3.6',
)
