#!/bin/bash

sudo apt-get update
sudo apt-get install pdftk paps -y

input_pdf="pdfs/chapters.pdf"
output_pdf="pdfs/final.pdf"
temp_dir="temp_pages"

# Create a temporary directory if it doesn't exist
mkdir -p "$temp_dir"

# Get total number of pages
total_pages=$(pdftk "$input_pdf" dump_data | grep "NumberOfPages" | awk '{print $2}')

# Loop through each page
for ((page=1; page<=total_pages; page++)); do
    # Create a temporary file for the modified page
    temp_page="$temp_dir/temp_page_$page.pdf"

    # Add pagination to the current page
    # pdftk "$input_pdf" cat $page output "$temp_page"

    # Add page number to the bottom right corner
    pdftk "$temp_page" stamp <(echo "[$page / $total_pages]" | \
        paps --bottom-margin=10 --font="Helvetica 8") output "$temp_page"

    # Concatenate pages
    if [[ $page -eq 1 ]]; then
        cp "$temp_page" "$output_pdf"
    else
        pdftk "$output_pdf" "$temp_page" cat output "$output_pdf"
    fi
done

# Clean up temporary directory
rm -r "$temp_dir"

echo "Done."
