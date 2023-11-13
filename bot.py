#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# =============================================================================
# Created By  : Jeromie Kirchoff
# Created Date: Mon Aug 02 17:46:00 PDT 2018
# =============================================================================


# Imports
# =============================================================================
import smtplib
import random
import os

# =============================================================================
# SET EMAIL LOGIN REQUIREMENTS
# =============================================================================
gmail_user = 'killuadummy2000@gmail.com'
gmail_app_password = 'afmgchkeaeadtvjt'

# =============================================================================
# SET THE INFO ABOUT THE SAID EMAIL
# =============================================================================

# GETTING THE PYTHON SCRIPT PATH
current_path = os.path.dirname(os.path.abspath(__file__))

# CONVERTS NAME FILE TXT INTO LIST
with open(current_path + '/list_names.txt', 'r') as file:
    name_list = [line.strip() for line in file]
 
# CONVERTS SUBJECT FILE TXT INTO LIST
with open(current_path + '/list_subjects.txt', 'r') as file:
    subject_list = [line.strip() for line in file]

# CONVERTS SUBJECT FILE TXT INTO LIST
#with open(current_path + '/list_body.txt', 'r') as file:
#    body_list = [line.split(',') for line in file]

body_list = [f"""Hey {random.choice(name_list)},
                
Hope this email finds you well! It's been a while since we caught up, and I was thinking it's high time we grab a coffee and chat about life. How about we meet up this week? I found this cozy new coffee spot downtown that I've been dying to try.

Let me know what day works for you, and we can make it happen. Looking forward to some good laughs and catching up!
                
Cheers,
{random.choice(name_list)}""",

             f"""Hey, what's up? friend!
                
I hope you have been well!

Cheers,
{random.choice(name_list)}""",

            f"""Hi {random.choice(name_list)},
                
Long time, no talk! How about a quick coffee catch-up or a virtual chat? I've got some updates to share and would love to hear what's new with you. Let me know when you're free!

Yours,
{random.choice(name_list)}""",

            f"""Hi {random.choice(name_list)},

How are you doing? I haven't talked to you in a while, so I wanted to reach out and see how you're doing.

I've been keeping busy with my acads. I'm also really excited about seeing you soon.

I hope to hear from you soon!""",

            f"""Hey {random.choice(name_list)},

Got some good news to share. Let's celebrate over dinner tonight!

Best,
{random.choice(name_list)}""",

            f"""Hey {random.choice(name_list)},

I just saw you and thought of you.

Let me know what you've been up to lately. I'd love to catch up sometime soon.

Talk to you soon,
{random.choice(name_list)}""",

            f"""Hey {random.choice(name_list)},

Happy Holidays!

I hope you're having a great day.

I'm sending you my best wishes.

Talk to you soon,
{random.choice(name_list)}""",

            f"""Hi {random.choice(name_list)},

I just wanted to say that I'm thinking of you today.

I hope you're doing well.

Take care,
{random.choice(name_list)}""",
]

sent_from = gmail_user
sent_to = ['ephishsense@gmail.com', 'ephishsense@gmail.com']  	    # palitan na lang 'to if san gusto i-send
sent_subject = random.choice(subject_list)              		
sent_body = random.choice(body_list)

email_text = """\
From: %s
To: %s
Subject: %s

%s
""" % (sent_from, ", ".join(sent_to), sent_subject, sent_body)

# =============================================================================
# SEND EMAIL OR DIE TRYING!!!
# Details: http://www.samlogic.net/articles/smtp-commands-reference.htm
# =============================================================================

try:
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(gmail_user, gmail_app_password)
    server.sendmail(sent_from, sent_to, email_text)
    server.close()

    print('Email sent!')
except Exception as exception:
    print("Error: %s!\n\n" % exception)
