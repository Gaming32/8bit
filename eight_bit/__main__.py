import argparse
import configparser
import sys
import os
from typing import Optional
from types import ModuleType

from eight_bit.computer import Computer
from eight_bit.colonimport import import_module, colonimport
from eight_bit.module import Module


python_executable = os.path.basename(sys.executable)
argument_parser = argparse.ArgumentParser(f'{python_executable} -m eight_bit')
argument_parser.add_argument('-m', '--module', action='append', dest='modules', default=[], metavar='MODULE', help='add another module by name (python_module:class_name)')
argument_parser.add_argument('-l', '--library', action='append', dest='libraries', default=[], metavar='MODULE', help='add another module by name (python_module:class_name)')
argument_parser.add_argument('-s', '--simple', action='store_true', help="don't include standard library modules (IO, RAM, and ROM)")
argument_parser.add_argument('ini', metavar='INI', help='the ini file that contains the running configuration')


def get_obj_listing(module: ModuleType) -> list[str]:
    if hasattr(module, '__all__'):
        return module.__all__
    return dir(module)


def main(argv: Optional[list[str]] = None):
    args = argument_parser.parse_args(argv)

    library_list = []
    if not args.simple:
        library_list.append('eight_bit.builtin_modules')
    library_list.extend(args.libraries)
    module_list: list[type[Module]] = args.modules
    for (i, module_name) in enumerate(module_list):
        module_list[i] = colonimport(module_name)
    for library_name in library_list:
        library = import_module(library_name)
        for subname in get_obj_listing(library):
            libobj = getattr(library, subname)
            if issubclass(libobj, Module):
                module_list.append(libobj)
    modules: dict[str, type[Module]] = {}
    for module in module_list:
        modules[module.module_name] = module

    config = configparser.ConfigParser()
    config.read(args.ini)

    pc_config = config.pop('pc', {})
    pc_modules = {}
    for mod_config_name in config:
        if mod_config_name == 'DEFAULT':
            continue
        mod_config = config[mod_config_name]
        mod_type_name = mod_config.pop('type')
        mod_type = modules[mod_type_name]
        start = int(mod_config.pop('start'), 0)
        length = int(mod_config.pop('length'), 0)
        pc_modules[mod_config_name] = mod_type(start=start, length=length, **mod_config)
    computer = Computer(list(pc_modules.values()))
    computer.run()


if __name__ == '__main__':
    main()
