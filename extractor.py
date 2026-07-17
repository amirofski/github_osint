import json
import re
from typing import List, Dict, Set, Any
from pathlib import Path

class WalletKeyExtractor:
    def __init__(self):
        self.private_keys: Set[str] = set()
        self.mnemonics: Set[str] = set()
        self.addresses: Set[str] = set()
        self.api_keys: Set[str] = set()
        self.seeds: Set[str] = set()
        
    def extract_private_key_64hex(self, text: str) -> List[str]:
        patterns = [
            r'\b[0-9a-fA-F]{64}\b',
            r'0x[0-9a-fA-F]{64}',
            r'private[_\s]*key[_\s]*[:=][_\s]*["\']?([0-9a-fA-F]{64})["\']?',
            r'PRIVATE[_\s]*KEY[_\s]*[:=][_\s]*["\']?([0-9a-fA-F]{64})["\']?',
            r'privateKey[_\s]*[:=][_\s]*["\']?([0-9a-fA-F]{64})["\']?',
        ]
        
        found = []
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                if isinstance(match, tuple):
                    match = match[0] if match[0] else match[1] if len(match) > 1 else ''
                if match and len(match) >= 64:
                    key = match[:64] if len(match) > 64 else match
                    if len(key) == 64 and all(c in '0123456789abcdefABCDEF' for c in key):
                        found.append(key.lower())
        
        return found
    
    def extract_private_key_various(self, text: str) -> List[str]:
        patterns = [
            r'private[_\s]*key[_\s]*[:=][_\s]*["\']([^"\'\n]{20,})["\']',
            r'PRIVATE[_\s]*KEY[_\s]*[:=][_\s]*["\']([^"\'\n]{20,})["\']',
            r'privateKey[_\s]*[:=][_\s]*["\']([^"\'\n]{20,})["\']',
            r'secret[_\s]*key[_\s]*[:=][_\s]*["\']([^"\'\n]{20,})["\']',
            r'SECRET[_\s]*KEY[_\s]*[:=][_\s]*["\']([^"\'\n]{20,})["\']',
        ]
        
        found = []
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                if len(match) >= 20:
                    found.append(match.strip())
        
        return found
    
    def extract_mnemonic(self, text: str) -> List[str]:
        patterns = [
            r'mnemonic[_\s]*[:=][_\s]*["\']([^"\'\n]{20,})["\']',
            r'MNEMONIC[_\s]*[:=][_\s]*["\']([^"\'\n]{20,})["\']',
            r'seed[_\s]*phrase[_\s]*[:=][_\s]*["\']([^"\'\n]{20,})["\']',
            r'SEED[_\s]*PHRASE[_\s]*[:=][_\s]*["\']([^"\'\n]{20,})["\']',
            r'["\']([a-z]+\s+){11,23}[a-z]+["\']',
            r'([a-z]+\s+){11,23}[a-z]+',
        ]
        
        found = []
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                if isinstance(match, tuple):
                    match = match[0] if match[0] else ''
                words = match.strip().split()
                if 12 <= len(words) <= 24:
                    words_lower = [w.lower() for w in words]
                    if all(len(w) >= 3 and w.isalpha() for w in words_lower):
                        found.append(' '.join(words))
        
        return found
    
    def extract_ethereum_address(self, text: str) -> List[str]:
        pattern = r'0x[a-fA-F0-9]{40}'
        matches = re.findall(pattern, text)
        return [m.lower() for m in matches]
    
    def extract_api_keys(self, text: str) -> List[str]:
        patterns = [
            r'api[_\s]*key[_\s]*[:=][_\s]*["\']([^"\'\n]{10,})["\']',
            r'API[_\s]*KEY[_\s]*[:=][_\s]*["\']([^"\'\n]{10,})["\']',
            r'alchemy[_\s]*key[_\s]*[:=][_\s]*["\']([^"\'\n]{10,})["\']',
            r'ALCHEMY[_\s]*KEY[_\s]*[:=][_\s]*["\']([^"\'\n]{10,})["\']',
            r'infura[_\s]*key[_\s]*[:=][_\s]*["\']([^"\'\n]{10,})["\']',
            r'INFURA[_\s]*KEY[_\s]*[:=][_\s]*["\']([^"\'\n]{10,})["\']',
        ]
        
        found = []
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                if isinstance(match, tuple):
                    match = match[0] if match[0] else ''
                if len(match) >= 10:
                    found.append(match.strip())
        
        return found
    
    def extract_from_content(self, content: str) -> Dict[str, List[str]]:
        if not content:
            return {}
        
        results = {
            'private_keys_64hex': self.extract_private_key_64hex(content),
            'private_keys_other': self.extract_private_key_various(content),
            'mnemonics': self.extract_mnemonic(content),
            'ethereum_addresses': self.extract_ethereum_address(content),
            'api_keys': self.extract_api_keys(content),
        }
        
        return results
    
    def extract_from_json_file(self, json_file: str) -> Dict[str, Any]:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        results = {
            'private_keys_64hex': set(),
            'private_keys_other': set(),
            'mnemonics': set(),
            'ethereum_addresses': set(),
            'api_keys': set(),
        }
        
        items = data.get('results', [])
        print(f"Processing {len(items)} results from JSON file...")
        
        for idx, item in enumerate(items, 1):
            if idx % 100 == 0:
                print(f"  Processed {idx}/{len(items)} items...")
            
            file_content = item.get('file', {}).get('content', '')
            if file_content:
                extracted = self.extract_from_content(file_content)
                for key in results:
                    results[key].update(extracted.get(key, []))
        
        return {k: list(v) for k, v in results.items()}
    
    def save_to_txt(self, output_file: str, extracted_data: Dict[str, List[str]]):
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write("EXTRACTED WALLET KEYS AND SENSITIVE DATA\n")
            f.write("=" * 80 + "\n\n")
            
            if extracted_data.get('private_keys_64hex'):
                f.write(f"\n{'='*80}\n")
                f.write(f"PRIVATE KEYS (64 hex characters) - {len(extracted_data['private_keys_64hex'])} found\n")
                f.write(f"{'='*80}\n\n")
                for key in extracted_data['private_keys_64hex']:
                    f.write(f"{key}\n")
            
            if extracted_data.get('private_keys_other'):
                f.write(f"\n{'='*80}\n")
                f.write(f"PRIVATE KEYS (other formats) - {len(extracted_data['private_keys_other'])} found\n")
                f.write(f"{'='*80}\n\n")
                for key in extracted_data['private_keys_other']:
                    f.write(f"{key}\n")
            
            if extracted_data.get('mnemonics'):
                f.write(f"\n{'='*80}\n")
                f.write(f"MNEMONIC PHRASES - {len(extracted_data['mnemonics'])} found\n")
                f.write(f"{'='*80}\n\n")
                for mnemonic in extracted_data['mnemonics']:
                    f.write(f"{mnemonic}\n")
            
            if extracted_data.get('ethereum_addresses'):
                f.write(f"\n{'='*80}\n")
                f.write(f"ETHEREUM ADDRESSES - {len(extracted_data['ethereum_addresses'])} found\n")
                f.write(f"{'='*80}\n\n")
                for addr in extracted_data['ethereum_addresses']:
                    f.write(f"{addr}\n")
            
            if extracted_data.get('api_keys'):
                f.write(f"\n{'='*80}\n")
                f.write(f"API KEYS - {len(extracted_data['api_keys'])} found\n")
                f.write(f"{'='*80}\n\n")
                for key in extracted_data['api_keys']:
                    f.write(f"{key}\n")
            
            f.write(f"\n{'='*80}\n")
            f.write("SUMMARY\n")
            f.write(f"{'='*80}\n\n")
            f.write(f"Total Private Keys (64 hex): {len(extracted_data.get('private_keys_64hex', []))}\n")
            f.write(f"Total Private Keys (other): {len(extracted_data.get('private_keys_other', []))}\n")
            f.write(f"Total Mnemonics: {len(extracted_data.get('mnemonics', []))}\n")
            f.write(f"Total Ethereum Addresses: {len(extracted_data.get('ethereum_addresses', []))}\n")
            f.write(f"Total API Keys: {len(extracted_data.get('api_keys', []))}\n")
