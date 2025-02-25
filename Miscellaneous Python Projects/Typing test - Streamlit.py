import streamlit as st
import time

def calculate_accuracy(input_text, user_input):
  """
  Calculates the accuracy of the user's typing compared to the input text.
  """
  correct_chars = 0
  for i in range(min(len(input_text), len(user_input))):
    if input_text[i] == user_input[i]:
      correct_chars += 1
  return (correct_chars / len(input_text)) * 100

def calculate_wpm(time_taken, num_words):
  """
  Calculates Words Per Minute (WPM) based on time taken and number of words.
  """
  minutes = time_taken / 60
  if minutes == 0:
    return 0
  wpm = num_words / minutes
  return int(wpm)

def typing_test(category, custom_input=None):
  """
  Runs the typing test for the selected category or custom text.
  """
  if category == 'Custom' and custom_input is None:
    st.warning("Please enter custom text for the typing test.")
    return

  if category != 'Custom':
    input_text = ""
    if category == 'Short':
        input_text = "The quick brown fox jumps over the lazy dog."
    elif category == 'Medium':
        input_text = "Many people underestimate the importance of strong typing skills. In today's digital world, the ability to type quickly and accurately is essential for a variety of tasks, from communication to productivity.  Regular typing practice can significantly improve your speed and confidence. Aim for both speed and accuracy during this test."
    elif category == 'Long':
        input_text = "Once upon a time, in a land far, far away, lived a curious young cat named Mittens.  Mittens loved exploring his surroundings, chasing butterflies, and napping in sunbeams.  One sunny afternoon, while venturing into the garden, Mittens stumbled upon a strange, glowing portal hidden behind a rose bush.  Intrigued, he cautiously stepped through the portal, embarking on a journey that would change his life forever.  Test your typing endurance and precision in this longer passage."

  st.write("Type the following text:")
  st.write(input_text)
  st.write("-------------------------")

  user_input = st.text_input("Your turn:")

  if st.button("Start Test"):
    start_time = time.time()
    st.session_state["start_time"] = start_time

  if st.button("Stop Test"):
    end_time = time.time()
    time_taken = end_time - st.session_state["start_time"]
    del st.session_state["start_time"]  # Clear start time after test finishes

    accuracy = calculate_accuracy(input_text, user_input)
    num_words = len(user_input.split())
    wpm = calculate_wpm(time_taken, num_words)

    st.write("Test Finished!")
    st.success(f"Time taken: {time_taken:.2f} seconds")
    st.success(f"Accuracy: {accuracy:.2f}%")
    st.success(f"WPM: {wpm}")

if __name__ == "__main__":
  st.title("Typing Test")
  category = st.sidebar.selectbox(
      "Select a category:", ('Short', 'Medium', 'Long', 'Custom'))

  if category == 'Custom':
    custom_input = st.text_area("Enter custom text for typing test:")
    typing_test(category, custom_input)
  else:
    typing_test(category)
