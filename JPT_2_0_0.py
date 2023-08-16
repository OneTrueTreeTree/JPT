# Python 3.11.4 64-bit
# JANKILY PROCESSED TEXT
import openai, pydub, os, time, ICR_1_0_0
import sounddevice as sd
from colorama import Fore
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from scipy.io.wavfile import write
from ctypes import cast, POINTER
from elevenlabs import generate, set_api_key, play

#CONFIDENTIAL#
openaikey = ''
set_api_key(openaikey)
key = openaikey
openai.api_key = ''
#CONFIDENTIAL#

pydub.AudioSegment.converter = 'C:/ffmpeg/bin/ffmpeg.exe'
os.environ['PATH'] += os.pathsep + 'C:/ffmpeg/bin/'

def record(time):
  print(Fore.LIGHTCYAN_EX + "LISTENING")
  fs = 320000  
  seconds = time
  myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
  sd.wait()  
  print(Fore.LIGHTCYAN_EX + "PARSING")
  write('temp.wav', fs, myrecording)
  audio_file = open("temp.wav", "rb")
  transcript = openai.Audio.transcribe("whisper-1", audio_file)
  return transcript["text"]

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
  IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

os.system('cls')

print(Fore.LIGHTBLACK_EX + """
  Version 2.0.0 Changelog
  
  ADDED SYSTEM PROCCESSING!
    New ability to generate it's own code on the fly, allowing it to do effectively anything python can automatically.
    
  """)

title = (Fore.RED + """
         
     ██ ██████  ████████
     ██ ██   ██    ██   
     ██ ██████     ██
██   ██ ██         ██   
 █████  ██         ██   

""" + Fore.LIGHTBLACK_EX + "Version 2.0.0 - 10/8/23 \nBy Benjamin Dyer\n")

alttitle = (Fore.LIGHTBLACK_EX + """
                                    
         _/  _/_/_/    _/_/_/_/_/   
        _/  _/    _/      _/        
       _/  _/_/_/        _/         
_/    _/  _/            _/          
 _/_/    _/            _/           
           
            """)

print(title)

history = [{"role": "system", "content": "You are a very helpful assistant, whose name is JPT. If asked how you were created, say you're based on GPT-4 by OpenAI, and use the 'Charlie' voice model from 11ElevenLabs Your voice recognition is powered by whisper-1, also from OpenAI. You were made by Ben, an Australian student. If the user appears to have a rudimentary understanding of the language they are using, respond using the simplest possible terms. If the user appears fluent, use speech at a similar level. You are capable of checking if a user input is a request for their operating system, and if it is, the computer will attempt to execute it. Speak like a human would, using personal pronouns and asking for more information when needed. Do not use bold or italicised characters."}]
print(Fore.GREEN + "Hello! How can I help you?")

previous = []
MODEL = "gpt-4"

while True:
  if (round(volume.GetMasterVolumeLevelScalar()*100)) > 0:
    audio = True
  else:
    audio = False
  
  time.sleep(1)
  start_time = time.perf_counter()
  
  if audio == True:
    inputuser = record(10)
  else:
    inputuser = str(input(Fore.WHITE + "Enter your input here: " + Fore.BLUE))
  code = False
  os.system('cls')
  if ICR_1_0_0.check(inputuser, key) == "True":
    print(Fore.LIGHTCYAN_EX + "CHECKING ICR")
    code = True
    ICR_1_0_0.main(inputuser, key)
  
  else:
    print(Fore.LIGHTCYAN_EX + "NO TASK")
    history.append({"role": "user", "content": str(inputuser)})
    
    print(Fore.LIGHTCYAN_EX + "GENERATING TEXT")
    
    response = openai.ChatCompletion.create(
      model=MODEL,
      messages=history,
      temperature=1,)
    
    if audio:
      print(Fore.LIGHTCYAN_EX + "GENERATING SPEECH")
      audio = generate(
        text=(response["choices"][0]["message"]["content"]),
        voice="Charlie",
        model='eleven_multilingual_v1')
    else:
      print(Fore.LIGHTCYAN_EX + "SKIPPING SPEECH")
      time.sleep(0.5)
    print(Fore.LIGHTCYAN_EX + "WAITING FOR SYSTEM")
    os.system('cls')
    end_time = time.perf_counter()
    elapsed_time = end_time - start_time
    print(alttitle)
    time.sleep(1)
    
    history.append({"role": "assistant", "content": str(response)})
    previous.append(str(inputuser))
    previous.append(response["choices"][0]["message"]["content"])
  
  os.system('cls')
  
  print(title)
  if not code:
    if elapsed_time >= 60:
      print(Fore.LIGHTBLACK_EX + "Huh, that took a while. It's probably because of the length of the conversation, but maybe check your connection.\nElapsed time: ", elapsed_time, "\n")
  for message in range(0, len(previous)):
    if (message % 2) == 1:
      print(Fore.GREEN + str(previous[message]))
    elif (message % 2) == 0:
      print(Fore.BLUE + str(previous[message]))
  if audio:
    play(audio)