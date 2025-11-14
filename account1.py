# #!/usr/bin/env python3
# account.py



import json
import os
from typing import List, Dict,Any

FILE = 'account.json'
Record = Dict[str, Any]          # 类型别名，方便阅读


# ---------- IO 数据存取----------
def load_records() -> List[Record]:
    """加载 JSON 数据；文件不存在或损坏时返回空列表"""
    if not os.path.exists(FILE):
        return []
    try:
        with open(FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        # 简单校验：每条记录必须有 amount(float) 和 note(str)
        for r in data:
            if not isinstance(r.get('amount'), (int, float)) or not isinstance(r.get('note'), str):
                raise ValueError('格式错误')
        return data
    except (json.JSONDecodeError, ValueError):
        print('⚠️  数据文件损坏，已自动重置！')
        return []


def save_records(records: List[Record]) -> None:
    """保存列表到 JSON"""
    with open(FILE, 'w', encoding='utf-8') as f:
        json.dump(records, f, ensure_ascii=False, indent=2)


# ---------- 业务 ----------
def input_amount() -> float:
    """循环直到用户输入合法数字"""
    while True:
        try:
            return float(input('请输入金额（正数为收入，负数为支出）：'))
        except ValueError:
            print('⚠️  请输入合法的数字！')


def add_record(records: List[Record]) -> None:
    """添加一条记录"""
    amount = input_amount()
    note = input('请输入备注：').strip()
    records.append({'amount': amount, 'note': note})
    print('✅ 添加成功！')


def view_records(records: List[Record]) -> None:
    """打印所有记录"""
    if not records:
        print('暂无记录')
        return
    for i, r in enumerate(records, 1):
        print(f'{i}. 金额：{r["amount"]:+.2f}  备注：{r["note"]}')
        print(f"共 {len(records)} 条记录")


def statistics(records: List[Record]) -> None:
    """统计收支"""
    total_income = sum(r['amount'] for r in records if r['amount'] > 0)
    total_expense = sum(r['amount'] for r in records if r['amount'] < 0)
    balance = total_income + total_expense
    print(f'总收入：{total_income:.2f}')
    print(f'总支出：{total_expense:.2f}')
    print(f'余额：{balance:.2f}')


# ---------- 主循环 ----------
def main() -> None:
    records = load_records()
    menu = (
        '=== 记账本 ===\n'
        '1. 添加记录\n'
        '2. 查看记录\n'
        '3. 统计收支\n'
        '4. 退出\n'
        '请选择操作：'
    )
    while True:
        choice = input(menu).strip()
        if choice == '1':
            add_record(records)
        elif choice == '2':
            view_records(records)
        elif choice == '3':
            statistics(records)
        elif choice == '4':
            save_records(records)
            print('数据已保存，再见！')
            break
        else:
            print('⚠️  请输入 1-4 之间的数字！')
            input("\n按 Enter 返回主菜单...")


if __name__ == '__main__':
    main()
    #让脚本既可以作为独立程序直接运行（执行 main() 启动功能），
    # 又可以作为模块被其他文件导入（此时不自动执行主程序，只提供函数 / 类供复用）

