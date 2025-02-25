import pandas as pd
import streamlit as st

def calculate_arr(investment_periods, annual_returns):
  # Convert investment periods to integer (handle empty input)
  try:
    num_periods = int(investment_periods)
  except ValueError:
    st.write("Please enter a valid number of investment periods.")
    return None  # Or any specific error message

  # Convert annual returns to a list of floats (handle empty input)
  try:
    returns_list = list(map(float, annual_returns.split(",")))
  except ValueError:
    st.write("Please enter annual returns separated by commas (e.g., 10, 5, -2).")
    return None  
  
  # Check if number of returns matches investment periods
  if len(returns_list) != num_periods:
    st.write("Number of annual returns should match the number of investment periods.")
    return None  

  # Calculate total return (as a decimal)
  total_return = sum(returns_list) / 100

  # Calculate ARR (geometric mean)
  arr = (1 + total_return)**(1/num_periods) - 1

  # Display ARR as a percentage
  st.write("Average Rate of Return (ARR):", f"{arr * 100:.2f}%")

  return arr  # Return the calculated ARR

st.header('AVERAGE RATE OF RETURN CALCULATOR')

# Text input for investment periods
investment_periods = st.text_input("Number of Investment Periods:", "")

# Text input for annual returns (separated by commas)
annual_returns = st.text_input("Annual Returns (%):", "")

# Button to calculate ARR
if st.button("Calculate ARR"):
  # Call the calculate_arr function and handle the returned value
  arr = calculate_arr(investment_periods, annual_returns)
  if arr is not None:
    st.write("ARR is Calculated Using Geometric Mean")
