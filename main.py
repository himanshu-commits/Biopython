import tkinter as tk
from tkinter import messagebox, ttk

from Bio import Entrez, SeqIO


def fetch_sequence(accession_number):
        try:
            Entrez.email = "ps11031706@gmail.com"  
            handle = Entrez.efetch(db="nucleotide", id=accession_number, rettype="gb", retmode="text")
            record = SeqIO.read(handle, "genbank")
            dna_sequence = str(record.seq)
            protein_sequence = str(record.seq.translate())
            definition = record.description
            handle.close()
            return dna_sequence, protein_sequence, definition
        except Exception:
            return None, None, None

def on_fetch_sequence():
            accession_number = accession_entry.get()
            dna_sequence, protein_sequence, definition = fetch_sequence(accession_number)
            if dna_sequence and protein_sequence:
                dna_text.delete(1.0, tk.END)
                dna_text.insert(tk.END, dna_sequence)

                protein_text.delete(1.0, tk.END)
                protein_text.insert(tk.END, protein_sequence)

                result_label.config(text=f"Definition: {definition}")
            else:
                result_label.config(text="Error fetching sequence. Check accession number.")

def copy_dna_sequence():
  sequence_to_copy = dna_text.get(1.0, tk.END)
  root.clipboard_clear()
  root.clipboard_append(sequence_to_copy.strip())
  root.clipboard_get()
  messagebox.showinfo("Copy Successful", "DNA sequence copied to clipboard.")

def copy_protein_sequence():
  sequence_to_copy = protein_text.get(1.0, tk.END)
  root.clipboard_clear()
  root.clipboard_append(sequence_to_copy.strip())
  root.clipboard_get()
  messagebox.showinfo("Copy Successful", "Protein sequence copied to clipboard.")

# Create the main window
root = tk.Tk()
root.title("DNA to Protein Converter")

# Create and place widgets
fetch_button = ttk.Button(root, text="Fetch Sequence", command=on_fetch_sequence)
fetch_button.grid(row=0, column=0, padx=10, pady=10)

reset_button = ttk.Button(root, text="Reset", command=lambda: result_label.config(text=""))
reset_button.grid(row=0, column=1, padx=10, pady=10)

accession_label = ttk.Label(root, text="Accession Number:")
accession_label.grid(row=0, column=2, padx=10, pady=10, sticky="w")

accession_entry = ttk.Entry(root, width=20)
accession_entry.grid(row=0, column=3, padx=10, pady=10)

result_label = ttk.Label(root, text="")
result_label.grid(row=1, column=0, columnspan=4, pady=10)

# Create a frame for DNA and Protein sequences
sequence_frame = ttk.Frame(root)
sequence_frame.grid(row=2, column=0, columnspan=4, padx=10, pady=10)

dna_label = ttk.Label(sequence_frame, text="DNA Sequence:")
dna_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

dna_text = tk.Text(sequence_frame, height=5, width=40)
dna_text.grid(row=1, column=0, padx=10, pady=10)

# Add a vertical scrollbar for the DNA sequence text
dna_scrollbar = ttk.Scrollbar(sequence_frame, command=dna_text.yview)
dna_scrollbar.grid(row=1, column=1, sticky='nsew')
dna_text['yscrollcommand'] = dna_scrollbar.set

protein_label = ttk.Label(sequence_frame, text="Protein Sequence:")
protein_label.grid(row=0, column=2, padx=10, pady=10, sticky="w")

protein_text = tk.Text(sequence_frame, height=5, width=40)
protein_text.grid(row=1, column=2, padx=10, pady=10)

# Add a vertical scrollbar for the Protein sequence text
protein_scrollbar = ttk.Scrollbar(sequence_frame, command=protein_text.yview)
protein_scrollbar.grid(row=1, column=3, sticky='nsew')
protein_text['yscrollcommand'] = protein_scrollbar.set

copy_dna_button = ttk.Button(sequence_frame, text="Copy DNA", command=copy_dna_sequence)
copy_dna_button.grid(row=2, column=0, padx=10, pady=10)

copy_protein_button = ttk.Button(sequence_frame, text="Copy Protein", command=copy_protein_sequence)
copy_protein_button.grid(row=2, column=2, padx=10, pady=10)

# Run the Tkinter event loop
root.mainloop()
