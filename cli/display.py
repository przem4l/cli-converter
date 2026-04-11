from tqdm import tqdm

def progress_bar(items, desc="Processing..."):
    return tqdm(items, desc=desc, bar_format="{desc}: {percentage:3.0f}%|{bar}| {n}/{total}")
