import asyncio
import inspect
import logging
import typing


logger = logging.getLogger(__name__)

builtin_simple_types = (int, float, str, bool)
builtin_types = (list, tuple, dict, set)


def cast_arg_to_type(arg, arg_type):
    if arg_type in builtin_simple_types:
        return arg_type(arg)

    if inspect.isclass(arg_type) and hasattr(arg_type, 'from_dict'):
        return arg_type.from_dict(arg)

    arg_origin = typing.get_origin(arg_type)
    arg_items_types = typing.get_args(arg_type)

    if arg_origin == list:
        return [
            cast_arg_to_type(el, arg_items_types[0]) for el in arg
        ]

    if arg_origin == dict: 
        return {
            cast_arg_to_type(key, arg_items_types[0]): cast_arg_to_type(value, arg_items_types[1])
            for key, value in arg.items()
        }

    return arg


def cast_args_to_annotation_types(args, func_annotations):
    for arg_name, arg_value in args.items():
        if arg_name not in func_annotations:
            continue
        args[arg_name] = cast_arg_to_type(arg_value, func_annotations[arg_name])
    return args


class DefaultState:
    def __init__(self):
        self._lock = asyncio.Lock()

    def _list_items_to_dict(self, list_):
        return [
            item.to_dict() if hasattr(item, 'to_dict') else item
            for item in list_
        ]
    
    def _dict_items_to_dict(self, dict_):
        return {
            key: value.to_dict() if hasattr(value, 'to_dict') else value
            for key, value in dict_.items()
        }

    def to_dict(self):
        logging.info(f'Runnung to_dict for {self.__class__}')
        dict_ = dict()
        for key, value in self.__dict__.items():
            if isinstance(value, list):
                value = self._list_items_to_dict(value)
            elif isinstance(value, dict):
                value = self._dict_items_to_dict(value)
            elif hasattr(value, 'to_dict'):
                value = value.to_dict()
            dict_[key] = value
        dict_.pop('_lock', None)
        return dict_

    @classmethod
    def from_dict(cls, dict_):
        logging.info(f'Runnung from_dict for {cls}')
        instance = cls.__new__(cls)

        init_params = inspect.signature(instance.__init__).parameters.keys()
        init_args = {
            key: value for key, value in dict_.items()
            if key in init_params
        }
        init_args = cast_args_to_annotation_types(init_args, instance.__init__.__annotations__)
        instance.__init__(**init_args)
        return instance
