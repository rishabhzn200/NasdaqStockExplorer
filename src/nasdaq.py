import calendar
import pandas
import yfinance as yf
from divident_calender import DividendCalender


def get_dividend_calender(year, month):
    """
    Returns a dataframe with dividend calendar data scraped from nasdaq.
    :param year: year
    :param month: month
    :return: dataframe with dividend data scraped from nasdaq.
    """
    # get number of days in month
    days_in_month = calendar.monthrange(year, month)[1]
    num_days_in_month = list(range(1, days_in_month + 1))

    div_calender = DividendCalender(year, month)
    data = list(map(lambda days: div_calender.calendar(days), num_days_in_month))
    concat_df = pandas.concat(data)
    drop_df = concat_df.dropna(how='any')

    # set the dataframe's row index to the company name
    resultant_df = drop_df.set_index('companyName')
    return resultant_df

class DefaultObj:
    @staticmethod
    def get_info():
        return {
            "currentPrice": 0.0,
            "recommendationKey": "NA"
        }

def get_yfinance_data(ticker):
    """
    Returns the data for a ticker symbol using yfinance.
    :param ticker: ticker symbol
    :return: ticket data
    """
    try:
        if yfd.get(ticker) is None:
            yfd[ticker] = yf.Ticker(ticker)
        return yfd[ticker]
    except:
        return DefaultObj()

def get_return(div_rate, curr_price):
    """
    Calculates the dividend return per 1000 usd. Not applicable for ETF's.
    :param div_rate: dividend rate
    :param curr_price: current stock price
    :return: dividend per 1000 usd.
    """
    if curr_price != 0.0:
        return div_rate * 1000 / curr_price
    return div_rate

if __name__ == "__main__":
    pandas.set_option('display.max_columns', None)
    pandas.set_option("display.max_rows", None)
    selected_attributes = ["symbol", "dividend_Ex_Date", "payment_Date", "dividend_Rate", "indicated_Annual_Dividend"]
    year = 2024
    month = 11

    yfd = dict()

    # Get dividend calendar
    final_df = get_dividend_calender(year, month)
    min_df = final_df[selected_attributes]
    min_df = min_df.reset_index()

    # Save dividend calendar
    min_df.to_csv(f"./stock_dividend_calendar_{year}_{month}.csv")

    # Add additional columns
    min_df['curr_price'] = min_df['symbol'].apply(lambda x: get_yfinance_data(x).get_info().get("currentPrice", 0))
    min_df['return'] = min_df.apply(lambda x: get_return(x.dividend_Rate, x.curr_price), axis=1)
    min_df['recommendation'] = min_df['symbol'].apply(
        lambda x: get_yfinance_data(x).get_info().get("recommendationKey", "NA"))
    min_df['etf'] = min_df['companyName'].apply(
        lambda x: 'ETF' if 'ETF' in x else None)

    # Save to file
    min_df.to_csv(f"./stock_data_{year}_{month}.csv")

    # Sort dataframe and save to file
    sorted_min_ddf = min_df.sort_values('dividend_Rate', ascending=False)
    sorted_min_ddf.to_csv(f"./stock_data_sorted_div_rate_{year}_{month}.csv")

    new_sorted_ddf = min_df.sort_values('curr_price', ascending=True)
    new_sorted_ddf.to_csv(f"./stock_data_sorted_curr_price_{year}_{month}.csv")

    new_sorted_ddf = min_df.sort_values('return', ascending=False)
    new_sorted_ddf.to_csv(f"./stock_data_sorted_return_{year}_{month}.csv")
