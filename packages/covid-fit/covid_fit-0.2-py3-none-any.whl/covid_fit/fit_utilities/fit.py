#!/usr/local/bin/python3

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy
from scipy.optimize import leastsq
import datetime
# from matplotlib import pyplot
from scipy.stats import chisquare
# import os
import sys

sys.path.append('../..')
from covid_fit.fit_functions.funcs import map_func

########################################
def plotter(x_val, y_val, x_fit_val = None, y_fit_val = None):
    
    if isinstance(x_val, list):
        plt.figure(figsize=(12, 8))
        series = zip(x_val, y_val, x_fit_val, y_fit_val)
        for x, y, x_fit, y_fit in series:
            plt.scatter(x, y, label='Data')
            plt.plot(x_fit, y_fit,
                     label='Fitted function')
            plt.legend(loc='best')
            plt.xlabel('range')
        plt.show()

    else:
        plt.figure(figsize=(12, 8))
        if show:
            plt.scatter(x0, y0, label='Data')
        plt.scatter(x_val, y_val, label='Data')
        plt.plot(x_fit_val, y_fit_val,
                 label='Fitted function')
        plt.legend(loc='best')
        plt.xlabel('range')
    #     plt.xticks(x, dates_fit, rotation='vertical')
        plt.show()


class TableFiltering():
    
    def __init__(self):
        """ Initialization of the class table filtering: simple filtering process
        Class object to filter a pandas dataframe
        no params required for instanciations
        """
    def preprocessing(self, df, select = None, cuts = None, return_original=False):
        '''apply filters on categorical or continuos variables. Use "select" and "cuts" params 
        dictionary to filter pandas dataframe columns. 
        
        param df: dataframe
        param select: dictionary of selection to apply on categorical variables
        param cuts: dictionary of cuts to apply on continuos variables
        
        type df: Pandas Dataframe
        type select: dictionary
        type cuts: dictionary
        
        Example: 
        select = {categorical_var: [mod_1, mod_2]} To filter categorical variables
        cuts = {continuos_variable_1: < 10 and > 30,
                continuos_variable_2: <= 10 or > 20} To filter continuos variables
        '''
        if select is not None:
            for k,v in select.items():
                if isinstance(v, list):
                    df = df[df[k].isin(v)]
                else:
                    df = df[df[k].isin([v])]

        if cuts is not None:
            for k,v in cuts.items():
                if 'and' in v:
                    condition = v.replace(' ','')
                    condition = condition.split('and')
                    for con in condition:
                        print('{} {} {}'.format(k,con[0],con[1:]))
                        df = df.query('{} {} {}'.format(k,con[0],con[1:]))
                elif 'or' in v:
                    condition = v.replace(' ','')
                    condition = condition.split('or')
                    df_filtered = pd.DataFrame(columns = df.columns)
                    for con in condition:
                        df_filtered = df_filtered.append(df.query('{} {} {}'.format(k,con[0],con[1:])))
                    df = df_filtered.drop_duplicates(df_filtered.columns)
                else:
                    con = v.replace(' ','')
                    print(con)
                    if con[0] == '=':
                        comp = '=='
                        cond = con[1:]
                        df = df.query('{} {} {}'.format(k,comp,cond))
                    elif con[0:2] in ['==','eq']:
                        comp = '=='
                        cond = con[2:]

                        df = df.query('{} {} {}'.format(k,comp,cond))
                        print('{} {} {}'.format(k,comp,cond))
                    else:
                        df = df.query('{} {} {}'.format(k,con[0],con[1:]))
        if return_original:
            return df, df
        else:        
            return df

class FitterValues():
    def __init__(self):
        """ Initialization of the class fitter: Fit y values on x range
        """
    
    def fit(self, model, x_val, y_val, n_previsions, p0=None, plot=True):
        """ fit on x_val range and predict y_val on next n_prevision day:
        
        :params model: model to apply among [linear, exponential, logistic, logistig_der
                                            gompertz, gompertz_der, logistic_gen, logistic_gen_der]
        :params x_val: x range of the fit
        :params y_val: y value to fit
        :n_previsions: number of day to predict beyond the x_range
        :p0: initia guess parameters
        :plot: plot or not the results
        
        :type model: string
        :type x_val: np.array
        :type y_val: np.array
        :n_previsions: int
        :p0: list of int(float)
        :plot: boolean
        """
        
        if isinstance(x_val,list):
            pass
        else:
            x_val = [x_val]
            y_val = [y_val]
            
        dic_list = []
        x_fitted_list = []
        y_fitted_list = []
        y_values_list = []
        x_values_list = []
        for x,y in zip(x_val,y_val):
            pars_fit = scipy.optimize.curve_fit(map_func[model]['get_fit']
                                           ,x , y, p0)
            pars = pars_fit[0]
            sigma_pars = np.sqrt(np.diag(pars_fit[1]))
            n_days = len(x)
            ddof = n_days - len(pars)
            fitted_values = map_func[model]['get_values'](x, pars)
            chi, p = chisquare(y, fitted_values, ddof)

            all_x = np.array([i for i in range(x[0], x[0] + n_days + n_previsions)])
            all_y = map_func[model]['get_values'](all_x, pars)

            dic = {}
            dic['parameters_fit'] = pars
            dic['sigma_pars'] = sigma_pars
            dic['fitted_day'] = n_days
            dic['chi_2'] = {'chi_value':chi, 'p_value':p}
            dic['model'] = model
            dic['previsions'] = n_previsions
            dic['fit_prevs_values'] = all_y
            dic['fit_prevs_range'] = all_x
            dic['fit_values'] = y
            dic['fit_range'] = x

            dic_list.append(dic)

            x_values_list.append(x)
            y_values_list.append(y)
            x_fitted_list.append(all_x)
            y_fitted_list.append(all_y)

        if plot:
            plotter(x_values_list, y_values_list, x_fitted_list, y_fitted_list)

        return dic_list
    
#     def __fit_predict_plot(self, x, y, n_previsions, report = True, plot = True):
#         print(self.model)

#         return pars
    
    def _hidden_func(self, x, y, n_previsions):
        print(self.model)
        
# _ for hidden method
# __ method that are protected adding the object prefix ahead of the method


class FitterTimeSeries(FitterValues,TableFiltering):
    def __init__(self, df, datetime_columns = None, format_date = "%Y-%m-%d",select=None, cuts = None
                 , multiseries_on = False):
        
        """ Initialization of the class fitter: Fit y values on x range
        :param df: dataframe
        :param datetime_columns: date column to set as index
        :param format_date: how to format datetime_columns
        :param select: dictionary of selection to apply on categorical variables
        :param cuts: dictionary of cuts to apply on continuos variables
        :param multiseries_on: columns that specify modalities for multiseries analysis
        (example: 'denominazione_regione' >>> analyse for all different region)
        
        :type df: Pandas Dataframe
        :type datetime_columns: string
        :type select: dictionary
        :type cuts: dictionary
        :type multiseries_on: string
        
        Example of select and cuts application: 
        select = {categorical_var: [mod_1, mod_2]} To filter categorical variables
        cuts = {continuos_variable_1: < 10 and > 30,
                continuos_variable_2: <= 10 or > 20} To filter continuos variables
        
        """
        if(isinstance(df,pd.DataFrame)):
            if (select is not None) | (cuts is not None):
                df = self.preprocessing(df, select, cuts)
                self.df = df.copy()
            else:
                self.df = df.copy()
        self.df[datetime_columns] = pd.to_datetime(self.df[datetime_columns], format = format_date)
        self.df.set_index(datetime_columns,inplace = True)
        self.cuts = cuts
        self.select = select
        self.multiseries_on = multiseries_on
        self.format_date = format_date
        super().__init__()
        
    def __delattr__(self, name):
        print("deleting {}".format(str(name)))
        del self.__dict__[name]
        print("{} deleted".format(str(name)))
    
    def fit_time_series(self,columns_analysis= None, start_date= None, end_date= None, n_previsions= 0,
                        p0 = None, model='linear', plot = True, semilog=False, show_test = True):
        '''
        :params columns_analysis: name of the column to analyse 
        :params start_date: fit starting day
        :params end_date: last day of fit
        :n_previsions: number of day to predict beyond the x_range
        :p0: initial guess parameters
        :params model: model to apply among [linear, exponential, logistic, logistig_der
                                            gompertz, gompertz_der, logistic_gen, logistic_gen_der]
        :plot: plot or not the results
        :semilog: apply log scale on y values
        :show_test: if end_date < last date in dataframe columns decide to show or not the additional
        values of the dataframe inthe plot
        
        :type columns_analysis: string or list fo string
        :type start_date: string
        :type end_date: string
        :type n_previsions: int
        :type p0: list of int(float)
        :type model: string 
        :type plot: boolean
        :type semilog: boolean
        :type show_test: boolean
        '''
        
        if isinstance(model, str):
            pass
        else:
            raise(ValueError('the model is not a string'))
        
        if columns_analysis == None:
            ValueError('column analysis is None')
        
        df_fit_date = self.df.loc[start_date:end_date]
        df_all_date = self.df.loc[start_date:None]
        
        if len(df_all_date) > len(df_fit_date):
            extra_values = True
        else:
            extra_values = False
            
        show = extra_values*show_test
        if isinstance(columns_analysis, list):
            pass
        else:
            columns_analysis = [columns_analysis]
            
        dic_list = []
        most_update_dic_list = []
        setting_list = []
        
        for col in columns_analysis:
            if self.multiseries_on:
                series = np.unique(df_fit_date[str(self.multiseries_on)])
                y = []
                y0 = []
                dates0 = df_all_date[df_all_date[self.multiseries_on] == series[-1]].loc[:, col].index
                x0 = np.array(np.arange(len(dates0)))
                for serie in series:
                    y.append(df_fit_date[df_fit_date[self.multiseries_on] == serie].loc[:, col].values)
                    y0 = np.array(df_all_date[df_all_date[self.multiseries_on] == serie].loc[:, col].values)
                    
                    setting_list.append('{}/{}'.format(col,serie))
                    most_update_dic_list.append({'x':x0, 'y':y0, 'dates':dates0})

                dates = df_fit_date[df_fit_date[self.multiseries_on] == serie].loc[:, col].index
                x = [np.array(np.arange(len(dates)))]*len(series)
                
            else:
                dates = df_fit_date.index
                dates0 = df_all_date.index
                y = np.array(df_fit_date.loc[:, col])
                x = np.array(np.arange(len(dates)))
                x0 = np.array(np.arange(len(dates0)))
                y0 = np.array(df_all_date.loc[:, col])
                
                most_update_dic_list.append({'x':x0, 'y':y0, 'dates':dates0})
                setting_list.append('{}'.format(col))
                
            dic_list.append(self.fit(model,x, y, n_previsions, p0, plot=False))
       
        sl_idx = 0
        for idx in range(len(dic_list)):
            if plot:
                plt.figure(figsize=(16, 8))
            for dic in dic_list[idx]:
                x_fit = dic['fit_prevs_range']
                y_fit = dic['fit_prevs_values'] 
                x_val = dic['fit_range']
                y_val = dic['fit_values'] 
                model = dic['model']
                p_chi2 = dic['chi_2']['p_value']
                
                x_0 = most_update_dic_list[sl_idx]['x']
                y_0 = most_update_dic_list[sl_idx]['y']

                label = '_'.join(setting_list[sl_idx].split('/'))
                dic['label'] = label
                
                if len(x_fit) >= len(x_0):
                     dates_plot = [(dates[0] + datetime.timedelta(days=xi)).strftime(self.format_date)\
                         for xi in range(len(x_fit))]
                elif len(x_fit) < len(x_0):
                     dates_plot = [(dates0[0] + datetime.timedelta(days=xi)).strftime(self.format_date)\
                         for xi in range(len(x_0))]
                            
                dic['dates_plot'] = dates_plot
                
                if show:
                    dic['data_range_plot'] = x_0
                    dic['data_values_plot'] = y_0
                else:
                    dic['data_range_plot'] = x_val
                    dic['data_values_plot'] = y_val
                        
                if plot:
                    if show:
                        plt.scatter(x_0, y_0, label='{} Data'.format(setting_list[sl_idx]))
                    else:
                         plt.scatter(x_val, y_val, label='{} Data'.format(setting_list[sl_idx]))
                    plt.plot(x_fit, y_fit, label='{} Fit {} p_chi2 {:.2f}'\
                             .format(setting_list[sl_idx], model, p_chi2))
                    plt.xticks([d for d in range(len(dates_plot))],  dates_plot, rotation='vertical', fontsize = 14)
                    plt.legend(loc='best',fontsize = 12)
                    plt.title('{}'.format(setting_list[sl_idx].split('/')[0]),fontsize = 16)
                    plt.xlabel('Day', fontsize = 16)
                    plt.ylabel('{}'.format(setting_list[sl_idx].split('/')[0]), fontsize = 16)
                    if len(x_val)< len(dates_plot):
                        plt.axvline(len(x_val)-1, alpha = 0.5,linewidth=3, ls = '--')
                    if semilog:
                        plt.yscale('log')
                sl_idx += 1
        plt.show()

        return dic_list

class FitterTimeSeriesComparison(FitterTimeSeries,TableFiltering):
    def __init__(self, df, datetime_columns = None, format_date = "%Y-%m-%d",select=None, cuts = None
                 , multiseries_on = False):
        
        """ Initialization of the class fitter: Fit y values on x range
        Compare on different series different model (extension of FitterTimeSeries)
        In this class "model" and "column_analysis" of fit_time_series_comparison method
        are allowed to be a list
        
        :param df: dataframe
        :param datetime_columns: date column to set as index
        :param format_date: how to format datetime_columns
        :param select: dictionary of selection to apply on categorical variables
        :param cuts: dictionary of cuts to apply on continuos variables
        :param multiseries_on: columns that specify modalities for multiseries analysis
        (example: 'denominazione_regione' >>> analyse for all different region)
        
        :type df: Pandas Dataframe
        :type datetime_columns: string
        :type select: dictionary
        :type cuts: dictionary
        :type multiseries_on: string
        
        Example of select and cuts application: 
        select = {categorical_var: [mod_1, mod_2]} To filter categorical variables
        cuts = {continuos_variable_1: < 10 and > 30,
                continuos_variable_2: <= 10 or > 20} To filter continuos variables
        
        """
#         super().__init__(self, df)
        if(isinstance(df,pd.DataFrame)):
            if (select is not None) | (cuts is not None):
                df = self.preprocessing(df, select, cuts)
                self.df = df.copy()
            else:
                self.df = df.copy()
#         df.apply(lambda x: x['data'].split('T')[0], axis = 1)
#         self.df[datetime_columns] = self.df[datetime_columns].apply(lambda x: x.split('T')[0])
        self.df[datetime_columns] = pd.to_datetime(self.df[datetime_columns], format = format_date)
        self.df.set_index(datetime_columns,inplace = True)
        self.cuts = cuts
        self.select = select
        self.multiseries_on = multiseries_on
        self.format_date = format_date

        
    def fit_time_series_comparison(self,columns_analysis= None, start_date= None, end_date= None, n_previsions= 0,
                        p0 = None, model='linear', plot = True, semilog=False, show_test = True):
        
        '''
        :params columns_analysis: name of the column to analyse 
        :params start_date: fit starting day
        :params end_date: last day of fit
        :n_previsions: number of day to predict beyond the x_range
        :p0: initial guess parameters
        :params model: model to apply among [linear, exponential, logistic, logistig_der
                                            gompertz, gompertz_der, logistic_gen, logistic_gen_der]
        :plot: plot or not the results
        :semilog: apply log scale on y values
        :show_test: if end_date < last date in dataframe columns decide to show or not the additional
        values of the dataframe inthe plot
        
        :type columns_analysis: string or list fo string
        :type start_date: string
        :type end_date: string
        :type n_previsions: int
        :type p0: list of int(float)
        :type model: string or list of strinf
        :type plot: boolean
        :type semilog: boolean
        :type show_test: boolean
        '''
        
        if isinstance(model, list):
            pass
        else:
            model = [model]
        if isinstance(columns_analysis, list):
            pass
        else:
            columns_analysis = [columns_analysis]
            
        for col in columns_analysis:
            
            dic_list = []
            for mod in model:
                print(mod)
                update = self.fit_time_series(columns_analysis=col, start_date=start_date
                                     , end_date=end_date, n_previsions=n_previsions,
                                    p0=p0, model=mod, plot=False, semilog=semilog, show_test=show_test)
                dic_list.extend(update[0])
            if plot:
                plt.figure(figsize=(16, 8))
                for dic in dic_list:
                    x_fit = dic['fit_prevs_range']
                    y_fit = dic['fit_prevs_values'] 
                    model_label = dic['model']
                    p_chi2 = dic['chi_2']['p_value']

                    label = dic['label'] 
                    x_val = dic['data_range_plot']
                    y_val = dic['data_values_plot'] 
                    dates_plot = dic['dates_plot'] 

                    plt.plot(x_fit, y_fit, label='{} Fit {} p_chi2 {:.2f}'\
                             .format(label, model_label, p_chi2))
                    if self.multiseries_on:
                        plt.scatter(x_val, y_val, label='{} Data'.format(label)) 
                if not(self.multiseries_on):       
                    plt.scatter(x_val, y_val, label='{} Data'.format(label))    
                    
                plt.xticks([d for d in range(len(dates_plot))],  dates_plot, rotation='vertical', fontsize = 14)
                plt.legend(loc='best',fontsize = 12)
                plt.title('{}'.format(label),fontsize = 16)
                plt.xlabel('Day', fontsize = 16)
                plt.ylabel('{}'.format(label), fontsize = 16)
                if len(x_val)< len(dates_plot):
                    plt.axvline(len(x_val)-1, alpha = 0.5,linewidth=3, ls = '--')
                if semilog:
                    plt.yscale('log')
                plt.show()

        return dic_list