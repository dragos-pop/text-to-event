PROMPT_TEMPLATE = '''Parse event details from the following input and give the results in the following format:
NAME:
LOCATION:
START:
END:
DESCRIPTION:

<Example 1>
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

<End of example 1>

<Example 2>
INPUT TO PARSE:

"Dear Mr. Smith, 

I am happy to tell you that the hiring manager believes you have the right profile for our vacancy and would like to schedule an interview with you on the 3rd of October, from 9am to 10:30am, at the Conference Hotel.

During the interview, she will discuss further the role and responsibilities, the team’s expectations of you, as well as any questions you may have.

Let me know if you have any other questions and good luck to the interview!

Best regards, 
Thomas Mark

ANSWER:

NAME: Interview with Hiring Manager
LOCATION: Conference Hotel
START: 2023-10-03
END: 2023-10-03
DESCRIPTION: role, responsabilities, team's expectations, questions

<End of example 2>

If the year is not mentioned, fill it in with 2023 for the start and end. 
If the end is not mentioned, make it the same as the start.
Do not include the "ANSWER:" at the beginning of the message!

INPUT TO PARSE: "{user_input}"'''