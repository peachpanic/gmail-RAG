from simplegmail import Gmail
from simplegmail.query import construct_query

gmail = Gmail()

# query_params = {
#     'query': 'is:unread',  # Example query to fetch unread emails
#     'label_ids': ['INBOX'],  # Specify label IDs if needed
#     'max_results': 10,  # Limit the number of results
# }

query_params = {
    "newer_than": "3d",  # Fetch emails newer than 7 days
    "unread": True,  # Fetch only unread emails
}

messages = gmail.get_messages(query=construct_query(query_params))

for message in messages:
    print(f"Subject: {message.subject}")
    print(f"From: {message.sender}")
    print(f"Snippet: {message.snippet}")
    print(f"Date: {message.date}")
    print("-" * 40)  # Separator for readability
    # Uncomment the next line to mark the message as read after processing
    # message.mark_as_read()
    # Uncomment the next line to delete the message after processing
    # message.delete()
    # Uncomment the next line to print the full message body
    # print(message.body)
    # Uncomment the next line to print the full HTML body
    # print(message.body_html)      
