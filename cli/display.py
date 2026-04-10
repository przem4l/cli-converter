from tqdm import tqdm


def progress_bar(items, desc="Processing..."):
    return tqdm(items, desc=desc)
