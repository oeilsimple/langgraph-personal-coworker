import gradio as gr
from sidekick import Sidekick


async def setup():
    sidekick = Sidekick() # Initialize a new Sidekick instance
    await sidekick.setup() # Setup the new instance (This is an async function)
    return sidekick


async def process_message(sidekick, message, success_criteria, history):
    results = await sidekick.run_superstep(message, success_criteria, history)
    return results, sidekick

async def reset():
    new_sidekick = Sidekick() # Initialize a new Sidekick instance
    await new_sidekick.setup() # Setup the new instance (This is an async function)
    return "", "", None, new_sidekick

# Cleanup function to free resources when the state object is deleted
def free_resources(sidekick):
    print("Cleaning up")
    try:
        if sidekick:
            sidekick.cleanup()
    except Exception as e:
        print(f"Exception during cleanup: {e}")


with gr.Blocks(title="Sidekick", theme=gr.themes.Default(primary_hue="emerald")) as ui:
    gr.Markdown("## Sidekick Personal Co-Worker")

    # Gradio state is used to hold an application state object
    # Whenever this UI is reset, the delete_callback is triggered for the state object to free resources
    # This ensures the application can maintain it's state across multiple interactions without stale instances
    sidekick = gr.State(delete_callback=free_resources) 

    with gr.Row():
        chatbot = gr.Chatbot(label="Sidekick", height=300, type="messages")
    with gr.Group():
        with gr.Row():
            message = gr.Textbox(show_label=False, placeholder="Your request to the Sidekick")
        with gr.Row():
            success_criteria = gr.Textbox(
                show_label=False, placeholder="What are your success critiera?"
            )
    with gr.Row():
        reset_button = gr.Button("Reset", variant="stop")
        go_button = gr.Button("Go!", variant="primary")

    ui.load(setup, [], [sidekick]) # Calls setup function to initialize the Sidekick instance and store it in the state object
    message.submit(
        process_message, [sidekick, message, success_criteria, chatbot], [chatbot, sidekick]
    )
    success_criteria.submit(
        process_message, [sidekick, message, success_criteria, chatbot], [chatbot, sidekick]
    )
    go_button.click(
        process_message, [sidekick, message, success_criteria, chatbot], [chatbot, sidekick]
    )
    reset_button.click(reset, [], [message, success_criteria, chatbot, sidekick])


ui.launch(inbrowser=True)
