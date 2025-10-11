import argparse
import os
from kslingo.version import __version__
from kslingo.audio.tts import Generate_Txt_Audio_mp3, Generate_Markdown_Audio_mp3
from kslingo.utils.fs import ensure_dir
from kslingo.convert.file import add_prefix_on_markdown, Convert_json2md, Convert_md2json, Convert_json2csv

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
    
    # --- JSON to CSV ---
    json2csv_parser = convert_subparsers.add_parser("json2csv", help="Convert JSON to CSV")
    json2csv_parser.add_argument("input", help="Input json file")
    json2csv_parser.add_argument("--output", metavar="DIR", default="output", help="Output directory (default: ./output)")
    
    # --- PREFIX COMMAND---
    prefix_parser = convert_subparsers.add_parser("prefix", help="Add metadata prefix to Markdown phrases.")
    prefix_parser.add_argument("input", help="Input markdown file")
    prefix_parser.add_argument("--output", metavar="DIR", default="output", help="Output directory (default: ./output)")


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
            output_file = f"{args.output}/converted_from_json.md"
            Convert_json2md(args.input, output_file, args.learn, args.native)

        elif args.convert_command == "md2json":
            output_file = f"{args.output}/converted_from_markdown.json"
            Convert_md2json(args.input, output_file, args.learn, args.native)
            
        elif args.convert_command == "json2csv":
            output_file = f"{args.output}/converted_from_json.csv"
            Convert_json2csv(args.input, output_file)
            
            
        elif args.convert_command == "prefix":
            ensure_dir(args.output)
            output_file = f"{args.output}/prefixed.md"
            prefix = "%%A2,W,D%%"
            add_prefix_on_markdown(args.input, output_file, prefix)
         
        else:
            print("Error: --json2md or --md2json --json2csv is required with 'convert' command")
    else:
        print("Please choose running mode 'audio' or 'convert'")
