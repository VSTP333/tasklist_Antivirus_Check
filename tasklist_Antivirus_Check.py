import subprocess

def read_dict_from_file(file_path):
    dictionary = {}
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if line:
                    try:
                        key, value = line.split(':', 1)  # 仅分割一次
                        key = key.strip().strip('"')
                        dictionary[key] = value.strip().strip('"')
                    except ValueError:
                        print(f"Warning: Skipping invalid line in dict file: {line}")
    except FileNotFoundError:
        print(f"Error: File not found - {file_path}")
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
    return dictionary

def read_list_from_file(file_path):
    first_column = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if line:
                    first_column.append(line.split()[0])
    except FileNotFoundError:
        print(f"Error: File not found - {file_path}")
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
    return first_column

def check_existence(list1, dict2):
    result = [(item, dict2[item]) for item in list1 if item in dict2]
    return result

def get_tasklist_first_column():
    try:
        result = subprocess.run(['tasklist'], capture_output=True, text=True, check=True)
        lines = result.stdout.splitlines()
        first_column = [line.split()[0] for line in lines[3:] if line]  # 跳过前两行标题
        return first_column
    except subprocess.CalledProcessError as e:
        print(f"Error running tasklist command: {e}")
        return []
    except Exception as e:
        print(f"Error: {e}")
        return []

def compare_files(file1_path, file2_path):
    list1 = read_list_from_file(file1_path)
    dict2 = read_dict_from_file(file2_path)
    result = check_existence(list1, dict2)
    if result:
        print("\033[31m存在10000个杀毒软件:\033[0m")
        for item, value in result:
            print(f"\033[31m{item}: {value}:\033[0m")
    else:
        print("存在-10000个杀毒软件")

def compare_tasklist(file2_path):
    tasklist_first_column = get_tasklist_first_column()
    dict2 = read_dict_from_file(file2_path)
    result = check_existence(tasklist_first_column, dict2)
    if result:
        print("\033[31m存在10000个杀毒软件:\033[0m")
        for item, value in result:
            print(f"\033[31m{item}: {value}:\033[0m")
    else:
        print("存在-10000个杀毒软件")

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Compare tasklist data with a dictionary.")
    parser.add_argument('--file', type=str, help="Path to the file to compare")
    parser.add_argument('--tasklist', action='store_true', help="Compare tasklist command output with dictionary")
    parser.add_argument('--dict', type=str, required=True, help="Path to the dictionary file")

    args = parser.parse_args()

    if args.file:
        compare_files(args.file, args.dict)
    elif args.tasklist:
        compare_tasklist(args.dict)
    else:
        print("Please provide either --file or --tasklist option.")

if __name__ == "__main__":
    main()
