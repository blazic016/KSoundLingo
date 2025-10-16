from gtts import gTTS
from pydub import AudioSegment
from kslingo.utils.fs import get_resource_path
from kslingo.utils.fs import ensure_dir
from kslingo.utils.fs import create_temp_dir, remove_dir_if_exists
from kslingo.utils.text import split_pair
from kslingo.parsers.txt import ReadFromTxtFile
from kslingo.parsers.markdown import get_phrases_markdown, generate_output_md_from_phrases
from kslingo.convert.file import Generate_pdf_from_md

def Generate_Txt_Audio_mp3(input_file, out_dir, learn_lang, native_lang):
    print("start Generate_Txt_Audio_mp3")

    out_file = f"{out_dir}/simple.mp3"

    # sanity
    ensure_dir(out_dir)
        
    phrases = ReadFromTxtFile(input_file)
    if not phrases:
        print("ERROR: phrases is empty array!")
        return
        
    generate_mp3_from_phrases(phrases, out_file, learn_lang, native_lang)
    

def Generate_Markdown_Audio_mp3(input_file, out_dir, learn_lang, native_lang):
    print("start Generate_Markdown_Audio_mp3")

    # sanity
    ensure_dir(out_dir)

    phrases = get_phrases_markdown(input_file)

    if not phrases:
        print("ERROR: phrases is empty array!")
        return


    for i, section in enumerate(phrases):
        if not section or not section.get("phrases"):
            continue

        section_title = section.get("title", f"section_{i}")
        hu_title, sr_title = split_pair(section_title)

        # audio list of pairs [(hu, sr)]
        pairs = [(hu_title, sr_title)]

        for phrase in section["phrases"]:
            # if phrase.get("only_learn"):
            #     continue

            hu = phrase.get("hu", "").strip()
            sr = phrase.get("sr", "")
            sr = sr.strip() if sr else ""

            # if not hu or not sr:
            #     print(f"SKIP (incomplete): hu='{hu}' | sr='{sr}'")
            #     continue

            pairs.append((hu, sr))

        if len(pairs) <= 1:
            print(f"SKIP section (no valid audio pairs): {section_title}")
            continue

        safe_title = section_title.replace(" ", "_").replace("/", "_")
        out_file = f"{out_dir}/{i:02d}_{safe_title}.mp3"

        generate_mp3_from_phrases(pairs, out_file, learn_lang, native_lang)

    out_md=f"{out_dir}/cleaned.md"
    generate_output_md_from_phrases(phrases, out_md)
    
    out_pdf=f"{out_dir}/cleaned.pdf"
    Generate_pdf_from_md(out_md, out_pdf)


def generate_mp3_from_phrases(phrases, out_file, learn_lang, native_lang):
    print(f"start generate_mp3_from_phrases {learn_lang} -> {native_lang}")

    wav_path = get_resource_path("assets/end_sound.wav")
    end_sound = AudioSegment.from_file(wav_path)
    end_sound = end_sound.apply_gain(-10)
    final_audio = AudioSegment.silent(duration=1000)
    temp_dir = create_temp_dir()
    
    print(f"Temp directory created : {temp_dir}")
    
    # sanity
    ensure_dir(temp_dir)

    for i, (left, right) in enumerate(phrases):
        print(f"Generating: {left} - {right}")
        
        # left generate always (learn lang)
        left_path = f"{temp_dir}/{learn_lang}_{i}.mp3"
        gTTS(text=left, lang=learn_lang).save(left_path)
        left_audio = AudioSegment.from_file(left_path)

        if right != "":
            # Means that exist phrases on both langs (learn lang - native lang)
            # Then generate left and right.
            right_path = f"{temp_dir}/{native_lang}_{i}.mp3"
            gTTS(text=right, lang=native_lang).save(right_path)
            right_audio = AudioSegment.from_file(right_path)

            # LEARN-LANG -> NATIVE-LANG -> LEARN-LANG -> End Sound
            final_audio += left_audio + AudioSegment.silent(duration=800)
            final_audio += right_audio + AudioSegment.silent(duration=800)
            final_audio += left_audio + AudioSegment.silent(duration=800)
            final_audio += end_sound + AudioSegment.silent(duration=1200)

        else:
            # LEARN-LANG -> End Sound
            final_audio += left_audio + AudioSegment.silent(duration=800)

    final_audio.export(out_file, format="mp3")

    remove_dir_if_exists(temp_dir)

    print(f"\nFinish! File saved: {out_file}")

