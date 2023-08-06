# -*- coding: utf-8 -*-
""" class实例化 延迟 """
import re
from functools import wraps
from inspect import signature


class Box(object):

    def __init__(self):
        self.__payload = None
        self.__objs_class_mappings = {}

    def inject(self, *class_args, **class_kwargs):
        _payload = class_kwargs.get('payload', None)
        if _payload is None:
            _payload = {}

        _dependency = class_kwargs.get('dependency', None)
        __class_args = list(class_args)
        if _dependency is not None:
            __class_args.append(_dependency)

        pattern = "[A-Z]"
        for _c in __class_args:
            __c_name = re.sub(pattern, lambda x: "_" + x.group(0).lower(), _c.__name__).strip('_')
            self.__objs_class_mappings.update({__c_name: dict(_obj=None, _cls=_c, _payload=_payload)})

    def depend(self, *depend_args, **depend_kwargs):

        def decorator(_func):

            self.inject(_func)

            @wraps(_func)
            def _wrap(_self, *wrap_args, **wrap_kwargs):
                print(_self)
                print(wrap_args)
                print(wrap_kwargs)
                return
            return _wrap

        return decorator

    def invoke(self, name,  *payload_args, **payload_kwargs):
        return self.__invoke(name, *payload_args, **payload_kwargs)

    def __get_probable_instance_or_class(self, _c_name):
        if self.__objs_class_mappings[_c_name]['_obj'] is None:
            return self.__objs_class_mappings[_c_name]['_cls'], False
        return self.__objs_class_mappings[_c_name]['_obj'], True

    def __get_payload(self, _c_name):
        return self.__objs_class_mappings[_c_name]['_payload']

    def __invoke(self, _c_name, *payload_args, **payload_kwargs):
        _maybe_ins_obj, is_ins = self.__get_probable_instance_or_class(_c_name)
        if is_ins:
            return _maybe_ins_obj
        else:
            _ins_obj = _maybe_ins_obj(*payload_args, **payload_kwargs)
            self.__set_inst_obj(_c_name, _ins_obj)
            return _ins_obj

    def __set_inst_obj(self, _c_name, _ins_obj):
        if self.__objs_class_mappings[_c_name]['_obj'] is None:
            self.__objs_class_mappings[_c_name]['_obj'] = _ins_obj

    def __get_instance_obj(self, _c_name):
        _maybe_ins_obj, is_ins = self.__get_probable_instance_or_class(_c_name)
        if is_ins:
            return _maybe_ins_obj
        else:
            __get_payload = self.__get_payload(_c_name)
            if len(__get_payload):
                _ins_obj = _maybe_ins_obj(**__get_payload)
            else:
                _ins_obj = _maybe_ins_obj()
            self.__set_inst_obj(_c_name, _ins_obj)
            return _ins_obj

    def __getattr__(self, _c_name):

        if _c_name in self.__objs_class_mappings:
            return self.__get_instance_obj(_c_name)

