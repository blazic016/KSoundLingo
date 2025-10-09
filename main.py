from gtts import gTTS
from pydub import AudioSegment
import shutil
import os
import sys
import argparse
import re
from version import __version__

def ReadFromTxtFile(input_file):
    #TODO: Napravi sanity jel inputfile .txt file
    
    phrases = []
    with open(input_file, "r", encoding="utf-8") as f:
        for  line in f:
            line = line.replace("–", "-")
            if "-" in  line:
                left, right =  line.strip().split("-", maxsplit=1)
                phrases.append((left.strip(), right.strip()))
    return phrases

def resource_path(rel_path: str) -> str:
    # in onlefile mode PyInstaller extract resources in the temp dir: sys._MEIPASS
    base = getattr(sys, "_MEIPASS", os.path.abspath("."))
    return os.path.join(base, rel_path)

def clean_markdown(input_path, output_path):
    print("start clean_markdown")

    inside_code_block = False
    cleaned_lines = []

    if not os.path.isfile(input_path):
        print(f" ERROR: File {input_path} doesn't exist!")

    with open(input_path, "r", encoding="utf-8") as f:
        for line in f:
            stripped = line.strip()

            # toggle code block
            if stripped.startswith("```"):
                inside_code_block = not inside_code_block
                continue
            if inside_code_block:
                continue

            # 1) remove all %%...%%
            line = re.sub(r"%%[^%]*%%", "", line)

            # 2) if is title ### then get text inside the **...**
            stripped = line.strip()
            if stripped.startswith("###"):
                m = re.search(r"\*\*(.*?)\*\*", stripped)
                if m:
                    title = m.group(1).strip()
                else:
                    title = stripped.lstrip("#").strip()

                # normalize title
                cleaned_lines.append(f"### {title}\n")
                continue

            # 3) remove ** marker
            line = line.lstrip()
            line = re.sub(r"\*\*(.*?)\*\*", r"\1", line)

            # 4) save line if not empty
            if line.strip():
                cleaned_lines.append(line)

    with open(output_path, "w", encoding="utf-8") as f:
        f.writelines(cleaned_lines)

    print(f"Cleaned markdown saved in: {output_path}")


def ReadFromMarkdownFile(inputfile, output):
    print("start ReadFromMarkdownFile")

    #TODO: Napravi sanity jel inputfile .md file

    cleaned_md=f"{output}/cleaned.md"
    phrases = []
    current_section = []
    
    clean_markdown(inputfile, cleaned_md)
 
    if not os.path.isfile(cleaned_md):
        print(f"ERROR: File {cleaned_md} doesn't exist!")
        return phrases

    with open(cleaned_md, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            if line.startswith("###"):
                title = line.lstrip("#").strip()
                if current_section:
                    phrases.append(current_section)
                current_section = [title]
            else:
                current_section.append(line)

    # append last section
    if current_section:
        phrases.append(current_section)

    # debug print
    # for i, sec in enumerate(phrases):
    #     print(f"Section {i}:")
    #     for j, phrase in enumerate(sec):
    #         print(f"  [{i}][{j}] {phrase}")

    return phrases

def Generate_mp3_from_Phrases(phrases, out_file, learn_lang, native_lang):
    print(f"start Generate_mp3_from_Phrases {learn_lang}->{native_lang}")

    wav_path = resource_path("assets/end_sound.wav")
    end_sound = AudioSegment.from_file(wav_path)
    end_sound = end_sound.apply_gain(-10)

    final_audio = AudioSegment.silent(duration=1000)
    os.makedirs("/tmp/temp_lang_audio_gen", exist_ok=True)

    for i, (hu, sr) in enumerate(phrases):
        print(f"Generating: {hu} - {sr}")
        # TODO: GENERISI RANDOM DIREKTORIJUM I TAJ DIREKTORIJUM KORISTI
        # Bitno je da nije fixan dir, jer u suprotnom ako se pokrene 2x istovremeno, zbunice se. 
        hu_path = f"/tmp/temp_lang_audio_gen/hu_{i}.mp3"
        sr_path = f"/tmp/temp_lang_audio_gen/sr_{i}.mp3"

        gTTS(text=hu, lang=learn_lang).save(hu_path)
        gTTS(text=sr, lang=native_lang).save(sr_path)

        hu_audio = AudioSegment.from_file(hu_path)
        sr_audio = AudioSegment.from_file(sr_path)

        # HU -> SR -> HU -> End Sound
        final_audio += hu_audio + AudioSegment.silent(duration=800)
        final_audio += sr_audio + AudioSegment.silent(duration=800)
        final_audio += hu_audio + AudioSegment.silent(duration=800)
        final_audio += end_sound + AudioSegment.silent(duration=1200)

# final_audio.export(out_dir + "/" + out_file, format="mp3")
    final_audio.export(out_file, format="mp3")

    if os.path.exists("/tmp/temp_lang_audio_gen"):
        shutil.rmtree("/tmp/temp_lang_audio_gen")

    print(f"\nFinish! File saved: {out_file}")


SEP = r"\s[-–]\s"  # split " - " or " – "

def split_pair(text):
    parts = re.split(SEP, text.strip(), maxsplit=1)
    if len(parts) == 2:
        return parts[0].strip(), parts[1].strip()
    # fallback: if not exist separator, then use the same text for HU and SR
    return text.strip(), text.strip()


def Generate_Txt_Audio_mp3(phrases, out_dir, learn_lang, native_lang):
    print("start Generate_Txt_Audio_mp3")

    out_file = f"{out_dir}/simple.mp3"
    Generate_mp3_from_Phrases(phrases, out_file, learn_lang, native_lang)


def Generate_Markdown_Audio_mp3(phrases, out_dir, learn_lang, native_lang):
    print("start Generate_Markdown_Audio_mp3")
    # os.makedirs("output", exist_ok=True)

    for i, section in enumerate(phrases):
        if not section:
            continue

        # 1) title of the section is section[0]; make hu_title, sr_title
        section_title = section[0].strip()
        hu_title, sr_title = split_pair(section_title)

        # 2) create list of tuples and add title as first pair
        pairs = [(hu_title, sr_title)]

        # 3) convert every single line to phrase (HU, SR) and append to pairs
        for line in section[1:]:
            line = line.strip()
            if not line:
                continue
            hu, sr = split_pair(line)
            # skip if anything is wrong (ie: empty)
            if not hu and not sr:
                print(f"SKIP (empty after split): {line}")
                continue
            pairs.append((hu, sr))

        if len(pairs) == 0:
            print(f"SKIP section (no valid phrases): {section_title}")
            continue

        out_file = f"{out_dir}/{i:02d}_{section_title}.mp3"

        Generate_mp3_from_Phrases(pairs, out_file, learn_lang, native_lang)



if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Magyar Audio Generator")
    parser.add_argument("--txt",        metavar="FILE", help="Run script in simple txt mode.")
    parser.add_argument("--markdown",   metavar="FILE", help="Run script in markdown mode with input file.")
    parser.add_argument("--output",     metavar="DIR", default="output", help="Output directory (default: ./output)")
    parser.add_argument("--version",    action="version", version=f"%(prog)s {__version__}")
    parser.add_argument("--learn",      help="Language which you learning ")
    parser.add_argument("--native",     help="Yourself mother language")
    args = parser.parse_args()

    print(f"Magyar Audio Generator v{__version__}")

    if args.txt:
        input_path = args.txt
        output_dir = args.output
        os.makedirs(output_dir, exist_ok=True)
        phrases = ReadFromTxtFile(input_path)
        Generate_Txt_Audio_mp3(phrases, output_dir, learn_lang=args.learn, native_lang=args.native)

    elif args.markdown:
        input_path = args.markdown
        output_dir = args.output
        os.makedirs(output_dir, exist_ok=True)
        phrases = ReadFromMarkdownFile(input_path, output_dir)
        if not phrases:
            print("ERROR: phrases is empty array!")
        Generate_Markdown_Audio_mp3(phrases, output_dir, learn_lang=args.learn, native_lang=args.native)

    else:
        print("Please choose running mode!")