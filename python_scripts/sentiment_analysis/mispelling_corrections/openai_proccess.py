import csv
import os
from openai import OpenAI
import time

# Initialize the OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_misspellings(main_name):
    """
    Generates a list of 50 common misspellings for the main_name using OpenAI.
    """
    prompt = f"""
For the name '{main_name}', generate a list of 50 common misspellings. Include the original name as the first item in the list.
If the name consists of multiple words, generate misspellings accordingly for each word and the combined name.
Provide the list in a comma-separated format, without numbering.
Example format: Original, Misspelling1, Misspelling2, etc
"""
    try:
        response = client.chat.completions.create(
            model="gpt-4o",  # You can change this to gpt-3.5-turbo if needed
            messages=[
                {"role": "system", "content": "You are an assistant that helps generate common misspellings of names."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=600,
            n=1,
            temperature=0.7,
        )
        misspellings = response.choices[0].message.content.strip()
        return misspellings
    except Exception as e:
        print(f"Error generating misspellings for '{main_name}': {e}")
        return None

def main():
    # Define file paths relative to project root
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    input_file = os.path.join(base_dir, 'data', 'item_lists', 'item_main_names.csv')
    output_file = os.path.join(base_dir, 'data', 'item_lists', 'accepted_item_raw.csv')

    # Create/open output file
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile_out:
        writer = csv.writer(csvfile_out)
        writer.writerow(['ITEM', 'ITEMS'])  # Write header

        # Read input file
        with open(input_file, 'r', encoding='utf-8') as csvfile_in:
            reader = csv.DictReader(csvfile_in)
            
            for row in reader:
                item_name = row['ITEM']
                main_name = row['MAIN_NAME']
                
                print(f"\nProcessing: {item_name}")
                print(f"Main name: {main_name}")
                print("Generating misspellings...")
                
                # Generate misspellings
                misspellings = generate_misspellings(main_name)
                
                if misspellings:
                    print("\nGenerated misspellings:")
                    print(misspellings)
                    print("-" * 50)
                    
                    # Write to CSV
                    writer.writerow([item_name, misspellings])
                
                # Add a small delay to avoid rate limiting
                time.sleep(0)

        print(f"\nProcessing complete! Output saved to: {output_file}")

if __name__ == '__main__':
    main()