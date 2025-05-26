import json
import os

def files_in_directory(directory):
    """List all files in a directory."""
    import os
    return [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

def load_json_file(file_path):
    """Load JSON data from a file."""
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)
    
def save_json_file(data, file_path):
    """Save JSON data to a file."""
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def divide_comments_by_tab(comments, tab):
    """Divide comments into tabs based on the specified tab."""
    divided_comments = []
    for comment in comments:
        if comment.get('tab') == tab:
            divided_comments.append(comment)
    return divided_comments

if __name__ == "__main__":
    # Load comments from a JSON file
    file_dir = "comments_with_replies"
    files = files_in_directory(file_dir)
    for file in files:
        print(f"Processing file: {file}")
        all_comments = []
        filename = file.split(".json")[0]
        file_path = os.path.join(file_dir, file)
        comments = load_json_file(file_path)
        all_comments.extend(comments)

        # Divide comments by tab
        tabs = ["information", "opinion", "question"]
        divided_comments = {}
        for tab in tabs:
            divided_comments[tab] = divide_comments_by_tab(all_comments, tab)

        # Save divided comments to separate JSON files
        output_dir = f"tab_divided_comments/{filename}"
        os.makedirs(output_dir, exist_ok=True)
        for tab, comments in divided_comments.items():
            output_file = os.path.join(output_dir, f"{tab}.json")
            save_json_file(comments, output_file)
            print(f"Saved {len(comments)} comments to {output_file}")

        print("Comments divided by tab and saved successfully.")
