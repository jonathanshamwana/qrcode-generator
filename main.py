import os
import qrcode
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox

class CodeGenerator:
    def __init__(self):
        self.window = Tk()
        self.window.title("Batch QR Code Generator")
        self.window.geometry("700x675")
        self.window.config(padx=20, pady=30)
        self.window.resizable(width=False, height=False)

        self.heading = Label(
            self.window, text="Generate QR Codes in Bulk", font=("Helvetica", 24)
        )
        self.heading.grid(row=0, column=0, columnspan=3, pady=(15, 30))

        logo_image = PhotoImage(file="images/code.png")
        self.logo_label = Label(self.window, image=logo_image)
        self.logo_label.grid(row=1, column=0, columnspan=3, pady=(15, 30))

        self.label_frame = LabelFrame(self.window)
        self.label_frame.grid(row=4, column=0, columnspan=3, pady=(10, 20))

        self.instructions_title = Label(self.label_frame, text="Instructions:")
        self.instructions_title.grid(row=4, column=0, columnspan=3, pady=(10, 0))

        instructions_text = """1. Create a spreadsheet of which all your data will go in the first column. 
2. For each row, enter your url + a comma + your desired file name.
E.g., https://google.com,google-search
3. Save the spreadsheet as a csv.
4. Upload the csv. Wait a second as your qr codes are saved in separate image files."""
        self.instructions_label = Label(
            self.label_frame, text=instructions_text, justify="left"
        )
        self.instructions_label.grid(row=5, column=0, columnspan=3, pady=(10, 30), padx=10, sticky="w")

        self.upload_button = Button(
            self.window, text="Upload CSV", command=self.generate_qr_codes
        )
        self.upload_button.grid(row=6, column=1, pady=(10, 0), sticky="w")

        self.window.grid_columnconfigure(0, weight=1)
        self.window.grid_columnconfigure(2, weight=1)

        self.window.mainloop()

    def generate_qr_codes(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])

        if not file_path:
            messagebox.showwarning("No CSV File", "Please upload a CSV file first.")
            return

        with open(file_path, "r") as file:
            lines = file.readlines()

        generated_qr_codes = 0  # Track the number of successfully generated QR codes

        # Create the 'codes' directory if it doesn't exist
        if not os.path.exists("codes"):
            os.makedirs("codes")

        for index, line in enumerate(lines):
            data = line.strip().split(",")
            if len(data) == 2:
                link = data[0].strip()
                filename = data[1].strip()
                qr = qrcode.QRCode(
                    version=1,
                    error_correction=qrcode.constants.ERROR_CORRECT_H,
                    box_size=10,
                    border=4,
                )
                qr.add_data(link)
                qr.make(fit=True)

                img = qr.make_image(fill_color="black", back_color="white")

                img_file = f"codes/{filename}.png"  # Save the QR code file in the 'codes' directory
                img.save(img_file)
                generated_qr_codes += 1
            else:
                print(f"Skipping line {index+1} due to incorrect format.")

        if generated_qr_codes > 0:
            messagebox.showinfo(
                "Success", f"{generated_qr_codes} QR codes generated successfully!"
            )
        else:
            messagebox.showwarning("No QR Codes", "No QR codes were generated.")

app = CodeGenerator()
