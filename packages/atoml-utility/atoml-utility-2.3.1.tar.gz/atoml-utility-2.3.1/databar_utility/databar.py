
import os
import sys
from general_utility import utils as us
from general_utility.appbase import ab

class Databar():
    def __init__(self, **kwargs):
        self.protocol_version = '1.0'
        if (us.att_isin(kwargs, 'protocol_version')):
            self.protocol_version = kwargs.pop('protocol_version')

        ab.print_log('data protocol version: %s' % self.protocol_version)

        self.databar_pro = None
        try:
            search_dir = os.path.dirname(__file__)
            sys.path.append(search_dir)

            imp_module = ('databar_%s' % (self.protocol_version.replace('.', '_')))
            imp_class = 'Databar_Pro'

            ab.print_log('load databar parser: %s' % imp_module)

            import importlib
            databar_module = importlib.import_module(imp_module)
            ab.print_log('load databar parser successful')
            
            databar_module_cls = getattr(databar_module, imp_class)

            input = us.check_attribute(kwargs, 'input', None)
            params = us.check_attribute(kwargs, 'params', None)

            self.databar_pro = databar_module_cls(input = input, params = params)
        except Exception as e:
            ab.print_log("load databar_pro error: %s" % e)
            self.databar_pro = None

        pass

    def ver_fun(self, fun_name, values):
        if (self.databar_pro is None):
            return None
        if us.obj_hasattr(self.databar_pro, fun_name):
            fun = us.obj_getattr(self.databar_pro, fun_name)
            return fun(values)
        return None

    def add(self, values):
        return self.ver_fun(fun_name = sys._getframe().f_code.co_name, values = values)

    def load(self, values):
        return self.ver_fun(fun_name = sys._getframe().f_code.co_name, values = values)

    def serializes(self, values = None):
        result = self.ver_fun(fun_name = sys._getframe().f_code.co_name, values = values)

        result['writer'] = ("%s.%s" % (self.__class__.__name__, sys._getframe().f_code.co_name))
        result['protocol_version'] = self.protocol_version
        
        return result
    
    def get_values(self, **kwargs):
        if (self.databar_pro is None):
            return None
        return self.databar_pro.get_values(**kwargs)

    ####################################################################
