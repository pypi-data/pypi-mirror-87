
import os
import argparse
import json

from .plugin_object import Plugin_Runner, Plugin_Object, default_params

from general_utility import utils as us
from general_utility.appbase import ab

#######################################################################################
# 核心功能函数

# 加载插件
def load_plugin(file_path):
    from imp import acquire_lock, release_lock, load_module, PY_SOURCE
    from .iplugin import iPlugin

    plugin = None
    try:        
        with open(file_path, 'r', encoding='UTF-8') as openfile:
            acquire_lock()
            mod = load_module("mod", openfile, file_path, ('.py', 'r', PY_SOURCE))
            if hasattr(mod, "__all__"):
                attrs = [getattr(mod, x) for x in mod.__all__]
                for obj in attrs:
                    if not issubclass(obj, iPlugin):
                        continue
                    plugin = obj()
                    print("find plug name: %s" % plugin.name)
    except Exception as e:
        plugin = None
    finally:
        pass
    release_lock()  
    if openfile:
        openfile.close()
    return plugin

# 分析插件包，获取相关信息
def plugin_analysis(pulgin_url):
    pulgin_filepath = get_filepath_from_url(pulgin_url, None) # 如果是网络地址则先下载到临时目录下再读取
    if (pulgin_filepath == None):
        pulgin_filepath = os.path.join(pulgin_url) # 本地地址

    if (path_exists(pulgin_filepath) == False):
        ab.print_log("plugin file is not exists (%s)" % pulgin_filepath, "error")
        return None
    _, _, name, suffix = get_path_name_suffix_from_filepath(pulgin_filepath)

    plugin_config_jaon = {}
    if (suffix.lower() == '.zip'):
        config_file_data = get_file_from_zipfile(pulgin_filepath, default_params['plugin_config_filename'])
        config_file_data = str(config_file_data, 'utf-8')

        plugin_config_jaon = json.loads(config_file_data)
    elif (suffix.lower() == '.py'):
            plugin_obj = load_plugin(pulgin_filepath)
            if (plugin_obj is not None):
                base = {}
                base['name'] = plugin_obj.name
                base['showname'] = plugin_obj.showname
                base['version'] = plugin_obj.version
                base['description'] = plugin_obj.description
                base['role'] = plugin_obj.role
                plugin_config_jaon['base'] = base

                plugin_config_jaon['params'] = plugin_obj.params
    else:
        plugin_config_jaon = None

    if (plugin_config_jaon is not None):
        ab.print_log("plugin analysis: (name: %s, showname: %s, version: %s, description: %s, role: %s)" % ( \
                    plugin_config_jaon['base']['name'], \
                    plugin_config_jaon['base']['showname'], \
                    plugin_config_jaon['base']['version'], \
                    plugin_config_jaon['base']['description'], \
                    plugin_config_jaon['base']['role'] \
                    ), "info")

    return plugin_config_jaon

# 根据url获取插件项目信息，并生成相关结构返回
def plugin_load(pulgin_url):
    parsed = get_parse_from_url(pulgin_url)
    if (parsed.scheme.lower() != 'http'): # 暂时只支持http协议
        return None
    hostaddr = parsed.scheme + '://' + parsed.netloc

    plugin_config_jaon = get_json_from_url(pulgin_url)
    if (plugin_config_jaon is None):
        return None
    meta_json_obj = plugin_config_jaon['meta']
    ab.print_log(meta_json_obj)

    plugins_json_obj = plugin_config_jaon['plugins']
    for plugin_info in plugins_json_obj:
        plugin_info_obj = plugins_json_obj[plugin_info]
        download_url = hostaddr + plugin_info_obj['download_url']

        plugin_obj = Plugin_Object(download_url)

        # ab.print_log(plugin_info_obj)

    return plugin_config_jaon

def plugin_test(pulgin_url):
    return plugin_load(pulgin_url)

#######################################################################################

def parse_args():
    
    """Parse arguments."""
    # Parameters settings
    parser = argparse.ArgumentParser(prog="python main.py", description="-- 插件解析及相关工具 --", epilog="---------------------")

    # 压缩打包
    parser.add_argument('-p', '--pack', action='store_true', default=False, help='插件打包')

    # 解压解析
    parser.add_argument('-a', '--analysis', action='store_true', default=False, help='解压解析')

    # 加载插件
    parser.add_argument('-l', '--load', action='store_true', default=False, help='加载插件')

    # 测试插件
    parser.add_argument('-t', '--test', action='store_true', default=False, help='测试插件')

    # 运行插件框架
    parser.add_argument('-r', '--run', action='store_true', default=False, help='运行插件框架')

    # 目录设置
    parser.add_argument('--dir', type=str, default='', help='目录设置')

    # 插件路径
    parser.add_argument('--url', type=str, default='', help='插件路径')

    # parse the arguments
    args = parser.parse_args()

    return args

def main():
    args = parse_args()

    plugin_dir = os.path.join(os.getcwd(), './data/output/plugin/')

    # 打包流程
    if args.pack:
        subdir_pack(args.dir, plugin_dir)
        return

    # 解压解析
    if args.analysis:
        plugin_obj = plugin_analysis(args.url, plugin_dir = plugin_dir)
        return

    # 加载插件
    if args.load:
        url = args.url
        scheme = get_scheme_from_url(url)
        if (scheme == None):
            if (os.path.isdir(url)):
                pass
            elif (os.path.isfile(plugin_url)):
                url = os.path.join(plugin_dir, url) # 非网络地址，转换为本地地址
        plugin_obj = Plugin_Object(url)
        if (plugin_obj is None):
            ab.print_log('load plugin error!')
            return

        if (args.test):
            test = plugin_obj.test()

        return

    # 运行插件框架
    if args.run:
        plugin_Runner = None
        url = args.url
        scheme = get_scheme_from_url(url)
        if (scheme == None):
            plugin_Runner = Plugin_Runner(url)
        else:
            # plugins_json = plugin_load(url)
            plugin_Runner = Plugin_Runner(url, plugin_dir)

        if (plugin_Runner is not None):
            print(plugin_Runner.getPluginsDict())
            plugin_Runner.run()

        return

#######################################################################################

if __name__ == '__main__':
    main()