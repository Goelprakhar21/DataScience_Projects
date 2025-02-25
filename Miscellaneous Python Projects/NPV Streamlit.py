import numpy_financial as npf
import streamlit as st

st.header('NET PRESENT VALUE CALCULATOR')
# Text input for discount rate (as percentage)
discount_rate_as_percentage = st.text_input("Discount Rate (%):", "")

# Convert discount rate to decimal (handle empty input)
if discount_rate_as_percentage:
  discount_rate = float(discount_rate_as_percentage) / 100
else:
  discount_rate = None  # Or any default value

# Text input for cashflows
cashflows = st.text_input("Cashflows (separated by commas):", "")

# Text input for initial investment
initial_investment = st.text_input("Initial Investment:", "")

# Button to calculate NPV
if st.button("Calculate NPV"):
  # Convert cashflows to a list
  cashflows_list = list(map(float, cashflows.split(',')))

  # Check if initial investment is not empty before conversion
  if initial_investment:
    # Add initial investment to the list (as negative value)
    cashflows_list.insert(0, -float(initial_investment))
  else:
    # Handle empty initial investment (optional)
    st.write("Please enter a valid initial investment.")

  # Check if discount rate is valid before calculation
  if discount_rate is not None:
    # Calculate NPV
    npv = npf.npv(discount_rate, cashflows_list)

    # Display NPV
    st.write("Net Present Value: ", npv)
  else:
    st.write("Please enter a valid discount rate.")
