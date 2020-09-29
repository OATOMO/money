# -*- coding: utf-8 -*-#
# -------------------------------------------------------------------------------
# Name:         main_ui
# Description:  
# Date:         2020/9/29
# -----------------------------------------------------------------------------
"""
        baostock证券数据可视化交互
"""
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as dhc
from dash.dependencies import Input, Output
import plotly.express as px
import comm
import my_sql

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


@app.callback(
    dash.dependencies.Output('code_kline', 'figure'),
    [dash.dependencies.Input('select_code', 'value'),
     dash.dependencies.Input('select_valid_date', 'value')])
def code_d_kline(code, date):
    if code is None:
        return px.scatter()
    data = my_sql.sql_code_kline(conn, code)
    print(code)
    fig = px.line(data_frame=data, x='date', y='close')
    return fig


if __name__ == "__main__":
    conn = comm.initPgDB(comm.pgDB, comm.pgUSER, comm.pgPW, comm.pgHost, comm.pgPort)
    cur = conn.cursor()
    cur.execute("SET TIME ZONE 'Asia/Chongqing';")
    conn.commit()
    codes_options = my_sql.sql_select_all_code(conn)
    valid_date = my_sql.sql_kline_valid_date(conn)

    app.layout = dhc.Div(children=[
        dhc.Label('select_code'),
        dhc.Div(
            children=[dcc.Dropdown(id='select_code', options=codes_options)]
        ),
        dhc.Div([
            dcc.Graph(id='code_kline'),
            dcc.RangeSlider(
                id='select_valid_date',
                min=int(valid_date[0]),
                max=int(valid_date[-1]),
                value=[int(valid_date[0]), int(valid_date[-1])],
                marks={str(year): str(year) for year in valid_date},
                step=None
            )
        ], style={'display': 'inline-block', 'width': '49%'})
    ])
    app.run_server(debug=True)


