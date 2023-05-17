import os
import json
import shutil
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import threading

from agent_actors.run import JobHive

from utils.style_outputs import (
    display_children,
    display_memories,
    display_results,
)

app = FastAPI()

# Configure CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # client-side application domain(s)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def activate_agents():
    def run_jobhive():
        job_hive = JobHive()
        try:
            job_hive.run()
        except Exception as e:
            print(f"500 - Error activating agents: {e}")
        except KeyboardInterrupt:
            print("Tasks were interrupted by user")

    thread = threading.Thread(target=run_jobhive)
    thread.start()

    return {"message": "Agents' tasks have started!"}


@app.post('/api/file-upload')
async def upload_file(file: UploadFile = File(...)):
    if file:
        # Emptying the source_docs directory
        dir_path = "./client_data/documents"
        for file_name in os.listdir(dir_path):
            os.remove(os.path.join(dir_path, file_name))

        # file_path = "../agent-actors/client_data/documents/" + secure_filename(filename)
        file_path = "./client_data/documents/doc.pdf"
        # Saving pdf for use with Chroma
        with open(file_path, 'wb') as f:
            shutil.copyfileobj(file.file, f)

        activate_agents()

    return {"message": "200 - File uploaded successfully"}

@app.get('/api/activate')
def start_agents():
    print("Agents activated")
    JobHive().run()
    return {"message": "200 - Agents' tasks are complete!"}


@app.get('/api/user-profile')
async def get_task():
    directory_path = "./client_data/agent_interactions"
    matching_files = []
    memory_contents = []

    # Loop through all files in directory
    for file_name in os.listdir(directory_path):
        if file_name.startswith("input_") and file_name.endswith(".json"):
            file_path = os.path.join(directory_path, file_name)

            # Check if file is a dictionary with key "task"
            with open(file_path, "r") as file:
                try:
                    data = json.load(file)
                except json.JSONDecodeError:
                    continue
                if isinstance(data, dict) and "task" in data:
                    matching_files.append(file_path)
                    task_parts = data["task"].split(":")
                    if len(task_parts) < 2:
                        # Skip this task if it cannot be split into at least two parts
                        continue
                    task_value = task_parts[1].strip() # remove whitespace before first character of second element
                    memory_contents.append(task_value)

    # Return matching files' memory_content as JSON
    response_data = {"matching_files": matching_files, "memory_contents": memory_contents}
    return response_data


@app.get('/api/agent-memories')
async def crawl_directory():
    directory_path = "./client_data/agent_interactions"
    matching_files = []
    memory_contents = []

    # Loop through all files in directory
    for file_name in os.listdir(directory_path):
        if file_name.startswith("input_") and file_name.endswith(".json"):
            file_path = os.path.join(directory_path, file_name)

            # Check if file is a dictionary with key "memory_content"
            with open(file_path, "r") as file:
                try:
                    data = json.load(file)
                except json.JSONDecodeError:
                    continue
                if isinstance(data, dict) and "memory_content" in data:
                    matching_files.append(file_path)
                    memory_contents.append(data["memory_content"])

    # Return matching files' memory_content
    response_data = {"matching_files": matching_files, "memory_contents": memory_contents}
    return display_memories(response_data)


@app.get('/api/agent-profiles')
async def agent_profiles():
    directory_path = "./client_data/agent_interactions"
    matching_files = []
    agent_profiles = []

    # Loop through all files in directory
    for file_name in os.listdir(directory_path):
        if file_name.startswith("input_") and file_name.endswith(".json"):
            file_path = os.path.join(directory_path, file_name)

            # Check if file is a dictionary with key "memory_content"
            with open(file_path, "r") as file:
                try:
                    data = json.load(file)
                except json.JSONDecodeError:
                    continue
                if isinstance(data, dict) and "child_summary" in data:
                    matching_files.append(file_path)
                    agent_profiles.append(data["child_summary"])

    # Return matching files' memory_content
    response_data = {"matching_files": matching_files, "agent_profiles": agent_profiles}
    return display_children(response_data)


@app.get('/api/results')
async def get_results():
    directory_path = "./client_data/agent_interactions"
    matching_files = []
    results = []

    # Loop through all files in directory
    for file_name in os.listdir(directory_path):
        if file_name.startswith("output_") and file_name.endswith(".json"):
            file_path = os.path.join(directory_path, file_name)

            # Check if file is a dictionary with key "memory_content"
            with open(file_path, "r") as file:
                try:
                    data = json.load(file)
                except json.JSONDecodeError:
                    continue
                if isinstance(data, dict) and "json" in data:
                    matching_files.append(file_path)
                    results.append(data["json"])

    response_data = {"matching_files": matching_files, "results": results}
    return display_results(response_data)


@app.get('/api/tasks')
async def get_results():
    directory_path = "./client_data/agent_interactions"
    matching_files = []
    results = []

    # Loop through all files in directory
    for file_name in os.listdir(directory_path):
        if file_name.startswith("output_") and file_name.endswith(".json"):
            file_path = os.path.join(directory_path, file_name)

            # Check if file is a dictionary with key "memory_content"
            with open(file_path, "r") as file:
                try:
                    data = json.load(file)
                except json.JSONDecodeError:
                    continue
                if isinstance(data, dict) and "json" in data:
                    matching_files.append(file_path)
                    results.append(data["json"])

    response_data = {"matching_files": matching_files, "results": results}
    return response_data
