#!/bin/bash

sudo apt-get update
sudo apt-get install pdftk paps -y

input_pdf="pdfs/output.pdf"
output_pdf="pdfs/final.pdf"
temp_dir="temp_pages"
output_dir="output_pdfs"

# Create temporary and output directories if they don't exist
mkdir -p "$temp_dir"
mkdir -p "$output_dir"

# Get total number of pages
total_pages=$(pdftk "$input_pdf" dump_data | grep "NumberOfPages" | awk '{print $2}')

# Loop through each page
for ((page=1; page<=total_pages; page++)); do
    # Create a temporary file for the modified page
    temp_page="$temp_dir/temp_page_$page.pdf"

    # Add pagination to the current page
    pdftk "$input_pdf" cat $page output "$temp_page"

    # Add page number to the bottom right corner
    pdftk "$temp_page" stamp <(echo "[$page / $total_pages]" | \
        paps --bottom-margin=10 --font="Helvetica 8") output "$temp_page"

    # Move processed page to the output directory
    mv "$temp_page" "$output_dir/"

    # Concatenate pages
    if [[ $page -eq 1 ]]; then
        cp "$output_dir/temp_page_$page.pdf" "$output_pdf"
    else
        pdftk "$output_pdf" "$output_dir/temp_page_$page.pdf" cat output "$output_pdf"
    fi
done

# Clean up temporary directory
rm -r "$temp_dir"

echo "Done."
