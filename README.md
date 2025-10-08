# About script

**KSoundLingo** is a Python-based tool that converts **words and phrases** into **audio files**. It is designed for language learners who want to easily transform written vocabulary into spoken form, making it simple to practice listening, pronunciation, and memorization.


This script reads phrases from input.txt and converts them into an audio MP3 file.
It is important to have character `-` between serbian and hungarian language.

# How to run?

**CHECK VERSION**

Example: `py main.py --version `


**SIMPLE MODE**

With option --simple it is read from the input.txt file, and store mp3 in simple.mp3 file

Example: `py main.py --simple  && ffplay simple.mp3 `


**MARKDOWN MODE**

Example:

```bash
py magyar_audio_generator.py \
   --markdown ~/Mega/Beleske/OBSIDIAN/Readme-OBS/MADJARSKI.md \
   --output ~/Music/Madjarski
   --learn hu \
   --native sr
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


