#!/usr/bin/env python3
from typing import List
from db import add_record, list_records, month_stats, delete_record


# ---------- 业务 ----------
def input_amount() -> float:
    while True:
        try:
            return float(input('请输入金额（正数为收入，负数为支出）：'))
        except ValueError:
            print('⚠️  请输入合法的数字！')


def add_rec() -> None:
    amount = input_amount()
    note = input('请输入备注：').strip()
    add_record(amount, note)
    print('✅ 添加成功！')


def view_recs() -> None:
    rows = list_records()
    if not rows:
        print('暂无记录')
        return
    for r in rows:
        print(f"{r['id']}. 金额：{r['amount']:+.2f}  备注：{r['note']}  日期：{r['date']}")
    print(f'\n共 {len(rows)} 条记录')


def statistics() -> None:
    rows = list_records()
    income = sum(r['amount'] for r in rows if r['amount'] > 0)
    expense = sum(r['amount'] for r in rows if r['amount'] < 0)
    print(f'总收入：{income:.2f}')
    print(f'总支出：{-expense:.2f}')
    print(f'余额：{income + expense:.2f}')


def month_total() -> None:
    month = input('请输入月份（格式 2025-11）：').strip()
    stat = month_stats(month)
    print(f'{month} 汇总：{stat["total"]:+.2f}')
    for r in stat['detail']:
        print(f'  {r["date"]}  {r["amount"]:+.2f}  {r["note"]}')


def del_rec() -> None:
    view_recs()
    rid = input('请输入要删除的编号（id）：').strip()
    if rid.isdigit() and delete_record(int(rid)):
        print('✅ 删除成功！')
    else:
        print('⚠️  删除失败，请检查编号。')


# ---------- 主循环 ----------
def main() -> None:
    menu = (
        '\n=== 记账本 ===\n'
        '1. 添加记录\n'
        '2. 查看记录\n'
        '3. 统计收支\n'
        '4. 按月份汇总\n'
        '5. 删除记录\n'
        '6. 退出\n'
        '请选择操作：'
    )
    while True:
        choice = input(menu).strip()
        match choice:
            case '1': add_rec()
            case '2': view_recs()
            case '3': statistics()
            case '4': month_total()
            case '5': del_rec()
            case '6':
                print('再见！')
                break
            case _:
                print('⚠️  请输入 1-6 之间的数字！')


if __name__ == '__main__':
    main()