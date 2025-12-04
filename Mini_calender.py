import tkinter as tk
from tkinter import simpledialog, messagebox
import calendar, json, os
from datetime import datetime, date

STORE = 'events.json'
events = json.load(open(STORE)) if os.path.exists(STORE) else []

def save(): json.dump(events, open(STORE,'w'))

def iso(dt): return dt.strftime('%Y-%m-%d')

root = tk.Tk()
root.title("Mini Calendar")

current_year = date.today().year
current_month = date.today().month

header = tk.Frame(root); header.pack(pady=6)
label = tk.Label(header, text="")
label.pack(side=tk.LEFT, padx=8)

def render():
    label.config(text=f"{calendar.month_name[current_month]} {current_year}")
    for w in grid.winfo_children(): w.destroy()
    # Weekday headers
    for i,wd in enumerate(['Sun','Mon','Tue','Wed','Thu','Fri','Sat']):
        tk.Label(grid, text=wd, fg="#64748b").grid(row=0, column=i, padx=3, pady=3)

    month_cal = calendar.monthcalendar(current_year, current_month)
    for r,row in enumerate(month_cal, start=1):
        for c,day in enumerate(row):
            txt = " " if day == 0 else str(day)
            btn = tk.Button(grid, text=txt, width=6)
            btn.grid(row=r, column=c, padx=3, pady=3)
            if day != 0:
                diso = f"{current_year}-{current_month:02d}-{day:02d}"
                btn.config(command=lambda d=diso: select_date(d))

def select_date(d):
    evs = [e for e in events if e['date']==d]
    msg = f"Events for {d}:\n" + "\n".join([f"- {e['title']}" for e in evs]) if evs else "No events yet."
    if messagebox.askyesno("Selected", msg + "\n\nAdd new?"):
        title = simpledialog.askstring("Title", "Event title:")
        if title:
            events.append({'id': str(len(events)+1), 'date': d, 'title': title, 'notes': ''})
            save()
            render()

grid = tk.Frame(root); grid.pack(padx=8, pady=8)

def prev(): 
    global current_month, current_year
    if current_month == 1: current_month, current_year = 12, current_year-1
    else: current_month -= 1
    render()

def next():
    global current_month, current_year
    if current_month == 12: current_month, current_year = 1, current_year+1
    else: current_month += 1
    render()

tk.Button(header, text="Prev", command=prev).pack(side=tk.LEFT)
tk.Button(header, text="Next", command=next).pack(side=tk.LEFT)

render()
root.mainloop()
