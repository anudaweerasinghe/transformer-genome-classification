def truncate_line(file_path, line_number, max_length):
    """
    Truncates a specific line in a file to a specified maximum length.

    Args:
        file_path (str): The path to the file.
        line_number (int): The line number to truncate (starting from 1).
        max_length (int): The maximum length for the line.

    Returns:
        None
    """
    with open(file_path, "r") as file:
        lines = file.readlines()

    if line_number < 1 or line_number > len(lines):
        print(f"Invalid line number. The file has {len(lines)} lines.")
        return

    lines[line_number - 1] = lines[line_number - 1][:max_length] + "\n"

    with open(file_path, "w") as file:
        file.writelines(lines)

    print(f"Line {line_number} truncated to {max_length} characters.")


if __name__ == "__main__":
    file_path = "./train.fasta"
    max_length = 50
    while True:
        line_number = int(
            input("Enter the line number to truncate (starting from 1): ")
        )
        truncate_line(file_path, line_number, max_length)
