# 🔐 SecureVault

![Python](https://img.shields.io/badge/Python-3.14-3776AB?style=for-the-badge&logo=python&logoColor=white)
![AES-256](https://img.shields.io/badge/Encryption-AES--256--CBC-red?style=for-the-badge&logo=letsencrypt&logoColor=white)
![HMAC](https://img.shields.io/badge/Integrity-HMAC--SHA256-orange?style=for-the-badge&logo=verizon&logoColor=white)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-blue?style=for-the-badge&logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

A desktop application for encrypting and decrypting files securely using AES-256 encryption, built with Python and Tkinter.

---

## 📋 Project Description

SecureVault is a cryptography focused desktop application that allows users to encrypt any file (PDF, JPG, DOCX, PNG, etc.) using a password and decrypt it back using the same password. It uses industry-standard cryptographic techniques to ensure files are protected against brute-force attacks, tampering, and pattern analysis.

---

## ✨ Features

- Encrypt any file type (PDF, JPG, DOCX, PNG, TXT, and more)
- Decrypt encrypted `.enc` files back to their original format
- AES-256-CBC encryption — industry standard, never cracked
- PBKDF2 key derivation with 100,000 iterations — brute-force resistant
- HMAC-SHA256 authentication — detects tampering before decryption
- Random salt and IV generated for every encryption — defeats pattern attacks
- Brute-force lockout after 3 wrong password attempts
- Clean dark-themed desktop GUI built with Tkinter
- All encrypted files saved neatly to `encrypted_files/` folder

---

## 🛠️ Technologies Used

- Python 3
- Tkinter — GUI framework
- PyCryptodome — AES encryption, PBKDF2 key derivation, padding
- HMAC (Python standard library) — file integrity verification
- Hashlib (Python standard library) — SHA-256 hashing
- OS & Sys (Python standard library) — file handling and system operations

---

## 📁 Project Structure
securevault-1/
│
├── ui.py                        # Main GUI — all buttons, layout, and user interaction
│
├── core/
│   ├── init.py
│   ├── key_manager.py           # Password → AES-256 key using PBKDF2 + random salt
│   ├── encryptor.py             # AES-256-CBC encryption + HMAC generation
│   └── decryptor.py             # HMAC verification + AES-256-CBC decryption
│
├── utils/
│   ├── init.py
│   ├── file_handler.py          # Builds input/output file paths automatically
│   └── validator.py             # Input validation + wrong attempt lockout
│
├── encrypted_files/             # All .enc files are saved here automatically
│
├── fuzzy_search.py              # Typo-tolerant keyword search over encrypted file tags (v2)
│
└── requirements.txt             # Project dependencies

---

## ▶️ How To Run

**1. Clone or download the project**

**2. Create and activate virtual environment**
```bash
python -m venv .venv
.venv\Scripts\activate
```

**3. Install dependencies**
```bash
pip install pycryptodome
```

**4. Create the encrypted files folder**
```bash
mkdir encrypted_files
```

**5. Run the application**
```bash
python ui.py
```

---

## 🔒 Security Concepts Used

- **AES-256-CBC** — Advanced Encryption Standard with 256-bit key in Cipher Block Chaining mode
- **PBKDF2** — Password-Based Key Derivation Function 2, runs 100,000 SHA-256 iterations to slow brute-force attacks
- **Random Salt** — 16 bytes of randomness added to password before key derivation, defeats rainbow table attacks
- **IV (Initialization Vector)** — Fresh random 16 bytes generated every encryption, ensures identical files encrypt differently each time
- **HMAC-SHA256** — Cryptographic signature over the encrypted data, detects any tampering before decryption begins
- **Encrypt-then-MAC** — HMAC is calculated after encryption, the most secure ordering
- **Timing-safe comparison** — `hmac.compare_digest()` used instead of `==` to prevent timing attacks
- **Brute-force lockout** — Application exits after 3 wrong password attempts

---
## 🔍 New in v2: Fuzzy Keyword Search over Encrypted Tags

SecureVault v2 adds typo-tolerant keyword search, so files can be found by tag even with small spelling mistakes, without ever storing tags in plaintext.

Inspired by the wildcard-based fuzzy keyword search technique from:
> J. Wang, H. Ma, Q. Tang, J. Li, H. Zhu, S. Ma, X. Chen, "Efficient Verifiable Fuzzy Keyword Search over Encrypted Data in Cloud Computing," *ComSIS* Vol. 10, No. 2, 2013.

**How it works:**
- Each tag generates a set of wildcard variants (e.g. `bank` → `b*nk`, `ban*`, `*bank`, etc.), covering all single-character edits
- Every variant is hashed with HMAC-SHA256 (the same primitive SecureVault already uses for integrity checks) to produce a **trapdoor**
- Trapdoors are stored in an index mapping hash → file ID — the actual tag word is never stored
- A search query goes through the same wildcard + hash process; if a query's trapdoor matches one already in the index, the file is found — even with a typo

**Adapted for a local, single-user context:**
- The original paper's symbol-tree index (built for large-scale cloud datasets) is replaced with a flat dictionary lookup, since SecureVault's scale doesn't need the O(1) tree optimization
- The paper's verifiability layer (proving an untrusted cloud server didn't cheat) isn't included, since there's no untrusted server in this architecture — noted here as a natural extension if SecureVault is ever deployed in a client-server model

---


## 🚀 Future Improvements

- Add a password strength checker before encryption
- Support encrypting entire folders at once
- Add a progress bar for large file encryption
- Implement a secure password manager to store hints
- Add file shredding — securely delete original after encryption
- Cross-platform packaging as a standalone `.exe` using PyInstaller
- Add drag-and-drop file support to the GUI

---

##  Screenshot
![Main UI](assets/ui_main.png)

---

## 👤 Author

**Sara Ahmed**
Cybersecurity Project — SecureVault
Built with Python, PyCryptodome, and Tkinter


[def]: assets/ui_main.png