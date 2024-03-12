"""An application that reads text and outputs an event in .ics format,
leveraging Streamlit, LangChain, and OpenAI API."""
from io import StringIO
import datetime
import arrow
import ics
import streamlit as st
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.output_parsers import CommaSeparatedListOutputParser


URL_OPENAI_KEY = "https://beta.openai.com/account/api-keys"

st.set_page_config(
    page_title="text-to-event",
    layout="wide"
)
st.title(body="text-to-event")

with st.sidebar:
    openai_api_key = st.text_input(
        label="OpenAI API Key",
        type="password"
    )
    st.write(
        f"You can find your Secret API key in your [OpenAI User settings]({URL_OPENAI_KEY}).")

st.subheader(body="Select your timezone:")
tz = st.slider(
    label=" ",
    min_value=-12,
    max_value=14,
    value=0
)
if tz < 0:
    st.write(f"Your selected timezone is UTC{tz}")
    timezone_str = "Etc/GMT"
elif tz == 0:
    st.write("Your selected timezone is UTC")
    timezone_str = f"Etc/GMT {-tz}"
else:
    st.write(f"Your selected timezone is UTC+{tz}")
    timezone_str = f"Etc/GMT{-tz}"

left, right = st.columns([3, 2])
with left:
    st.subheader(body="Enter text below:")
    st.text_area(
        label=" ",
        key="text",
        height=120
    )
with right:
    st.subheader(body="Or upload .txt file here:")
    file = st.file_uploader(
        label=" ",
        accept_multiple_files=False
    )

user_input = ""
if st.button(label="Submit"):
    if not openai_api_key:
        st.info(body="Please add your OpenAI API key to continue.")
        st.stop()
    if st.session_state.text:
        user_input = st.session_state.text
    elif file:
        try:
            string_buffer = StringIO(
                file.getvalue().decode(
                    encoding="utf-8"
                )
            )
            user_input = string_buffer.read()
        except UnicodeDecodeError:
            st.info(
                body=":red[ERROR:] File format not accepted. Provide a file in .txt format."
            )
    else:
        st.info(body="No input.")

if user_input:
    with open(
        file="prompt_template.txt",
        mode="r",
        encoding="utf-8"
    ) as file:
        prompt_template = file.read()
    prompt = PromptTemplate(
        input_variables=["user_input"],
        template=prompt_template
    )
    llm = OpenAI(
        model_name="text-davinci-003",
        openai_api_key=openai_api_key
    )
    answer = llm(
        prompt.format(
            user_input=user_input
        )
    )

    cleaned_answer = answer[10:]
    parser = CommaSeparatedListOutputParser()
    parsed_answer = parser.parse(
        text=cleaned_answer
    )

    c = ics.Calendar()
    e = ics.Event()
    e.name = parsed_answer[0]
    e.location = parsed_answer[1]
    e.begin = arrow.get(
        parsed_answer[2],
        tzinfo=timezone_str
    )
    e.end = arrow.get(
        parsed_answer[3],
        tzinfo=timezone_str
    )

    # Support for some temporal deictic expressions:
    if "today" in user_input.lower():
        today = datetime.date.today()
        day = today.day
        month = today.month
        e.end = e.end.replace(
            month=month,
            day=day
        )
        e.begin = e.begin.replace(
            month=month,
            day=day
        )
    if "tomorrow" in user_input.lower():
        tomorrow = (datetime.date.today() +
                    datetime.timedelta(days=1))
        day = tomorrow.day
        month = tomorrow.month
        e.end = e.end.replace(
            month=month,
            day=day
        )
        e.begin = e.begin.replace(
            month=month,
            day=day
        )
    elif (
            "next" in user_input.lower() or
            "upcoming" in user_input.lower() or
            "following" in user_input.lower()
    ):
        today = datetime.date.today()
        dayofweek = today
        if "monday" in user_input.lower():
            dayofweek = (today +
                         datetime.timedelta((-today.weekday()) % 7))
        if "tuesday" in user_input.lower():
            dayofweek = (today +
                         datetime.timedelta((1 - today.weekday()) % 7))
        if "wednesday" in user_input.lower():
            dayofweek = (today +
                         datetime.timedelta((2 - today.weekday()) % 7))
        if "thursday" in user_input.lower():
            dayofweek = (today +
                         datetime.timedelta((3 - today.weekday()) % 7))
        if "friday" in user_input.lower():
            dayofweek = (today +
                         datetime.timedelta((4 - today.weekday()) % 7))
        if "saturday" in user_input.lower():
            dayofweek = (today +
                         datetime.timedelta((5 - today.weekday()) % 7))
        if "sunday" in user_input.lower():
            dayofweek = (today +
                         datetime.timedelta((6 - today.weekday()) % 7 + 7))
        day = dayofweek.day
        month = dayofweek.month
        e.end = e.end.replace(
            month=month,
            day=day
        )
        e.begin = e.begin.replace(
            month=month,
            day=day
        )

    e.description = parsed_answer[4]
    c.events.add(e)

    result = f"""
    NAME: {parsed_answer[0]}
    LOCATION: {parsed_answer[1]}
    START: {str(e.begin)[:-6]}
    END: {str(e.end)[:-6]}
    DESCRIPTION {parsed_answer[4]}
    """

    st.write(f"# Event Summary: {result}")
    with open(
            file="event.ics",
            mode="w",
            encoding="utf-8"
    ) as f:
        f.writelines(c.serialize_iter())

    st.download_button(
        label="Download .ics file",
        data=open(
            file="event.ics",
            encoding="utf-8"
        ),
        file_name="event.ics"
    )
