import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
from parsers.inbox import InboxParser


# print('Enter the year (default none)')
# print('-> ', end='')
# try:
#     year = str(int(input()))
# except:
#     year = None
#
# print('Enter your IG username:')
# print('-> ', end='')
# try:
#     username = input()
# except:
#     raise Error('You must enter a username')

inbox_parser = InboxParser(username='alegs.chow')
inbox_parser.process(year='2020')
min_message_threshold = 100
users, user_to_percentage_you_sent = inbox_parser.get_users_by_message_disparity(min_message_threshold=min_message_threshold)

percent_sent = []
percent_received = []
total_messages = []
usernames = []
max_message_count = min_message_threshold
for user in users:
    percent_sent.append(user_to_percentage_you_sent[user])
    percent_received.append(100 - user_to_percentage_you_sent[user])
    total_messages.append(len(inbox_parser.get_all_messages_from_user(user=user)))
    usernames.append(inbox_parser.cleanup_username(username=user))
    max_message_count = max(max_message_count, len(inbox_parser.get_all_messages_from_user(user=user)))

app = dash.Dash(__name__)
df = pd.DataFrame({
    "% Sent": percent_sent,
    "% Received": percent_received,
    "Total Messages": total_messages,
    "User": usernames
})
fig = px.scatter(df, x="Total Messages", y="% Sent", hover_name="User", size=[1]*len(usernames), log_x=True)
fig.add_shape(type='line', x0=min_message_threshold, y0=50, x1=max_message_count, y1=50, line=dict(color='Red', width=2))


app.layout = html.Div(children=[
    html.H1(children='Instagram Message Disparity'),

    html.Div(children='''
        How much of the conversation are you messaging?
    '''),

    dcc.Graph(
        id='message_disparity_scatter_graph',
        figure=fig
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
