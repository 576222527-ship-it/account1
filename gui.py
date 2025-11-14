

#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime
import db                      # 复用之前的 db.py

# ---------- 业务 ----------
def refresh_tree():
    """刷新表格"""
    for item in tree.get_children():
        tree.delete(item)
    for r in db.list_records():
        tree.insert('', 'end', values=(r['id'], f"{r['amount']:+.2f}", r['note'], r['date']))

def add_record_gui():
    try:
        amount = float(amount_var.get())
        note = note_var.get().strip()
        if not note:
            raise ValueError('备注不能为空')
        db.add_record(amount, note)
        refresh_tree()
        amount_var.set(''); note_var.set('')
        messagebox.showinfo('成功', '已添加记录')
    except ValueError as e:
        messagebox.showerror('错误', str(e))

def del_record_gui():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning('提示', '请先选择要删除的行')
        return
    rid = tree.item(selected[0])['values'][0]  # 第一列是 id
    db.delete_record(rid)
    refresh_tree()
    messagebox.showinfo('成功', '已删除')

def pie_chart():
    """饼图：收入/支出占比"""
    rows = db.list_records()
    income = sum(r['amount'] for r in rows if r['amount'] > 0)
    expense = sum(r['amount'] for r in rows if r['amount'] < 0)
    if income == 0 and expense == 0:
        messagebox.showwarning('提示', '暂无数据')
        return
    labels = ['收入', '支出']; sizes = [income, -expense]; colors = ['#4CAF50', '#F44336']
    plt.clf()
    plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
    plt.title('收支占比')
    plt.show()

# ---------- GUI 搭建 ----------
root = tk.Tk()
root.title('记账本')
root.geometry('600x400')

amount_var, note_var = tk.StringVar(), tk.StringVar()

# 顶部输入区
frm_input = ttk.Frame(root); frm_input.pack(pady=10)
ttk.Label(frm_input, text='金额').grid(row=0, column=0, padx=5)
ttk.Entry(frm_input, textvariable=amount_var, width=10).grid(row=0, column=1, padx=5)
ttk.Label(frm_input, text='备注').grid(row=0, column=2, padx=5)
ttk.Entry(frm_input, textvariable=note_var, width=20).grid(row=0, column=3, padx=5)
ttk.Button(frm_input, text='添加', command=add_record_gui).grid(row=0, column=4, padx=10)
ttk.Button(frm_input, text='删除', command=del_record_gui).grid(row=0, column=5, padx=5)

# 中部表格
cols = ('ID', '金额', '备注', '日期')
tree = ttk.Treeview(root, columns=cols, show='headings', height=12)
for c in cols:
    tree.heading(c, text=c)
    tree.column(c, width=100 if c != '备注' else 200)
tree.pack(fill='both', expand=True, padx=10, pady=10)

# 底部按钮
frm_btn = ttk.Frame(root); frm_btn.pack(pady=10)
ttk.Button(frm_btn, text='统计饼图', command=pie_chart).pack(side='left', padx=5)
ttk.Button(frm_btn, text='退出', command=root.quit).pack(side='left', padx=5)

refresh_tree()          # 启动即刷新
#root.mainloop()
import tray
tray.create_tray(root)   # 先隐藏到托盘
root.mainloop()