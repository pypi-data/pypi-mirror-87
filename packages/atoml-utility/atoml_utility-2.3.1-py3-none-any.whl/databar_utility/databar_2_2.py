import pandas as pd
import numpy as np

from general_utility import utils as us
from general_utility.appbase import ab

class Databar_Pro():
    def __init__(self, **kwargs):
        self.params = us.check_attribute(kwargs, 'params', None)
        self.values = {}
        input = us.check_attribute(kwargs, 'input', None)
        if (input is not None):
            self.load(input)

    def param(self, key, default = None):
        return us.check_attribute(self.params, key, default)

    ####################################################################

    def add(self, data = None):
        if (data is None):
            return False, None

        for (K, V) in data.items():
            values = us.check_attribute(self.values, K, {})
            if ('databar' in K.lower()):
                value = us.check_attribute(values, K, [])
                for databar in V:
                    value.append(databar[K])
                self.values[K] = value
            else:
                self.values[K] = V
        
        return True, self.serializes()

    def serializes(self, data = None):
        if (data is None):
            data = self.values
        
        result = {}
        if (isinstance(data, dict)):
            for (K, V) in data.items():
                if (isinstance(V, list)):
                    for item in V:
                        item_serializes = us.check_attribute(result, K, [])
                        if (hasattr(item, 'serialize')): # 复数序列化
                            item_serializes.append(item.serialize())

                        result[K] = item_serializes
                elif (isinstance(V, dict)):
                    result[K] = us.dict_copy(V, '*', '')
                else:
                    result[K] = V
        elif (isinstance(data, list)):
            result['values'] = data

        return result

    ####################################################################

    def load(self, databars):
        if (databars is None):
            return False

        if (isinstance(databars, list)):
            for item in databars:
                self.load(item) # 循环添加
            return True

        if (not isinstance(databars, dict)):
            return False

        df = None
        index_field = None
        strategy_type = None
                    
        ab.print_log('-------------------------------------------------------')
        ab.print_log("load databars: %s" % databars)

        if (us.att_isin(databars, 'date_range')):
            date_range = us.check_attribute(databars, 'date_range')
            """ 起始日期 """
            start_date = us.check_date(us.check_attribute(date_range, 'start_date'), "%Y%m%d")
            end_date = us.check_date(us.check_attribute(date_range, 'end_date'), "%Y%m%d")

            ab.print_log("start & end datetime: %s ~ %s" % (start_date, end_date))

        if (us.att_isin(databars, 'databarx')):
            databar = us.check_attribute(databars, 'databarx')
            databars['x'] = self.load_databar(databar, start_date, end_date)

        if (us.att_isin(databars, 'databary')):
            databar = us.check_attribute(databars, 'databary')
            databars['y'] = self.load_databar(databar, start_date, end_date)

        self.values = us.dict_merged(self.values, databars)

        return True
        
    def load_databar(self, databar, start_date = 'NOW', end_date = 'NOW'):
        params_list = 'time_step, random_seed, translation, train_data_rate, valid_data_rate, shuffle_train_data'

        dfs = None
        num = 0
        for item in databar:
            source_type = us.check_attribute(databar, 'source_type')
            source_pool = us.check_attribute(databar, 'source_pool')
            all_fields = us.check_attribute(databar, 'all_fields')
            index_field = us.check_attribute(databar, 'index_field')
            calc_field = us.check_attribute(databar, 'calc_field')
            strategy_type = us.check_attribute(databar, 'strategy_type')
            normalization = us.check_attribute(databar, 'normalization')
            
            df = None
            if ("file." in source_type): # 文件
                df = self.load_databar_from_csv(source_type, source_pool, all_fields, index_field, start_date, end_date)
                df = self.strategy(df, calc_field, strategy_type) # 数据预处理
            elif ("db." in source_type): # 数据库
                pass

            if (df is None) and (df.empty):
                continue

            # 更改标签名，避免合并的时候丢失数据
            for field in us.params_split(calc_field, ','):
                df = df.rename(columns={field: field + '_' + str(num)})

            num = num + 1

            if (dfs is not None):
                dfs = pd.merge(dfs, df, on = index_field).sort_values(by = index_field)
            else:
                dfs = df.sort_values(by = index_field)

        if ((index_field != None) and (index_field.lower() != 'null')):
            dfs = dfs.drop(index_field, axis=1) # 删除索引列

        if (dfs is not None):
            ab.print_log(dfs.head(3))
            ab.print_log('.........')
            ab.print_log(dfs.tail(3))
            ab.print_log('-------------------------------------------------------')

        result = us.dict_copy(self.params, params_list, '')
        result['columns'] = dfs.columns.tolist()
        dfs = dfs.values

        if (dfs is not None) and (normalization):
            # 数据的均值和方差
            result['mean'] = np.mean(dfs, axis= 0)
            result['std'] = np.std(dfs, axis = 0)

            result['values'] = (dfs - result['mean']) / result['std'] # 归一化，去量纲
        else:
            result['values'] = dfs

        train_data_rate = us.check_attribute(result, 'train_data_rate', 1)
        result['data_num'] = dfs.shape[0]
        result['train_num'] = int(result['data_num'] * train_data_rate)
        result['test_num'] = result['data_num'] - result['train_num']

        result['sample_interval'] = min(result['test_num'], result['time_step'])     # 防止time_step大于测试集数量
        result['start_num_in_test'] = result['test_num'] % result['sample_interval']  # 这些天的数据不够一个sample_interval
        result['time_step_size'] = result['test_num'] // result['sample_interval']

        return result

    def load_databar_from_csv(self, source_type, source_pool, all_fields, index_field, start_date, end_date):
        if ('.csv' not in source_type.lower()):
            return None

        filepath = source_pool # 这里只做了单文件处理
        if (us.path_exists(filepath) == False):
            filepath = us.make_param(filepath, None)
            if (us.path_exists(filepath) == False):
                return None

        df = pd.read_csv(filepath, nrows = 1)

        columns = []
        if (all_fields.lower() == 'all') or (all_fields == '*'):
            columns = df.columns.values.tolist()
        else:
            fields_list = us.params_split(all_fields, ',')
            for field in fields_list:
                if field[0] == '-': # 判断是白名单还是黑名单
                    if (len(columns) <= 0):
                        columns = df.columns.values.tolist()
                    columns.remove(field[1:])
                else:
                    columns.append(field)

        df = pd.read_csv(filepath, usecols = columns)
        # if ('date' in columns): # 时间筛选，目前还有问题，先注释5
        #     df = df.loc[(df['date'] >= start_date) & (df['date'] <= end_date)]

        if ((index_field != None) and (index_field.lower() != 'null')):
            df.set_index(index_field)

        return df

    def strategy(self, df, calc_field, strategy_type):
        if (df is None) and (strategy_type is None): # 这里如果设置了策略类型，则需要进行数据再加工处理
            return df

        calc_field = us.params_split(calc_field, ',') # 字符串转换为列表格式
        if (strategy_type.lower() == 'field'):
            pass # 直接返回所有
        else:
            
            if (strategy_type.lower() == 'avg'):
                df[strategy_type] = df[calc_field].mean(axis=1)
            elif (strategy_type.lower() == 'sum'):
                df[strategy_type] = df[calc_field].sum(axis=1)
            
            df = df.drop(calc_field, axis=1) # 应为转换了，所以删除

        return df

    def get_values(self, **kwargs):

        ###############################################################################

        def get_train_data(values, name = '', islabel = False):
            if (name == ''):
                x = get_train_data(values, name = 'x')
                y = get_train_data(values, name = 'y', islabel = True)
                
                from sklearn.model_selection import train_test_split
                result = train_test_split(x, y, 
                            test_size = self.params['valid_data_rate'],
                            random_state = self.params['random_seed'],
                            shuffle = self.params['shuffle_train_data']) 

                return result
            
            values = us.check_attribute(values, name)

            train_data_rate = us.check_attribute(values, 'train_data_rate', 0.6)
            time_step = us.check_attribute(values, 'time_step', 20)
            translation = us.check_attribute(values, 'translation', 0)
            train_num = us.check_attribute(values, 'train_num', 1)

            result = us.check_attribute(values, 'values')
            
            if (islabel):
                result = result[translation : translation + train_num]
            else:
                result = result[:train_num]

            return np.array([result[i : i + time_step] for i in range(train_num - time_step)])

        ###############################################################################

        def get_test_data(values, name = '', islabel = False):
            if (name == ''):
                x = get_test_data(values, name = 'x')
                y = get_test_data(values, name = 'y', islabel = True)
                return x, y

            values = us.check_attribute(values, name)

            train_data_rate = us.check_attribute(values, 'train_data_rate', 0.6)
            time_step = us.check_attribute(values, 'time_step', 20)
            translation = us.check_attribute(values, 'translation', 0)
            train_num = us.check_attribute(values, 'train_num', 1)

            sample_interval = us.check_attribute(values, 'sample_interval', 0)
            start_num_in_test = us.check_attribute(values, 'start_num_in_test', 0)
            time_step_size = us.check_attribute(values, 'time_step_size', 0)

            result = us.check_attribute(values, 'values')
            result = result[train_num:]

            if (not islabel):
                result = [result[start_num_in_test + i * sample_interval : start_num_in_test + (i + 1) * sample_interval]
                            for i in range(time_step_size)]
            else:
                result = result[start_num_in_test:]

            return np.array(result)

        ###############################################################################

        def get_other(values, name = ''):
            if (name == ''):
                x = get_other(values, 'x')
                y = get_other(values, 'y')
                return x, y

            params_list = 'data_num, train_num, test_num, start_num_in_test, time_step_size, translation, mean, std, columns'

            return us.dict_copy(us.check_attribute(values, name), params_list, '')

        ###############################################################################

        if (self.values is None):
            return None

        type = us.check_attribute(kwargs, 'type', 'train')

        if (type.lower() == 'train'):
            x_train, x_valid, y_train, y_valid = get_train_data(self.values)

            ab.print_log('x_train shape: ')
            ab.print_log(x_train.shape)
            ab.print_log('x_valid shape: ')
            ab.print_log(x_valid.shape)
            ab.print_log('y_train shape: ')
            ab.print_log(y_train.shape)
            ab.print_log('y_valid shape: ')
            ab.print_log(y_valid.shape)
            ab.print_log('-------------------------------------------------------')

            return x_train, y_train, x_valid, y_valid
        elif (type.lower() == 'test'):
            x_test, y_test = get_test_data(self.values)

            ab.print_log('x_test shape: ')
            ab.print_log(x_test.shape)
            ab.print_log('y_test shape: ')
            ab.print_log(y_test.shape)
            ab.print_log('-------------------------------------------------------')

            return x_test, y_test

        elif (type.lower() == 'other'):

            return get_other(self.values)

        return None, None
