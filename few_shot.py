import pandas as pd
import json

class FewShotPosts:
    def __init__(self, file_path="data/processed_posts.json"):
        self.df = None
        self.unique_tags = []
        self.load_posts(file_path)

    def load_posts(self, file_path):
        with open(file_path, encoding="utf-8") as f:
            posts = json.load(f)
            print(f"✅ Loaded {len(posts)} posts from JSON")
            self.df = pd.json_normalize(posts)

            # Categorize length
            self.df['length'] = self.df['line_count'].apply(self.categorize_length)

            # Ensure 'tags' is a list
            self.df['tags'] = self.df['tags'].apply(lambda x: x if isinstance(x, list) else [])

            # Collect unique tags
            all_tags = []
            for tags in self.df['tags']:
                all_tags.extend(tags)
            self.unique_tags = sorted(list(set(all_tags)))  # Sorted for neat dropdown
            print(f"🏷️ Found {len(self.unique_tags)} unique tags")
    def get_filtered_posts(self, length, language, tag):
        df_filtered = self.df[
            (self.df['tags'].apply(lambda tags: tag in tags)) &
            (self.df['language'] == language) &
            (self.df['length'] == length)
        ]
        return df_filtered.to_dict(orient='records')

    def categorize_length(self, line_count):
        if line_count < 5:
            return "Short"
        elif 5 <= line_count <= 10:
            return "Medium"
        else:
            return "Long"

    def get_tags(self):
        return self.unique_tags


# Debug/test run
if __name__ == "__main__":
    fs = FewShotPosts()
    print("Tags:", fs.get_tags())
    posts = fs.get_filtered_posts("Medium", "Hinglish", "Job Search")
    print("Filtered Posts:", posts)
