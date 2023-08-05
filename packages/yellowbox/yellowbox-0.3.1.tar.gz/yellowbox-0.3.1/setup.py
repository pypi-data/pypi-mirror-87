# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['yellowbox', 'yellowbox.extras']

package_data = \
{'': ['*']}

install_requires = \
['docker>=4.2.0,<5.0.0', 'requests', 'yaspin>=1.0.0,<2.0.0']

extras_require = \
{'all': ['redis>=3.3.0',
         'pika',
         'kafka-python',
         'azure-storage-blob>=12.0.0,<13.0.0',
         'cffi>=1.14.0,<2.0.0'],
 'azure': ['azure-storage-blob>=12.0.0,<13.0.0', 'cffi>=1.14.0,<2.0.0'],
 'kafka': ['kafka-python'],
 'rabbit': ['pika'],
 'redis': ['redis>=3.3.0']}

setup_kwargs = {
    'name': 'yellowbox',
    'version': '0.3.1',
    'description': '',
    'long_description': '# Yellowbox\n![Test YellowBox](https://github.com/biocatchltd/yellowbox/workflows/Test%20YellowBox/badge.svg?branch=master)\n[![Coverage](https://codecov.io/github/biocatchltd/yellowbox/coverage.svg?branch=master)](https://codecov.io/github/biocatchltd/yellowbox?branch=master)\n\n\nYellowbox makes it easy to run docker containers as part of black box tests.\n## Examples\nSay you want to run a blackbox test on a service that depends on a redis server.\n```python\nfrom docker import DockerClient\nfrom yellowbox.extras import RedisService\n\ndef test_black_box():\n    docker_client = DockerClient.from_env()\n    with RedisService.run(docker_client) as redis:\n        redis_port = redis.client_port()  # this the host port the redis\n        ...  # run your black box test here\n    # yellowbox will automatically close the service when exiting the scope\n\ndef test_black_box_with_initial_data():\n    # you can use the service\'s built-in utility functions to\n    # easily interoperate the service\n    docker_client = DockerClient.from_env()\n    with RedisService.run(docker_client) as redis:\n        with redis.client() as client:\n            client.set("foo","bar")\n        ...\n```\n## Supported Extras\nThe currently supported built-in services are:\n* Kafka: `from yellowbox.extras import KafkaService`\n    * currently, the kafka service supports only plaintext protocol, and always binds to the host port 9092\n* Logstash: `from yellowbox.extras import LogstashService`\n* RabbitMQ: `from yellowbox.extras import RabbitMQService`\n* Redis: `from yellowbox.extras import RedisService`\n\nNote: all these extras require additional dependencies as specified in the project\'s `extras`.\n## Networks\nYellowbox also makes it easy to set up temporary docker networks, so that different containers and services can\ncommunicate directly.\n```python\nfrom docker import DockerClient\nfrom yellowbox import temp_network, connect\nfrom yellowbox.extras import RabbitMQService\n\ndef test_network():\n    docker_client = DockerClient.from_env()\n    with RabbitMQService.run(docker_client) as rabbit, \\\n        temp_network(docker_client) as network, \\\n        connect(network, rabbit) as alias:\n        # yellow\'s "connect" function connects between a network and a\n        # Container/YellowService, retrieves the container\'s alias(es) on \n        # the network, and disconnects the two when done\n        another_container = docker_client.containers.create("my-image", \n            environment={"RABBITMQ_HOSTNAME": alias[0]}\n        )\n        with connect(network, another_container):\n            another_container.start()\n            another_container.wait()\n```\n## As Pytest Fixtures\nBoth yellow services and networks can be used fluently with `pytest` fixures\n```python\nfrom docker import DockerClient\nfrom pytest import fixture\n\nfrom yellowbox.extras import RedisService\n\n@fixture\ndef docker_client():\n    docker_client = DockerClient.from_env()\n    yield docker_client\n    docker_client.close()\n\n@fixture\ndef redis_service(docker_client):\n    with RedisService.run(docker_client) as service:\n        yield service\n\ndef black_box(redis_service):\n    # run your test with the redis service provided\n    ...\n```\nsince docker container may take some time to set up, it\'s advisable to set their scope to at least `"module"`\n## Extending Yellow\nUsers can create their own Yellow Service classes by implementing the `YellowService` abstract class.\nIf the service encapsulates only a single container, the `SingleContainerService` class already implements\nthe necessary methods.\n\n## License\nYellowbox is registered under the MIT public license\n',
    'author': 'biocatch ltd',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/biocatchltd/yellowbox',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
