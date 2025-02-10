import smtplib
import random
import tkinter as tk
from tkinter import messagebox
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Function to generate a 6-digit OTP
def generate_otp():
    return str(random.randint(100000, 999999))

# Function to send the OTP to the user's email
def send_email(recipient_email, otp):
    try:
        # Email configurations
        sender_email = "monakumari08@gmail.com"
        sender_password = "niueguwoshoruejc" 

        # Setting up the email message
        subject = "Your OTP Verification Code"
        body = f"Your One-Time Password (OTP) is: {otp}\n\nThis OTP is valid for 5 minutes."
        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = recipient_email
        message['Subject'] = subject
        message.attach(MIMEText(body, 'plain'))

        # Sending email using SMTP server
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()  # Enable encryption
            server.login(sender_email, sender_password)
            server.send_message(message)
        
        print("OTP sent successfully to email.")
    except smtplib.SMTPAuthenticationError:
        messagebox.showerror("Error", "Authentication failed. Check email or app password.")
        exit(1)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to send email: {e}")
        exit(1)

# GUI: Function to handle sending OTP
def send_otp_gui():
    email = email_entry.get()
    if email:
        otp = generate_otp()
        send_email(email, otp)
        global generated_otp
        generated_otp = otp
        global retries
        retries = 3  # Reset retries when a new OTP is sent
        messagebox.showinfo("Success", "OTP sent to your email!")
    else:
        messagebox.showwarning("Warning", "Please enter an email address.")

# GUI: Function to handle verifying OTP with retries
def verify_otp_gui():
    global retries  # Track retries
    entered_otp = otp_entry.get().strip()
    if entered_otp == generated_otp:
        messagebox.showinfo("Success", "OTP verified successfully! Access granted.")
        root.destroy()  # Close the application upon successful verification
    else:
        retries -= 1
        if retries > 0:
            messagebox.showwarning("Warning", f"Incorrect OTP. You have {retries} attempt(s) remaining.")
        else:
            messagebox.showerror("Error", "Verification failed. Access denied.")
            root.destroy()  # Close the application after exhausting retries

# Validation function to restrict OTP input to 6 digits
def validate_otp_input(new_value):
    # Allow only digits and restrict to a maximum of 6 characters
    return new_value.isdigit() and len(new_value) <= 6

# Setting up GUI
root = tk.Tk()
root.title("OTP Verification System")
root.geometry("400x300")         # Set window size
root.configure(bg="#7BC9FF")     # Set background color

# Custom Styles
label_font = ("Arial", 11, "bold")
entry_font = ("Arial", 11)
button_font = ("Arial", 11, "bold")
button_bg = "#4834d4"            # Dark blue for buttons
button_fg = "#ffffff"            # White text for buttons
label_fg = "#130f40"             # Dark color for text labels

# Header Label
header_label = tk.Label(root, text="OTP Verification System", font=("Arial", 16, "bold"), bg="#D9EAFD", fg="#333")
header_label.pack(pady=10)

# Email Label and Entry
email_label = tk.Label(root, text="Enter Email:", font=label_font, bg="#D9EAFD", fg="#333")
email_label.pack(pady=(10, 5))
email_entry = tk.Entry(root, font=entry_font, width=30, relief="solid", bd=1)  # Added border with `relief` and `bd`
email_entry.pack(pady=(0, 10))

# Send OTP Button
send_otp_button = tk.Button(root, text="Send OTP", font=button_font, bg=button_bg, fg=button_fg, command=send_otp_gui)
send_otp_button.pack(pady=(0, 20))

# OTP Label and Entry
otp_label = tk.Label(root, text="Enter OTP:", font=label_font, bg="#D9EAFD", fg="#333")
otp_label.pack(pady=(10, 5))

# Set up validation for OTP entry
otp_validation = root.register(validate_otp_input)
otp_entry = tk.Entry(root, font=entry_font, width=15, validate="key", validatecommand=(otp_validation, "%P"), relief="solid", bd=1)
otp_entry.pack(pady=(0, 10))

# Verify OTP Button
verify_otp_button = tk.Button(root, text="Verify OTP", font=button_font, bg=button_bg, fg=button_fg, command=verify_otp_gui)
verify_otp_button.pack(pady=(0, 20))


# Run the GUI
root.mainloop()
