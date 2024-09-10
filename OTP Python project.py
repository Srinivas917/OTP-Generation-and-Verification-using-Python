import random
import smtplib
import time
import tkinter as tk
from tkinter import messagebox

class OTPGenerator:
    def __init__(self):
        self.otp = None
        self.expiry_time = None

    def generate_otp(self):
        # Generate a 6-digit OTP
        self.otp = random.randint(100000, 999999)
        # Set the expiry time (5 minutes from now)
        self.expiry_time = time.time() + 300
        return self.otp

    def send_otp(self, to_email):
        try:
            # Email configuration
            sender_email = "psr01283@gmail.com"
            sender_password = "pmdg pvhl scth ylxr"  # Use App Password if 2-Step Verification is enabled

            # Generate OTP
            otp = self.generate_otp()

            # Create the email message
            subject = "Your OTP Code"
            body = f"Your OTP is {otp}. It is valid for the next 5 minutes."
            message = f"Subject: {subject}\n\n{body}"

            # Send the email
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(sender_email, sender_password)
                server.sendmail(sender_email, to_email, message)

            print(f"OTP sent to {to_email}")
            return True

        except smtplib.SMTPAuthenticationError:
            messagebox.showerror("Authentication Error", "Invalid email credentials. Please check your email and password.")
            return False

        except smtplib.SMTPRecipientsRefused:
            messagebox.showerror("Invalid Email", "The email address provided is invalid.")
            return False

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
            return False

    def verify_otp(self, input_otp):
        try:
            if not input_otp.isdigit():
                raise ValueError("OTP should contain only digits.")

            input_otp = int(input_otp)

            # Check if the OTP is still valid
            if time.time() > self.expiry_time:
                return "OTP has expired."

            # Verify the provided OTP
            if input_otp == self.otp:
                return "OTP verified successfully."
            else:
                return "Invalid OTP. Please try again."

        except ValueError as e:
            return str(e)

        except Exception as e:
            return f"An error occurred: {e}"

# GUI Implementation
class OTPApp:
    def __init__(self, root):
        self.root = root
        self.root.title("OTP Generator and Verifier")
        self.otp_generator = OTPGenerator()

        # GUI Elements
        self.email_label = tk.Label(root, text="Enter Email:")
        self.email_label.grid(row=0, column=0, padx=10, pady=10)
        
        self.email_entry = tk.Entry(root, width=30)
        self.email_entry.grid(row=0, column=1, padx=10, pady=10)
        
        self.send_otp_button = tk.Button(root, text="Send OTP", command=self.send_otp)
        self.send_otp_button.grid(row=1, columnspan=2, pady=10)
        
        self.otp_label = tk.Label(root, text="Enter OTP:")
        self.otp_label.grid(row=2, column=0, padx=10, pady=10)
        
        self.otp_entry = tk.Entry(root, width=10)
        self.otp_entry.grid(row=2, column=1, padx=10, pady=10)
        
        self.verify_otp_button = tk.Button(root, text="Verify OTP", command=self.verify_otp)
        self.verify_otp_button.grid(row=3, columnspan=2, pady=10)
        
    def send_otp(self):
        recipient_email = self.email_entry.get()
        if recipient_email:
            if self.otp_generator.send_otp(recipient_email):
                messagebox.showinfo("Success", "OTP has been sent to your email.")
        else:
            messagebox.showwarning("Input Error", "Please enter an email address.")
        
    def verify_otp(self):
        input_otp = self.otp_entry.get()
        if input_otp:
            result = self.otp_generator.verify_otp(input_otp)
            messagebox.showinfo("Verification Result", result)
        else:
            messagebox.showwarning("Input Error", "Please enter the OTP.")

# Create the main window
root = tk.Tk()
app = OTPApp(root)
root.mainloop()
