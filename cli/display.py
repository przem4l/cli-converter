from tqdm import tqdm


def progress_bar(items, desc="Processing..."):
    return tqdm(
        items, desc=desc, bar_format="{desc}: {percentage:3.0f}%|{bar}| {n}/{total}"
    )


def show_conversion_stats(handler):
    in_size = handler.get_size(handler.input_path)
    out_size = handler.get_size(handler.output_path)
    
    in_mb = handler.convert_to_megabytes(in_size)
    out_mb = handler.convert_to_megabytes(out_size)
    
    savings = handler.get_savings_percent(in_size, out_size)
    
    print("\nConversion process successfully completed!")
    
    if savings > 0:
        savings_txt = f"\033[92m(Saved {savings}%)\033[0m"
    elif savings < 0:
        savings_txt = f"\033[91m(Increased by {abs(savings)}%)\033[0m"
    else:
        savings_txt = "(File size remained the same)"

    print(f"   Size: {in_mb} MB -> {out_mb} MB {savings_txt}\n")
