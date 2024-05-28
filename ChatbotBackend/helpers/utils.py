import importlib

def import_module(dotted_path):
    module_parts = dotted_path.split('.')
    module_path = '.'.join(module_parts[:-1])
    module = importlib.import_module(module_path)

    return getattr(module, module_parts[-1])


def create_instance_from_path(source, *init_args, **init_kwargs):
    if isinstance(source, dict):
        class_path = source.pop('import_path', None)
        source.update(init_kwargs)
        class_to_create = import_module(class_path)
        return class_to_create(*init_args, **source)
    else:
        class_to_create = import_module(source)
        return class_to_create(*init_args, **init_kwargs)
