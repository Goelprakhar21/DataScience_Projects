import streamlit as st

def temperature_converter(from_unit: str, to_unit: str, value: float) -> float:
    """
    Converts temperature from one unit to another using specific formulas.

    Args:
        from_unit (str): Unit from which the user is converting (C, F, or K).
        to_unit (str): Unit to which the user wants to convert (C, F, or K).
        value (float): Value of the temperature in the from_unit.

    Returns:
        float: Converted temperature value in the to_unit.

    Raises:
        ValueError: If invalid units are entered.
    """

    if from_unit == to_unit:
        return value  # No conversion needed if units are the same

    # Conversion factors
    celsius_to_fahrenheit = 9 / 5
    fahrenheit_to_celsius = 5 / 9
    kelvin_offset = 273.15

    # Convert to Celsius first (common base for most conversions)
    if from_unit == 'F':
        value = (value - 32) * fahrenheit_to_celsius
    elif from_unit == 'K':
        value -= kelvin_offset
    elif from_unit not in ['C', 'F', 'K']:
        raise ValueError("Invalid from_unit entered. Please use C, F, or K.")

    # Convert from Celsius to desired unit
    if to_unit == 'F':
        value = value * celsius_to_fahrenheit + 32
    elif to_unit == 'K':
        value += kelvin_offset
    elif to_unit not in ['C', 'F', 'K']:
        raise ValueError("Invalid to_unit entered. Please use C, F, or K.")

    return value

def main():
    st.title("Temperature Converter")

    unit1 = st.selectbox("Select unit 1:", ['C', 'F', 'K'])
    unit2 = st.selectbox("Select unit 2:", ['C', 'F', 'K'])

    temperature = st.number_input("Enter temperature value:")

    if st.button("Convert"):
        try:
            converted_temp = temperature_converter(unit1, unit2, temperature)
            st.success(f"{temperature}{unit1} is equal to {converted_temp:.2f}{unit2}")
        except ValueError as e:
            st.error(e)

if __name__ == "__main__":
    main()
