import sys
import os

# Define the path to store responses
file_path = "./helpers/response.txt"

def main():
    round_no = int(sys.argv[1])
    prev_opponent_response = sys.argv[2]

    # Ensure the helpers directory exists
    if not os.path.exists('./helpers'):
        os.makedirs('./helpers')
    
    # Initialize the response history if the file does not exist or is empty
    if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
        with open(file_path, 'w') as f:
            # Initial responses with a buffer of YES for history
            f.write("NONE\nYES\n" + "YES\n" * 10 + "YES\n" * 10)

    # Read the file to get the last opponent's and our responses
    with open(file_path, 'r') as f:
        lines = f.readlines()
        past_opponent_response = lines[0].strip() if lines else "NONE"
        my_last_response = lines[1].strip() if len(lines) > 1 else "YES"
        opponent_history = [line.strip() for line in lines[2:12]] if len(lines) > 2 else ["YES"] * 10
        my_history = [line.strip() for line in lines[12:22]] if len(lines) > 12 else ["YES"] * 10

    # Update the history
    if prev_opponent_response != "NONE":
        opponent_history.pop(0)
        opponent_history.append(prev_opponent_response)
    if round_no != 1:
        my_history.pop(0)
        my_history.append(my_last_response)

    # Decision based on the last 10 rounds of the opponent's responses
    if round_no == 1 or prev_opponent_response == "NONE":
        my_response = "YES"
    elif all(response == "YES" for response in opponent_history):
        my_response = "NO"  # Be sneaky if all last 10 responses were "YES"
    elif len(set(opponent_history)) == 2 and opponent_history[0] != opponent_history[1]:
        my_response = "YES"  # Be nice if the opponent alternates between "YES" and "NO"
    else:
        my_response = "YES" if prev_opponent_response == "YES" or past_opponent_response == "YES" else "NO"

    # Write the current round's responses and the updated history to the file
    with open(file_path, 'w') as f:
        f.write(f"{prev_opponent_response}\n{my_response}\n" + "\n".join(opponent_history) + "\n" + "\n".join(my_history) + "\n")
    
    # Output the current response
    print(my_response)

if __name__ == "__main__":
    main()
