import pandas


def get_filename_for_year(year, index="NYSE"):
    #if year in range(1981,1991):
    #    return "file://localhost/Users/amounir/Downloads/1981-1990.csv"
    #if year in range(1991,2001):
    #    return "file://localhost/Users/amounir/Downloads/1991-2000.csv"
    #if year in range(2001,2011):
    #    return "file://localhost/Users/amounir/Downloads/2001-2010.csv"
    #return "file://localhost/Users/amounir/Downloads/2011-2014.csv"
    if index == "NYSE":
        return "file://localhost/Users/amounir/Downloads/NYSE Returns.csv"
    return "file://localhost/Users/amounir/Downloads/NASDAQ Returns.csv"


class StockReturnsQuerier(object):
    def __init__(self):
        self.filenames_data = {}

    def _load_file_for_year(self, year):
        filename = get_filename_for_year(year)
        year_data = self.filenames_data.get(filename)
        if year_data is None:
            year_data = pandas.read_csv(
                filename, usecols=["GVKEY", "datadatefix", "trt1m"], na_values=["NaN", "nan"], keep_default_na=False,
                parse_dates=True, keep_date_col=True, index_col=['GVKEY','datadatefix'], low_memory = False)
            self.filenames_data[filename] = year_data
        return year_data

    def get_monthly_data_from_company_year(self, company, year):
        year_data = self._load_file_for_year(year)
        try:
            if year_data.ix[company].get(str(year)) is not None:
                return year_data.ix[company].get(str(year)).get_values().tolist()
        except KeyError:
            return []
        return []


if __name__ == '__main__':
    querier = StockReturnsQuerier()
    # print querier.get_monthly_data_from_company_year(, 1981)
