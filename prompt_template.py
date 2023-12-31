PROMPT_TEMPLATE = '''Parse event details from the following INPUT TO PARSE and give the ANSWER as a list of five strings: name, location, start, end, description; like in the following examples:

<Example 1>
INPUT TO PARSE:

"The pass issuance / renewal / cancellation appointment for M4 is on 21 Aug 2023 (Monday), 08:30 AM at Employment Pass Services Centre.

Your appointment reference no. is M43467.

Please be on time and check-in at the registration kiosk with the Appointment Letter. If you are late for your appointment, we may need to reschedule you to another date.

Yours sincerely,
Work Pass Division
Employment Pass Services Centre"

ANSWER:
Appointment Employment Pass Services Centre, Employment Pass Services Centre, 2023-08-21 08:30:00, 2023-08-21 09:30:00, Appointment reference no. is M43467
<End of example 1>

<Example 2>
INPUT TO PARSE:

"Dear Mr. Smith, 

I am happy to tell you that the hiring manager believes you have the right profile for our vacancy and would like to schedule an interview with you on the 3rd of October, from 13 to 14:30, at the Conference Hotel.

During the interview, she will discuss further the role and responsibilities, the team’s expectations of you, as well as any questions you may have.

Let me know if you have any other questions and good luck to the interview!

Best regards, 
Thomas Mark"

ANSWER:
Interview with Hiring Manager, Conference Hotel, 2023-10-03 13:00:00, 2023-10-03 14:30:00, role, responsabilities, team's expectations, questions
<End of example 2>

If the year is not mentioned, fill it in with 2023 for the dates. 
If the END is not mentioned, set it at the same data as the START but one hour later.

INPUT TO PARSE: "{user_input}"'''