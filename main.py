#!/usr/bin/env python3
import sys
import os
import argparse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from github_client import GitHubClient
from search_engine import SearchEngine
from output_handler import OutputHandler
from state_manager import StateManager
from config import get_output_format, get_output_file, MAX_RESULTS_PER_QUERY

def print_banner():
    banner = """
    ╔═══════════════════════════════════════════════════════════╗
    ║         GitHub Intelligence Tool                          ║
    ║         Search repositories, files, and code patterns      ║
    ╚═══════════════════════════════════════════════════════════╝
    """
    print(banner)

def interactive_mode():
    print_banner()
    print("\nInteractive Mode - Enter search queries (type 'exit' to quit)\n")
    print("Special commands:")
    print("  auto          - Auto-search all dangerous patterns")
    print("  exit/quit/q   - Exit program")
    print("\nExamples:")
    print("  filename:hardhat.config.js")
    print("  filename:.env")
    print("  \"privateKey\"")
    print("  \"mnemonic\"")
    print("  \"alchemy\"")
    print("  \"infura\"")
    print()
    
    client = GitHubClient()
    engine = SearchEngine(client)
    
    while True:
        try:
            query = input("\nEnter search query (or 'auto' for auto-search): ").strip()
            
            if not query:
                continue
            
            if query.lower() in ["exit", "quit", "q"]:
                print("Goodbye!")
                break
            
            if query.lower() == "auto":
                max_results = input("Max results per pattern (default 50, max 1000): ").strip()
                max_results = int(max_results) if max_results.isdigit() else 50
                max_results = min(max_results, MAX_RESULTS_PER_QUERY)
                
                fetch_content = input("Fetch file content? (y/n, default: y): ").strip().lower()
                fetch_content = fetch_content != "n"
                
                output_format = input("Output format (json/csv, default: json): ").strip().lower()
                output_format = output_format if output_format in ["json", "csv"] else "json"
                
                results = engine.search_all_dangerous_patterns(max_results, fetch_content)
                
                if results:
                    handler = OutputHandler(output_format)
                    handler.save(results)
                else:
                    print("No results to save.")
                continue
            
            max_results = input("Max results (default 100, max 1000): ").strip()
            max_results = int(max_results) if max_results.isdigit() else 100
            max_results = min(max_results, MAX_RESULTS_PER_QUERY)
            
            fetch_content = input("Fetch file content? (y/n, default: y): ").strip().lower()
            fetch_content = fetch_content != "n"
            
            output_format = input("Output format (json/csv, default: json): ").strip().lower()
            output_format = output_format if output_format in ["json", "csv"] else "json"
            
            results = engine.search_and_collect(query, max_results, fetch_content)
            
            if results:
                handler = OutputHandler(output_format)
                handler.save(results)
            else:
                print("No results to save.")
        
        except KeyboardInterrupt:
            print("\n\nInterrupted by user. Goodbye!")
            break
        except Exception as e:
            print(f"\nError: {e}")
            print("Please try again.")

def cli_mode(args):
    print_banner()
    
    client = GitHubClient()
    
    state_manager = None
    if args.continuous or args.auto_search:
        state_file = args.state_file or "github_intel_state.json"
        state_manager = StateManager(state_file)
        print(f"📝 State file: {state_file}")
        stats = state_manager.get_stats()
        print(f"📊 Previously seen: {stats['total_seen']} unique results\n")
    
    engine = SearchEngine(client, state_manager)
    
    if args.auto_search:
        output_format = args.format or get_output_format()
        output_file = args.output or get_output_file()
        append_mode = args.continuous or (output_file and os.path.exists(output_file))
        
        handler = OutputHandler(output_format, output_file, append_mode=append_mode) if output_file or args.continuous else None
        
        try:
            results = engine.search_all_dangerous_patterns(
                args.max_results,
                args.fetch_content,
                continuous=args.continuous,
                output_handler=handler
            )
            
            if results and not args.continuous:
                if not handler:
                    handler = OutputHandler(output_format, output_file)
                handler.save(results)
            
            if state_manager:
                state_manager.save_state()
                stats = state_manager.get_stats()
                print(f"\n📊 Final stats: {stats['total_seen']} unique results tracked")
        except KeyboardInterrupt:
            print("\n\n⚠️  Interrupted by user. Saving state...")
            if state_manager:
                state_manager.save_state()
                stats = state_manager.get_stats()
                print(f"📊 Saved {stats['total_seen']} unique results to state file")
            sys.exit(0)
    else:
        results = engine.search_and_collect(
            args.query,
            args.max_results,
            args.fetch_content
        )
        
        if results:
            output_format = args.format or get_output_format()
            output_file = args.output or get_output_file()
            
            handler = OutputHandler(output_format, output_file)
            handler.save(results)
        else:
            print("No results to save.")
            sys.exit(1)

def main():
    parser = argparse.ArgumentParser(
        description="GitHub Intelligence Tool - Search repositories, files, and code patterns",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run.py "privateKey"
  python run.py filename:hardhat.config.js --max-results 500
  python run.py "mnemonic" --format csv --output results.csv
  python run.py filename:.env --no-fetch-content
  python run.py --auto
  python run.py --auto --continuous --output results.json
  python run.py --interactive
        """
    )
    
    parser.add_argument(
        "query",
        nargs="?",
        help="Search query (e.g., 'filename:hardhat.config.js' or '\"privateKey\"')"
    )
    
    parser.add_argument(
        "-a", "--auto",
        action="store_true",
        dest="auto_search",
        help="Auto-search all dangerous patterns (files and code patterns)"
    )
    
    parser.add_argument(
        "-c", "--continuous",
        action="store_true",
        help="Continuous mode: Keep searching and saving new results until manually stopped"
    )
    
    parser.add_argument(
        "--state-file",
        default="github_intel_state.json",
        help="State file to track seen results (default: github_intel_state.json)"
    )
    
    parser.add_argument(
        "-i", "--interactive",
        action="store_true",
        help="Run in interactive mode"
    )
    
    parser.add_argument(
        "-m", "--max-results",
        type=int,
        default=100,
        help=f"Maximum number of results (default: 100, max: {MAX_RESULTS_PER_QUERY})"
    )
    
    parser.add_argument(
        "-f", "--format",
        choices=["json", "csv"],
        help="Output format (default: json or from OUTPUT_FORMAT env var)"
    )
    
    parser.add_argument(
        "-o", "--output",
        help="Output file path (default: auto-generated with timestamp)"
    )
    
    parser.add_argument(
        "--no-fetch-content",
        action="store_true",
        dest="no_fetch_content",
        help="Don't fetch file contents (faster, but less data)"
    )
    
    args = parser.parse_args()
    
    if args.max_results > MAX_RESULTS_PER_QUERY:
        args.max_results = MAX_RESULTS_PER_QUERY
        print(f"Warning: Max results capped at {MAX_RESULTS_PER_QUERY}")
    
    args.fetch_content = not args.no_fetch_content
    
    if args.interactive or (not args.query and not args.auto_search):
        interactive_mode()
    else:
        if args.auto_search and args.query:
            print("Warning: Both --auto and query specified. Using --auto mode.")
        cli_mode(args)

if __name__ == "__main__":
    main()

