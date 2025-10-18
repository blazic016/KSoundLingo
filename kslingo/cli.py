import argparse
import os
from kslingo.version import __version__
from kslingo.audio.tts import Generate_Txt_Audio_mp3, Generate_Markdown_Audio_mp3
from kslingo.utils.fs import ensure_dir
from kslingo.convert.file import Convert_json2md, Convert_md2json, Convert_json2xlsx, Convert_xlsx2json
from kslingo.parsers.markdown import just_only_reparse_md

def main():
    parser = argparse.ArgumentParser(prog="kslingo", description="Multilingual audio generator and converter")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    # === AUDIO COMMAND ===
    audio_parser = subparsers.add_parser("audio", help="Generate audio from txt or markdown.")
    audio_parser.add_argument("--txt", metavar="FILE", help="Run in simple txt mode.")
    audio_parser.add_argument("--markdown", metavar="FILE", help="Run in markdown mode.")
    audio_parser.add_argument("-o", metavar="DIR", default="output", help="Output directory (default: ./output)")
    audio_parser.add_argument("-learn", required=True, help="Language you are learning")
    audio_parser.add_argument("-native", required=True, help="Your native language")
    
    # === CONVERT COMMAND ===
    convert_parser = subparsers.add_parser("convert", help="Convert between formats")
    convert_subparsers = convert_parser.add_subparsers(dest="convert_command", required=True)

    # === PARSE COMMAND ===
    parse_parser = subparsers.add_parser("parse", help="Parsing files")
    parse_subparsers = parse_parser.add_subparsers(dest="parse_command", required=True)


    # --- JSON to MARKDOWN ---
    json2md_parser = convert_subparsers.add_parser("json2md", help="Convert JSON to Markdown")
    json2md_parser.add_argument("-i", help="Input JSON file")
    json2md_parser.add_argument("-o", metavar="DIR", default="output", help="Output directory (default: ./output)")
    json2md_parser.add_argument("-learn", required=True, help="First language")
    json2md_parser.add_argument("-native", required=True, help="Second language")
    
    # --- MARKDOWN to JSON ---
    md2json_parser = convert_subparsers.add_parser("md2json", help="Convert Markdown to JSON")
    md2json_parser.add_argument("-i", help="Input Markdown file")
    md2json_parser.add_argument("-o", metavar="DIR", default="output", help="Output directory (default: ./output)")
    md2json_parser.add_argument("-learn", required=True, help="First language")
    md2json_parser.add_argument("-native", required=True, help="Second language")
    
    # # --- JSON to CSV ---
    # json2csv_parser = convert_subparsers.add_parser("json2csv", help="Convert JSON to CSV")
    # json2csv_parser.add_argument("-i", help="Input json file")
    # json2csv_parser.add_argument("-o", metavar="DIR", default="output", help="Output directory (default: ./output)")
    
    # --- JSON to XLSX ---
    json2xlsx_parser = convert_subparsers.add_parser("json2xlsx", help="Convert JSON to XLSX")
    json2xlsx_parser.add_argument("-i", help="Input json file")
    json2xlsx_parser.add_argument("-o", metavar="DIR", default="output", help="Output directory (default: ./output)")

    # --- XLSX to JSON ---
    xlsx2json_parser = convert_subparsers.add_parser("xlsx2json", help="Convert XLSX to JSON")
    xlsx2json_parser.add_argument("-i", help="Input xlsx file")
    xlsx2json_parser.add_argument("-o", metavar="DIR", default="output", help="Output directory (default: ./output)")
    
    # # --- MD to MD ---
    # md2md_parser = convert_subparsers.add_parser("md2md", help="Convert MD to MD")
    # md2md_parser.add_argument("-i", help="Input md file")
    # md2md_parser.add_argument("-o", metavar="DIR", default="output", help="Output directory (default: ./output)")
    

    # --- PARSE MARKDOWN ---
    parse_parser = parse_subparsers.add_parser("only-reparse-markdown", help="Description...")
    parse_parser.add_argument("-i", help="Input markdown file")
    parse_parser.add_argument("-o", default="output/Only-Reparsed.md", help="Output markdown file")


    args = parser.parse_args()
    
    print(f"kslingo v{__version__}")

    if args.command == "audio":
        ensure_dir(args.o)
        if args.txt:
            print("Running in TXT mode")
            Generate_Txt_Audio_mp3(args.txt, args.o, args.learn, args.native)
        elif args.markdown:
            print("Running in MARKDOWN mode")
            Generate_Markdown_Audio_mp3(args.markdown, args.o, args.learn, args.native)
        else:
            print("Error: --txt or --markdown is required with 'audio' command")
            
    elif args.command == "convert":
        ensure_dir(args.o)
        if args.convert_command == "json2md":
            output_file = f"{args.o}/converted_from_json.md"
            Convert_json2md(args.i, output_file, args.learn, args.native)

        elif args.convert_command == "md2json":
            output_file = f"{args.o}/converted_from_markdown.json"
            Convert_md2json(args.i, output_file, args.learn, args.native)
            
        # elif args.convert_command == "json2csv":
        #     output_file = f"{args.o}/converted_from_json.csv"
        #     Convert_json2csv(args.i, output_file)

        elif args.convert_command == "json2xlsx":
            output_file = f"{args.o}/converted_from_json.xlsx"
            Convert_json2xlsx(args.i, output_file)

        elif args.convert_command == "xlsx2json":
            output_file = f"{args.o}/converted_from_xlsx.json"
            Convert_xlsx2json(args.i, output_file)

            
    elif args.command == "parse":
        # ensure_dir(args.o) # odnosi se na dir, a sad je file. FIX IT!
        if args.parse_command == "only-reparse-markdown":
            print("Just only markdown reparsing")
            # Convert_json2md(args.i, output_file, args.learn, args.native)
            just_only_reparse_md(args.i,args.o)

         
        else:
            print("Error: json2md or md2json json2csv is required with 'convert' command")
    else:
        print("Please choose running mode 'audio' or 'convert'")
