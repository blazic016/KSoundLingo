****# About script

**KSoundLingo** is a Python-based tool that converts **words and phrases** into **audio files**. It is designed for language learners who want to easily transform written vocabulary into spoken form, making it simple to practice listening, pronunciation, and memorization.


This script reads phrases from input.txt and converts them into an audio MP3 file.
It is important to have character `-` between serbian and hungarian language.


# Install requirments

```bash
pip install -r requirements.txt
```

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

### CHECK VERSION

*Example:*
```bash
python3 -m kslingo --version
```

### AUDIO TXT MODE

*Example:*
```bash
python3 -m kslingo audio --txt ./templates/template.txt --learn hu --native sr
&& ffplay output/simple.mp3
```

### AUDIO MARKDOWN MODE

*Example:*
```bash

python3 -m kslingo audio \
	--markdown ksltest/ksl-vault/English-kslt.md
	-learn en -native sr
	
```

### CONVERT JSON to MARKDOWN

*Example:*
```bash
python3 -m kslingo convert json2md \
	 -i ./output/md2json.json \
	-learn en -native sr
```

### CONVERT MARKDOWN to JSON

*Example:*
```bash
python3 -m kslingo convert md2json \
	-i ksltest/ksl-vault/English-kslt.md \
	-learn en -native sr
	
python3 -m kslingo convert md2json \
	-i ../KSoundLingo-phw/Obsidian/KSoundLingo-Vault/Madjarski-ksound.md\
	-learn hu -native sr
	
```

### ADD PREFIX ON MARKDOWN
Default prefix is: `%%A2,W,D%%`

*Example:*
```bash
python3 -m kslingo convert prefix Madjarski-ksound.md 
```

### CONVERT JSON to CSV

*Example:*
```bash
python3 -m kslingo convert json2csv ./output/converted_from_markdown.json
```

### CONVERT JSON to XLSX

*Example:*
```bash
python3 -m kslingo convert json2xlsx \
	-i ./output/converted_from_markdown.json
```

### CONVERT XLSX to JSON

*Example:*
```bash

python3 -m kslingo convert xlsx2json \
	-i ./output/converted_from_json.xlsx

```

### JUST ONLY REPARSE MARKDOWN
Use for only reparsing markdown file, in order to be better than current markdown file.

*Example:*
```bash

python3 -m kslingo parse only-reparse-markdown \
	-i ksltest/ksl-vault/English-kslt.md

```


# How to build source code?

**LINUX**

```bash
pyinstaller --clean -F main.py -n lang-audio-gen \
  --add-data "assets/end_sound.wav:assets" \
  --add-binary "/usr/lib/x86_64-linux-gnu/libpython3.10.so.1.0:."
```


**WINDOWS**

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

* The **category** always be presented in markdown, and always be generated sound translation.
  That is the reason why not presneted in category *(.josn file)* field like: `level, enabled, isword`. Every category have translation for every defined language.


# Beleske za dokumentaciju
- **md2json** Kada se radi `md2json` bitno je izabrati opcije `learn en -native sr` jer se od md pravi json, a json ima sve supported jezike, u md fajlu ima samo 2 jezika, i to su bas ta dva koje si odabrao sa opcijom.
  Namenjeno je za pravljenje inicijalne json baze podataka iz koje ce se imati samo dva jezika, i kasnije tu bazu treba prosirivati na ostale jezike.
```
python3 -m kslingo convert md2json     -i ksltest/ksl-vault/Reparsed.md        -learn en -native sr
	RADI DOBRO
	   
 python3 -m kslingo convert md2json \
	-i ksltest/ksl-vault/English-kslt.md \
	-learn en -native sr
	RADI DOBRO
 
python3 -m kslingo convert md2json \
	-i ../KSoundLingo-phw/Obsidian/KSoundLingo-Vault/Madjarski-ksound.md\
	-learn hu -native sr
	RADI DOBRO
```

# WHAT TO DO NEXT?
1. Implement Just Only reparse md 
	- ako ima 1+ redova razmaka negde da zakuca na tacno 1
	- oni koji su E da bolduje
2. automatski racuna jel rec ili fraza, ako na learn jeziku ima vise od 2 reci racunaj ga kao frazu u suprotnom kao rec
3. po novom **md2json** ne parsira dobro
	FIXOVANO!
```

REPARSIRANJE
python3 -m kslingo parse only-reparse-markdown \
	-i ksltest/ksl-vault/English-kslt.md \
	-o ksltest/ksl-vault/Reparsed.md  
	RADI DOBRO
```

4. kada fixujes md2json onda fixuj **json2md**
   FIXOVANO!!
```
python3 -m kslingo convert md2json \
	-i ksltest/ksl-vault/English-kslt.md \
	-learn en -native sr && \
python3 -m kslingo convert json2md \
	 -i ./output/md2json.json \
	 -o ./ksltest/ksl-vault \
	-learn en -native sr
RADI DOBRO

```



5. **json2xlsx**
6. **xlsx2json**