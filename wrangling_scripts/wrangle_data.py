import requests
import pandas as pd
import plotly.graph_objs as go


def new_case_calculator(data):
    if data["date"] < pd.to_datetime("26/11/2020"):
        val = data["patients"]
    else:
        val = data["cases"]
    return val

def get_data():
    payload = {'format': 'json'}
    data = requests.get('https://raw.githubusercontent.com/ozanerturk/covid19-turkey-api/master/dataset/timeline.json',params=payload)
    return data

def prepare_df():
    data = get_data()
    jsonfile = get_data()
    data_all = pd.DataFrame(jsonfile.json()).transpose()
    data_all.drop(columns=['totalIntubated', 'totalIntensiveCare',"critical","pneumoniaPercent"],axis=1,inplace=True)
    data_all["date"] = pd.to_datetime(data_all["date"], dayfirst=True)
    data_all['cases'] = data_all['cases'].fillna(0)
    data_all['patients'] = data_all['patients'].astype('int')
    data_all['totalPatients'] = data_all['totalPatients'].astype('int')
    data_all['deaths'] = data_all['deaths'].astype('int')
    data_all['totalDeaths'] = data_all['totalDeaths'].astype('int')
    data_all['recovered'] = data_all['recovered'].astype('int')
    data_all['totalRecovered'] = data_all['totalRecovered'].astype('int')
    data_all['tests'] = data_all['tests'].astype('int')
    data_all['totalTests'] = data_all['totalTests'].astype('int')
    data_all['cases'] = data_all['cases'].astype('int')
    data_all["new_cases"] = data_all.apply(new_case_calculator,axis=1)
    data_all['total_new_cases'] = data_all['new_cases'].cumsum()
    data_all['totalRecovered'] = data_all['recovered'].cumsum()
    data_all["daily_case_rate"] = data_all["new_cases"] / data_all["tests"]
    data_all["death_rate"] = data_all["totalDeaths"] / data_all["total_new_cases"]
    data_all["recovery_rate"] = data_all["totalRecovered"] / data_all["total_new_cases"]
    data_all["patient_rate"] = 1- data_all["recovery_rate"] - data_all["death_rate"]
    return data_all  

def return_figures():
    """Creates four plotly visualizations

    Args:
        None

    Returns:
        list (dict): list containing the four plotly visualizations

    """

# first chart plots arable land from 1990 to 2015 in top 10 economies 
# as a line chart
    data_all = prepare_df()
    graph_one = []
    y1 = data_all.new_cases.tolist()
    y_list = [y1]
    y_list_map = ["New Cases"]
    for y in y_list:
        x_val = data_all.date.tolist()
        y_val =  y
        graph_one.append(
          go.Scatter(
          x = x_val,
          y = y_val,
          mode = 'lines',
          name = y_list_map[y_list.index(y)],
           )
          )

    layout_one = dict(title = 'Covid-19 - Turkey / Daily Confirmed New Cases',
                xaxis = dict(title = 'Date',
                  autotick=False, tickmode = 'auto'),
                    rangeslider=dict(visible=False) )

# first chart plots arable land from 1990 to 2015 in top 10 economies 
# as a line chart
    
    graph_two = []
    y1 = data_all.deaths.tolist()
    y_list = [y1]
    y_list_map = ["Daily Deaths"]
    for y in y_list:
        x_val = data_all.date.tolist()
        y_val =  y
        graph_two.append(
          go.Scatter(
          x = x_val,
          y = y_val,
          mode = 'lines',
          name = y_list_map[y_list.index(y)],
           )
          )

    layout_two = dict(title = 'Covid-19 - Turkey / Daily Deaths',
                xaxis = dict(title = 'Date',
                  autotick=False, tickmode = 'auto'),
                      rangeslider=dict(visible=False))
# first chart plots arable land from 1990 to 2015 in top 10 economies 
# as a line chart
    
    graph_three = []
    y1 = data_all.tests.tolist()
    y_list = [y1]
    y_list_map = ["Daily Tests"]
    for y in y_list:
        x_val = data_all.date.tolist()
        y_val =  y
        graph_three.append(
          go.Scatter(
          x = x_val,
          y = y_val,
          mode = 'lines',
          name = y_list_map[y_list.index(y)],
           )
          )

    layout_three = dict(title = 'Covid-19 - Turkey / Daily Tests Completed',
                xaxis = dict(title = 'Date',
                  autotick=False, tickmode = 'auto'),
                      rangeslider=dict(visible=False))
# first chart plots arable land from 1990 to 2015 in top 10 economies 
# as a line chart
    
    graph_four = []
    y1 = data_all.daily_case_rate.tolist()
    y_list = [y1]
    y_list_map = ["Daily Positive Case Rate"]
    for y in y_list:
        x_val = data_all.date.tolist()
        y_val =  y
        graph_four.append(
          go.Scatter(
          x = x_val,
          y = y_val,
          mode = 'lines',
          name = y_list_map[y_list.index(y)],
           )
          )

    layout_four = dict(title = 'Covid-19 - Turkey / Daily Positive Rate in All Tests',
                xaxis = dict(title = 'Date',
                  autotick=False, tickmode = 'auto'),
                      rangeslider=dict(visible=False))
# first chart plots arable land from 1990 to 2015 in top 10 economies 
# as a line chart
    
    graph_five = []
    y1 = data_all.total_new_cases.tolist()
    y_list = [y1]
    y_list_map = ["Total Cases"]
    for y in y_list:
        x_val = data_all.date.tolist()
        y_val =  y
        graph_five.append(
          go.Scatter(
          x = x_val,
          y = y_val,
          mode = 'lines',
          name = y_list_map[y_list.index(y)],
           )
          )

    layout_five = dict(title = 'Covid-19 - Turkey / Total Cases',
                xaxis = dict(title = 'Date',
                  autotick=False, tickmode = 'auto'),
                      rangeslider=dict(visible=False))


# third chart plots percent of population that is rural from 1990 to 2015
    graph_six = []
    y1 = data_all.death_rate.tolist()
    y2 = data_all.recovery_rate.tolist()
    y3 = data_all.patient_rate.tolist()
    y_list = [y1,y2,y3]
    y_list_map = ["Death Rate","Recovery Rate","Receiving Treatment Rate"]
    for y in y_list:
        x_val = data_all.date.tolist()
        y_val =  y
        graph_six.append(
          go.Scatter(
          x = x_val,
          y = y_val,
          mode = 'lines',
          name = y_list_map[y_list.index(y)],
           )
          )

    layout_six = dict(title = 'Covid-19 - Turkey / Death, Recovery and Current Patient Rates in All Patients',
                xaxis = dict(title = 'Date',
                  autotick=False, tickmode = 'auto'),
                      rangeslider=dict(visible=False))

    
    # append all charts to the figures list
    figures = []
    figures.append(dict(data=graph_one, layout=layout_one))
    figures.append(dict(data=graph_two, layout=layout_two))
    figures.append(dict(data=graph_three, layout=layout_three))
    figures.append(dict(data=graph_four, layout=layout_four))
    figures.append(dict(data=graph_five, layout=layout_five))
    figures.append(dict(data=graph_six, layout=layout_six))

    return figures