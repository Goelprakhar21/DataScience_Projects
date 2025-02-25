import streamlit as st
import time

def countdown(duration):
    """Counts down from the given duration (in minutes) and returns the remaining time.

    Args:
        duration (float): The total duration of the countdown in minutes.

    Returns:
        str: Remaining time in a user-friendly format.
    """
    # Convert duration to seconds for time.sleep()
    total_seconds = duration * 60

    while total_seconds > 0:
        # Calculate remaining minutes and seconds
        minutes, seconds = divmod(int(total_seconds), 60)

        # Format the remaining time for clear display
        time_remaining = f"{minutes:02d}:{seconds:02d}"

        yield time_remaining

        # Pause for 1 second
        time.sleep(1)

        # Decrement total seconds
        total_seconds -= 1

    # Return completion message when time is up
    yield "TIME IS UP! Your dish is ready."

def main():
    st.title("Cooking Countdown Timer")

    duration = st.number_input("Enter the cooking duration in minutes:", min_value=0.0001, step=0.1, format="%0.1f")

    if st.button("Start Countdown"):
        st.write("### Cooking time remaining:")
        with st.empty():  # Placeholder for dynamic updating
            for time_remaining in countdown(duration):
                st.write(f"## {time_remaining}")
                time.sleep(1)

        st.success("🎉 Your dish is ready! Enjoy! 🍽️")

if __name__ == "__main__":
    main()
