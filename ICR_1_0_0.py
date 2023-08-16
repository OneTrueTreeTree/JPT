# Python 3.11.4 64-bit
# INTERACTION CHECK & RUN
import openai, os, subprocess
from colorama import Fore

def check(possible_instruction, key):
    print(Fore.LIGHTCYAN_EX + "CHECKING FOR TASK")
    openai.api_key = key
    prompt = [{"role": "system", "content": "Your only job is to determine whether a statement conveys an instruction a computer is intended to follow. ONLY reply with 'True' or 'False'. For example, 'Tell me about cheese', or 'Hey there!' should return False, whereas 'Open program.exe from my desktop', or 'Google xyz' should return True."}]
    prompt.append({"role": "user", "content": str(possible_instruction)})
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages = prompt,
    )
    return(response["choices"][0]["message"]["content"])

def instruct(possible_instruction, key):
    print(Fore.LIGHTCYAN_EX + "BUILDING TASK")
    openai.api_key = key
    prompt = [{"role": "system", "content": "Your only job is to deconstruct an instruction to a computer into multiple steps that could be followed by a programmer. Do nothing but this. Do not comment on the steps. For example, if the user stated 'open file.exe from my desktop', an output may be: '1, Find desktop folder on computer. 2. Find file.exe. 3, Run file.exe using relevant program.' Do not say things like 'Double click on x', as a program running natively on the computer would not do this. Do not print instructions across multiple lines."}]
    prompt.append({"role": "user", "content": str(possible_instruction)})
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages = prompt,
    )
    return(response["choices"][0]["message"]["content"])

def generate(possible_instruction, key):
    print(Fore.LIGHTCYAN_EX + "FINALISING TASK")
    openai.api_key = key
    prompt = [{"role": "system", "content": "Your only job is to generate python code to perform the action the user desires on a windows operating system. Do not comment within, or provide output from the program unless it is strictly required. When googling or searching for something, using webbrowser.open with the search query is preferred. DO NOT put quotes around the whole program. Output NOTHING but the code, do not provide an explanation of the code."}]
    prompt.append({"role": "user", "content": str(possible_instruction)})
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages = prompt,
        temperature=0,
    )
    return(response["choices"][0]["message"]["content"])

def main(possible_instruction, key):
    print(Fore.LIGHTCYAN_EX + "TASK IDENTIFIED")
    instruction = instruct(possible_instruction, key)
    code = generate(instruction, key)
    run(code)


def run(code):
    print(Fore.LIGHTCYAN_EX + "RUNNING TASK")
    current_working_directory = os.getcwd()
    filename = os.path.join(current_working_directory, 'temp.py')
    with open(filename, 'w') as file:
        file.write(code)
    subprocess.run(['python', filename])

if __name__ == "__main__":
    print(main(input("DEBUG: "), ""))