PATTERNS = {
    "dangerous_files": [
        "filename:hardhat.config.js",
        "filename:deploy.js",
        "filename:.env",
        "filename:.env.example",
        "filename:.env.local",
        "filename:.env.production",
        "filename:.env.development",
        "filename:.env.test",
        "filename:.env.staging",
        "filename:env",
        "filename:environment",
        "filename:mnemonic.txt",
        "filename:wallet.js",
        "filename:config.js",
        "filename:secrets.js",
        "filename:keys.js",
        "filename:credentials.js",
        "filename:secret.js",
        "filename:private.js",
        "filename:key.js",
        "filename:api.js",
        "filename:auth.js",
        "filename:token.js",
        "filename:access.js",
        "filename:.secrets",
        "filename:secrets.json",
        "filename:config.json",
        "filename:credentials.json",
        "filename:keys.json",
        "filename:private.json"
    ],
    "dangerous_patterns": [
        "ethers.Wallet",
        "Wallet.fromMnemonic",
        "new ethers.Wallet",
        "privateKey",
        "private_key",
        "private-key",
        "PRIVATE_KEY",
        "PRIVATE-KEY",
        "PRIVATE_KEY",
        "mnemonic",
        "MNEMONIC",
        "owner",
        "secretKey",
        "secret_key",
        "secret-key",
        "SECRET_KEY",
        "process.env.PRIVATE_KEY",
        "process.env.MNEMONIC",
        "process.env.SECRET",
        "0x",
        "0x",
        "seed phrase",
        "seed_phrase",
        "seed-phrase",
        "SEED_PHRASE",
        "recovery phrase",
        "recovery_phrase",
        "recovery-phrase",
        "RECOVERY_PHRASE",
        "wallet seed",
        "wallet_seed",
        "wallet-seed",
        "WALLET_SEED"
    ],
    "dangerous_strings": [
        "privateKey",
        "private_key",
        "private-key",
        "PRIVATE_KEY",
        "PRIVATE-KEY",
        "mnemonic",
        "MNEMONIC",
        "secretKey",
        "secret_key",
        "secret-key",
        "SECRET_KEY",
        "accessToken",
        "access_token",
        "access-token",
        "ACCESS_TOKEN",
        "seedPhrase",
        "seed_phrase",
        "seed-phrase",
        "SEED_PHRASE",
        "recoveryPhrase",
        "recovery_phrase",
        "recovery-phrase",
        "RECOVERY_PHRASE",
        "walletSeed",
        "wallet_seed",
        "wallet-seed",
        "WALLET_SEED"
    ]
}

def get_all_patterns():
    all_patterns = []
    
    all_patterns.extend(PATTERNS["dangerous_files"])
    
    for pattern in PATTERNS["dangerous_patterns"]:
        all_patterns.append(f'"{pattern}"')
    
    for string in PATTERNS["dangerous_strings"]:
        all_patterns.append(f'"{string}"')
    
    return all_patterns

def get_file_patterns():
    return PATTERNS["dangerous_files"]

def get_code_patterns():
    patterns = []
    for p in PATTERNS["dangerous_patterns"]:
        p_clean = p.replace('"', '').replace("'", "").replace("(", "").replace(")", "").replace("=", "").replace(":", "")
        if p_clean.strip():
            patterns.append(p_clean)
    for s in PATTERNS["dangerous_strings"]:
        s_clean = s.replace('"', '').replace("'", "").replace("(", "").replace(")", "").replace("=", "").replace(":", "")
        if s_clean.strip():
            patterns.append(s_clean)
    return patterns

