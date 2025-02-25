import streamlit as st

def calculate_present_value(cashflow, discount_rate, period):
    """
    Calculates the present value of a cashflow at a given discount rate and period.

    Args:
        cashflow (float): The cashflow amount for a specific period.
        discount_rate (float): The discount rate to use for present value calculation.
        period (int): The period number (starting from 1).

    Returns:
        float: The present value of the cashflow.
    """
    return cashflow / (1 + discount_rate) ** period

def calculate_profitability_index(initial_investment, cashflows, discount_rate):
    """
    Calculates the Profitability Index (PI) of a project based on initial investment,
    cashflows, and discount rate.

    Args:
        initial_investment (float): The initial investment amount.
        cashflows (list): A list of cashflows for each period.
        discount_rate (float): The discount rate to use for present value calculation.

    Returns:
        float: The Profitability Index of the project.
    """

    present_values = []
    for i, cashflow in enumerate(cashflows):
        present_values.append(calculate_present_value(cashflow, discount_rate, i + 1))

    present_value_of_cashflows = sum(present_values)
    profitability_index = present_value_of_cashflows / initial_investment

    return profitability_index

def display_profitability_index(profitability_index, st):
    """
    Displays the profitability index and its interpretation.

    Args:
        profitability_index (float): The calculated Profitability Index.
        st (streamlit.st): The Streamlit instance to use for displaying the results.
    """
    st.write("Profitability Index:", profitability_index)
    if profitability_index > 1:
        st.write("Interpretation: The project is considered profitable as the PI is greater than 1.")
    elif profitability_index == 1:
        st.write("Interpretation: The project breaks even (PI equals 1).")
    else:
        st.write("Interpretation: The project is considered unprofitable as the PI is less than 1.")

st.header('PROFITABILITY INDEX CALCULATOR')

# Text input for initial investment
initial_investment = st.text_input("Initial Investment:", "")

# Text input for cashflows (separated by commas)
cashflows = st.text_input("Cashflows (separated by commas):", "")

# Text input for discount rate
discount_rate = st.text_input("Discount Rate (%):", "")

# Button to calculate profitability index
if st.button("Calculate Profitability Index"):
    # Convert cashflows to a list of floats (handle empty input)
    try:
        cashflows_list = list(map(float, cashflows.split(",")))

        # Check if initial investment and discount rate are valid numbers
        initial_investment = float(initial_investment)
        discount_rate = float(discount_rate) / 100  # Convert discount rate from percentage to decimal

        # Calculate profitability index using the defined function
        profitability_index = calculate_profitability_index(initial_investment, cashflows_list, discount_rate)

        # Display profitability index and interpretation (call the function)
        display_profitability_index(profitability_index, st)

    except ValueError:
        st.write("Please enter valid numbers for initial investment, cashflows, and discount rate.")
