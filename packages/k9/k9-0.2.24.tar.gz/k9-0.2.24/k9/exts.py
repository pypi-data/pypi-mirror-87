from kubernetes import client, config
from k9.pretty_object import PrettyObject
from k9.core import *

po = PrettyObject()
config.load_kube_config()

v1_exts = client.ExtensionsV1beta1Api()

###########################################################################
# Ingress
###########################################################################

def list_ingress(namespace: str = None):
    """
    Lists ingresses in a namespace.

    :param namespace: The namespace to search in. If not present, we use the default namespace.
    :return: A list of every ingress in the namespace.

    Example Output::
    
        [
          {
            'name': 'kibana-ing',
            'namespace': 'logging',
            'hosts': [
              'kibana.np.sandbox.simoncomputing.com'
            ],
            'address': [
              '10.10.100.123',
              '10.10.101.145',
              '10.10.102.167'
            ],
            'age': 123456789
          }
        ]
    """
    if namespace is None:
        namespace = get_default_namespace()

    return [
        {
            'name': ing.metadata.name,
            'namespace': ing.metadata.namespace,
            'hosts': [
                tls.hosts
                for tls in ing.spec.tls
            ],
            'address': [
                rule.host
                for rule in ing.spec.rules
            ],
            'age': get_age(ing.metadata.creation_timestamp)
        }
        for ing in v1_exts.list_namespaced_ingress(namespace).items
    ]


def ingress_exists(name: str, namespace: str = None):
    """
    Checks existence of specified ingress.

    :param name: Name of ingress to check.
    :param namespace: Namespace to check, if None, check in default namespace.
    :return: True if specified ingress exists.
    """
    try:
        if namespace is None:
            namespace = get_default_namespace()

        result = get_ingress(name, namespace)
        return result.metadata.name == name

    except:
        return False


def get_ingress(name: str, namespace: str = None):
    """
    Get details of specified ingress.

    :param name: Name of ingress to get.
    :param namespace: Namespace to get ingress from.  If None, get from default namespace.
    :return: `ExtensionsV1beta1Ingress <https://github.com/kubernetes-client/python/blob/master/kubernetes/docs/ExtensionsV1beta1Ingress.md>`_
    """
    if namespace is None:
        namespace = get_default_namespace()

    return v1_exts.read_namespaced_ingress(name, namespace)


def create_ingress(body: dict, namespace: str = None):
    """
    Creates an ingress point - which defines

    :param body: Contains Ingress Definition - https://github.com/kubernetes-client/python/blob/master/kubernetes/docs/ExtensionsV1beta1Ingress.md
    :param namespace: Namespace to create ingress in.  If None, use default namespace
    :return: `ExtensionsV1beta1Ingress <https://github.com/kubernetes-client/python/blob/master/kubernetes/docs/ExtensionsV1beta1Ingress.md>`_

    Example YAML File::

        apiVersion: extensions/v1beta1
        kind: Ingress
        metadata:
          name: tomcat-ing-dev
        spec:
          rules:
            - host: tomcat.dev.sandbox.simoncomputing.com
              http:
                paths:
                  - path: /
                    backend:
                      serviceName: tomcat-svc-dev
                      servicePort: 8080
          tls:
          - hosts:
            - dev.sandbox.simoncomputing.com

    Example Call:

        from k9.helper import read_yaml, create_ingress

        body = read_yaml('../test/tomcat-ing-dev.yml')
        create_ingress(body)

    """
    if namespace is None:
        namespace = get_default_namespace()

    return v1_exts.create_namespaced_ingress(namespace, body)

def add_ingress_rule(name: str, service_name: str, service_port: int, host: str = None, paths = None, namespace: str = None):
    """
    Adds a rule to an ingress.

    :param name: the name of the ingress to add the rule to
    :param service_name: the service the rule points to
    :param service_port: the port the service is listening on
    :param host: the hostname to use (optional)
    :param paths: list of paths to use (optional). If not supplied, serves on any path ('/')
    :param namespace: the namespace the ingress is in. if not supplied, we use the default namespace
    """

    if namespace is None:
        namespace = get_default_namespace()

    ing = get_ingress(name, namespace) # will throw an exception if not found

    rules = ing.get('spec', {}).get('rules', [])
    new_rule = { "paths": [] }
    if host:
        new_rule['host'] = host
    if paths:
        for p in paths:
            new_rule['paths'].append({
              "path": p,
              "backend": {
                "service_name": service_name,
                "service_port": service_port
              }
            })
    else:
      # add base path
      new_rule['paths'].append({
              "path": "/",
              "backend": {
                "service_name": service_name,
                "service_port": service_port
              }
            })

    rules.append(new_rule)
    ing['spec']['rules'].append(new_rule)
    return v1_exts.patch_namespaced_ingress(name, namespace, ing)


def delete_ingress(name: str, namespace: str = None):
    """
    Deletes specified ingress.

    :param name: Name of ingress
    :param namespace: Namespace to delete from.  If None, remove from default namespace.
    :return: None if ingress doesn't exist, `V1Status <https://github.com/kubernetes-client/python/blob/master/kubernetes/docs/V1Status.md>`_
    """
    if namespace is None:
        namespace = get_default_namespace()

    if ingress_exists(name, namespace):
        return v1_exts.delete_namespaced_ingress(name, namespace)
    else:
        return None
