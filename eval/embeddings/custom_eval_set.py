from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
import matplotlib.pyplot as plt
import os
from scipy.spatial.distance import cosine
import streamlit as st


model_service = os.getenv("MODEL_ENDPOINT",
                          "http://localhost:8001")
model_service = f"{model_service}/v1"

embedding_model = os.getenv("EMBEDDING_MODEL",
                            "BAAI/bge-base-en-v1.5")

def get_embedding(string, e):
    embeddings = e.embed_query(string)
    return embeddings


st.title("📊 Create Custom LLM Eval Set")  

if "Question" not in st.session_state:
    st.session_state["Question"] = "What is the Higgs Boson?"

if "Answers" not in st.session_state:
    st.session_state["Answers"] = {}
    st.session_state["Answers"]["Right_Answer_1"] = "The Higgs boson, sometimes called the Higgs particle, is an elementary particle in the Standard Model of particle physics produced by the quantum excitation of the Higgs field, one of the fields in particle physics theory"
    st.session_state["Answers"]["Wrong_Answer_1"] = "Alan Turing was the first person to conduct substantial research in the field that he called machine intelligence."

st.session_state["Question"] = st.text_input(label="Question", value=st.session_state["Question"])

col1,col2,col3 = st.columns(3)
with col1:
    st.session_state["Answers"]["Right_Answer_1"] = st.text_input("Right Answer 1", 
                                                      value=st.session_state["Answers"]["Right_Answer_1"])
with col2:
    st.session_state["Answers"]["Right_Answer_2"] = st.text_input("Right Answer 2")

with col3:
    st.session_state["Answers"]["Right_Answer_3"] = st.text_input("Right Answer 3")


col1,col2,col3 = st.columns(3)
with col1:
     st.session_state["Answers"]["Wrong_Answer_1"] = st.text_input("Wrong Answer 1", 
                                                                  value=st.session_state["Answers"]["Wrong_Answer_1"])
with col2:
    st.session_state["Answers"]["Wrong_Answer_2"] = st.text_input("Wrong Answer 2")
with col3:
    st.session_state["Answers"]["Wrong_Answer_3"] = st.text_input("Wrong Answer 3")


text = {k:[v] for (k,v) in st.session_state["Answers"].items() if v != ""}
text["Question"] = [st.session_state["Question"]]
e = SentenceTransformerEmbeddings(model_name=embedding_model)

for t in text.keys():
    text[t].append(get_embedding(text[t][0],e))

answer_embedding = text["Question"][1]

for t in text.keys():
    question_embedding = text[t][1]
    distance = cosine(answer_embedding, question_embedding)
    text[t].append(round(distance,3))

distances = [text[key][2] for key in text.keys()]
ones = [1]* len(distances)
fig = plt.figure()
plt.vlines(1,.001,1)
plt.scatter(ones, distances)
for key in text.keys():
   plt.annotate(key,(1, text[key][2]))
plt.xticks([])
plt.ylabel("Cosine Similarity")
st.pyplot(fig)

submit = st.button("Check Against Model")
if submit:
    llm = ChatOpenAI(base_url=model_service, 
        api_key="sk-no-key-required")
    
    prompt = ChatPromptTemplate.from_messages([
    ("system", "You are world class technical advisor."),
    ("user", "{input}")])

    chain = LLMChain(llm=llm, 
                prompt=prompt,
                verbose=False,)
     
    response = chain.invoke(st.session_state["Question"])
    st.session_state["Answers"]["LLM Response"] = response["text"]
    st.markdown(st.session_state["Answers"]["LLM Response"])
    st.rerun()
    