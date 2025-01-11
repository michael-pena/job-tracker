from sqlalchemy.ext.declarative import declarative_base
from application import Application
from base import Base, Session, engine
import pandas as pd
import dash
from repository import ApplicationRepository
from dash import html, dcc
from dash import dash_table
from dash.dependencies import Input, Output, State
from graph_utils import generate_graph

session = Session()
repository = ApplicationRepository(session)
app = dash.Dash(__name__)

@app.callback(
    Output('applications-graph', 'figure'),
    Input('stored-data', 'data')
)
def update_graph(data):
    return generate_graph(repository)

def fetch_applications():
    applications = session.query(Application).all()
    return pd.DataFrame([{
        'id': app.id,
        'company': app.company,
        'position': app.position,
        'date': app.date,
        'status': app.status,
        'offer': app.offer,
        'accepted': app.accepted
    } for app in applications])

app.layout = html.Div([
    dash_table.DataTable(
        id='applications-table',
        columns=[
            {'name': 'ID', 'id': 'id', 'editable': False},
            {'name': 'Company', 'id': 'company', 'editable': True},
            {'name': 'Position', 'id': 'position', 'editable': True},
            {'name': 'Date', 'id': 'date', 'editable': True},
            {'name': 'Status', 'id': 'status', 'presentation': 'dropdown', 'editable': True},            
            {'name': 'Offer', 'id': 'offer', 'presentation': 'dropdown', 'editable': True},
            {'name': 'Accepted', 'id': 'accepted', 'presentation': 'dropdown', 'editable': True},
        ],
        dropdown = {
            'status': {
                'options': [
                    {'label': 'Rejected', 'value': 'rejected'},
                    {'label': 'No Response', 'value': 'no response'},
                    {'label': 'Interview', 'value': 'interview'}
                ]
            },
            'offer': {
                'options': [
                    {'label': 'Yes', 'value': 'yes'},
                    {'label': 'No', 'value': 'no'}
                ]
            },
            'accepted': {
                'options': [
                    {'label': 'Yes', 'value': 'yes'},
                    {'label': 'No', 'value': 'no'}
                ]
            }
        },
        data=fetch_applications().to_dict('records'),
        editable=True,
        row_deletable=True,
    ),
    html.Button('Add Row', id='add-row-button', n_clicks=0),
    html.Button('Save Changes', id='save-button', n_clicks=0),
    dcc.Store(id='stored-data', data=fetch_applications().to_dict('records')),
    dcc.Graph(id='applications-graph')
])

@app.callback(
 [Output('applications-table', 'data'),
     Output('stored-data', 'data')],
    [Input('add-row-button', 'n_clicks'),
     Input('save-button', 'n_clicks')],
    [State('applications-table', 'data'),
     State('applications-table', 'columns'),
     State('applications-table', 'data_previous')]
)
def modify_table(add_clicks, save_clicks, rows, columns, previous_rows):
    ctx = dash.callback_context

    if not ctx.triggered:
        return rows, rows

    button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if button_id == 'add-row-button' and add_clicks > 0:
        rows.append({c['id']: '' for c in columns})
        return rows, rows

    if button_id == 'save-button' and save_clicks > 0:
        # Handle deletions
        if previous_rows:
            previous_ids = {row['id'] for row in previous_rows}
            current_ids = {row['id'] for row in rows if row['id']}
            ids_to_delete = previous_ids - current_ids
            for id_to_delete in ids_to_delete:
                application = session.query(Application).filter(Application.id == id_to_delete).first()
                if application:
                    session.delete(application)

        # Handle updates and additions
        for row in rows:
            if row['id'] == '':
                application = Application(
                    company=row['company'],
                    position=row['position'],
                    date=row['date'],
                    status=row['status'],
                    offer=row['offer'],
                    accepted=row['accepted']
                )
                session.add(application)
            else:
                application = session.query(Application).filter(Application.id == row['id']).first()
                if application:
                    application.company = row['company']
                    application.position = row['position']
                    application.date = row['date']
                    application.status = row['status']
                    application.offer = row['offer']
                    application.accepted = row['accepted']
        session.commit()
        updated_data = fetch_applications().to_dict('records')
        return updated_data, updated_data

    return rows, rows

# To do : add pagination, filtering, and sorting to the table
# To do : accept offer data to the graph
# To do : add title and labels to the graph

if __name__ == '__main__':
    app.run_server(debug=True)