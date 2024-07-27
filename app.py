from llm import handle_chat
import gradio as gr

# print(handle_chat(file='Medical_book.pdf', question='what is this book about'))
# print(normal_chat("what is today date "))

ui = gr.Interface(
    fn=handle_chat,              
    inputs=[gr.File(), 'text'],  
    outputs=gr.Textbox(lines=10),              
    title="Chatbot",        
    description="Upload a PDF file and ask a question to get an answer, or ask a question directly.",
    theme=gr.themes.Base()
)

ui.launch()