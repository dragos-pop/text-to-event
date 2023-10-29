import streamlit as st
from io import StringIO
import ics
import arrow
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from prompt_template import PROMPT_TEMPLATE
from langchain.output_parsers import CommaSeparatedListOutputParser

st.set_page_config(page_title="text-to-event", layout="wide")
st.title("text-to-event")

with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", type="password")
    st.write("You can find your Secret API key in your [OpenAI User settings](https://beta.openai.com/account/api-keys).")

st.subheader('Select your timezone:')
tz = st.slider('', -12, 14, 0)
if tz < 0:
    s = "Your selected timezone is UTC" + str(tz)
    st.write(s)
    timezone_str = 'Etc/GMT'
elif tz == 0:
    st.write("Your selected timezone is UTC")
    timezone_str = 'Etc/GMT' + str(-tz)
else:
    s = "Your selected timezone is UTC+" + str(tz)
    st.write(s)
    timezone_str = 'Etc/GMT' + str(-tz)

left, right = st.columns([3, 2])
with left:
    st.subheader('Enter text below:')
    st.text_area("", key="text", height=120)
with right:
    st.subheader('Or upload .txt file here:')
    file = st.file_uploader("", accept_multiple_files=False)

user_input = ""
if st.button("Submit"):
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()
    if st.session_state.text:
        user_input = st.session_state.text
    elif file:
        try:
            stringio = StringIO(file.getvalue().decode("utf-8"))
            user_input = stringio.read()
        except:
            st.info(":red[ERROR:] File format not accepted. Provide a file in .txt format.")
    else:
        st.info("No input.")

if user_input:
    prompt = PromptTemplate(input_variables=["user_input"], template=PROMPT_TEMPLATE)
    llm = OpenAI(model_name="text-davinci-003", openai_api_key=openai_api_key)
    answer = llm(prompt.format(user_input=user_input))

    cleaned_answer = answer[10:]
    parser = CommaSeparatedListOutputParser()
    parsed_answer = parser.parse(cleaned_answer)

    c = ics.Calendar()
    e = ics.Event()
    e.name = parsed_answer[0]
    e.location = parsed_answer[1]
    e.begin = parsed_answer[2]
    e.begin = arrow.get(e.begin, tzinfo=timezone_str)
    e.end = parsed_answer[3]
    e.end = arrow.get(e.end, tzinfo=timezone_str)
    # st.info(e.begin)
    # st.error(arrow.get(e.begin, tzinfo=timezone_str))
    e.description = parsed_answer[4]
    c.events.add(e)

    result = ("NAME: " + parsed_answer[0] + "  \n LOCATION: " + parsed_answer[1] + \
             "  \n START: " + str(parsed_answer[2]) + "  \n END: " + str(parsed_answer[3]) + \
             "  \n DESCRIPTION: " + str(parsed_answer[4]))

    st.write("# Event Summary:\n", result)
    with open('event.ics', 'w') as f:
        f.writelines(c.serialize_iter())

    st.download_button('Downloads .ics file', open('event.ics'), file_name='event.ics')
