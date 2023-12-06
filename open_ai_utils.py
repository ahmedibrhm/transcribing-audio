from openai import OpenAI
import re
import uuid

client = OpenAI()
# Step 1: Create an Assistant
my_assistant = client.beta.assistants.create()

my_thread = client.beta.threads.create()

def get_openai_response(messages):
    # Step 3: Add a Message to a Thread
    my_thread_message = client.beta.threads.messages.create(
    thread_id=my_thread.id,
    role="user",
    content=messages,
    )

    # Step 4: Run the Assistant
    my_run = client.beta.threads.runs.create(
    thread_id=my_thread.id,
    assistant_id=my_assistant.id,
    )

    # Step 5: Periodically retrieve the Run to check on its status to see if it has moved to completed
    while my_run.status != "completed":
        keep_retrieving_run = client.beta.threads.runs.retrieve(
            thread_id=my_thread.id,
            run_id=my_run.id
        )

        if keep_retrieving_run.status == "completed":
            print("\n")
            break

    # Step 6: Retrieve the Messages added by the Assistant to the Thread
    all_messages = client.beta.threads.messages.list(
    thread_id=my_thread.id
    )
    return all_messages.data[0].content[0].text.value


def convert_audio_text(audio_path, language='', prompt=''):
    # use OPENAI API to convert audio to text
    file = open(audio_path, "rb")
    print('file', file)
    transcript = client.audio.transcriptions.create(model="whisper-1", file=file, response_format="text", language=language, prompt=prompt)
    return transcript

def convert_text_audio(text):
    # use OPENAI API to convert text to audio
    print('hhh', text)
    response = client.audio.speech.create(
        model="tts-1",
        voice="shimmer",
        input=text,
    )

    file_name = str(uuid.uuid4()) + ".mp3"
    response.stream_to_file(file_name)
    return file_name

    