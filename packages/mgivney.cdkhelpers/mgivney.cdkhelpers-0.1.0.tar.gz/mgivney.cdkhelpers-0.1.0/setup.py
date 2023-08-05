from setuptools import setup

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    # this library name
    name='mgivney.cdkhelpers',

    # the version scheme for this library
    # MAJOR.MINOR.MAINTENANCE
    version='0.1.0',

    description='CDK helpers and custom resources with sensible defaults',

    # maintainer
    author='Matt Givney',

    # maintainer email
    author_email='matt@givney.com',

    # the War and Peace version of the documentation
    long_description=long_description,

    # Markdown,for all-around awesomeness
    long_description_content_type='text/markdown',

    # these are the dependencies used
    # by this package
    install_requires=[
        "aws-cdk.core ~= 1.75.0",
        "aws-cdk.aws-ecs ~= 1.75.0",
        "aws-cdk.aws-autoscaling ~= 1.75.0",
        "aws-cdk.aws-elasticloadbalancing ~= 1.75.0",
        "aws-cdk.aws-elasticsearch ~= 1.75.0",
        "aws-cdk.aws-kms ~= 1.75.0",
        "aws-cdk.aws-sqs ~= 1.75.0",
        "aws-cdk.aws-sns ~= 1.75.0",
        "aws-cdk.aws-s3  ~= 1.75.0",
        "aws-cdk.aws-dynamodb ~= 1.75.0",
        "aws-cdk.aws-ecr ~= 1.75.0",
        "aws-cdk.aws-lambda ~= 1.75.0",
        "aws-cdk.aws-cognito ~= 1.75.0",
        "aws-cdk.aws-rds ~= 1.75.0",
        "aws-cdk.aws-iam ~= 1.75.0",
        "aws-cdk.aws-ses ~= 1.75.0",
        "aws-cdk.aws-cloudwatch ~= 1.75.0",
        "aws-cdk.aws-logs ~= 1.75.0",
        "aws-cdk.aws-route53 ~= 1.75.0",
        "aws-cdk.aws-ssm ~= 1.75.0",
        "aws-cdk.aws-athena ~= 1.75.0",
        "aws-cdk.aws-secretsmanager ~= 1.75.0"
    ],

    keywords='sherwood, aws, cloudformation, cdk',

    packages=['cdkhelpers'],

    python_requires='>=3.7',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Framework :: AWS CDK'
    ]
)
