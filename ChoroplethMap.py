import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output
import numpy as np

external_stylesheets=['https://codepen.io/amyoshino/pen/jzXypZ.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = 'Choropleth Map'

path_to_file = "AllEffect_map.csv"
df = pd.read_csv(path_to_file)
available_industries = df['sector'].unique()
# available_industries = np.append("All industries", available_industries)
available_states = df['state'].unique()
state_df = df[df.state != "United States"]
state_df.insert(9,'yvar',0)
state_df.insert(10,'hoverdata',0)
sector_df = df[df.sector != "All industries"]


def generate_choropleth(chosen_sector):
    state_dff = state_df[state_df.sector == chosen_sector]
    return{
        'data': [
            dict(
                type='choropleth',
                colorbar=dict(
                    tickvals=[1,2,3,4,5,6],
                    ticktext=["<0.5","0.5-1.5","1.5-3","3-5","5-10",">10"],
                    tickfont=dict(family='Times New Roman', size=12, color="#515151"),
                    tickmode="array",
                    ticks="",
                    thickness=5,
                    len=0.5,
                    lenmode="fraction",
                    title=dict(text="contribution scale (%)",
                               font=dict(family='Times New Roman', size=12, color="#515151"),
                               side="top"),
                ),
                margin=dict(l=0, r=0, b=100, t=100, pad=5),
                colorscale='Reds',
                autocolorscale=False,
                locations=state_dff['statecode'],
                locationmode='USA-states',
                z=state_dff['yvar'].astype(float),
                meta=state_dff['hoverdata'],
                hovertemplate="Contribution:%{meta[1]:.2f}%  <extra>State:%{location}</extra>",
                hoverlabel=dict(bgcolor='D68C24',font=dict(family='Times New Roman', color='white')),
                marker=dict(line=dict(width=1, color='rgb(255, 255, 255)'))
            )
        ],
        'layout':
        dict(
            title=dict(
                text='Regional Contribution to Employment Effects <br> <b>{}</b>'.format(chosen_sector),
                font=dict(family="Open Sans, sans-serif", size=14, color="#515151"),
            ),
            margin=dict(l=0, r=0, b=50, t=100, pad=5),
            geo=dict(
                scope='usa',
                projection=dict(type='albers usa'),
                showlakes=True,  # lakes
                lakecolor='rgb(255, 255, 255)')
        ),
    }


def generate_leftbar(chosen_state, chosen_sector):

    onestate_df = sector_df[sector_df.state == chosen_state]

    onestate_df = onestate_df.sort_values(by=['secnum'], ascending=False)
    if chosen_sector == "Manufacturing":
        onestate_df = onestate_df[(onestate_df.secnum < 14) & (onestate_df.secnum > 1)]
    else:
        onestate_df = onestate_df[onestate_df.secnum >= 14]

    data = [
        go.Bar(
            y=onestate_df['sector'],
            x=onestate_df['welfare_effect'],
            marker=dict(line=dict(width=1, color=onestate_df['welfare_effect']), color=onestate_df['welfare_effect']),
            hovertemplate="Changes:%{x:.4f}%  <extra></extra>",
            orientation='h'

        )
    ]

    layout = go.Layout(
        title=dict(
            text='Change in Welfare by Industries <br> <b>{}</b>'.format(chosen_state),
            font=dict(family="Open Sans, sans-serif", size=14, color="#515151"),
        ),

            # legend=go.layout.Legend(
        #     x=0,
        #     y=1.0
        # ),
        xaxis=dict(
            showgrid=False,
            showline=False,
            showticklabels=False,
            zeroline=False,
        ),
        yaxis=dict(
            showgrid=False,
            showline=False,
            showticklabels=True,
            zeroline=False,
        ),
        paper_bgcolor='rgb(255, 255, 255)',
        plot_bgcolor='rgb(255, 255, 255)',
        margin=dict(l=150, r=0, t=100, b=100),
        showlegend=False,
    )
    return {"data": data, "layout": layout}


def generate_midbar(chosen_state, chosen_sector):

    onestate_df = sector_df[sector_df.state == chosen_state]

    onestate_df = onestate_df.sort_values(by=['secnum'], ascending=False)

    if chosen_sector=="Manufacturing":
        onestate_df=onestate_df[(onestate_df.secnum < 14) & (onestate_df.secnum > 1)]
    else:
        onestate_df = onestate_df[onestate_df.secnum >= 14]

    data = [
        go.Bar(
            y=onestate_df['sector'],
            x=onestate_df['emp_effect'],
            marker=dict(line=dict(width=1, color=onestate_df['emp_effect']), color=onestate_df['emp_effect']),
            hovertemplate="Changes:%{x:.4f}%  <extra></extra>",
            orientation='h'

        )
    ]

    layout = go.Layout(
        title=dict(
            text='Change in Employment Shares by Industries <br> <b>{}</b>'.format(chosen_state),
            font=dict(family="Open Sans, sans-serif", size=14, color="#515151"),
        ),

            # legend=go.layout.Legend(
        #     x=0,
        #     y=1.0
        # ),
        xaxis=dict(
            showgrid=False,
            showline=False,
            showticklabels=False,
            zeroline=False,
        ),
        yaxis=dict(
            showgrid=False,
            showline=False,
            showticklabels=True,
            zeroline=False,
        ),
        paper_bgcolor='rgb(255, 255, 255)',
        plot_bgcolor='rgb(255, 255, 255)',
        margin=dict(l=150, r=0, t=100, b=100),
        showlegend=False,
    )
    return {"data": data, "layout": layout}


def generate_rightbar(chosen_state, chosen_sector):
    if chosen_sector==1:
        figure3_title=dict(text=" ")

    else:
        figure3_title = dict(
            text='Labor Market Contribution <br> <b>{}</b>'.format(chosen_state),
            font=dict(family="Open Sans, sans-serif", size=14, color="#515151"))

    onestate_df = sector_df[sector_df.state == chosen_state]
    onestate_df = onestate_df.sort_values(by=['secnum'], ascending=False)

    if chosen_sector=="Manufacturing":
        onestate_df=onestate_df[(onestate_df.secnum < 14) & (onestate_df.secnum > 1)]
    else:
        onestate_df = onestate_df[onestate_df.secnum >= 14]

    data = [
        go.Bar(
            y=onestate_df['sector'],
            x=onestate_df['emp_seccontri'],
            marker=dict(line=dict(width=1, color=onestate_df['welfare_effect']), color=onestate_df['welfare_effect']),
            hovertemplate="Changes:%{x:.4f}%  <extra></extra>",
            orientation='h'
        )
    ]

    layout = go.Layout(
        title=figure3_title,
        xaxis=dict(
            showgrid=False,
            showline=False,
            showticklabels=False,
            zeroline=False,
        ),
        yaxis=dict(
            showgrid=False,
            showline=False,
            showticklabels=False,
            zeroline=False,
        ),
        paper_bgcolor='rgb(255, 255, 255)',
        plot_bgcolor='rgb(255, 255, 255)',
        margin=dict(l=150, r=0, t=100, b=100),
        showlegend=False,
    )
    return {"data": data, "layout": layout}


app.layout = html.Div(
    html.Div([


        html.Div(
            [
                html.Div(
                    [
                        html.P('Choose regions:'),
                        dcc.Dropdown(
                            id='Dropdown',
                            options=[{'label': i, 'value': i} for i in available_states],
                            value='United States',
                            multi=False
                        ),
                    ],
                    className='six columns',
                    style={'margin-top': '10'}
                ),
                html.Div(
                    [
                        html.P('Choose sectors:'),
                        dcc.RadioItems(
                            id='RadioItems',
                            options=[{'label': k, 'value': k} for k in ['Manufacturing', 'Non-manufacturing']],
                            value='Manufacturing',
                            labelStyle={'display': 'inline-block'}
                        ),
                    ],
                    className='six columns',
                    style={'margin-top': '10'}
                )
            ], className="row"
        ),

        html.Div([
            html.Div(children='**Mouse over bar area to get contribution in chosen industry',
                     className="twelve columns",
                     style={'color': 'blue', 'fontSize': 10}),
            html.Div(children='**Mouse over blank area to return to sector-aggregated contribution ',
                     className="twelve columns",
                     style={'color': 'blue', 'fontSize': 10}),
            # html.Img(
            #     src="http://test.fulcrumanalytics.com/wp-content/uploads/2015/10/Fulcrum-logo_840X144.png",
            #     className='three columns',
            #     style={
            #         'height': '14%',
            #         'width': '14%',
            #         'float': 'right',
            #         'position': 'relative',
            #         'margin-top': 20,
            #         'margin-right': 20
            #     },
            # ),

        ], className="row"),

        html.Div([
            html.Div([
                dcc.Graph(
                    id="figure1",
                    style={"height": "100vh"},
                    clear_on_unhover=True
                )
            ], className='six columns'),

            html.Div([
                dcc.Graph(
                    id="figure2",
                    style={"height": "100vh"},
                    clear_on_unhover=True

                )
            ], className='six columns'),



        ], className="row"),


    ], className='ten columns offset-by-one')
)


@app.callback(
    Output('figure1', 'figure'),
    [Input('Dropdown', 'value'),
     Input('RadioItems', 'value'),
     Input('figure2', 'hoverData')]
)
def update_figure1(dd_select, radio_select, clickdata):
    if dd_select == "United States":
        if radio_select == "Manufacturing":
            if clickdata is not None:
                state_df.yvar = state_df.emp_regcontri_scale
                state_df.hoverdata = state_df.emp_regcontri
                chosen_sector = clickdata['points'][0]['y']
                return generate_choropleth(chosen_sector)

            else:
                state_df.yvar = state_df.emp_regcontri_manuf_scale
                state_df.hoverdata = state_df.emp_regcontri_manuf
                chosen_sector = "All industries"
                return generate_choropleth(chosen_sector)

        elif radio_select == "Non-manufacturing":
            if clickdata is not None:
                state_df.yvar = state_df.emp_regcontri_scale
                state_df.hoverdata = state_df.emp_regcontri
                chosen_sector = clickdata['points'][0]['y']
                return generate_choropleth(chosen_sector)

            else:
                state_df.yvar = state_df.emp_regcontri_nonmanuf_scale
                state_df.hoverdata = state_df.emp_regcontri_nonmanuf
                chosen_sector = "All industries"
                return generate_choropleth(chosen_sector)

    elif dd_select != "United States":
        chosen_state = dd_select
        chosen_sector = radio_select

        return generate_leftbar(chosen_state, chosen_sector)



@app.callback(
    Output('figure2', 'figure'),
    [Input('Dropdown', 'value'),
     Input('RadioItems', 'value')]
)
def update_figure2(dd_select, radio_select):
    chosen_state = dd_select
    chosen_sector = radio_select

    return generate_midbar(chosen_state, chosen_sector)

#
# @app.callback(
#     Output('figure3', 'figure'),
#     [Input('Dropdown', 'value'),
#      Input('RadioItems', 'value')]
# )
# def update_figure3(dd_select,radio_select):
#     if dd_select == "United States":
#         chosen_state=1
#         chosen_sector=1
#         return generate_rightbar(chosen_state, chosen_sector)
#
#     else:
#         chosen_state = dd_select
#         chosen_sector = radio_select
#
#         return generate_rightbar(chosen_state, chosen_sector)



if __name__ == '__main__':
    app.run_server(debug=True)
