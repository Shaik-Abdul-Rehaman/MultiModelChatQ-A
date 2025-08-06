from fastapi import FastAPI
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from src.logger.logger import setup_logger  
from src.models.GroqLLM import GroqLLM
from src.models.AzureLLM import AzureLLM
from langgraph.checkpoint.memory import MemorySaver
from pydantic import BaseModel, Field
from src.graphs.Graph_builder import GraphBuilder
from langchain_core.messages import HumanMessage,SystemMessage
import uvicorn




load_dotenv()
logger = setup_logger()

app = FastAPI()

@app.get("/health")
async def health_status():
    logger.info("logging started, system is in healthy state")
    return JSONResponse(content={"status": "200", "content": "system is healthy"})


# Initialize components during startup
@app.on_event("startup")
async def startup_event():
    logger.info("Initializing application components")
    groq_obj = AzureLLM()
    llm = groq_obj.get_llm()
    memory_saver = MemorySaver()
    builder = GraphBuilder(llm=llm, memory=memory_saver)
    app.state.qa_graph = builder.build_QA_graph()
    logger.info("Application components initialized")





###############################################################  Response API Started ##############################################################



class InputRequest(BaseModel):
    student_id: str = Field(..., example="stu_123")
    video_title: str = Field(..., example="Introduction to Recursion")
    video_summary: str = Field(..., example="This video covers the concept of recursion...")
    student_question: str = Field(..., example="Why does recursion give a memory error?")
    
    
    
@app.post('/ask_assistant')
async def ask_assistant(request: InputRequest):
    logger.info("response api is triggered")
    
    # Load pre-built LangGraph
    qa_graph = app.state.qa_graph  

    session_id = request.student_id
    config = {"configurable": {"thread_id": session_id}}

    # Check if this is a new session — use a simple session tracker
    # You can use Redis, a DB, or a Python dict for this (here we use app state for simplicity)
    if not hasattr(app.state, "active_sessions"):
        app.state.active_sessions = set()

    is_new_session = session_id not in app.state.active_sessions

    messages = []

    if is_new_session:
        # Add system message only once
        messages.append(SystemMessage(content=f"""
        You are an AI tutor on an edtech platform.

        Video Title: {request.video_title}  
        Video Summary: {request.video_summary}  

        Instructions:
        - Focus only on answering the question clearly and accurately.
        - Do not add greetings, compliments, or closing remarks.
        - Base your response primarily on the video content; use external knowledge only if needed for clarity.
        - If the question is slightly off-topic, give a concise answer and guide back to the video topic.
        - If the question is vague, respond with a clarifying prompt.

        Provide only the answer below:
        """))
        app.state.active_sessions.add(session_id)

    # Add the student's question as HumanMessage
    messages.append(HumanMessage(content=request.student_question))

    # Call the graph with the constructed message
    result = qa_graph.invoke({"messages": messages}, config=config)

    return JSONResponse(content={
        "status_code": 200,
        "student_id": request.student_id,
        "question": request.student_question,
        "answer": result["response"]
    })

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
