import math
import numpy

def calculate_yearly_returns(monthly_returns_for_stock):
    yearly_returns = 1
    for [monthly_return] in monthly_returns_for_stock:
        yearly_returns *= 1 + float(monthly_return) / 100.0
    return (yearly_returns - 1) * 100


def calculate_annualized_returns(total_return, years_count):
    return (math.pow(1 + total_return / 100.0, 1.0 / years_count) - 1) * 100.0


class Strategy(object):

    def __init__(self, all_data, years, querier, display_name, ascending=True):
        self.overall_strategy_return = 1
        self.overall_monthly_returns = []
        self.overall_annualized_returns = -1
        self.overall_standard_deviation = -1
        self.stock_year_picks = {}
        self.all_data = all_data
        self.years = years
        self.querier = querier
        self.display_name = display_name
        self.ascending = ascending

    def find_top_column_picks(self, column_name, number=20, asc=True):
        for year in self.years:
            self.stock_year_picks[year] = self.all_data[str(year - 1)].sort(
                column_name, ascending=self.ascending).get('gvkey').get_values()[0:number]
        return self

    def find_double_sort_picks(self, parameter_1, parameter_2, double_sort_candidate_number=100, number=20):
        for year in self.years:
            self.stock_year_picks[year] = self.all_data[str(year - 1)].sort(
                parameter_1)[0:double_sort_candidate_number].sort(
                parameter_2).get('gvkey').get_values()[0:number]
        return self

    def find_load_balance_picks(self, parameter_1, parameter_2, parameter_1_percentage=50, number=20):
        parameter_1_count = int(parameter_1_percentage * number / 100.0)
        for year in self.years:
            self.stock_year_picks[year] = numpy.append(self.all_data[str(year - 1)].sort(
                parameter_1).get(
                'gvkey').get_values()[0:parameter_1_count], self.all_data[str(year - 1)].sort(
                    parameter_2).get('gvkey').get_values()[0:(number-parameter_1_count)])
        return self

    def calculate_returns_for_strategy(self, year):
        monthly_returns = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        stocks = self.stock_year_picks[year]
        skipped = 0
        for stock in stocks:
            monthly_returns_for_stock = self.querier.get_monthly_data_from_company_year(stock, year)
            if len(monthly_returns_for_stock) != 12:
                skipped += 1
                continue
            for month in range(0, 12):
                monthly_returns[month] += float(monthly_returns_for_stock[month][0])
        overall_yearly_return = 1
        for month in range(0, 12):
            if (len(stocks) - skipped) == 0:
                continue
            monthly_returns[month] /= len(stocks) - skipped
            overall_yearly_return *= 1 + monthly_returns[month] / 100
        overall_yearly_return = (overall_yearly_return - 1) * 100
        return overall_yearly_return, monthly_returns

    def calculate_portfolio_returns(self):
        for year in self.years:
            overall_return, monthly_returns = self.calculate_returns_for_strategy(year)
            self.overall_monthly_returns += monthly_returns
            self.overall_strategy_return *= 1 + overall_return / 100
        self.overall_strategy_return = (self.overall_strategy_return - 1) * 100
        self.overall_annualized_returns = calculate_annualized_returns(
            self.overall_strategy_return, len(self.years))
        self.overall_standard_deviation = numpy.std(self.overall_monthly_returns) * math.sqrt(12)
