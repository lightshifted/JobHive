from bs4 import BeautifulSoup
from termcolor import colored
from pprint import pprint
import json


def display_children(input_dict: dict):
    # Extract the agent profiles from the input dictionary
    agent_profiles = input_dict["agent_profiles"]

    # Split the input string into individual child summaries
    summaries = agent_profiles[0].split('\n\n\n')

    # Loop through each child summary and extract its components
    for summary in summaries:
        lines = summary.split('\n')
        id_value = lines[0].split()[1]
        name_value = lines[1].split()[1]
        print(colored("\n 🤖 Child Summary 🤖", "yellow"))
        print(colored("ID: ", "green") + colored(id_value, "grey"))
        print(colored("Name: ", "cyan") + colored(name_value, "white"))
        print(colored("Traits: ", "cyan") + lines[2].split(':')[1].strip())
        print(colored("Task: ", "red") + lines[3].split(':')[1].strip())
        print(colored("Working Memory: ", "red") + lines[4].split(':')[1].strip())
        print()


def display_memories(input_dict: dict):
    # Extract the agents' memories from the input dictionary
    agent_memories = input_dict["memory_contents"]

    # Loop through the list of memories:
    for content in agent_memories:

        # Split the input string into individual agent memories
        memories = content.split('\n\n\n')

        try:
            for memory in memories:
                lines = memory.split('\n')
                memory_id = lines[0].split()
                thought_value = lines[1].split(':')[1]
                reasoning_value = lines[2].split(':')[1]
                action_value = lines[3].split(':')[1]
                action_input_value = lines[4].split(':')[1]
                action_output_value = lines[5:]
                print(colored("\n 🧠 Agent Memory 🧠"))
                print(colored("Thought: ", "cyan") + thought_value)
                print(colored("Reasoning: ", "cyan") + reasoning_value)
                print(colored("Action: ", "cyan") + action_value)
                print(colored("Action Input: ", "cyan") + action_input_value)
                print(colored("Action Output: ", "cyan") + action_output_value[0])
        except IndexError:
            pass

def display_results(input_dict: dict):
    agent_results = input_dict["results"][1]
    confidence = agent_results['confidence']
    speak = agent_results[1]['speak']
    result = agent_results[1]['result']
    print(colored("\n 📊 Agent Results 📊", "yellow"))
    print(colored("Confidence: ", "cyan") + colored(confidence, "grey"))
    print(colored("Speak: ", "cyan") + colored(speak, "white"))
    print(colored("Result: ", "cyan") + colored(result, "white"))
    print()