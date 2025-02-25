import streamlit as st

def calculate_payback_period(initial_investment, cashflows_list):
    """
    Calculates the payback period for a project based on initial investment and cashflows.

    Args:
        initial_investment (float): The initial investment amount.
        cashflows_list (list): A list of cashflows for each period.

    Returns:
        float: The payback period in years, or None if not found.
    """

    # Calculate cumulative cashflows
    cumulative_cashflows = [0]
    for cashflow in cashflows_list:
        cumulative_cashflows.append(cumulative_cashflows[-1] + cashflow)

    # Find the payback period (year where cumulative cashflow becomes positive or zero)
    payback_period = None
    for i, cashflow in enumerate(cumulative_cashflows):
        if cashflow >= initial_investment:
            payback_period = i + 1  # Account for 0-based indexing
            # Check if there's unrecovered cost in the current period
            if cashflow > initial_investment:
                unrecovered_cost = initial_investment - cumulative_cashflows[i-1]
                # Calculate remaining payback period as a fraction of the year
                remaining_period = unrecovered_cost / (cashflow - cumulative_cashflows[i-1])
                payback_period += remaining_period
            break

    return payback_period

st.header('PAYBACK PERIOD CALCULATOR')

# Text input for initial investment
initial_investment = st.text_input("Initial Investment:", "")

# Text input for cashflows (separated by commas)
cashflows = st.text_input("Cashflows (separated by commas):", "")

# Button to calculate payback period
if st.button("Calculate Payback Period"):
    # Convert cashflows to a list of floats (handle empty input)
    try:
        cashflows_list = list(map(float, cashflows.split(",")))
    except ValueError:
        st.write("Please enter cashflows separated by commas (e.g., -10000, 1500, 2000).")
    else:
        # Check if initial investment is not empty before conversion
        if not initial_investment:
            st.write("Please enter a valid initial investment.")
        else:
            # Calculate payback period using the defined function
            payback_period = calculate_payback_period(float(initial_investment), cashflows_list)

            # Display payback period
            if payback_period is not None:
                st.write("Payback Period:", f"{payback_period:.2f} years")
            else:
                st.write("Project cashflows might not have a payback period within the provided data.")