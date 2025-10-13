from gtts import gTTS
from pydub import AudioSegment
from kslingo.utils.fs import get_resource_path
from kslingo.utils.fs import ensure_dir
from kslingo.utils.fs import create_temp_dir, remove_dir_if_exists
from kslingo.utils.text import split_pair
from kslingo.parsers.txt import ReadFromTxtFile
from kslingo.parsers.markdown import ReadFromMarkdownFile


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

    phrases = ReadFromMarkdownFile(input_file, out_dir)
    if not phrases:
        print("ERROR: phrases is empty array!")
        return
            
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

        generate_mp3_from_phrases(pairs, out_file, learn_lang, native_lang)


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

