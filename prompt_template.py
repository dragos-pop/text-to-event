PROMPT = '''Parse event details from the following email and give the results in the following format:
NAME:
LOCATION:
START DATE:
END DATE:
DESCRIPTION:

Example:
EMAIL:

"The pass issuance / renewal / cancellation appointment for M4 is on 21 Aug 2023 (Monday), 08:30 AM at Employment Pass Services Centre.

Your appointment reference no. is M43467.

Please be on time and check-in at the registration kiosk with the Appointment Letter. If you are late for your appointment, we may need to reschedule you to another date.

Yours sincerely,
Work Pass Division
Employment Pass Services Centre"


ANSWER:

NAME: Appointment Employment Pass Services Centre
LOCATION: Employment Pass Services Centre
START DATE: 2023-08-21
END DATE:
DESCRIPTION: Appointment reference no. is M43467

If the year is not mentioned, fill it in with 2023 for the start and end dates. 
If the end date is not mentioned, make it the same as the start date.
Do not include the "ANSWER:" at the beginning of the message!

EMAIL TO PARSE: {email}'''