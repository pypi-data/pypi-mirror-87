try:
    import docker as _docker
    _docker_client = _docker.from_env()
except:
    _docker_client = None
import time
import requests
DEFAULT_MONGO_IMAGE = 'mongo:4'
DEFAULT_ELASTIC_IMAGE = 'elasticsearch:7.8.0'
MONGO_PORT = 27017
ELASTIC_PORT = 9200


def client():
    return _docker_client


def _mongo_is_running(container):
    host = "mongodb://%s:%d/" % (container.attrs['NetworkSettings']['IPAddress'], MONGO_PORT)
    try:
        import pymongo
        client = pymongo.MongoClient(host)
        client.server_info()
        return True
    except:
        return False


def _elastic_is_running(container):
    host = "http://%s:%d" % (container.attrs['NetworkSettings']['IPAddress'], ELASTIC_PORT)
    try:
        resp = requests.get(host + '/_cluster/health')
        if resp.status_code == 200:
            return True
        return False
    except:
        return False


def mongo_instance(instance_name, data_path=None, restart=True, create=True, mongo_image=DEFAULT_MONGO_IMAGE):
    try:
        container = _docker_client.containers.get(instance_name)
    except:
        container = None

    if restart and container is not None and container.status == 'exited':
        container.start()
    elif create and (container is None or container.status == 'exited'):
        volumes = None if data_path is None else {data_path: {'bind': '/data/db', 'mode': 'rw'}}
        container = _docker_client.containers.run(mongo_image, name=instance_name, volumes_from=volumes, detach=True)

    tries = 0
    while tries < 100:
        if container.status == 'running' and _mongo_is_running(container):
            break
        tries += 1
        time.sleep(2)
        container = _docker_client.containers.get(instance_name)

    if container is not None and container.status == 'running' and _mongo_is_running(container):
        return container, "mongodb://%s:%d/" % (container.attrs['NetworkSettings']['IPAddress'], MONGO_PORT)
    if container is not None:
        container.stop()
    return None, None


def elastic_instance(instance_name, data_path=None, restart=True, create=True, image=DEFAULT_ELASTIC_IMAGE):
    try:
        container = _docker_client.containers.get(instance_name)
    except:
        container = None

    if restart and container is not None and container.status == 'exited':
        container.start()
    elif create and (container is None or container.status == 'exited'):
        volumes = None if data_path is None else {data_path: {'bind': '/usr/share/elasticsearch/data', 'mode': 'rw'}}
        environment = ["discovery.type=single-node", ]  # xpack.security.enabled=false
        container = _docker_client.containers.run(image, name=instance_name, volumes_from=volumes, detach=True,
                                                  environment=environment)

    tries = 0
    while tries < 150:
        if container.status == 'running' and _elastic_is_running(container):
            break
        tries += 1
        time.sleep(2)
        container = _docker_client.containers.get(instance_name)

    if container is not None and container.status == 'running' and _elastic_is_running(container):
        return container, "http://%s:%d" % (container.attrs['NetworkSettings']['IPAddress'], ELASTIC_PORT)
    stop_container(container)
    return None, None


def stop_container(container):
    if container is not None:
        container.stop()
