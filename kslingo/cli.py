import argparse
import os
from kslingo.version import __version__
from kslingo.audio.tts import Generate_Txt_Audio_mp3, Generate_Markdown_Audio_mp3
from kslingo.utils.fs import ensure_dir
from kslingo.convert.json_to_markdown import Convert_json2md
from kslingo.convert.markdown_to_json import Convert_md2json

def main():
    parser = argparse.ArgumentParser(prog="kslingo", description="Multilingual audio generator and converter")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    # === AUDIO COMMAND ===
    audio_parser = subparsers.add_parser("audio", help="Generate audio from txt or markdown.")
    audio_parser.add_argument("--txt", metavar="FILE", help="Run in simple txt mode.")
    audio_parser.add_argument("--markdown", metavar="FILE", help="Run in markdown mode.")
    audio_parser.add_argument("--output", metavar="DIR", default="output", help="Output directory (default: ./output)")
    audio_parser.add_argument("--learn", required=True, help="Language you are learning")
    audio_parser.add_argument("--native", required=True, help="Your native language")
    
    # === CONVERT COMMAND ===
    convert_parser = subparsers.add_parser("convert", help="Convert between formats")
    convert_subparsers = convert_parser.add_subparsers(dest="convert_command", required=True)

    # --- JSON to MARKDOWN ---
    json2md_parser = convert_subparsers.add_parser("json2md", help="Convert JSON to Markdown")
    json2md_parser.add_argument("input", help="Input JSON file")
    json2md_parser.add_argument("--output", metavar="DIR", default="output", help="Output directory (default: ./output)")
    json2md_parser.add_argument("--learn", required=True, help="First language")
    json2md_parser.add_argument("--native", required=True, help="Second language")
    
    # --- MARKDOWN to JSON ---
    md2json_parser = convert_subparsers.add_parser("md2json", help="Convert Markdown to JSON")
    md2json_parser.add_argument("input", help="Input Markdown file")
    md2json_parser.add_argument("--output", metavar="DIR", default="output", help="Output directory (default: ./output)")
    md2json_parser.add_argument("--learn", required=True, help="First language")
    md2json_parser.add_argument("--native", required=True, help="Second language")
    
    args = parser.parse_args()
    
    print(f"kslingo v{__version__}")


    if args.command == "audio":
        ensure_dir(args.output)
        if args.txt:
            print("Running in TXT mode")
            Generate_Txt_Audio_mp3(args.txt, args.output, args.learn, args.native)
        elif args.markdown:
            print("Running in MARKDOWN mode")
            Generate_Markdown_Audio_mp3(args.markdown, args.output, args.learn, args.native)
        else:
            print("Error: --txt or --markdown is required with 'audio' command")
            
    elif args.command == "convert":
        ensure_dir(args.output)
        if args.convert_command == "json2md":
            output_path = f"{args.output}/converted_from_json.md"
            print(f"Markdown output path {output_path}")
            Convert_json2md(args.input, output_path, args.learn, args.native)

        elif args.convert_command == "md2json":
            output_path = f"{args.output}/converted_from_markdown.json"
            print(f"JSON output path {output_path}")
            Convert_md2json(args.input, output_path, args.learn, args.native)
        else:
            print("Error: --json2md or --md2json is required with 'convert' command")
            
    else:
        print("Please choose running mode 'audio' or 'convert")
