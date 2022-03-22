__author__ = 'Edward'
"""
Usage: tasks.py

This holds all celery tasks to help run asynchronous operations.
"""

from datetime import datetime

import pandas
from celery import shared_task
from django.template.defaultfilters import pluralize

from bidnamic.base_settings import BASE_DIR
from portal.models import Campaign, AdGroup, SearchTerm
from portal.utils import EmailHandler


@shared_task()
def import_campaigns(email=None):
    """
    A function to import csv data into Campaign model

    :param email: The email address to send completion alert to
    :return: None
    """
    data_frame = pandas.read_csv(BASE_DIR / "campaigns.csv")
    campaigns = Campaign.objects.all()
    processed = [campaign.campaign_id for campaign in campaigns]  # retrieve existing campaigns to avoid duplicates
    to_be_created = []  # hold objects to be processed for bulk_create
    for index, row in data_frame.iterrows():
        uniqueness = str(row['campaign_id'])  # used to check if row already exists in database
        if uniqueness not in processed:
            to_be_created.append(Campaign(
                campaign_id=row['campaign_id'],
                structure_value=row['structure_value'],
                status=row['status']
            ))
            processed.append(uniqueness)

    Campaign.objects.bulk_create(to_be_created)

    if email:
        try:
            subject = 'Completed campaigns import'
            message = f'Successfully imported {len(to_be_created)} campaign{pluralize(len(to_be_created))}.'
            mail_sent = EmailHandler(email_subject=subject, email_to=email, email_msg=message).send_email_text()
            print('Sent' if mail_sent else 'Not Sent')
        except Exception as e:
            print(str(e))


@shared_task()
def import_ad_groups(email=None):
    """
    A function to import csv data into AdGroup model

    :param email: The email address to send completion alert to
    :return: None
    """
    data_frame = pandas.read_csv(BASE_DIR / "adgroups.csv")
    campaigns = Campaign.objects.all()
    ad_groups = AdGroup.objects.all().select_related('campaign')
    processed = [(ad_group.campaign.campaign_id, ad_group.ad_group_id) for ad_group in ad_groups]  # retrieve existing ad groups to avoid duplicates
    to_be_created = []  # hold objects to be processed for bulk_create
    for index, row in data_frame.iterrows():
        uniqueness = (str(row['campaign_id']), str(row['ad_group_id']))  # used to check if row already exists in database
        if uniqueness not in processed:
            to_be_created.append(AdGroup(
                campaign=campaigns.get(campaign_id=row['campaign_id']),
                ad_group_id=row['ad_group_id'],
                alias=row['alias'],
                status=row['status']
            ))
            processed.append(uniqueness)

    AdGroup.objects.bulk_create(to_be_created)

    if email:
        try:
            subject = 'Completed ad groups import'
            message = f'Successfully imported {len(to_be_created)} ad group{pluralize(len(to_be_created))}.'
            mail_sent = EmailHandler(email_subject=subject, email_to=email, email_msg=message).send_email_text()
            print('Sent' if mail_sent else 'Not Sent')
        except Exception as e:
            print(str(e))


@shared_task()
def import_search_terms(email=None):
    data_frame = pandas.read_csv(BASE_DIR / "search_terms.csv")
    campaigns = Campaign.objects.all()
    ad_groups = AdGroup.objects.all()
    search_terms = SearchTerm.objects.all().select_related('campaign', 'ad_group')
    processed = [(search_term.campaign.campaign_id, search_term.ad_group.ad_group_id, search_term.search_term, search_term.clicks, search_term.cost,
                  search_term.conversion_value, search_term.conversions) for search_term in search_terms]  # retrieve existing search terms to avoid duplicates
    to_be_created = []  # hold objects to be processed for bulk_create
    for index, row in data_frame.iterrows():
        uniqueness = (str(row['campaign_id']), str(row['ad_group_id']), row['search_term'], row['clicks'], row['cost'], row['conversion_value'],
                      row['conversions'])  # used to check if row already exists in database
        if uniqueness not in processed:
            to_be_created.append(SearchTerm(
                campaign=campaigns.get(campaign_id=row['campaign_id']),
                ad_group=ad_groups.get(ad_group_id=row['ad_group_id']),
                search_term=row['search_term'],
                clicks=row['clicks'],
                cost=row['cost'],
                conversion_value=row['conversion_value'],
                conversions=row['conversions'],
                date=datetime.strptime(row['date'], "%Y-%m-%d")
            ))
            processed.append(uniqueness)

    SearchTerm.objects.bulk_create(to_be_created)

    if email:
        try:
            subject = 'Completed search terms import'
            message = f'Successfully imported {len(to_be_created)} search term{pluralize(len(to_be_created))}.'
            mail_sent = EmailHandler(email_subject=subject, email_to=email, email_msg=message).send_email_text()
            print('Sent' if mail_sent else 'Not Sent')
        except Exception as e:
            print(str(e))
