import streamlit as st
import replicate
import os
from langchain.llms import Replicate
from langchain import PromptTemplate, LLMChain 

# App title
st.set_page_config(page_title="Cloud Zen")
#Sure, here are some of the popular serverless services offered by AWS, Azure, and GCP:AWS: AWS Lambda (for function-based architectures) and AWS #API Gateway (for RESTful APIs)Azure: Azure Functions (for function-based architectures) and Azure API Management (for RESTful APIs)GCP: Cloud #Functions (for function-based architectures) and Cloud Run (for containerized workloads) Additionally, all three providers offer event-driven #architectures based on publish-subscribe models, such as AWS SQS, Azure Service Bus, and GCP Pub/Sub. These services allow you to decouple your #application components and enable loosely coupled, scalable, and resilient systems.User: That's helpful. What are the benefits of serverless #architectures?Assistant: Some benefits of serverless architectures include:1. Reduced administrative burden: With serverless architectures, the #providers manage the underlying infrastructure, freeing up your time to focus on your application logic.2. Scalability: Serverless architectures #scale automatically to handle changes in traffic, ensuring that your application is responsive and available when needed.3. Cost-effectiveness: #You only pay for the compute time consumed by your application, which can lead to significant cost savings compared to traditional server-based #architectures.4. Faster time to market: With serverless architectures, you can quickly and easily spin up new applications and services, speeding #up your time to market.5. Increased resilience: With built-in redundancy and failover capabilities, serverless architectures can help ensure high #availability and resilience for your applications.User: That sounds great. Are there any challenges or drawbacks to serverless architectures?#Assistant: Yes, here are some challenges
# Replicate Credentials
#with st.sidebar:
replicate_api = "r8_eFkWWKgzwpWQmB1R5Gq3IdrvByUPEDq4LMDNI"
#st.title('Cloud Zen')
st.write("""
# Cloud Zen
""")
st.write('---')
    #if 'REPLICATE_API_TOKEN' in st.secrets:
    #    st.success('API key already provided!', icon='✅')
    #    replicate_api = st.secrets['REPLICATE_API_TOKEN']
    #else:
    #    replicate_api = st.text_input('Enter Replicate API token:', type='password')
    #    if not (replicate_api.startswith('r8_') and len(replicate_api)==40):
    #        st.warning('Please enter your credentials!', icon='⚠️')
    #    else:
    #        st.success('Proceed to entering your prompt message!', icon='👉')
    #st.markdown('📖 Learn how to build this app in this [blog](#link-to-blog)!')
os.environ['REPLICATE_API_TOKEN'] = "r8_QuWFyGf7iQe3gz7QL9dwdDl9Czmglz41sFuTj"

# Store LLM generated responses
if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "Welcome to Cloud Zen. Please raise your query below."}]

#if st.button('sample1'):
#    console.log('here')
#if st.button('sample2'):
#    console.log('sample2')
#st.text_area("", "dfjkbdsjfbhdjsfvjkdsnfvjkdnvjndjvndjvnjdnvjdfnvjdfnjvkndfv", height=25)

# Display or clear chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]
st.sidebar.button('Clear Chat History', on_click=clear_chat_history)

# Function for generating LLaMA2 response
# Refactored from <https://github.com/a16z-infra/llama2-chatbot>
def generate_llama2_response(prompt_input):
    string_dialogue = "You are a helpful assistant. You do not respond as 'User' or pretend to be 'User'. You only respond once as 'Assistant'."
    print('in response')
    for dict_message in st.session_state.messages:
        if dict_message["role"] == "user":
            string_dialogue += "User: " + dict_message["content"] + "\\n\\n"
        else:
            string_dialogue += "Assistant: " + dict_message["content"] + "\\n\\n"
    #output = replicate.run('a16z-infra/llama13b-v2-chat:df7690f1994d94e96ad9d568eac121aecf50684a0b0963b25a41cc40061269e5', 
     #                      input={"prompt": f"{string_dialogue} {prompt_input} Assistant: ",
     #                             "temperature":0.9, "top_p":0.9, "max_length":50, "repetition_penalty":1})
    #st.write(output)
    llm = Replicate(
        model="a16z-infra/llama13b-v2-chat:df7690f1994d94e96ad9d568eac121aecf50684a0b0963b25a41cc40061269e5",
        input={"temperature": 0.9, "max_length": 500, "top_p": 1},
    )
    prompt = f"{string_dialogue} {prompt_input} Assistant: "
    output = llm(prompt)
    print(output)
    return output

# User-provided prompt
if prompt := st.chat_input(disabled=not replicate_api):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

def click_button(data):
    clear_chat_history()
    data = "provide more information on the following text." + data
    message = {"role": "user", "content": data}
    st.session_state.messages.append(message)
    #st.write(" clicked")

# Generate a new response if last message is not from assistant
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking...."):
            response = generate_llama2_response(prompt)
            placeholder = st.empty()
            full_response = ''
            for item in response:
                full_response += item
                print(item)
                #st.button(item, on_click=click_button,args=[item])
                #placeholder.markdown(full_response)
            #placeholder.markdown(full_response)
            items = full_response.split('.')
            for data in items:
                st.button(data, on_click=click_button,args=[data])
    message = {"role": "assistant", "content": full_response}
    st.session_state.messages.append(message)
    