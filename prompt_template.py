PROMPT_TEMPLATE = '''Parse event details from the following input and give the results in the following format:
NAME:
LOCATION:
START:
END:
DESCRIPTION:

<Example>
INPUT TO PARSE:

"The pass issuance / renewal / cancellation appointment for M4 is on 21 Aug 2023 (Monday), 08:30 AM at Employment Pass Services Centre.

Your appointment reference no. is M43467.

Please be on time and check-in at the registration kiosk with the Appointment Letter. If you are late for your appointment, we may need to reschedule you to another date.

Yours sincerely,
Work Pass Division
Employment Pass Services Centre"


ANSWER:

NAME: Appointment Employment Pass Services Centre
LOCATION: Employment Pass Services Centre
START: 2023-08-21
END: 2023-08-21
DESCRIPTION: Appointment reference no. is M43467

<End of example>

If the year is not mentioned, fill it in with 2023 for the start and end. 
If the end is not mentioned, make it the same as the start.
Do not include the "ANSWER:" at the beginning of the message!

INPUT TO PARSE: {user_input}'''