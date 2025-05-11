#!/usr/bin/env python3
import argparse
import matplotlib
matplotlib.use("Agg")  # Use non-interactive backend suitable for servers
import matplotlib.pyplot as plt
import os

def parse_args():
    parser = argparse.ArgumentParser(description="Plot a histogram of ORF lengths from a GLIMMER prediction file.")
    parser.add_argument("--input", "-i", required=True, help="Path to the .glimmer.predict file")
    parser.add_argument("--output", "-o", help="Optional output PNG file name. Defaults to <input_basename>_hist.png")
    return parser.parse_args()

def main():
    args = parse_args()
    input_file = args.input

    # Define output filename
    if args.output:
        output_file = args.output
    else:
        base_name = os.path.splitext(os.path.basename(input_file))[0]
        output_file = f"ORFlength_{base_name}_hist.png"

    orf_lengths = []

    # Read GLIMMER predictions and calculate ORF lengths
    with open(input_file, "r") as fil:
        next(fil)  # Skip header
        for line in fil:
            Sline = line.split()
            if len(Sline) >= 3:
                try:
                    orf_len = abs(float(Sline[2]) - float(Sline[1]))
                    if orf_len <= 500000:  # Exclude ORFs longer than 500,000 bp
                        orf_lengths.append(orf_len)
                except ValueError:
                    continue  # Skip lines with non-numeric data

    # Plot histogram
    plt.figure(figsize=(10, 6))
    plt.hist(orf_lengths, bins=50, color="skyblue", edgecolor="black")
    plt.title(f"Histogram of ORF Lengths from {os.path.basename(input_file)}")
    plt.xlabel("ORF Length (bp)")
    plt.ylabel("Frequency")
    plt.tight_layout()
    plt.savefig(output_file)
    print(f"Histogram saved to: {output_file}")

if __name__ == "__main__":
    main()
