import fitz  # PyMuPDF is imported as 'fitz'
import os

def extract_with_pymupdf(pdf_path):
    """
    Extracts all embedded data streams from a PDF using PyMuPDF and saves them.
    """
    try:
        # Create a directory to store extracted files
        output_dir = "extracted_pymupdf_files"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        print(f"Created directory: {output_dir}")

        # Open the PDF file
        doc = fitz.open(pdf_path)
        
        object_count = 0
        # Iterate through all objects in the PDF by their cross-reference number (xref)
        # We start at 1 because xref 0 is a special null object.
        for xref in range(1, doc.xref_length()):
            
            # Get the raw, decompressed stream data for the object
            stream_data = doc.xref_stream(xref)
            
            # If the object has a stream, stream_data will not be empty
            if stream_data:
                object_count += 1
                
                # Give the file a descriptive name
                file_path = os.path.join(output_dir, f"object_{xref}_stream.dat")
                
                # Write the raw data to a file
                with open(file_path, "wb") as f:
                    f.write(stream_data)
                
                print(f"Extracted data stream from object {xref} to '{file_path}' ({len(stream_data)} bytes)")
                # Print the first 16 bytes to help identify the file type (its "magic number")
                print(f"  -> File Header (first 16 bytes): {stream_data[:16]}")

        if object_count == 0:
            print("No extractable data streams were found in the PDF.")
        else:
            print(f"\nExtraction complete. Please check the '{output_dir}' directory.")
            print("Look for files that might be zip archives (header starts with 'PK'), images, or other interesting files.")

    except FileNotFoundError:
        print(f"Error: The file '{pdf_path}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

# --- Main execution ---
pdf_file = "challenge.pdf"
extract_with_pymupdf(pdf_file)