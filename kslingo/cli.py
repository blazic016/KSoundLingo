import argparse
import os
from kslingo.version import __version__
from kslingo.audio.tts import Generate_Txt_Audio_mp3, Generate_Markdown_Audio_mp3

def main():
    parser = argparse.ArgumentParser(description="Upisi neku deskripciju.")
    parser.add_argument("--txt",        metavar="FILE", help="Run script in simple txt mode.")
    parser.add_argument("--markdown",   metavar="FILE", help="Run script in markdown mode with input file.")
    parser.add_argument("--output",     metavar="DIR", default="output", help="Output directory (default: ./output)")
    parser.add_argument("--version",    action="version", version=f"%(prog)s {__version__}")
    parser.add_argument("--learn",      help="Language which you are learning")
    parser.add_argument("--native",     help="Your native language")
    args = parser.parse_args()

    print(f"kslingo v{__version__}")

    os.makedirs(args.output, exist_ok=True)

    if args.txt:
        print("Running in TXT mode")
        Generate_Txt_Audio_mp3(args.txt, args.output, args.learn, args.native)

    elif args.markdown:
        print("Running in MARKDOWN mode")
        Generate_Markdown_Audio_mp3(args.markdown, args.output, args.learn, args.native)
    else:
        print("Please choose running mode!")
