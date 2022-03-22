__author__ = 'Edward'
"""
Usage: utils.py

This holds all helper functions that can be used across the project.
"""

from datetime import datetime

import pytz
from django.core.mail import EmailMessage
from django.db.models import Sum, F
from django.template.loader import render_to_string

from portal.models import SearchTerm

tz = pytz.timezone('Africa/Lagos')


class EmailHandler:
    """
    A class to handle sending emails.
    """
    def __init__(self, email_subject=None, email_from=None, email_to=None, email_cc=None,
                 email_bcc=None, email_reply_to=None, email_msg=None, files=None, headers=None):
        """

        :param email_subject:
        :param email_from:
        :param email_to:
        :param email_cc:
        :param email_bcc:
        :param email_reply_to:
        :param email_msg:
        :param files:
        :param headers:
        """
        self.email_subject = email_subject
        self.email_from = email_from
        self.email_to = email_to
        self.email_cc = email_cc
        self.email_bcc = email_bcc
        self.email_reply_to = email_reply_to
        self.email_msg = email_msg
        self.files = files
        self.headers = headers

    def send_email_text(self, connection=None):
        """
        Send plain text email

        :param connection: A connection for sending mass emails
        :return: Integer 1 or 0 depending on if email was sent or not
        """
        email = EmailMessage()

        if self.email_subject:
            email.subject = self.email_subject
        if self.email_from:
            email.from_email = self.email_from
        if self.email_to:
            email.to = [x.strip() for x in self.email_to.split(',')]
        if self.email_cc:
            email.cc = [x.strip() for x in self.email_cc.split(',')]
        if self.email_bcc:
            email.bcc = [x.strip() for x in self.email_bcc.split(',')]
        if self.email_reply_to:
            email.reply_to = [x.strip() for x in self.email_reply_to.split(',')]
        if self.files:
            for file in self.files:
                email.attach(file['name'], file['bytes'])
        if self.headers:
            email.extra_headers.update(self.headers)

        email.body = self.email_msg
        email.connection = connection

        return email.send(fail_silently=False)

    def send_email_html(self, template, context, connection=None):
        """
        Send HTML email

        :param template: HTML template to be used
        :param context: A dictionary of values to be used in the template
        :param connection: A connection for sending mass emails
        :return: Integer 1 or 0 depending on if email was sent or not
        """
        now = datetime.now(tz)
        if 0 < now.hour <= 12:
            time_of_day = "morning"
        elif 12 < now.hour <= 17:
            time_of_day = "afternoon"
        else:
            time_of_day = "evening"

        context['time_of_day'] = time_of_day

        html_content = render_to_string(template, context)

        email = EmailMessage()

        if self.email_subject:
            email.subject = self.email_subject
        if self.email_from:
            email.from_email = self.email_from
        if self.email_to:
            email.to = [x.strip() for x in self.email_to.split(',')]
        if self.email_cc:
            email.cc = [x.strip() for x in self.email_cc.split(',')]
        if self.email_bcc:
            email.bcc = [x.strip() for x in self.email_bcc.split(',')]
        if self.email_reply_to:
            email.reply_to = [x.strip() for x in self.email_reply_to.split(',')]
        if self.files:
            for file in self.files:
                email.attach(file['name'], file['bytes'])
        if self.headers:
            email.extra_headers.update(self.headers)

        email.content_subtype = "html"
        email.mixed_subtype = 'related'
        email.body = html_content

        email.connection = connection

        return email.send(fail_silently=False)


def write_file(path, file):
    """
    A method to write file to a path

    :param path: Whether to fetch using structure value of campaign or alias of ad group
    :param file: the value to use as filter for either structure value or alias
    :return: returns True for success / False for failure
    """
    try:
        with open(path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        return True
    except:
        pass
    return False


def get_top_roas(which, query, limit=10):
    """
    A method to handle fetching and calculating the ROAS

    :param which: Whether to fetch using structure value of campaign or alias of ad group
    :param query: the value to use as filter for either structure value or alias
    :param limit: the number of rows to return
    :return: returns a dictionary with the query results or empty dictionary
    """
    if which == 'campaigns':
        results = SearchTerm.objects.filter(campaign__structure_value__iexact=query) \
                      .annotate(total_cost=Sum('cost'), total_conversion_value=Sum('conversion_value'),
                                roas=F('total_conversion_value') / F('total_cost')) \
                      .values('search_term', 'total_cost', 'total_conversion_value', 'roas', structure_value=F('campaign__structure_value')). \
                      order_by('-roas')[:limit]
    elif which == 'ad-groups':
        results = SearchTerm.objects.filter(ad_group__alias__iexact=query) \
                      .annotate(total_cost=Sum('cost'), total_conversion_value=Sum('conversion_value'),
                                roas=F('total_conversion_value') / F('total_cost')) \
                      .values('search_term', 'total_cost', 'total_conversion_value', 'roas', alias=F('ad_group__alias')) \
                      .order_by('-roas')[:limit]
    else:
        results = {}
    print(results)
    return results
