# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['datajob', 'datajob.glue', 'datajob.package', 'datajob.stepfunctions']

package_data = \
{'': ['*']}

install_requires = \
['aws-cdk.aws-glue>=1.70.0,<2.0.0',
 'aws-cdk.aws-s3-deployment>=1.70.0,<2.0.0',
 'aws-cdk.cloudformation-include>=1.76.0,<2.0.0',
 'aws-cdk.core>=1.70.0,<2.0.0',
 'aws-empty-bucket>=2.4.0,<3.0.0',
 'contextvars>=2.4,<3.0',
 'dephell>=0.8.3,<0.9.0',
 'stepfunctions>=1.1.2,<2.0.0',
 'typer>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['datajob = datajob.datajob:run']}

setup_kwargs = {
    'name': 'datajob',
    'version': '0.2.0',
    'description': 'Build and deploy a serverless data pipeline with no effort on AWS.',
    'long_description': '# Datajob\n\nBuild and deploy a serverless data pipeline with no effort on AWS.\n\n# Installation\n    \n    pip install datajob\n    # We depend on AWS CDK.\n    npm install -g aws-cdk\n\n# Create a pipeline\n\nsee the full example in `examples/simple_data_pipeline`\n\n    from datajob.datajob_stack import DataJobStack\n    from datajob.glue.glue_job import GlueJob\n    from datajob.stepfunctions.stepfunctions_workflow import StepfunctionsWorkflow\n    import pathlib\n    \n    current_dir = pathlib.Path(__file__).parent.absolute()\n    \n    with DataJobStack(\n        stack_name="simple-data-pipeline", project_root=current_dir\n    ) as datajob_stack:\n        task1 = GlueJob(\n            datajob_stack=datajob_stack,\n            name="task1",\n            path_to_glue_job="simple_data_pipeline/task1.py",\n        )\n        task2 = GlueJob(\n            datajob_stack=datajob_stack,\n            name="task2",\n            path_to_glue_job="simple_data_pipeline/task2.py",\n        )\n        task3 = GlueJob(\n            datajob_stack=datajob_stack,\n            name="task3",\n            path_to_glue_job="simple_data_pipeline/task3.py",\n        )\n    \n        with StepfunctionsWorkflow(\n            datajob_stack=datajob_stack,\n            name="simple-data-pipeline",\n        ) as sfn:\n            [task1, task2] >> task3\n\n        \nsave this code in a file called `datajob_stack.py` in the root of your project\n\n## Deploy a pipeline\n\n    export AWS_DEFAULT_ACCOUNT=077590795309\n    export AWS_PROFILE=my-profile\n    cd examples/simple_data_pipeline\n    datajob deploy --stage dev --config datajob_stack.py --package',
    'author': 'Vincent Claes',
    'author_email': 'vincent.v.claes@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/vincentclaes/datajob',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
