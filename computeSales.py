import json
import sys
import time
from pathlib import Path


def load_json(file_path):
    """
    Load a JSON file and return its content.
    Handles errors gracefully.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        print(f"Error: File not found -> {file_path}")
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format -> {file_path}")
    return None


def compute_total_sales(price_catalogue, sales_record):
    """
    Compute the total cost of all sales.
    Returns total cost and a list of errors.
    """
    total_cost = 0
    errors = []

    # Loop through all sales
    for sale in sales_record:
        # Each sale may have multiple items
        for item, quantity in sale.items():
            if item in price_catalogue:
                try:
                    total_cost += price_catalogue[item] * quantity
                except TypeError:
                    errors.append(f"Invalid quantity for item '{item}': {quantity}")
            else:
                errors.append(f"Unknown product in sales record: '{item}'")

    return total_cost, errors


def save_results(total_cost, errors, elapsed_time, output_file="SalesResults.txt"):
    """
    Save results (total cost, errors, execution time) to a text file.
    """
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("Sales Computation Results\n")
        f.write("------------------------\n")
        f.write(f"Total Sales: ${total_cost:.2f}\n")
        f.write(f"Execution Time: {elapsed_time:.4f} seconds\n\n")

        if errors:
            f.write("Errors encountered:\n")
            for error in errors:
                f.write(f"- {error}\n")

    print(f"\nResults saved to {output_file}")


def main():
    """
    Main program logic.
    """
    start_time = time.time()

    # Check command-line arguments
    if len(sys.argv) < 3:
        print("Usage: python computeSales.py priceCatalogue.json salesRecord.json")
        sys.exit(1)

    price_file = sys.argv[1]
    sales_file = sys.argv[2]

    # Load JSON files
    price_catalogue = load_json(price_file)
    sales_record = load_json(sales_file)

    if price_catalogue is None or sales_record is None:
        print("Cannot continue due to previous errors.")
        sys.exit(1)

    # Compute total sales
    total_cost, errors = compute_total_sales(price_catalogue, sales_record)

    # Compute elapsed time
    elapsed_time = time.time() - start_time

    # Print results to console
    print("\nSales Computation Results")
    print("------------------------")
    print(f"Total Sales: ${total_cost:.2f}")
    print(f"Execution Time: {elapsed_time:.4f} seconds")

    if errors:
        print("\nErrors encountered:")
        for error in errors:
            print(f"- {error}")

    # Save results to file
    save_results(total_cost, errors, elapsed_time)


if __name__ == "__main__":
    main()
