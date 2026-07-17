import json
import csv
import os
from datetime import datetime
from typing import List, Dict, Any, Optional

class OutputHandler:
    def __init__(self, output_format: str = "json", output_file: str = None, append_mode: bool = False):
        self.output_format = output_format.lower()
        self.output_file = output_file or self._generate_filename()
        self.append_mode = append_mode
        self.existing_data = []
        
        if append_mode and os.path.exists(self.output_file):
            self._load_existing_data()
    
    def _generate_filename(self) -> str:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        extension = "json" if self.output_format == "json" else "csv"
        return f"github_intel_results_{timestamp}.{extension}"
    
    def _load_existing_data(self):
        if self.output_format == "json":
            try:
                with open(self.output_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.existing_data = data.get("results", [])
            except:
                self.existing_data = []
        else:
            self.existing_data = []
    
    def save_json(self, data: List[Dict[str, Any]]):
        if self.append_mode:
            all_results = self.existing_data + data
            output = {
                "query_timestamp": datetime.now().isoformat(),
                "last_update": datetime.now().isoformat(),
                "total_results": len(all_results),
                "new_results_this_batch": len(data),
                "results": all_results
            }
            mode = "w"
        else:
            output = {
                "query_timestamp": datetime.now().isoformat(),
                "total_results": len(data),
                "results": data
            }
            mode = "w"
        
        with open(self.output_file, mode, encoding="utf-8") as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        
        if self.append_mode:
            print(f"\n✓ {len(data)} new results appended to: {self.output_file}")
            print(f"  Total results in file: {len(self.existing_data) + len(data)}")
        else:
            print(f"\nResults saved to: {self.output_file}")
            print(f"Total results: {len(data)}")
    
    def save_csv(self, data: List[Dict[str, Any]]):
        if not data:
            print("No data to save.")
            return
        
        with open(self.output_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            
            headers = [
                "Repository Owner",
                "Repository Name",
                "Repository URL",
                "Stars",
                "Forks",
                "Updated At",
                "Language",
                "File Path",
                "File URL",
                "Matched Pattern",
                "File Content (first 500 chars)"
            ]
            
            writer.writerow(headers)
            
            for item in data:
                repo = item.get("repository", {})
                file_info = item.get("file", {})
                content = file_info.get("content", "")
                content_preview = content[:500] if content else ""
                matched_pattern = item.get("matched_pattern", "")
                
                writer.writerow([
                    repo.get("owner", ""),
                    repo.get("name", ""),
                    repo.get("url", ""),
                    repo.get("stars", 0),
                    repo.get("forks", 0),
                    repo.get("updated_at", ""),
                    repo.get("language", ""),
                    file_info.get("path", ""),
                    file_info.get("url", ""),
                    matched_pattern,
                    content_preview.replace("\n", " ").replace("\r", "")
                ])
        
        print(f"\nResults saved to: {self.output_file}")
        print(f"Total results: {len(data)}")
    
    def save(self, data: List[Dict[str, Any]]):
        if self.output_format == "json":
            self.save_json(data)
        elif self.output_format == "csv":
            self.save_csv(data)
        else:
            raise ValueError(f"Unsupported output format: {self.output_format}")

