import xlsxwriter


class ExcelStrategyHandler(object):

    @staticmethod
    def display_overall_strategy(overall_strategy_worksheet, strategy):
        overall_strategy_worksheet.write('A1', 'Month')
        overall_strategy_worksheet.write('B1', 'Monthly Returns')
        monthly_return_index = 1
        month = 1
        year = strategy.years[0]
        for monthly_return in strategy.overall_monthly_returns:
            month_year = str(month) + "/" + str(year)
            overall_strategy_worksheet.write(monthly_return_index, 0, month_year)
            overall_strategy_worksheet.write(monthly_return_index, 1, monthly_return)
            monthly_return_index += 1
            month += 1
            if month > 12:
                month = 1
                year += 1
        overall_strategy_worksheet.write('C1', 'Overall Strategy Return')
        overall_strategy_worksheet.write('C2', strategy.overall_strategy_return)
        overall_strategy_worksheet.write('D1', 'Overall Annualized Return')
        overall_strategy_worksheet.write('D2', strategy.overall_annualized_returns)
        overall_strategy_worksheet.write('E1', 'Overall Standard Deviation')
        overall_strategy_worksheet.write('E2', strategy.overall_standard_deviation)

    @staticmethod
    def display_year(year_strategy_worksheet, strategy, year):
        year_strategy_worksheet.write('A1', 'Selected Stocks')
        stock_picks = strategy.stock_year_picks[year]
        stock_pick_index = 1
        for pick in stock_picks:
            year_strategy_worksheet.write(stock_pick_index, 0, str(pick))
            stock_pick_index += 1
        year_return, monthly_returns = strategy.calculate_returns_for_strategy(year)
        year_strategy_worksheet.write('B1', 'Month')
        year_strategy_worksheet.write('C1', 'Monthly Returns')
        monthly_return_index = 1
        for monthly_return in monthly_returns:
            year_strategy_worksheet.write(monthly_return_index, 1, str(monthly_return_index))
            year_strategy_worksheet.write(monthly_return_index, 2, monthly_return)
            monthly_return_index += 1
        year_strategy_worksheet.write('D1', 'Overall Year Return')
        year_strategy_worksheet.write('D2', year_return)

    @staticmethod
    def write_strategy_to_file(strategy, file_path):
        workbook = xlsxwriter.Workbook(file_path)
        overall_strategy_worksheet = workbook.add_worksheet("Overall")
        ExcelStrategyHandler.display_overall_strategy(overall_strategy_worksheet, strategy)
        for year in strategy.years:
            year_strategy_worksheet = workbook.add_worksheet(str(year))
            ExcelStrategyHandler.display_year(year_strategy_worksheet, strategy, year)
        workbook.close()
