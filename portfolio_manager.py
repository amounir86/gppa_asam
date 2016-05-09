import excel_handler

import matplotlib.pyplot as plt
import matplotlib
import numpy
import math
import pandas
import strategy_calculator
import stock_returns_querier


GROSS_PROFITABILITY_FILE_PATH = ('file://localhost/Users/amounir/Downloads/'
                                 'NYSE NASDAQ Data.xlsx')
SNP_FILE_PATH = ('file://localhost/Users/amounir/Downloads/'
                 'S&P500.csv')
ALL_DATA_RANGES = range(1980, 2015)


def calculate_snp_returns(years):
    snp_data = pandas.read_csv(
        SNP_FILE_PATH, usecols=['fxddt', 'vwretd', 'ewretd'], na_values=['NaN', 'nan'], keep_default_na=False,
        parse_dates=True, keep_date_col=True, index_col=['fxddt'], low_memory = False)
    equal_weighted_snp_returns = []
    value_weighted_snp_returns = []
    overall_equal_weighted_snp_returns = 1
    overall_value_weighted_snp_returns = 1
    for year in years:
        months_equal = snp_data[str(year)].get('ewretd')
        months_value = snp_data[str(year)].get('vwretd')
        for month in months_equal:
            equal_weighted_snp_returns += [float(month) * 100.0]
            overall_equal_weighted_snp_returns *= (1 + float(month))
        for month in months_value:
            value_weighted_snp_returns += [float(month) * 100.0]
            overall_value_weighted_snp_returns *= (1 + float(month))
    return (equal_weighted_snp_returns,
            value_weighted_snp_returns,
            (overall_equal_weighted_snp_returns - 1) * 100,
            (overall_value_weighted_snp_returns - 1) * 100)


def calculate_annualized_returns(total_return, years_count):
    return (math.pow(1 + total_return / 100.0, 1.0 / years_count) - 1) * 100.0


def display_strategies(years, strategies):
    for strategy in strategies:
        excel_handler.ExcelStrategyHandler.write_strategy_to_file(
            strategy,
            strategy.display_name + '-years-' + str(years[0]) + '-' + str(years[len(years) - 1]) + '.xlsx')

    plottable_data = list()
    plottable_data.append([1 for _ in range(0, len(strategies))])
    for e in range(0, len(strategies[0].overall_monthly_returns)):
        data_elements = []
        for s in range(0, len(strategies)):
            data_elements.append(plottable_data[e][s] * (1 + strategies[s].overall_monthly_returns[e] / 100))
        plottable_data.append(data_elements)
    returns_dataframe = pandas.DataFrame(
        plottable_data, index=pandas.date_range('31/1/' + str(years[0]), periods=len(plottable_data), freq='M'),
        columns=[strategy.display_name for strategy in strategies])
    plt.figure()
    returns_dataframe.plot()
    plt.savefig('returns-' + str(years[0]) + '-' + str(years[len(years) - 1]) + '.png')


class StrategiesManager(object):
    def __init__(self):
        self.querier = stock_returns_querier.StockReturnsQuerier()
        self.all_data = pandas.read_excel(
            GROSS_PROFITABILITY_FILE_PATH, [str(year) for year in ALL_DATA_RANGES],
            usecols=["gvkey",
                     "GPPA Ranking",
                     #"GPBM Rankings",
                     #"3-avg rankings",
                     "PA Ranking",
                     "GP Ranking",
                     #"B-T-M Ranking"
                     ],
            na_values=["NaN", "nan"], keep_default_na=False)

    def calculate_strategies_returns(self, years):
        strategies = [
            strategy_calculator.Strategy(
                self.all_data, years, self.querier, 'GPPA', ascending=False).find_top_column_picks('GPPA Ranking'),
            strategy_calculator.Strategy(
                self.all_data, years, self.querier, 'GP', ascending=False).find_top_column_picks('GP Ranking'),
            strategy_calculator.Strategy(
                self.all_data, years, self.querier, 'PA', ascending=False).find_top_column_picks('PA Ranking'),
            #strategy_calculator.Strategy(
            #    self.all_data, years, self.querier, 'GPBM', ascending=False).find_top_column_picks('GPBM Rankings'),
        ]
        for strategy in strategies:
            strategy.calculate_portfolio_returns()
        display_strategies(years, strategies)


if __name__ == '__main__':
    strategy_manager = StrategiesManager()
    strategy_manager.calculate_strategies_returns(range(1981, 2016))
    #strategy_manager.calculate_strategies_returns(range(1981, 1991))
    #strategy_manager.calculate_strategies_returns(range(1991, 2001))
    #strategy_manager.calculate_strategies_returns(range(2001, 2011))
    #strategy_manager.calculate_strategies_returns(range(2011, 2015))
    strategy_manager.calculate_strategies_returns(range(2004, 2016))
