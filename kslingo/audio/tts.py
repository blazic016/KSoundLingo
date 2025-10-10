from gtts import gTTS
from pydub import AudioSegment
from kslingo.utils.fs import get_resource_path
from kslingo.utils.fs import ensure_dir
from kslingo.utils.fs import remove_dir_if_exists
from kslingo.utils.text import split_pair



def Generate_Txt_Audio_mp3(phrases, out_dir, learn_lang, native_lang):
    print("start Generate_Txt_Audio_mp3")

    out_file = f"{out_dir}/simple.mp3"
    
    generate_mp3_from_phrases(phrases, out_file, learn_lang, native_lang)
    

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

        generate_mp3_from_phrases(pairs, out_file, learn_lang, native_lang)


def generate_mp3_from_phrases(phrases, out_file, learn_lang, native_lang):
    print(f"start generate_mp3_from_phrases {learn_lang}->{native_lang}")

    wav_path = get_resource_path("assets/end_sound.wav")
    end_sound = AudioSegment.from_file(wav_path)
    end_sound = end_sound.apply_gain(-10)

    final_audio = AudioSegment.silent(duration=1000)
    ensure_dir("/tmp/temp_lang_audio_gen")
    

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

    final_audio.export(out_file, format="mp3")

    remove_dir_if_exists("/tmp/temp_lang_audio_gen")

    print(f"\nFinish! File saved: {out_file}")

