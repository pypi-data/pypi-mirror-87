import sagemaker

import pprint
from aws_sagemaker_remote.util.fields import get_field
from aws_sagemaker_remote.util.json_read import json_urlparse

def training_describe(job_name, session, field=None):
    client = session.boto_session.client('sagemaker')
    job_name = json_urlparse(job_name, session=session)
    description = training_describe_get(job_name=job_name, client=client)
    description = get_field(description, field)
    return description


def training_describe_get(client, job_name):
    response = client.describe_training_job(
        TrainingJobName=job_name
    )
    return response


if __name__ == '__main__':
    session = sagemaker.Session()
    client = session.boto_session.client('sagemaker')
    training_describe(
        client=client, job_name='mnist-demo-2020-10-06-04-32-42-393')
