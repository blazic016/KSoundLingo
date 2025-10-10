# About script

**KSoundLingo** is a Python-based tool that converts **words and phrases** into **audio files**. It is designed for language learners who want to easily transform written vocabulary into spoken form, making it simple to practice listening, pronunciation, and memorization.


This script reads phrases from input.txt and converts them into an audio MP3 file.
It is important to have character `-` between serbian and hungarian language.


# Install requirments

`pip install -r requirements.txt`



# Struct of directories

```javascript
ksoundlingo/
├─ requirements.txt
├─ pyproject.toml              
└─ kslingo/                     
   ├─ __init__.py
   ├─ __main__.py               
   ├─ cli.py                    
   ├─ version.py
   ├─ utils/
   │  ├─ __init__.py
   │  └─ fs.py                  
   ├─ audio/
   │  ├─ __init__.py
   │  └─ tts.py                 
   └─ parsers/
      ├─ __init__.py
      ├─ txt.py                 
      └─ markdown.py            
```

# How to run?

**CHECK VERSION**

Example:
```bash
python3 -m kslingo --version
```

**AUDIO TXT MODE**

With option --txt it is read from the txt file, and store mp3 in simple.mp3 file

Example:
```bash
python3 -m kslingo audio --txt ./templates/template.txt --learn hu --native sr
&& ffplay output/simple.mp3
```

**AUDIO MARKDOWN MODE**

Example:
```bash
python3 -m kslingo audio --markdown ./templates/template_hu.md --learn hu --native sr
```

**CONVERT JSON to MARKDOWN**

Example:
```bash
python3 -m kslingo convert json2md ./templates/template.json --learn hu --native sr
```

**CONVERT MARKDOWN to JSON**

Example:
```bash
python3 -m kslingo convert md2json ./templates/template_hu.md --learn hu --native sr
```

**ADD PREFIX ON MARKDOWN**
Default prefix is: `%%A2,W,D%%`
Example:
```bash
python3 -m kslingo convert prefix Madjarski-ksound.md 
```


# How to build source code?

LINUX

```bash
pyinstaller --clean -F main.py -n lang-audio-gen \
  --add-data "assets/end_sound.wav:assets" \
  --add-binary "/usr/lib/x86_64-linux-gnu/libpython3.10.so.1.0:."
```


WINDOWS

```bash
pyinstaller --onefile --name lang-audio-gen ^
  --add-data "assets\end_sound.wav;assets" ^
  main.py
```


Under the `dist` directory there is a executable file `lang-audio-gen`


FOR ME:

```bash
cp dist/lang-audio-gen ~/Mega/bin/
# run slef bash command
generisi_madjarski_mp3
```


# ABOUT JSON
- The **category** always be presented in markdown, and always be generated sound translation.
That is the reason why not presneted in category *(.josn file)* field like: `level, enabled, isword`. Every category have translation for every defined language.


