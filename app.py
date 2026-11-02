import tkinter as tk

from tkinter import ttk, messagebox
import json
from unittest import result
import urllib.request  # part of stdlib; no external libs needed

API_URL = "http://localhost:5000/submit"

root = tk.Tk()
root.title("Mini Form App")

# ---------- FORM VARIABLES ----------
PID_var = tk.IntVar()
price_var = tk.DoubleVar(value=0.0)
Desc_var = tk.StringVar()
name_var = tk.StringVar()
email_var = tk.StringVar()
purchase = tk.BooleanVar()

# ---------- LAYOUT ----------
frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E))


def validate() -> bool:
    """Return True if all fields are valid; otherwise show an error."""
    # Simple non‑empty checks
    if not PID_var.get():
        messagebox.showerror("Validation Error", "Product ID cannot be empty.")
        return False
    email = email_var.get().strip()
    if not email or "@" not in email:
        messagebox.showerror("Validation Error", "Enter a valid email address.")
        return False
    Desc = Desc_var.get().strip()
    if not Desc:
        messagebox.showerror("Validation Error", "Description cannot be empty.")
        return False
    name = name_var.get().strip()
    if not name:
        messagebox.showerror("Validation Error", "Name cannot be empty.")
        return False
    price = price_var.get()
    if price <= 0 or price >= 1000:
        messagebox.showerror("Validation Error", "Price must be between 0 and 1000.")
        return False
    return True


def collect_data() -> dict:
    """Return a dictionary that represents the form."""
    return {
        "pid": PID_var.get(),
        "description": Desc_var.get().strip(),
        "price": price_var.get(),
        "email": email_var.get().strip(),
        "name": name_var.get().strip(),
        "purchase": purchase.get(),
    }


def submit_form() -> None:
    if not validate():
        return  # abort if validation failed
    payload = collect_data()
    json_payload = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        API_URL,
        data=json_payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req) as resp:
            result = json.loads(resp.read().decode())
            messagebox.showinfo("Success", f"Server replied: {result}")
    except urllib.error.HTTPError as e:
        error_msg = e.read().decode()
        messagebox.showerror("API Error", f"{e.code} – {error_msg}")
    except Exception as exc:
        messagebox.showerror("Connection Error", str(exc))


# Product ID
ttk.Label(frame, text="Product ID:").grid(column=0, row=0, sticky=tk.W)
PID_entry = ttk.Entry(frame, width=30, textvariable=PID_var)
PID_entry.grid(column=1, row=0)

# Description
ttk.Label(frame, text="Description:").grid(column=0, row=1, sticky=tk.W)
Description_entry = ttk.Entry(frame, width=30, textvariable=Desc_var)
Description_entry.grid(column=1, row=1)

# Price
ttk.Label(frame, text="Price:").grid(column=0, row=2, sticky=tk.W)
price_entry = ttk.Entry(frame, width=30, textvariable=price_var)
price_entry.grid(column=1, row=2)

# Name
ttk.Label(frame, text="Name:").grid(column=0, row=3, sticky=tk.W)
name_entry = ttk.Entry(frame, width=30, textvariable=name_var)
name_entry.grid(column=1, row=3)

# Email
ttk.Label(frame, text="Email:").grid(column=0, row=4, sticky=tk.W)
email_entry = ttk.Entry(frame, width=30, textvariable=email_var)
email_entry.grid(column=1, row=4)

# Purchase checkbox
purchase_cb = ttk.Checkbutton(
    frame, text="Is this an in-store purchase?", variable=purchase
)
purchase_cb.grid(columnspan=2, row=5, sticky=tk.W)

# Submit button
submit_btn = ttk.Button(frame, text="Submit", command=lambda: submit_form())
submit_btn.grid(row=6, columnspan=2, pady=(10, 0))

if __name__ == "__main__":
    root.mainloop()
