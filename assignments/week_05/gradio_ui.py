import gradio as gr  # Importing the Gradio library to create a UI interface for the API
import requests  # To make HTTP requests to the agent API
import json  # To handle JSON data parsing

# Function to parse Server-Sent Events (SSE) from the response stream
def parse_sse(line):
    # SSE events start with "data:", we process those lines to extract content
    if line.startswith("data:"):
        try:
            # Strip "data:" and decode the JSON content
            return json.loads(line[5:].strip())
        except json.JSONDecodeError:
            # If there's an issue with decoding JSON, return None
            return None
    return None

# Function to extract and process content from a message
def extract_content(message):
    # If the message content is a list, process it for "text" and "tool_use"
    if isinstance(message.get("content"), list):
        for content_item in message["content"]:
            if content_item.get("type") == "text":
                # Yielding text content
                yield content_item.get("text", "")
            elif content_item.get("type") == "tool_use":
                # Yielding tool usage information as JSON
                yield f"\n**Tool Use:** {content_item.get('name', 'Unknown Tool')}\n"
                yield f"```json\n{json.dumps(content_item.get('partial_json', {}), indent=2)}\n```\n"
    # If content is a simple string, yield it directly
    elif isinstance(message.get("content"), str):
        yield message["content"]

# Function to call the API and handle the streaming response
def api_call(message):
    try:
        # Making a POST request to the agent API endpoint
        response = requests.post(
            "http://localhost:8123/runs/stream",  # The API endpoint URL
            headers={
                "Content-Type": "application/json",  # Specifying JSON content type
            },
            json={
                # Sending the message and assistant ID to the API
                "assistant_id": "agent",
                "input": {
                    "messages": [{"role": "user", "content": message}]
                },
                "metadata": {},
                "config": {"configurable": {}},
                "multitask_strategy": "reject",
                "stream_mode": ["values"],  # Streaming mode set to "values"
            },
            stream=True  # Enable streaming response
        )
        # Raise an HTTP error if the request was unsuccessful
        response.raise_for_status()

        # Variable to hold the final result
        result = ""

        # Iterating over the response stream lines
        for line in response.iter_lines():
            if line:
                # Decode the line from byte format
                line = line.decode('utf-8')

                # Handling different types of SSE events
                if line.startswith("event:"):
                    event_type = line.split(":", 1)[1].strip()
                    # Uncomment the line below if you want to display event types in the result
                    # result += f"\n\n**Event:** {event_type}\n\n"

                # Handling data events (the core message content)
                elif line.startswith("data:"):
                    data = parse_sse(line)  # Parse the SSE data line
                    if data and "messages" in data:
                        for message in data["messages"]:
                            # Handling AI messages
                            if message["type"] == "ai":
                                ai_message = ""
                                # Extracting content from AI message
                                for content in extract_content(message):
                                    ai_message += content
                                if ai_message:
                                    result += "**AI Message:** " + ai_message
                            
                            # Uncomment the blocks below to handle human or tool messages
                            # Handling human messages
                            # elif message["type"] == "human":
                            #     result += f"\n**Human:** {message['content']}\n\n"

                            # Handling tool messages
                            # elif message["type"] == "tool":
                            #     result += f"\n**Tool Result ({message['name']}):**\n"
                            #     result += f"```json\n{message['content']}\n```\n"
                    else:
                        # If the data is not in expected format, pretty-print it as JSON
                        prettified = json.dumps(data, indent=2)
                        result += f"```json\n{prettified}\n```\n"

        return result  # Return the final result

    # Exception handling for HTTP errors
    except requests.exceptions.HTTPError as http_err:
        return f"HTTP error occurred: {http_err}"
    
    # Exception handling for general request issues
    except requests.exceptions.RequestException as req_err:
        return f"Request error occurred: {req_err}"
    
    # Exception handling for invalid JSON responses
    except ValueError:
        return "Error: Invalid JSON response"

# Gradio interface function to interact with the API
def gradio_interface(message):
    return api_call(message)

# Gradio interface layout
with gr.Blocks() as demo:
    with gr.Row():  # Arrange UI components in a row
        with gr.Column():  # Input field for the user's message
            user_input = gr.Textbox(
                label="Your Message", placeholder="Enter your message here")
        
        with gr.Column():  # Output field for the AI's response
            result_output = gr.Textbox(label="Response", interactive=False)
    
    # Link the user input with the API call, and display the response
    user_input.submit(gradio_interface, inputs=user_input, outputs=result_output)

# Launch the Gradio interface
# Set `share=True` to generate a public link for sharing
# Be cautious not to expose sensitive data through the public link
demo.launch(share=False)
