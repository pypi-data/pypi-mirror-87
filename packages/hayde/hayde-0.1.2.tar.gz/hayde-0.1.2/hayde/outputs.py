import copy
import io
import os.path
import sys

import jinja2 as j2
import yaml


def load_output_config(config):
    loaded_output_config = {}

    name = config["name"]
    dest_dir = config["destination_dir"]
    templates = config["templates"]

    if not (os.path.exists(dest_dir) and os.path.isdir(dest_dir)):
        sys.exit(f"'{name}:{dest_dir}' output Destination Dir is not exists!")

    loaded_output_config = copy.deepcopy(config)

    for t_name, t_path in templates.items():
        # @TODO: Use try-except
        if not os.path.exists(t_path):
            sys.exit(f"'{name}:{t_name}:{t_path}' output Template File is not exists!")

        with io.open(t_path) as f:
            data = f.read()

        loaded_output_config["templates"][t_name] = data

    return loaded_output_config


def generate_files(output_config, k8s_services):
    dest_dir = output_config["destination_dir"]
    default_template = output_config["default_template"]
    templates = output_config["templates"]
    extras = output_config["extras"]
    filename_format = output_config["filename_format"]

    for s_name, s_conf in k8s_services.items():
        namespace = s_conf["namespace"]
        node_ips = s_conf["node_ips"]
        node_port = s_conf["node_port"]
        template_type = s_conf["template"]
        if template_type == "":
            template_type = default_template

        filename = filename_format.format(name=s_name, namespace=namespace, **extras)
        filepath = os.path.join(dest_dir, filename)

        template = j2.Template(templates[template_type])

        with io.open(filepath, "w") as f:
            f.write(
                template.render(
                    name=s_name,
                    node_ips=node_ips,
                    node_port=node_port,
                    namespace=namespace,
                    **extras,
                )
            )
