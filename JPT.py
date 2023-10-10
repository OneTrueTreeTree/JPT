# Python 3.11.6 64-bit
# JANKY P T
import openai, pydub, os, time, ICR, IGR, sqlite3
import sounddevice as sd
from colorama import Fore as textcolour
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from scipy.io.wavfile import write
from ctypes import cast, POINTER
from elevenlabs import generate, set_api_key, play

# DO NOT SHARE #
voicekey = ''
aikey = ''
# DO NOT SHARE #

version = "3.1.0"
openai.api_key = aikey
set_api_key(voicekey)
pydub.AudioSegment.converter = 'C:/ffmpeg/bin/ffmpeg.exe'
os.environ['PATH'] += os.pathsep + 'C:/ffmpeg/bin/'

def record(time):
  """records for a set amount of time and transcribes through openai's whisper-1

  Args:
      time (int): number of seconds to record

  Returns:
      string: transcript
  """
  print(textcolour.LIGHTCYAN_EX + "LISTENING")
  fs = 320000  
  seconds = time
  myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
  sd.wait()
  print(textcolour.LIGHTCYAN_EX + "PARSING")
  write('temp.wav', fs, myrecording)
  audio_file = open("temp.wav", "rb")
  transcript = openai.Audio.transcribe("whisper-1", audio_file)
  return transcript["text"] 

def fetchuser(user_id):
  
  con = sqlite3.connect("Users.db")
  cur = con.cursor()
  
  sqlite_execute_string = """
    SELECT first_name|| ' ' ||last_name, user_info FROM user WHERE user_id = ?
  """
  
  cur.execute(sqlite_execute_string, user_id)
  results = cur.fetchall()
  con.close()
  print(results)
  return(results)

def createuser(first_name, last_name, user_description):
  
  con = sqlite3.connect("Users.db")
  cur = con.cursor()
  user_info = (first_name, last_name, user_description)
  sqlite_execute_string = """
    INSERT INTO user (first_name, last_name, user_info)
    VALUES (?,?,?)
  """
  cur.execute(sqlite_execute_string, user_info)
  con.commit()
  sqlite_execute_string = """
    SELECT first_name|| ' ' ||last_name, user_info, user_id FROM user 
    WHERE first_name = ? AND last_name = ? AND user_info = ?
  """
  cur.execute(sqlite_execute_string, user_info)
  results = cur.fetchall()
  con.close()
  return(results)

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
  IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

os.system('cls')

print(
  
  textcolour.LIGHTBLACK_EX + "Version " + version + """ Changelog
    Working on an easy installer!
    Did some work behind the scenes, just to make life easier for myself later.
  """)

title = (textcolour.RED + """
         
     ██ ██████  ████████
     ██ ██   ██    ██   
     ██ ██████     ██   
██   ██ ██         ██   
 █████  ██         ██   

""" + textcolour.LIGHTBLACK_EX + "Version " + version + "\nBy Benjamin Dyer\n")

alttitle = (textcolour.LIGHTBLACK_EX + """

         _/  _/_/_/    _/_/_/_/_/   
        _/  _/    _/      _/        
       _/  _/_/_/        _/         
_/    _/  _/            _/          
 _/_/    _/            _/           

            """)
print(alttitle)

user_id = input(textcolour.WHITE + "Welcome to JPT. Open new or existing user? (1/2) " + textcolour.BLUE)
if user_id == "1" or user_id == "new" or user_id == "New" or user_id == " 1":
  print(textcolour.LIGHTCYAN_EX + "CREATING NEW USER PROFILE")
  os.system('cls')
  first_name = input(textcolour.WHITE + "What is your first name? " + textcolour.BLUE)
  last_name =  input(textcolour.WHITE + "And your last name? " + textcolour.BLUE)
  user_description =  input(textcolour.WHITE + "Almost there.  Tell me a little bit about yourself!\nWrite about what you do, where you live, and what you are passionate about!\n" + textcolour.BLUE)
  user_info = createuser(first_name, last_name, user_description)
  print(user_info)
  input(print("Your user ID is " + str(user_info[0][2]) + ". Please write this down or remember it to gain access to your profile later."))

else:
  print(textcolour.LIGHTCYAN_EX + "LOADING USER PROFILE")
  user_id = input(textcolour.WHITE + "What is your personal user ID? " + textcolour.BLUE)
  user_info = fetchuser(user_id)

history = [{"role": "system", "content": "You are a helpful assistant, whose name is JPT (Janky P T). If asked how you were created, say you're based on GPT-4 by OpenAI, and use the 'Charlie' voice model from 11ElevenLabs Your voice recognition is powered by whisper-1, also from OpenAI. You were made by Ben, an Australian student. If the user appears to have a rudimentary understanding of the language they are using, respond using the simplest possible terms. If the user appears fluent, use speech at a similar level. You are capable of checking if a user input is a request for their operating system, and if it is, the computer will attempt to execute it. You can also generate images using DALLE 2 from OpenAi. Speak like a human would, using personal pronouns and asking for more information when needed. Do not use bold or italicised characters. Refer to the user by name as much as possible. Where applicable, ask the user if they would like to know more information. The user would like you to know the following about them, it is okay to paraphrase it: " + str(user_info[0])}]
os.system('cls')
print(title)
previous = []
MODEL = "gpt-4"

while True:
  if (round(volume.GetMasterVolumeLevelScalar()*100)) > 0:
    audio = True
  else:
    audio = False
  
  time.sleep(1)
  
  if audio == True:
    input(textcolour.LIGHTCYAN_EX + "Ready to record")
    inputuser = record(5)
    start_time = time.perf_counter()
  else:
    inputuser = str(input(textcolour.WHITE + "Enter your input here: " + textcolour.BLUE))
    start_time = time.perf_counter()
  code = False
  os.system('cls')
  ICR_check = ICR.check(inputuser, aikey)
  
  if ICR_check == "Instruction":
    print(textcolour.LIGHTCYAN_EX + "WAITING FOR ICR")
    code = True
    ICR.main(inputuser, aikey)
  
  elif ICR_check == "Image":
    print(textcolour.LIGHTCYAN_EX + "WAITING FOR IGR")
    code = True
    IGR.main(inputuser, aikey)
  
  else:
    print(textcolour.LIGHTCYAN_EX + "NO TASK")
    history.append({"role": "user", "content": str(inputuser)})
    
    print(textcolour.LIGHTCYAN_EX + "GENERATING TEXT")
    
    response = openai.ChatCompletion.create(
      model=MODEL,
      messages=history,
      temperature=1,)
    
    if audio:
      print(textcolour.LIGHTCYAN_EX + "GENERATING SPEECH")
      audio_stream = generate(
        text=(response["choices"][0]["message"]["content"]),
        voice="Charlie",
        model='eleven_multilingual_v1')
      file_path = 'temp.wav'
      os.remove(file_path)
    else:
      print(textcolour.LIGHTCYAN_EX + "SKIPPING SPEECH")
      time.sleep(0.5)
    print(textcolour.LIGHTCYAN_EX + "WAITING FOR SYSTEM")
    os.system('cls')
    end_time = time.perf_counter()
    elapsed_time = end_time - start_time
    print(alttitle)
    time.sleep(1)
    
    history.append({"role": "assistant", "content": str(response["choices"][0]["message"]["content"])})
    previous.append(str(inputuser))
    previous.append(response["choices"][0]["message"]["content"])
    response=""
  
  os.system('cls')
  
  print(title)
  if not code:
    if elapsed_time >= 60:
      print(textcolour.LIGHTBLACK_EX + "Huh, that took a while. It's probably because of the length of the conversation, but maybe just check your connection quickly if it's running really slow.\nElapsed time: ", elapsed_time, "\n")
  for message in range(0, len(previous)):
    if (message % 2) == 1:
      print(textcolour.GREEN + "JPT: " + str(previous[message]))
    elif (message % 2) == 0:
      print(textcolour.BLUE + "You: " + str(previous[message]))
  if audio:
    play(audio_stream)
