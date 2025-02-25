import numpy_financial as npf
import streamlit as st

def calculate_irr(cashflows, initial_investment):
  # Convert cashflows to a list of floats (handle empty input)
  try:
    cashflows_list = list(map(float, cashflows.split(",")))
  except ValueError:
    st.write("Please enter cashflows separated by commas (e.g., 1500, 2000).")
    return None  # Or any specific error message

  # Check if cashflows is empty
  if not cashflows:
      st.write("Please enter cashflows.")
      return None

  # Add initial investment as the first element (negative value)
  cashflows_list.insert(0, -float(initial_investment))

  # Calculate IRR
  try:
    irr = npf.irr(cashflows_list)
  except ValueError:
    st.write("Could not calculate IRR. Cashflows might not have a valid solution.")
    return None

  # Display IRR as a percentage
  st.write("Internal Rate of Return (IRR):", f"{irr * 100:.2f}%")

  return irr

st.header('INTERNAL RATE OF RETURN CALCULATOR')

# Text input for cashflows (separated by commas)
cashflows = st.text_input("Cashflows (excluding initial investment, separated by commas):", "")

# Text input for initial investment
initial_investment = st.text_input("Initial Investment:", "")

# Button to calculate IRR
if st.button("Calculate IRR"):
  # Call the calculate_irr function and handle the returned value
  irr = calculate_irr(cashflows, initial_investment)
