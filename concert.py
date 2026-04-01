import mysql.connector
import tkinter as tk
from tkinter import messagebox, ttk
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# ---------------- PLACEHOLDER ---------------- #
def add_placeholder(entry, text, is_password=False):
    entry.insert(0, text)
    entry.config(fg="grey")

    def on_focus_in(e):
        if entry.get() == text:
            entry.delete(0, tk.END)
            entry.config(fg="black")
            if is_password:
                entry.config(show="*")

    def on_focus_out(e):
        if entry.get() == "":
            entry.insert(0, text)
            entry.config(fg="grey")
            if is_password:
                entry.config(show="")

    entry.bind("<FocusIn>", on_focus_in)
    entry.bind("<FocusOut>", on_focus_out)

# ---------------- DATABASE ---------------- #
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="admin"
)
cursor = db.cursor()
cursor.execute("CREATE DATABASE IF NOT EXISTS ConcertDB")
cursor.execute("USE ConcertDB")

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
id INT AUTO_INCREMENT PRIMARY KEY,
email VARCHAR(100) UNIQUE,
password VARCHAR(100),
role VARCHAR(20)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS concerts(
id INT AUTO_INCREMENT PRIMARY KEY,
artist_name VARCHAR(100),
concert_name VARCHAR(100),
venue VARCHAR(100),
concert_date VARCHAR(50),
available_tickets INT,
price INT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS bookings(
id INT AUTO_INCREMENT PRIMARY KEY,
user_email VARCHAR(100),
artist_name VARCHAR(100),
tickets INT,
total_paid INT
)
""")

# ---------------- EMAIL ---------------- #
def send_email(to_email, artist, qty, total):
    try:
        sender = "sudhakondass19@gmail.com"
        app_password = "hnjzjyzwsbsmrjds"

        msg = MIMEMultipart()
        msg["From"] = sender
        msg["To"] = to_email
        msg["Subject"] = " Booking Confirmed"

        body = f"""
Hi your booking for your concert is successful

Artist: {artist}
Tickets: {qty}
Total: ₹{total}

Please show this email as an Entry pass
Enjoy the concert 

With regards,
Concert pro
"""
        msg.attach(MIMEText(body, "plain"))

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender, app_password)
        server.sendmail(sender, to_email, msg.as_string())
        server.quit()

    except Exception as e:
        print("Email Error:", e)

# ---------------- ADMIN PANEL ---------------- #
def open_admin():
    win = tk.Toplevel(root)
    win.title("Admin Panel")
    win.geometry("750x600")
    win.configure(bg="#eef2ff")

    tk.Label(win, text="Manage Concerts ", font=("Segoe UI", 18, "bold"), bg="#eef2ff").pack(pady=10)

    frame = tk.Frame(win, bg="#eef2ff")
    frame.pack()

    fields = ["Artist", "Tour", "Venue", "Date", "Tickets", "Price"]
    entries = []

    for i, f in enumerate(fields):
        tk.Label(frame, text=f, bg="#eef2ff").grid(row=i, column=0, padx=5, pady=5)
        e = tk.Entry(frame, width=25)
        e.grid(row=i, column=1, pady=5)
        add_placeholder(e, f"Enter {f}")
        entries.append(e)

    # TABLE
    columns = ("ID", "Artist", "Tour", "Venue", "Date", "Tickets", "Price")
    tree = ttk.Treeview(win, columns=columns, show="headings", height=8)

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor="center", width=100)

    tree.pack(pady=10)

    def load_data():
        tree.delete(*tree.get_children())
        cursor.execute("SELECT * FROM concerts")
        for row in cursor.fetchall():
            tree.insert("", tk.END, values=row)

    load_data()

    # SELECT ROW
    def select_item(event):
        selected = tree.selection()
        if selected:
            item = tree.item(selected)
            values = item["values"]

            for i in range(len(entries)):
                entries[i].delete(0, tk.END)
                entries[i].insert(0, values[i+1])

    tree.bind("<ButtonRelease-1>", select_item)

    # ADD
    def add():
        data = [e.get() for e in entries]
        if "" in data or any("Enter" in d for d in data):
            messagebox.showerror("Error", "Fill all fields")
            return

        cursor.execute("""
        INSERT INTO concerts (artist_name, concert_name, venue, concert_date, available_tickets, price)
        VALUES (%s,%s,%s,%s,%s,%s)
        """, (data[0], data[1], data[2], data[3], int(data[4]), int(data[5])))
        db.commit()
        load_data()
        messagebox.showinfo("Success", "Added")

    # UPDATE
    def update():
        selected = tree.selection()
        if not selected:
            messagebox.showerror("Error", "Select row")
            return

        cid = tree.item(selected)["values"][0]
        data = [e.get() for e in entries]

        cursor.execute("""
        UPDATE concerts SET artist_name=%s, concert_name=%s, venue=%s,
        concert_date=%s, available_tickets=%s, price=%s WHERE id=%s
        """, (*data, cid))

        db.commit()
        load_data()
        messagebox.showinfo("Updated", "Success")

    # DELETE
    def delete():
        selected = tree.selection()
        if not selected:
            messagebox.showerror("Error", "Select row")
            return

        cid = tree.item(selected)["values"][0]

        cursor.execute("DELETE FROM concerts WHERE id=%s", (cid,))
        db.commit()
        load_data()
        messagebox.showinfo("Deleted", "Success")

    # BUTTONS
    btn_frame = tk.Frame(win, bg="#eef2ff")
    btn_frame.pack(pady=10)

    tk.Button(btn_frame, text="Add", bg="green", fg="white", width=10, command=add).grid(row=0, column=0, padx=5)
    tk.Button(btn_frame, text="Update", bg="blue", fg="white", width=10, command=update).grid(row=0, column=1, padx=5)
    tk.Button(btn_frame, text="Delete", bg="red", fg="white", width=10, command=delete).grid(row=0, column=2, padx=5)

# ---------------- USER PANEL ---------------- #
def open_user(email):
    win = tk.Toplevel(root)
    win.title("Book Tickets")
    win.geometry("650x500")
    win.configure(bg="#fdf2f8")

    tk.Label(win, text="Book Your Concert ", font=("Segoe UI", 18, "bold"), bg="#fdf2f8").pack(pady=10)

    cursor.execute("SELECT artist_name, venue, price, available_tickets FROM concerts")
    data = cursor.fetchall()

    columns = ("Artist", "Venue", "Price", "Tickets")
    tree = ttk.Treeview(win, columns=columns, show="headings", height=8)

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor="center", width=120)

    for d in data:
        tree.insert("", tk.END, values=(d[0], d[1], f"₹{d[2]}", d[3]))

    tree.pack(pady=10)

    qty = tk.Entry(win)
    qty.pack()
    add_placeholder(qty, "Enter tickets")

    def book():
        selected = tree.selection()
        if not selected or "Enter" in qty.get():
            messagebox.showerror("Error", "Select concert & enter qty")
            return

        artist = tree.item(selected)["values"][0]
        q = int(qty.get())

        cursor.execute("SELECT price, available_tickets FROM concerts WHERE artist_name=%s", (artist,))
        price, stock = cursor.fetchone()

        if q > stock:
            messagebox.showerror("Error", "Not enough tickets")
            return

        total = price * q

        cursor.execute("UPDATE concerts SET available_tickets=available_tickets-%s WHERE artist_name=%s", (q, artist))
        cursor.execute("INSERT INTO bookings (user_email, artist_name, tickets, total_paid) VALUES (%s,%s,%s,%s)",
                       (email, artist, q, total))
        db.commit()

        send_email(email, artist, q, total)

        messagebox.showinfo("Success", f"Booked ₹{total}")

    tk.Button(win, text="Book Now", bg="#e11d48", fg="white", command=book).pack(pady=20)

# ---------------- AUTH ---------------- #
def register():
    e = email.get()
    p = password.get()
    r = role.get()

    if "Enter" in e or "Enter" in p:
        messagebox.showerror("Error", "Enter valid data")
        return

    try:
        cursor.execute("INSERT INTO users VALUES(NULL,%s,%s,%s)", (e, p, r))
        db.commit()
        messagebox.showinfo("Success", "Registered")
    except:
        messagebox.showerror("Error", "User exists")

def login():
    cursor.execute("SELECT role FROM users WHERE email=%s AND password=%s",
                   (email.get(), password.get()))
    res = cursor.fetchone()

    if res:
        open_admin() if res[0] == "admin" else open_user(email.get())
    else:
        messagebox.showerror("Error", "Invalid login")

# ---------------- MAIN UI ---------------- #
root = tk.Tk()
root.title("ConcertPro 🎶")
root.geometry("420x500")
root.configure(bg="#e0f2fe")

tk.Label(root, text="ConcertPro", font=("Segoe UI", 26, "bold"), bg="#e0f2fe").pack(pady=20)

email = tk.Entry(root, width=30)
email.pack(pady=10)
add_placeholder(email, "Enter Email")

password = tk.Entry(root, width=30)
password.pack(pady=10)
add_placeholder(password, "Enter Password", True)

role = tk.StringVar(value="user")
tk.Radiobutton(root, text="User", variable=role, value="user", bg="#e0f2fe").pack()
tk.Radiobutton(root, text="Admin", variable=role, value="admin", bg="#e0f2fe").pack()

tk.Button(root, text="Login", bg="#2563eb", fg="white", width=20, command=login).pack(pady=10)
tk.Button(root, text="Register", width=20, command=register).pack()

root.mainloop()