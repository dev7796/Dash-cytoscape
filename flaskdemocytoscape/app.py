import dash
import dash_cytoscape as cyto
import dash_html_components as html
import pandas as pd
import dash  # pip install dash
import dash_cytoscape as cyto  # pip install dash-cytoscape==0.2.0 or higher
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Output, Input, State
import pandas as pd  # pip install pandas
import plotly.express as px
from simple_colors import *
import math
from demos import dash_reusable_components as drc
from flask import render_template



external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__,external_stylesheets=external_stylesheets)
#Load extra layouts
#cyto.load_extra_layouts()
h=100
w=20

global node_only1
node_only1=['abcd']
d={}
d1={}
d2={}
d3={}
d01={}
d11={}
d21={}
d31={}
a=[]
a1=[]
a2=[]
a3=[]
a4=[]
a5=[]
a01=[]
a11=[]
a21=[]
a31=[]
F=[]
F1=[]
rows1 = []
rows_list1=[]
rows_dict1={}
df = pd.read_csv("test_Data.csv")
df_link = pd.read_csv("df_links.csv")
df_size= pd.read_csv("test_Data_Size.csv")
df_color_target = pd.read_csv("test_Data_color.csv")
df_size_index = df_size.set_index('Name').to_dict()
df_color_target_index = df_color_target.set_index('Name').to_dict()


df_name_index=df.set_index('Name').to_dict()
print("this is name index",df_name_index)
df_copy = {**df_name_index}
for k,v in df_copy.items():
    for i in list(v):
            if v[i] == 0:
                v.pop(i)
for i in df_copy.keys():
    a4.append(i)
print(a4)
df_copy = {**df_name_index}

# print result
for k,v in df_copy.items():
    for i in list(v):
            if v[i] == 0:
                v.pop(i)

print("this is 1",df_copy.keys())

for k1, s in df_copy.items():
    for k2,v in s.items():
        d['data']={k1:k2}

        a.append(d.copy())

print("this is a",a)
rows = []
rows_list=[]
rows_dict={}
# appending rows
for data in a:
    data_row = data['data']
    for k,v in data_row.items():
        rows.append(k)
        rows_list.append(v)

for k1, s in df_copy.items():
    for k2,v in s.items():
        d1['data']={'id':k1,'label':k1}
        a1.append(d1.copy())

for k1, s in df_copy.items():
    for k2,v in s.items():
        d3['data']={'id':k2,'label':k2}
        a3.append(d3.copy())

for k1, s in df_copy.items():
    # for each key and value in the sub-dict
    for k2,v in s.items():
        d2['data']={'source':k1,'target':k2}
        a2.append(d2.copy())



print("this is a",a)
print("this is a1",a1)
print("this is a2",a2)
print("this is a3",a1+a3)
print("this is rows",rows)
print("this is a4",a4)
elements = a1 + a3 + a2

default_stylesheet = [
    {
        "selector": "node",
        "style": {
            "width": "mapData(size, 0, 5, 20, 60)",
            "height": "mapData(size, 0, 5, 20, 60)",
            "content": "data(label)",
            "background-color": "mapData(weight, -1, 0, darkblue, white)"

        }
    },
    {
            'selector': '.red',
            'style': {
                'background-color': 'red',
                'line-color': 'red',
                'weight': 50
            }
        },
        {
            'selector': '.rectangle',
            'style': {
                'shape': 'diamond',
                'width':  50,
                'height': 50
            }
        },
        {
            'selector': '.yellow',
            'style': {
                'background-color': 'grey',
                'line-color': 'black',
                'weight': 50
            }
        },

]

styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}
app.layout = html.Div([html.Div([
        drc.NamedDropdown(
            name='NODE LAYOUT',
            id='dpdn',
            value='circle',
            clearable=False,
            options=[
                {'label': name.capitalize(), 'value': name}
                for name in ['breadthfirst', 'grid', 'random', 'circle', 'cose', 'concentric']
            ]
        ),
        # drc.NamedDropdown1(
        #     name='DROPDOWN + CHECKBOX',
        #     id='dpdndropdown',
        #     value='',
        #     options=[
        #         {'label': name.capitalize(), 'value': name}
        #         for name in a4
        #     ]
        #     ,multi=True
        # ),
        dcc.Checklist(
            id='checklist',
            value=['none']),
        html.Div(
        html.P("SEARCH GENE NAME:")),
        dcc.Textarea(
            id='textarea-state-example',
            value='',
            style={'width': '50%', 'height': 50},
        ),

        html.Div(),
        html.Button('Submit', id='textarea-state-example-button', n_clicks=0),
        html.Button('Clear', id='textarea-clear-example-button', n_clicks=0),
        html.Hr(),
        dcc.Checklist(
            #name='SOURCE NODE SELECTOR',
            id='dpdntargets',
            value=['none'],
            #clearable=False,
            # options=[
            #     {'label': name.capitalize(), 'value': name}
            #     for name in a4
            # ]
            #,multi=True
        ),
        html.Hr(),
        html.Div(),
    drc.NamedDropdown(
        name='SOURCE NODE SHAPE',
        id='dropdown-node-shape',
        value='diamond',
        clearable=False,
        options=drc.DropdownOptionsList(
            'ellipse',
            'triangle',
            'rectangle',
            'diamond',
            'pentagon',
            'hexagon',
            'heptagon',
            'octagon',
            'star',
            'polygon',
        )
        ),
        drc.NamedInput(
                    name='FOLLOWING COLOR',
                    id='input-following-color',
                    type='text',
                    value='red',
                    ),
        drc.NamedInput(
                    name='FOLLOWER COLOR',
                    id='input-follower-color',
                    type='text',
                    value='orange',
                    )
],className='six columns'),

        html.Div([
        cyto.Cytoscape(
            id='org-chart',
            autoungrabify=False,
            minZoom=0.2,
            maxZoom=1,
            layout={'name': 'random'},
            style={'width': '100%', 'height': '430px'},
            elements= elements,stylesheet=default_stylesheet

        )
        ],className='six columns'),

    #html.Hr(),
    html.Div([html.Hr(),
    html.Div(id='cytoscape-tapNodeData-output'),
    html.Hr(),
    html.Div(id='cytoscape-tapEdgeData-output')],className='twelve columns')

    #html.Hr(),
    #html.Div([html.Div(id='cytoscape-tapEdgeData-output')], className='five columns'),
    #html.Hr(),
    # html.Div([
    #     html.Div(id='empty-div', children='')
    # ], className='three column'),



], className='row')
reset_count_UPPER=[]
#html.Pre(id='cytoscape-tapNodeData-json', style=styles['pre']),
@app.callback(Output('org-chart', 'elements'),
              Input('dpdntargets','value'),
              Input('textarea-clear-example-button','n_clicks'))

def update_targets(value,n_clicks):

    global elements1
    print("Hello:",len(value))
    print("value:",value)
    a01.clear()
    a11.clear()
    a21.clear()
    a31.clear()
    d01.clear()
    d11.clear()
    d21.clear()
    d31.clear()
    for i in range(len(value)):
        print(i)
        element_value=str(value[i])
        print("hihihhi",element_value)
        element_value1=str(element_value)
        res = {key: df_name_index[key] for key in df_name_index.keys()
           & {element_value1}}

    # print result
        print("The filtered dictionary is : " + str(res))
        df_copy1 = {**res}
        print("this is df_copy1ihihihi",df_copy1)

        for k1, s in df_copy1.items():
            for k2, v in s.items():
                d01['data'] = {k1: k2}
                a01.append(d01.copy())
        print("this is a0", a01)
        # first_value=[]
        # first_value.append(len(value))
        # print("this is first_value",first_value)
        # if first_value[-1]<first_value[-2]:
        #     print(first_value)
        #     print("ijijijijijijijijijijijijij")

        rows1 = []
        rows_list1 = []
        rows_dict1 = {}
        # appending rows
        for data in a01:
            data_row = data['data']
            for k, v in data_row.items():
                rows1.append(k)
                rows_list1.append(v)

        for k1, s in df_copy1.items():
            # for each key and value in the sub-dict
            for k2, v in s.items():
                d11['data'] = {'id': k1, 'label': k1, 'size': 3.8}
                d11['classes'] = 'yellow rectangle'
                a11.append(d11.copy())
        for k1, s in df_copy1.items():
            # for each key and value in the sub-dict
            for k2, v in s.items():
                for k3, v1 in df_size_index['Size'].items():
                    for k4, v2 in df_color_target_index['Color'].items():
                        if k3 == k2 and k4 == k2:
                            d31['data'] = {'id': k2, 'label': k2, 'size': v1, 'weight':v2}
                            a31.append(d31.copy())
                # d31['data'] = {'id': k2, 'label': k2}
                # a31.append(d31.copy())
        for k1, s in df_copy1.items():
            # for each key and value in the sub-dict
            for k2, v in s.items():
                d21['data'] = {'source': k1, 'target': k2}
                a21.append(d21.copy())

        print("this is hihihih a01", a01)
        print("this is hoihiiih a11", a11)
        print("this is hihihihi a21", a21)

        rows_dict1 = {'Source': rows, 'Target': rows_list}
        print(rows_dict1)
        # using data frame
        df1 = pd.DataFrame(rows_dict1)
        print("this is df", df1)
        pd_final_df1 = pd.DataFrame(a01)
        pd_final_T1 = pd_final_df1.T
        pd_data1 = pd_final_T1.to_dict()
        df_final1 = pd.DataFrame(pd_data1)
        elements1 = a11+a31+a21

    if len(reset_count_UPPER)==0:
        reset_count_UPPER.append(0)
        print("this is reset count upaR",reset_count_UPPER)
    reset_count_UPPER.append(n_clicks)
    print("this is reset count upar", reset_count_UPPER)
    if reset_count_UPPER[-1] == reset_count_UPPER[-2]:
        print("hihihihi")
        return elements1
    else:
        print("hihihih N9ICHEW")
        return []



@app.callback(Output('org-chart', 'layout'),
              Input('dpdn', 'value'))
def update_layout(layout_value):
    if layout_value == 'breadthfirst':
        return {
            'name': layout_value,
            'roots': '[id = "Executive Director (Harriet)"]',
            'animate': True
        }
    else:
        return {
            'name': layout_value,
            'animate': True
        }


# @app.callback(
#     Output('empty-div', 'chi@app.callback(
# #     Output('empty-div', 'children'),
# #     Input('org-chart', 'mouseoverNodeData'),
# #     Input('org-chart', 'mouseoverEdgeData'),
# #     Input('org-chart', 'tapEdgeData'),
# #     Input('org-chart', 'tapNodeData'),
# #     Input('org-chart', 'selectedNodeData')
# # )
# # def update_layout(mouse_on_node, mouse_on_edge, tap_edge, tap_node, snd):
# #     print("Mouse on Node: {}".format(mouse_on_node))
# #     print("Mouse on Edge: {}".format(mouse_on_edge))
# #     print("Tapped Edge: {}".format(tap_edge))
# #     print("Tapped Node: {}".format(tap_node))
# #     print("------------------------------------------------------------")
# #     print("All selected Nodes: {}".format(snd))
# #     print("------------------------------------------------------------")
# #
# #     return ' 'ldren'),
#     Input('org-chart', 'mouseoverNodeData'),
#     Input('org-chart', 'mouseoverEdgeData'),
#     Input('org-chart', 'tapEdgeData'),
#     Input('org-chart', 'tapNodeData'),
#     Input('org-chart', 'selectedNodeData')
# )
# def update_layout(mouse_on_node, mouse_on_edge, tap_edge, tap_node, snd):
#     print("Mouse on Node: {}".format(mouse_on_node))
#     print("Mouse on Edge: {}".format(mouse_on_edge))
#     print("Tapped Edge: {}".format(tap_edge))
#     print("Tapped Node: {}".format(tap_node))
#     print("------------------------------------------------------------")
#     print("All selected Nodes: {}".format(snd))
#     print("------------------------------------------------------------")
#
#     return ' '

# @app.callback(Output('cytoscape-tapNodeData-json', 'children'),
#               Input('org-chart', 'mouseoverEdgeData'))
# def displayTapNodeData(data):
#     return json.dumps(data, indent=2)
#mouseoverEdgeData
# reset_count=[]
# @app.callback(Output('dpdntargets', 'options'),
#                 Input('textarea-state-example-button', 'n_clicks'),
#                 Input('textarea-clear-example-button','n_clicks'),
#                 State('textarea-state-example', 'value'))
#
# def update_output(n_clicks,reset, value):
#     F.clear()
#
#     if len(reset_count)==0:
#         reset_count.append(0)
#         print("this is reset count",reset_count)
#     reset_count.append(reset)
#     print("this is reset count", reset_count)
#     if reset_count[-1] == reset_count[-2]:
#                 if n_clicks > 0:
#                     for i in a:
#                         for k,v in i.items():
#                                 for m,n in v.items():
#                                     if value in m:
#                                         print("this is m",m)
#                                         if m in F:
#                                             continue
#                                         else:
#                                             F.append(m)
#                                     else:
#                                         continue
#                 print(F)
#                 options = [{'label': i, 'value': i} for i in F]
#                 print(options)
#                 return options
#     else:
#             F.clear()
#             for i in range(0):
#                 a5.append(a4[i])
#             options = [{'label': i, 'value': i} for i in a5]
#             print(options)
#             return options

# @app.callback(Output('cytoscape-tapNodeData-json', 'children'),
#               Input('org-chart', 'mouseoverEdgeData'))
# def displayTapNodeData(data):
#     return json.dumps(data, indent=2)
#mouseoverEdgeData

reset_count=[]
@app.callback(Output('dpdntargets', 'options'),
                Input('textarea-state-example-button', 'n_clicks'),
                State('textarea-state-example', 'value'))

def update_output(n_clicks, value):
    F.clear()

    if n_clicks > 0:
            for i in a:
                for k,v in i.items():
                        for m,n in v.items():
                            if value in m:
                                print("this is m",m)
                                if m in F:
                                    continue
                                else:
                                    F.append(m)
                            else:
                                continue
            print(F)
            options = [{'label': i, 'value': i} for i in F]
            print(options)
            return options
    else:
        for i in range(0):
            a5.append(a4[i])
        options = [{'label': i, 'value': i} for i in a5]
        print(options)
        return options

@app.callback(Output('textarea-state-example-button','n_clicks'),
             [Input('textarea-clear-example-button','n_clicks')])
def update(reset):
    return 0




@app.callback(Output('cytoscape-tapNodeData-output', 'children'),
                  Input('org-chart', 'tapNodeData'))
def displayTapNodeData(data):
    if data:
        global node_only1
        node_only1.clear()
        node_only1.append(data['label'])
        #node_only1=["NODE:  " , data['label']]
        print("this is node1",node_only1[0])
        df_links_dict = df_link.set_index('genename').to_dict()
        for i, j in df_links_dict.items():
            for m, n in j.items():
                if m == node_only1[0]:
                    return html.Div(["Click Here For More Information On",html.B(" Gene : {} → ".format(node_only1[0])),dcc.Link("Click here",id="this_is_dcclink",href="https://www.ncbi.nlm.nih.gov/gene/"+n, target='_blank')])

            return html.Div([html.B("NO MATCH FOUND! "), "Click Here To Find Information On",html.B(" Gene : {} → ".format(node_only1[0])),dcc.Link("Click here",id="this_is_dcclink",href="https://www.ncbi.nlm.nih.gov/gene/", target='_blank')])

@app.callback(Output('cytoscape-tapEdgeData-output', 'children'),
                  Input('org-chart', 'tapEdgeData'))
def displayTapEdgeData(data):
        if data:
            return html.Div(["Splicing Event:  ", html.B(data['source'].upper())]),html.Div(["  Splicing Factor:  ",html.B(data['target'].upper())])

@app.callback(Output('org-chart', 'stylesheet'),
              [Input('org-chart', 'tapNode'),
               Input('input-following-color', 'value'),
               Input('input-follower-color', 'value'),
               Input('dropdown-node-shape', 'value')])
def generate_stylesheet(node, following_color, follower_color, node_shape):
    if not node:
        return default_stylesheet

    stylesheet = [
        {
            "selector": ".rectangle",
            "style": {
                # "width": "mapData(size, 0, 5, 20, 60)",
                # "height": "mapData(size, 0, 5, 20, 60)",
                'background-color': 'black',
                'width': 80,
                'height': 50,
                "content": "data(label)",
                #"background-color": "green",
                'shape': node_shape,



            }
        },
        {
            "selector": "node",
            "style": {
                "width": "mapData(size, 0, 5, 20, 60)",
                "height": "mapData(size, 0, 5, 20, 60)",
                "content": "data(label)",
                "background-color": "mapData(weight, -1, 0, darkblue, white)"

            }
        },
        {
            'selector': '.red',
            'style': {
                'background-color': 'red',
                'line-color': 'red',
                'weight': 50
            }
        },
        # {
        # "selector": 'node',
        # 'style': {
        #     'opacity': 0.3,
        #
        # }
    # },
    #     {
    #     'selector': 'edge',
    #     'style': {
    #         'opacity': 0.2,
    #         "curve-style": "bezier",
    #     }
    # },
        # {
    #     "selector": 'node[id = "{}"]'.format(node['data']['id']),
    #     "style": {
    #         'background-color': '#B10DC9',
    #         "border-color": "purple",
    #         "border-width": 2,
    #         "border-opacity": 1,
    #         "opacity": 1,
    #
    #         "label": "data(label)",
    #         "color": "#B10DC9",
    #         "text-opacity": 1,
    #         "font-size": 12,
    #         'z-index': 9999
    #     }
    #}
    ]

    for edge in node['edgesData']:
        if edge['source'] == node['data']['id']:
            stylesheet.append({
                "selector": 'node[id = "{}"]'.format(edge['target']),
                "style": {
                    'opacity': 0.9
                }
            })
            stylesheet.append({
                "selector": 'edge[id= "{}"]'.format(edge['id']),
                "style": {
                    "mid-source-arrow-color": following_color,
                    "mid-source-arrow-shape": "vee",
                    "line-color": following_color,
                    'opacity': 0.9,
                    'z-index': 5000
                }
            })

        if edge['target'] == node['data']['id']:
            stylesheet.append({
                "selector": 'node[id = "{}"]'.format(edge['source']),
                "style": {
                    #'background-color': follower_color,
                    'opacity': 0.9,
                    'z-index': 9999
                }
            })
            stylesheet.append({
                "selector": 'edge[id= "{}"]'.format(edge['id']),
                "style": {
                    "mid-source-arrow-color": follower_color,
                    "mid-source-arrow-shape": "vee",
                    "line-color": follower_color,
                    'opacity': 1,
                    'z-index': 5000
                }
            })

    return stylesheet

# @app.callback(Output('cytoscape-selectedNodeData-markdown', 'children'),
#                   Input('cytoscape-event-callbacks-3', 'selectedNodeData'))
# def displaySelectedNodeData(data_list):
#     if not data_list:
#         return
#
# @app.callback(Output('display-selected-values', 'children'),
#               Input('org-chart', 'tapNodeData'))
# def displayTapNodeData(data):
#     return data
# @app.callback(
#     Output('display-selected-values', 'target'),
#     Input('org-chart', 'elements'))
# def set_display_children(value):
#     return value

def update_nodes(data):
    if data is None:
        return dash.no_update
    else:
        dff = df.copy()
        dff.loc[dff.name == data['label'], 'color'] = "yellow"



if __name__ == '__main__':
    app.run_server(debug=True)

