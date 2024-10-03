import gradio as gr
import requests
import json

def parse_sse(line):
    if line.startswith("data:"):
        try:
            return json.loads(line[5:].strip())
        except json.JSONDecodeError:
            return None
    return None

def extract_content(message):
    if isinstance(message.get("content"), list):
        for content_item in message["content"]:
            if content_item.get("type") == "text":
                yield content_item.get("text", "")
            elif content_item.get("type") == "tool_use":
                yield f"\n**Tool Use:** {content_item.get('name', 'Unknown Tool')}\n"
                yield f"```json\n{json.dumps(content_item.get('partial_json', {}), indent=2)}\n```\n"
    elif isinstance(message.get("content"), str):
        yield message["content"]

def api_call(message):
    try:
        response = requests.post(
            "http://localhost:8123/runs/stream",
            headers={
                "Content-Type": "application/json",
            },
            json={
                "assistant_id": "agent",
                "input": {
                    "messages": [{"role": "user", "content": message}]
                },
                "metadata": {},
                "config": {"configurable": {}},
                "multitask_strategy": "reject",
                "stream_mode": ["values"],
            },
            stream=True
        )
        response.raise_for_status()
        result = ""
        for line in response.iter_lines():
            if line:
                line = line.decode('utf-8')
                if line.startswith("event:"):
                    event_type = line.split(":", 1)[1].strip()
                    # un comment this line if in the output you want to see event types
                    # result += f"\n\n**Event:** {event_type}\n\n"
                elif line.startswith("data:"):
                    data = parse_sse(line)
                    if data and "messages" in data:
                        for message in data["messages"]:
                            if message["type"] == "human":
                                # un comment this line if in the output you want to see human messages
                                pass
                                # result += f"\n**Human:** {message['content']}\n\n"
                            elif message["type"] == "ai":
                                ai_message = ""
                                for content in extract_content(message):
                                    ai_message += content
                                if ai_message:
                                    result += "**AI Message:** " + ai_message
                            elif message["type"] == "tool":
                                # un comment this block if in the output you want to see the tool messages
                                pass
                                # result += f"\n**Tool Result ({message['name']}):**\n"
                                # result += f"```json\n{message['content']}\n```\n"
                    else:
                        prettified = json.dumps(data, indent=2)
                        result += f"```json\n{prettified}\n```\n"
        return result
    except requests.exceptions.HTTPError as http_err:
        return f"HTTP error occurred: {http_err}"
    except requests.exceptions.RequestException as req_err:
        return f"Request error occurred: {req_err}"
    except ValueError:
        return "Error: Invalid JSON response"
    
# Gradio Interface
def gradio_interface(message):
    return api_call(message)

with gr.Blocks() as demo:
    with gr.Row():
        with gr.Column():
            user_input = gr.Textbox(
                label="Your Message", placeholder="Enter your message here")
        with gr.Column():
            result_output = gr.Textbox(label="Response", interactive=False)
    user_input.submit(gradio_interface, inputs=user_input,
                    outputs=result_output)
    
# set share = True to enable sharing
# It will generate a public link to share the interface
# Make sure there is no sensitive information in the interface
demo.launch(share=False)