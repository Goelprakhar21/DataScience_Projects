import streamlit as st
from collections import defaultdict
from datetime import datetime

def create_expense_entry(category: str, amount: float, date: str) -> dict:
  '''Create an expense entry with a category, amount, and date.'''
  return {'category': category, 'amount': amount, 'date': date}

def add_expense(expenses: defaultdict, category: str, amount: float, date: str) -> None:
  '''Add an expense to the expenses dictionary.'''
  expenses[date].append(create_expense_entry(category, amount, date))

def get_total_expenses(expenses: defaultdict, start_date: str = None, end_date: str = None) -> float:
  '''Calculate the total expenses for a specific date or all dates.'''
  total_expense = 0
  for date, daily_expenses in expenses.items():
    if (start_date is None or date >= start_date) and (end_date is None or date <= end_date):
      for expense in daily_expenses:
        total_expense += expense['amount']
  return total_expense

def set_budget(budget: float) -> None:
  '''Set the budget for the expense tracker.'''
  global total_budget
  total_budget = budget

def get_remaining_budget() -> float:
  '''Calculate the remaining budget based on total expenses.'''
  return total_budget - get_total_expenses(st.session_state['expenses'])

# Initialize expenses dictionary
expenses = defaultdict(list)

# Streamlit UI
st.title("Expense Tracker")

# Load or initialize expenses from session state
if 'expenses' not in st.session_state:
  st.session_state.expenses = expenses

# Set the budget
st.subheader("Set Budget")
budget_amount_str = st.text_input("Enter Budget Amount:")

# Validate and convert budget input to float before setting
try:
  budget_amount = float(budget_amount_str)
  set_budget(budget_amount)
except ValueError:
  st.error("Please enter a valid number for budget.")

# Add new expense
st.subheader("Add New Expense")
new_category_key = 'new_category'
new_amount_key = 'new_amount'
new_date_key = 'new_date'

new_category = st.text_input("Category:", key=new_category_key)
new_amount = st.number_input("Amount:", min_value=0.01, format="%.2f", key=new_amount_key)
new_date = st.date_input("Date:", datetime.now(), key=new_date_key)

add_expense_button = st.button("Add Expense")
if add_expense_button:
  add_expense(st.session_state['expenses'], new_category, new_amount, str(new_date))
  st.session_state.expenses = st.session_state['expenses']  # Save expenses in session state
  st.success("Expense added successfully!")

# Display expenses in a table
st.subheader("Expense Table")
table_data = {'Date': [], 'Category': [], 'Amount': []}
for date, daily_expenses in st.session_state['expenses'].items():
  for expense in daily_expenses:
    table_data['Date'].append(expense['date'])
    table_data['Category'].append(expense['category'])
    table_data['Amount'].append(expense['amount'])

st.table(table_data)

# Show remaining budget
st.subheader("Remaining Budget")
remaining_budget = get_remaining_budget()
st.write(f"${remaining_budget:.2f}")

# Show total expenses
st.subheader("Total Expenses")
total_expenses = get_total_expenses(st.session_state['expenses'])
st.write(f"${total_expenses:.2f}")
