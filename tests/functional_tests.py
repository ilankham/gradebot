"""Create functional tests for project using unittest module

This module assumes the file examples/token.ini exists and has a single line of
contents comprising a valid Slack Web API Token.

"""

from contextlib import ExitStack
from datetime import date
from io import StringIO
from unittest import TestCase

from virtual_ta import (
    flatten_dict,
    convert_xlsx_to_yaml_calendar,
    mail_merge_from_csv_file,
    mail_merge_from_xlsx_file,
    mail_merge_from_yaml_file,
    SlackAccount,
)


class TAWorkflowTests(TestCase):
    def test_send_slack_messages_with_csv_import(self):
        # For the intended Slack Workspace and the user account from which they
        # wish to have messages originate, Prof. X creates an API Token by
        # (1) visiting https://api.slack.com/custom-integrations/legacy-tokens
        #     and generating a Legacy Token, or
        # (2) visiting https://api.slack.com/apps and creating a new app with
        #     permission scopes for chat:write:user, im:read, and users:read

        # Prof. X saves the API Token in a text file

        # Prof. X saves a gradebook csv file named with column headings and one
        # row per student grade record

        # Prof. X saves a template text file as a Jinja2 template, with each
        # variable name a column heading in the gradebook csv file

        # Prof. X uses the mail_merge_from_csv_file method to mail merge their
        # template file against their gradebook file, returning a dictionary of
        # messages keyed by Slack user name
        with ExitStack() as es:
            template_fp = es.enter_context(
                open('examples/example_feedback_template.txt')
            )
            gradebook_fp = es.enter_context(
                open('examples/example_gradebook.csv')
            )
            mail_merge_results = mail_merge_from_csv_file(
                template_fp, gradebook_fp, key='Slack_User_Name'
            )

        # Prof. X prints a flattened version of the dictionary to verify
        # message contents are as intended
        with open(
            'examples/expected_render_results_for_test_send_slack_messages_with'
            '_csv_import.txt'
        ) as test_fp:
            self.assertEqual(
                flatten_dict(
                    mail_merge_results,
                    key_value_separator="\n\n-----\n\n",
                    items_separator="\n\n--------------------\n\nMessage to "
                ),
                test_fp.read()
            )

        # Prof. X initiates a SlackAccount object and then uses the
        # set_api_token_from_file method to load their API Token
        test_bot = SlackAccount()
        with open('examples/token.ini') as fp:
            test_bot.set_api_token_from_file(fp)

        # Prof. X then checks the SlackAccount's API Token was loaded correctly
        with open('examples/token.ini') as fp:
            self.assertEqual(fp.readline(), test_bot.api_token)

        # Prof. X uses the SlackAccount direct_message_users method to send the
        # messages in the dictionary to the indicated students
        test_bot.direct_message_by_username(mail_merge_results)

        # Prof. X verifies in the Slack Workspace corresponding to their API
        # Token direct messages have been send with themselves as the sender

    def test_post_to_bb_with_xlsx_import(self):
        # Prof. X obtains a Blackboard API Token

        # Prof. X saves the API Token in a file

        # Prof. X saves a gradebook xlsx file named with column headings and
        # one row per student grade record

        # Prof. X saves a template text file as a Jinja2 template, with each
        # variable name a column heading in the gradebook xlsx file

        # Prof. X uses the mail_merge_from_xlsx_file method to mail merge their
        # template file against their gradebook file, returning a dictionary of
        # messages keyed by Blackboard account identifier
        with ExitStack() as es:
            template_fp = es.enter_context(
                open('examples/example_feedback_template.txt')
            )
            gradebook_fp = es.enter_context(
                open('examples/example_gradebook.xlsx', 'rb')
            )
            mail_merge_results = mail_merge_from_xlsx_file(
                template_fp,
                gradebook_fp,
                key='Slack_User_Name',
                worksheet='example_gradebook',
            )

        # Prof. X prints a flattened version of the dictionary to verify
        # message contents are as intended
        with open(
            'examples/expected_render_results_for_test_post_to_bb_with'
            '_xlsx_import.txt'
        ) as test_fp:
            self.assertEqual(
                flatten_dict(
                    mail_merge_results,
                    key_value_separator="\n\n-----\n\n",
                    items_separator="\n\n--------------------\n\nMessage to "
                ),
                test_fp.read()
            )

        # Prof. X initiates a BlackboardAccount object and then uses the
        # set_api_token_from_file method to load their API Token
        self.fail('Finish the test!')

        # Note: Per https://community.blackboard.com/docs/DOC-1733 and
        # https://community.blackboard.com/thread/3375-http-403-while-using
        # -rest-api-patch-and-post-requests-through-ajax , it might
        # not be possible to automate this process without having admin access
        # to a Blackboard server in order to grant access to make patch/post
        # requests from https://developer.blackboard.com/portal/displayApi

        # Prof. X then checks the BlackboardAccount's API Token was loaded
        # correctly

        # Prof. X uses the BlackboardAccount update_gradebook method to
        # send the assignment feedback in the dictionary to the indicated
        # students

        # Prof. X verifies the assignment feedback was correctly added

    def test_render_calendar_table(self):
        # Prof. X creates an Excel file with column labels for week number and
        # each day of the week (Monday through Sunday, following ISO 8601),
        # with each cell listing one or more delimited items to be calendared

        # Prof. X uses the generate_calendar_yaml function to create an ordered
        # sequence of nested YAML statements organized by week
        with open('examples/example_calendar_data.xlsx', 'rb') as assessment_fp:
            yaml_calendar = convert_xlsx_to_yaml_calendar(
                data_xlsx_fp=assessment_fp,
                start_date=date(2018, 1, 1),
                item_delimiter='|',
                week_number_column='Week',
                worksheet='Assessments',
            )

        # Prof. X prints calendar_yaml to inspect for accuracy
        with open(
            'examples/expected_render_results_for_test_render_calendar_table-'
            'yaml_calendar.yaml'
        ) as test_fp:
            self.assertEqual(
                yaml_calendar,
                test_fp.read()
            )

        # Prof. X saves calendar_yaml to a file for manual editing/updating,
        # including adding comments or additional content
        data_yaml_fp = StringIO(yaml_calendar)

        # Prof. X uses the mail_merge_from_yaml function to create a LaTeX
        # table representation of data_yaml_fp as a dictionary
        with open('examples/example_latex_table_template.tex') as template_fp:
            latex_results = mail_merge_from_yaml_file(
                template_fp=template_fp,
                data_yaml_fp=data_yaml_fp,
            )

        # Prof. X prints a flattened version of the dictionary to verify
        # calendar entries are as intended
        with open(
            'examples/expected_render_results_for_test_render_calendar_table-'
            'latex_table.tex'
        ) as test_fp:
            self.assertEqual(
                flatten_dict(
                    latex_results,
                    key_value_separator="",
                    items_separator='\n'+('%'*80+'\n')*3,
                    suppress_keys=True
                ),
                test_fp.read()
            )
