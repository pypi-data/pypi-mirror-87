import io
import sys

import cerberus
import kubernetes as k8s
import yaml

CONFIG_FILE_SCHEMA = """
output:
    type: dict
    required: True
    schema:
        name:
            type: string
            required: True
        destination_dir:
            type: string
            required: True
        default_template:
            type: string
            required: True
        templates:
            type: dict
            required: True
            allow_unknown: True
        extras:
            type: dict
            allow_unknown: True
        filename_format:
            type: string
            required: True

input:
    type: dict
    required: True
    schema:
        name:
            type: string
            required: True
        service:
            type: dict
            schema:
                annotations:
                    type: dict
        contexts:
            type: list
            required: True
            schema:
                type: string
        node:
            type: dict
            schema:
                labels:
                    type: dict
                    required: True
"""


def read_configuration_file(filepath):
    try:
        with io.open(filepath, "r") as f:
            data = yaml.safe_load(f)
            return data
    except Exception as e:
        sys.exit(e)


def get_configuration(filepath):
    data = read_configuration_file(filepath)

    # Validate the config file
    v = cerberus.Validator()
    v.schema = yaml.safe_load(CONFIG_FILE_SCHEMA)
    v.validate(data)
    if v.errors:
        sys.exit(v.errors)

    return data


def get_configuration_and_validate(filepath):
    c = get_configuration(filepath)

    # Remove duplicate context names
    c["k8s"]["contexts"] = list(set(c["k8s"]["contexts"]))

    check_context_names_is_defined_on_kubeconfig(wanted_contexts=c["k8s"]["contexts"])

    return c


def check_context_names_is_defined_on_kubeconfig(wanted_contexts):
    local_k8s_contexts = get_k8s_contexts_on_local_machine()
    local_k8s_context_names = [ctx["name"] for ctx in local_k8s_contexts]
    for wanted_context in wanted_contexts:
        if not wanted_context in local_k8s_context_names:
            sys.exit("'{}' is not defined on kube-config file".format(wanted_context))


def get_k8s_contexts_on_local_machine():
    contexts, active_context = k8s.config.list_kube_config_contexts()
    if not contexts:
        sys.exit("Cannot find any context in kube-config file.")

    return contexts
