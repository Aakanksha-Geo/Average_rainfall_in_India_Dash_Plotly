from dash import Dash, dcc, Output, Input  # pip install dash
import dash_bootstrap_components as dbc    # pip install dash-bootstrap-components
import plotly.express as px
import pandas as pd                        # pip install pandas
import geopandas as gpd


df = pd.read_csv("rainfall.csv")
print(df.head())

gdf = gpd.read_file('Indian_States.txt')
gdf["geometry"] = gdf.to_crs(gdf.estimate_utm_crs()).simplify(1000).to_crs(gdf.crs)
india_states = gdf.rename(columns={"NAME_1": "ST_NM"}).__geo_interface__

# Build your components
app = Dash(__name__, external_stylesheets=[dbc.themes.LUX])
mytitle = dcc.Markdown(children='')
mygraph = dcc.Graph(figure={})
dropdown = dcc.Dropdown(options=df.columns.values[1:],
                        value='Rainfall(mm)',  # initial value displayed when page first loads
                        clearable=False)

# Customize your own Layout
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([mytitle], width=6)
    ], justify='center'),
    dbc.Row([
        dbc.Col([mygraph], width=12)
    ]),
    dbc.Row([
        dbc.Col([dropdown], width=6)
    ], justify='center'),

], fluid=True)

# Callback allows components to interact
@app.callback(
    Output(mygraph, 'figure'),
    Output(mytitle, 'children'),
    Input(dropdown, 'value')
)
def update_graph(column_name):  # function arguments come from the component property of the Input

    print(column_name)
    print(type(column_name))
    fig = px.choropleth(
        pd.json_normalize(india_states["features"])["properties.ST_NM"],
        locations="properties.ST_NM",
        geojson=india_states,
        featureidkey="properties.ST_NM",
        color_discrete_sequence=["lightgrey"],
        )

    fig.add_traces(
        px.choropleth(
            df,
            locations="State",
            geojson=india_states,
            featureidkey="properties.ST_NM",
            locationmode="geojson-id",
            color="Rainfall(mm)",
            scope="asia",
        ).data
    )
    fig.update_geos(fitbounds="locations", visible=False)
   
             
   
    return fig, '# '+column_name  # returned objects are assigned to the component property of the Output


# Run app
if __name__=='__main__':
    app.run_server(debug=True, port=8054)
