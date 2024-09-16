import streamlit as st
import pandas as pd
import pickle
import matplotlib.pyplot as plt

st.title("簡易記帳 APP")

# 嘗試從檔案載入交易紀錄
try:
    with open('transaction.pkl', 'rb') as f:
        transactions = pickle.load(f)
except FileNotFoundError:
    transactions = pd.DataFrame(columns=['日期', '項目', '金額'])

# 輸入交易資訊
date = st.date_input("日期")
item = st.text_input("項目")
amount = st.number_input("金額")

# 添加交易到 DataFrame
if st.button("添加交易"):
    # Create a new DataFrame for the new transaction
    new_transaction = pd.DataFrame({'日期': [date], '項目': [item], '金額': [amount]})
    # Concatenate the DataFrames
    transactions = pd.concat([transactions, new_transaction], ignore_index=True)

    # 保存交易紀錄到檔案
    with open('transaction.pkl', 'wb') as f:
        pickle.dump(transactions, f)

# 顯示交易紀錄
st.subheader("交易紀錄")
st.dataframe(transactions)

# 計算帳戶餘額
balance = sum(transactions['金額'])
# 顯示帳戶餘額
st.subheader("帳戶餘額")
st.write(balance)

# 顯示收入和支出
st.subheader("收入與支出")
st.write(f"總收入: {transactions[transactions['金額'] > 0]['金額'].sum()}")
st.write(f"總支出: {transactions[transactions['金額'] < 0]['金額'].sum()}")


# Create a new column to indicate income or expense
transactions['類型'] = ['收入' if amount > 0 else '支出' for amount in transactions['金額']]
