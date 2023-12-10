import tkinter as tk

def text_to_code(text):
    text = text.upper()
    code = ""
    for char in text:
        if char.isalpha():
            grid = (ord(char) - ord('A')) // 9
            row = (ord(char) - ord('A')) % 3  # Swap row and column
            col = (ord(char) - ord('A')) % 9 // 3  # Swap row and column
            code += f"{grid + 1}{row + 1}{col + 1}"
        elif char.isdigit():
            if char == '0':
                code += "400"
            else:
                grid = 4
                row = (int(char) - 1) % 3
                col = (int(char) - 1) // 3
                code += f"{grid}{row + 1}{col + 1}"
        elif char == ' ':
            code += "333"  # SPACE is represented by (3rd grid, 3rd row, 3rd column)
        # else:
        #     # Special characters in grids 5, 6, and 7
        #     special_chars = '@#$%&()!"\'?;:,.\/<>=_-+*^[]{}~'
        #     if char in special_chars:
        #         grid = special_chars.index(char) // 9 + 5
        #         row = special_chars.index(char) % 3
        #         col = special_chars.index(char) // 3 % 3
        #         code += f"{grid}{row + 1}{col + 1}"

    return code

def code_to_text(code):
    text = ""
    while code:
        if len(code) < 3:
            raise ValueError("Invalid code format")

        if code.startswith("400"):
            text += '0'
            code = code[3:]
        else:
            grid = int(code[0])
            row = int(code[1])
            col = int(code[2])

            if grid == 4:
                num = (col - 1) * 3 + row + 1
                text += str(num)
            elif grid >= 5 and grid <= 7:
                special_chars = '@#$%&()!"\'?;:,.\/<>=_-+*^[]{}~'
                text += special_chars[(grid - 5) * 9 + col - 1 + row * 3]
            else:
                char_num = (grid - 1) * 9 + (col - 1) * 3 + (row - 1)  # Swap row and column
                if char_num < 26:
                    text += chr(ord('A') + char_num)
                elif char_num == 26:
                    text += ' '  # SPACE
                else:
                    raise ValueError("Invalid code")

            code = code[3:]

    return text

def update_preview(event):
    current_box = event.widget
    current_text = current_box.get()

    if current_box is encrypt_entry:
        encrypted_code = text_to_code(current_text)
        decrypt_entry.delete(0, tk.END)
        decrypt_entry.insert(0, encrypted_code)
    elif current_box is decrypt_entry:
        decrypted_text = code_to_text(current_text)
        encrypt_entry.delete(0, tk.END)
        encrypt_entry.insert(0, decrypted_text)

# Create main window
window = tk.Tk()
window.title("Text Code Converter")

# Create input widgets
encrypt_label = tk.Label(window, text="Encrypt:")
encrypt_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
encrypt_entry = tk.Entry(window, width=30)
encrypt_entry.grid(row=0, column=1, padx=10, pady=5)
encrypt_entry.bind("<KeyRelease>", update_preview)

decrypt_label = tk.Label(window, text="Decrypt:")
decrypt_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
decrypt_entry = tk.Entry(window, width=50)
decrypt_entry.grid(row=1, column=1, padx=10, pady=5)
decrypt_entry.bind("<KeyRelease>", update_preview)

# Run the Tkinter event loop
window.mainloop()
