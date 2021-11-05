import pandas as pd

fundraise = pd.read_csv("C:\\Data\\PreppinData\\Prep Generate Rows datasets - Charity Fundraiser.csv", 
                          parse_dates=['Date'],
                          date_parser=lambda x: pd.to_datetime(x, format='%d/%m/%Y'))
fundraise.index = pd.DatetimeIndex(fundraise['Date'])
fundraise = fundraise.reindex(pd.date_range(fundraise.index.min(), fundraise.index.max()),
                                  method='ffill').rename_axis('FillDate').reset_index()
fundraise = fundraise.sort_values('FillDate').rename_axis('Days into fund raising').reset_index()
fundraise['Value raised per day'] = fundraise.apply(lambda x: x['Total Raised to date']/x['Days into fund raising'] 
                                                        if x['Days into fund raising']>0 else None, axis=1)
fundraise['Date'] = fundraise['FillDate'].dt.strftime('%A')
fundraise['Average raised per weekday'] = fundraise['Value raised per day'].groupby(fundraise['Date']).transform('mean')
fundraise = fundraise[['Date', 'Total Raised to date', 'Days into fund raising',
                       'Value raised per day', 'Average raised per weekday']]
