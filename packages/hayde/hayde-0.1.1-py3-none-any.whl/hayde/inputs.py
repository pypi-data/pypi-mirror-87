import sys

import kubernetes as k8s

PROJECT_DOMAIN = "hayde.f9n.io"

K8S_ANNOTATION_SCHEMA = f"""
{PROJECT_DOMAIN}/enabled: true
{PROJECT_DOMAIN}name: ""
{PROJECT_DOMAIN}/template: http
"""


def get_node_ips_of_k8s_cluster(client, labels={}):
    node_ips = []
    node_objects = client.list_node().items
    for node_object in node_objects:
        _node_labels = node_object.metadata.labels

        shared_items = get_shared_items_between_2_dicts(labels, _node_labels)
        if not len(shared_items.keys()) == len(labels.keys()):
            continue

        for address_object in node_object.status.addresses:
            if address_object.type == "InternalIP":
                node_ips.append(address_object.address)
                continue

    return node_ips


def get_shared_items_between_2_dicts(x, y):
    return {k: x[k] for k in x if k in y and x[k] == y[k]}


# @TODO: Rename this function
def get_k8s_clusters(context_names, node_labels, service_config):
    k8s_clusters = {}

    for context_name in context_names:
        client = k8s.client.CoreV1Api(
            api_client=k8s.config.new_client_from_config(context=context_name)
        )
        cluster_node_ips = get_node_ips_of_k8s_cluster(
            client=client, labels=node_labels
        )
        cluster_services = get_proper_k8s_services(
            client, service_config=service_config
        )
        k8s_clusters[context_name] = {
            "node_ips": cluster_node_ips,
            "services": cluster_services,
        }

    return k8s_clusters


# Ihhhhhh!
def get_proper_k8s_services(client, service_config):
    service_filter_annotations = service_config.get("annotations", {})
    if service_filter_annotations:
        service_filter_annotations = {
            f"{PROJECT_DOMAIN}/{k}": v for k, v in service_filter_annotations.items()
        }

    services = []
    service_objects = client.list_service_for_all_namespaces().items

    for service_object in service_objects:
        s = {}
        s["name"] = service_object.metadata.name
        s["namespace"] = service_object.metadata.namespace

        if not service_object.spec.type == "NodePort":
            continue

        for port_object in service_object.spec.ports:
            s["node_port"] = port_object.node_port

        if not "node_port" in s:
            continue

        if service_filter_annotations == {}:
            services.append(s)
            continue

        _s_annotations = service_object.metadata.annotations

        if not _s_annotations:
            continue

        shared_items = get_shared_items_between_2_dicts(
            service_filter_annotations, _s_annotations
        )

        if not len(shared_items.keys()) == len(service_filter_annotations.keys()):
            continue

        _s_name_on_annotation = _s_annotations.get(f"{PROJECT_DOMAIN}/name", "")
        if not _s_name_on_annotation == "":
            s["name"] = _s_name_on_annotation

        s["template"] = _s_annotations.get(f"{PROJECT_DOMAIN}/template", "")

        services.append(s)

    return services


def get_all_proper_k8s_services(k8s_configs):
    contexts = k8s_configs["contexts"]
    node_labels = k8s_configs["node"]["labels"]
    service_config = k8s_configs.get("service", {})

    k8s_clusters = get_k8s_clusters(
        context_names=contexts, node_labels=node_labels, service_config=service_config
    )

    all_k8s_services = {}
    for k8s_cluster_name, k8s_cluster in k8s_clusters.items():
        for service in k8s_cluster["services"]:
            _service_name = service["name"]

            _s = all_k8s_services.get(
                _service_name, {"node_port": None, "node_ips": []}
            )
            _s["node_ips"].extend(k8s_clusters[k8s_cluster_name]["node_ips"])
            _s["node_port"] = service["node_port"]
            _s["namespace"] = service["namespace"]
            _s["template"] = service["template"]

            all_k8s_services[_service_name] = _s

    return all_k8s_services
