from llm import handle_chat
import gradio as gr

# print(handle_chat(file='Medical_book.pdf', question='what is this book about'))
# print(normal_chat("what is today date "))

ui = gr.Interface(
    fn=handle_chat,              
    inputs=[gr.File(), 'text'],  
    outputs=gr.Textbox(lines=14),              
    title="Chatbot",        
    description="Upload a PDF file and ask a question to get an answer, or ask a question directly.",
    theme=gr.themes.Default( primary_hue="violet",
    secondary_hue="violet",)
)

ui.launch(server_name="0.0.0.0", server_port=3000)

