# ui.py
# SecureVault — Desktop GUI using Tkinter
# Dark cybersecurity theme with full encrypt/decrypt functionality

import tkinter as tk
from tkinter import filedialog
import threading
import os

import utils.validator as validator_module
from core.encryptor import encrypt_file
from core.decryptor import decrypt_file
from utils.file_handler import get_output_encrypt_path, get_output_decrypt_path
from utils.validator import (validate_file_for_encryption, validate_file_for_decryption,
                              validate_password, check_attempts, reset_attempts)

# ─── COLORS & FONTS ────────────────────────────────────────────
BG          = "#0d0d0d"
PANEL       = "#111111"
BORDER      = "#1f1f1f"
GREEN       = "#00ff88"
GREEN_DIM   = "#00aa55"
RED         = "#ff4444"
YELLOW      = "#ffcc00"
TEXT        = "#e0e0e0"
TEXT_DIM    = "#666666"
FONT_TITLE  = ("Courier New", 22, "bold")
FONT_HEAD   = ("Courier New", 11, "bold")
FONT_BODY   = ("Courier New", 10)
FONT_SMALL  = ("Courier New", 9)


class SecureVaultApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SecureVault — AES-256 File Encryption")
        self.root.geometry("700x620")
        self.root.resizable(False, False)
        self.root.configure(bg=BG)

        self.selected_file = tk.StringVar(value="No file selected")
        self._build_ui()

    def _build_ui(self):
        self._build_header()
        self._build_file_selector()
        self._build_password_section()
        self._build_buttons()
        self._build_log()
        self._build_footer()

    def _build_header(self):
        header = tk.Frame(self.root, bg=BG)
        header.pack(fill="x", padx=30, pady=(25, 5))

        tk.Label(header, text="🔐 SecureVault", font=FONT_TITLE,
                 fg=GREEN, bg=BG).pack(anchor="w")

        tk.Label(header, text="AES-256 · PBKDF2 · HMAC-SHA256  |  Your files. Your password. No one else.",
                 font=FONT_SMALL, fg=TEXT_DIM, bg=BG).pack(anchor="w")

        tk.Frame(self.root, bg=BORDER, height=1).pack(fill="x", padx=30, pady=(10, 0))

    def _build_file_selector(self):
        frame = tk.Frame(self.root, bg=PANEL, highlightbackground=BORDER,
                         highlightthickness=1)
        frame.pack(fill="x", padx=30, pady=15)

        tk.Label(frame, text="SELECTED FILE", font=FONT_SMALL,
                 fg=TEXT_DIM, bg=PANEL).pack(anchor="w", padx=15, pady=(10, 0))

        row = tk.Frame(frame, bg=PANEL)
        row.pack(fill="x", padx=15, pady=(5, 12))

        path_box = tk.Entry(row, textvariable=self.selected_file,
                            font=FONT_BODY, fg=GREEN, bg="#0a0a0a",
                            insertbackground=GREEN, relief="flat",
                            highlightbackground=BORDER, highlightthickness=1,
                            state="readonly", readonlybackground="#0a0a0a")
        path_box.pack(side="left", fill="x", expand=True, ipady=6, padx=(0, 10))

        tk.Button(row, text="Browse", font=FONT_HEAD,
                  fg=BG, bg=GREEN, activebackground=GREEN_DIM,
                  relief="flat", cursor="hand2", padx=14,
                  command=self._browse_file).pack(side="right")

    def _build_password_section(self):
        frame = tk.Frame(self.root, bg=PANEL, highlightbackground=BORDER,
                         highlightthickness=1)
        frame.pack(fill="x", padx=30, pady=(0, 15))

        tk.Label(frame, text="PASSWORD", font=FONT_SMALL,
                 fg=TEXT_DIM, bg=PANEL).pack(anchor="w", padx=15, pady=(10, 0))

        row1 = tk.Frame(frame, bg=PANEL)
        row1.pack(fill="x", padx=15, pady=(5, 5))

        tk.Label(row1, text="Enter:", font=FONT_BODY, fg=TEXT, bg=PANEL,
                 width=8, anchor="w").pack(side="left")
        self.pw_entry = tk.Entry(row1, font=FONT_BODY, fg=GREEN, bg="#0a0a0a",
                                 show="●", insertbackground=GREEN,
                                 relief="flat", highlightbackground=BORDER,
                                 highlightthickness=1)
        self.pw_entry.pack(side="left", fill="x", expand=True, ipady=6)

        row2 = tk.Frame(frame, bg=PANEL)
        row2.pack(fill="x", padx=15, pady=(0, 12))

        tk.Label(row2, text="Confirm:", font=FONT_BODY, fg=TEXT, bg=PANEL,
                 width=8, anchor="w").pack(side="left")
        self.pw_confirm = tk.Entry(row2, font=FONT_BODY, fg=GREEN, bg="#0a0a0a",
                                   show="●", insertbackground=GREEN,
                                   relief="flat", highlightbackground=BORDER,
                                   highlightthickness=1)
        self.pw_confirm.pack(side="left", fill="x", expand=True, ipady=6)

        # Show/hide password toggle
        self.show_pw = tk.BooleanVar(value=False)
        tk.Checkbutton(frame, text="Show password", font=FONT_SMALL,
                       fg=TEXT_DIM, bg=PANEL, activebackground=PANEL,
                       selectcolor=PANEL, variable=self.show_pw,
                       command=self._toggle_password
                       ).pack(anchor="w", padx=15, pady=(0, 8))

    def _build_buttons(self):
        row = tk.Frame(self.root, bg=BG)
        row.pack(fill="x", padx=30, pady=(0, 15))

        tk.Button(row, text="🔒  ENCRYPT FILE", font=FONT_HEAD,
                  fg=BG, bg=GREEN, activebackground=GREEN_DIM,
                  relief="flat", cursor="hand2", pady=10,
                  command=self._run_encrypt).pack(side="left", fill="x",
                                                   expand=True, padx=(0, 8))

        tk.Button(row, text="🔓  DECRYPT FILE", font=FONT_HEAD,
                  fg=GREEN, bg="#0d2b1a", activebackground="#0a1f13",
                  relief="flat", cursor="hand2", pady=10,
                  highlightbackground=GREEN, highlightthickness=1,
                  command=self._run_decrypt).pack(side="left", fill="x",
                                                   expand=True, padx=(8, 0))

    def _build_log(self):
        frame = tk.Frame(self.root, bg=PANEL, highlightbackground=BORDER,
                         highlightthickness=1)
        frame.pack(fill="both", expand=True, padx=30, pady=(0, 10))

        header_row = tk.Frame(frame, bg=PANEL)
        header_row.pack(fill="x", padx=15, pady=(8, 0))

        tk.Label(header_row, text="ACTIVITY LOG", font=FONT_SMALL,
                 fg=TEXT_DIM, bg=PANEL).pack(side="left")

        tk.Button(header_row, text="Clear", font=FONT_SMALL,
                  fg=TEXT_DIM, bg=PANEL, relief="flat", cursor="hand2",
                  command=self._clear_log).pack(side="right")

        self.log = tk.Text(frame, font=FONT_SMALL, fg=TEXT, bg="#080808",
                           relief="flat", state="disabled",
                           highlightthickness=0, padx=10, pady=8,
                           height=8)
        self.log.pack(fill="both", expand=True, padx=15, pady=(5, 12))

        self.log.tag_config("success", foreground=GREEN)
        self.log.tag_config("error",   foreground=RED)
        self.log.tag_config("warning", foreground=YELLOW)
        self.log.tag_config("info",    foreground=TEXT_DIM)

    def _build_footer(self):
        tk.Label(self.root,
                 text="SecureVault v1.0  ·  BCA Major Project  ·  Built with PyCryptodome",
                 font=FONT_SMALL, fg=TEXT_DIM, bg=BG
                 ).pack(pady=(0, 12))

    def _log(self, message: str, tag: str = "info"):
        """Append a message to the activity log."""
        self.log.config(state="normal")
        self.log.insert("end", f"  {message}\n", tag)
        self.log.see("end")
        self.log.config(state="disabled")

    def _clear_log(self):
        self.log.config(state="normal")
        self.log.delete("1.0", "end")
        self.log.config(state="disabled")

    def _browse_file(self):
        """Open file picker — accepts all file types."""
        path = filedialog.askopenfilename(
            title="Select a file to encrypt or decrypt",
            filetypes=[("All files", "*.*"),
                       ("PDF files", "*.pdf"),
                       ("Images", "*.jpg *.jpeg *.png"),
                       ("Documents", "*.docx *.txt"),
                       ("Encrypted", "*.enc")]
        )
        if path:
            self.selected_file.set(path)
            self._log(f"Selected: {os.path.basename(path)}", "info")

    def _toggle_password(self):
        """Toggle password visibility."""
        new_show = "" if self.show_pw.get() else "●"
        self.pw_entry.config(show=new_show)
        self.pw_confirm.config(show=new_show)

    def _run_encrypt(self):
        file_path = self.selected_file.get()
        password  = self.pw_entry.get()
        confirm   = self.pw_confirm.get()

        if file_path == "No file selected":
            self._log("Please select a file first.", "warning")
            return
        if not validate_file_for_encryption(file_path):
            self._log("Invalid file. Already encrypted or not found.", "error")
            return
        if not validate_password(password):
            self._log("Password cannot be empty.", "error")
            return
        if password != confirm:
            self._log("Passwords do not match. Please re-enter.", "error")
            return

        output_path = get_output_encrypt_path(file_path)
        self._log(f"Encrypting: {os.path.basename(file_path)} ...", "info")

        def task():
            success = encrypt_file(file_path, output_path, password)
            if success:
                self._log("✓ Encrypted successfully!", "success")
                self._log(f"✓ Saved to: {output_path}", "success")
                self._clear_passwords()
            else:
                self._log("✗ Encryption failed. Check the file.", "error")

        threading.Thread(target=task, daemon=True).start()

    def _run_decrypt(self):
        file_path = self.selected_file.get()
        password  = self.pw_entry.get()

        if file_path == "No file selected":
            self._log("Please select a file first.", "warning")
            return
        if not validate_file_for_decryption(file_path):
            self._log("Invalid file. Must be a .enc file.", "error")
            return
        if not validate_password(password):
            self._log("Password cannot be empty.", "error")
            return

        # Show remaining attempts
        remaining = validator_module.MAX_ATTEMPTS - validator_module.failed_attempts
        if validator_module.failed_attempts > 0:
            self._log(f"Warning: {remaining} attempt(s) remaining.", "warning")

        output_path = get_output_decrypt_path(file_path)
        self._log(f"Decrypting: {os.path.basename(file_path)} ...", "info")

        def task():
            success = decrypt_file(file_path, output_path, password)
            if success:
                self._log("✓ Decrypted successfully!", "success")
                self._log(f"✓ Saved to: {output_path}", "success")
                reset_attempts()
                self._clear_passwords()
            else:
                # Manually increment and check
                validator_module.failed_attempts += 1
                remaining = validator_module.MAX_ATTEMPTS - validator_module.failed_attempts
                if validator_module.failed_attempts >= validator_module.MAX_ATTEMPTS:
                    self._log("✗ Too many wrong attempts. Restart the app.", "error")
                else:
                    self._log(f"✗ Wrong password. {remaining} attempt(s) left.", "error")

        threading.Thread(target=task, daemon=True).start()

    def _clear_passwords(self):
        """Clear password fields after operation for security."""
        self.pw_entry.delete(0, "end")
        self.pw_confirm.delete(0, "end")


# ─── ENTRY POINT ────────────────────────────────────────────────
if __name__ == "__main__":
    root = tk.Tk()
    app = SecureVaultApp(root)
    root.mainloop()