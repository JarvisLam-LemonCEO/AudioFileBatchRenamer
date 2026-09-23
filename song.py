#!/usr/bin/env python3

import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk


class BatchRenamer:
	def __init__(self, root):
		self.root = root
		self.root.title("Audio File Batch Renamer")
		self.root.geometry("900x600")
		self.root.minsize(750, 450)
		
		self.folder_path = tk.StringVar()
		
		self.create_ui()
		
	def create_ui(self):
		# ==============================
		# Title
		# ==============================
		title = tk.Label(
			self.root,
			text="Audio File Batch Renamer",
			font=("Arial", 20, "bold")
		)
		title.pack(pady=(20, 5))
		
		description = tk.Label(
			self.root,
			text='Removes everything before the 3rd " - " separator',
			font=("Arial", 11)
		)
		description.pack(pady=(0, 15))
		
		# ==============================
		# Folder selection
		# ==============================
		folder_frame = tk.Frame(self.root)
		folder_frame.pack(fill="x", padx=20)
		
		folder_entry = tk.Entry(
			folder_frame,
			textvariable=self.folder_path,
			font=("Arial", 11)
		)
		folder_entry.pack(
			side="left",
			fill="x",
			expand=True,
			padx=(0, 10),
			ipady=6
		)
		
		browse_button = tk.Button(
			folder_frame,
			text="Choose Folder",
			command=self.choose_folder,
			width=15
		)
		browse_button.pack(side="right")
		
		# ==============================
		# Preview buttons
		# ==============================
		button_frame = tk.Frame(self.root)
		button_frame.pack(fill="x", padx=20, pady=15)
		
		preview_button = tk.Button(
			button_frame,
			text="Preview",
			command=self.preview_files,
			width=15
		)
		preview_button.pack(side="left")
		
		rename_button = tk.Button(
			button_frame,
			text="Rename All",
			command=self.rename_all,
			width=15,
			bg="#007AFF",
			fg="white"
		)
		rename_button.pack(side="right")
		
		# ==============================
		# Preview table
		# ==============================
		table_frame = tk.Frame(self.root)
		table_frame.pack(
			fill="both",
			expand=True,
			padx=20,
			pady=(0, 10)
		)
		
		columns = ("old", "new")
		
		self.tree = ttk.Treeview(
			table_frame,
			columns=columns,
			show="headings"
		)
		
		self.tree.heading("old", text="Original Filename")
		self.tree.heading("new", text="New Filename")
		
		self.tree.column("old", width=420)
		self.tree.column("new", width=420)
		
		scrollbar = ttk.Scrollbar(
			table_frame,
			orient="vertical",
			command=self.tree.yview
		)
		
		self.tree.configure(yscrollcommand=scrollbar.set)
		
		self.tree.pack(
			side="left",
			fill="both",
			expand=True
		)
		
		scrollbar.pack(
			side="right",
			fill="y"
		)
		
		# ==============================
		# Status bar
		# ==============================
		self.status_label = tk.Label(
			self.root,
			text="Choose a folder to begin.",
			anchor="w"
		)
		self.status_label.pack(
			fill="x",
			padx=20,
			pady=(0, 15)
		)
		
	# ==================================
	# Choose Folder
	# ==================================
	def choose_folder(self):
		folder = filedialog.askdirectory()
		
		if folder:
			self.folder_path.set(folder)
			self.preview_files()
			
	# ==================================
	# Generate New Filename
	# ==================================
	def generate_new_name(self, filename):
		"""
		Split filename at most 3 times using:
		space + hyphen + space

		Example:
		Album - Album Name - 001 - Song Name.mp3

		Result:
		Song Name.mp3
		"""
		
		parts = filename.split(" - ", 3)
		
		if len(parts) == 4:
			return parts[3]
		
		return None
	
	# ==================================
	# Preview
	# ==================================
	def preview_files(self):
		folder = self.folder_path.get()
		
		if not folder or not os.path.isdir(folder):
			messagebox.showwarning(
				"No Folder",
				"Please choose a valid folder."
			)
			return
		
		# Clear existing table
		for item in self.tree.get_children():
			self.tree.delete(item)
			
		files_found = 0
		
		for filename in sorted(os.listdir(folder)):
			full_path = os.path.join(folder, filename)
			
			# Skip folders
			if not os.path.isfile(full_path):
				continue
			
			new_name = self.generate_new_name(filename)
			
			if new_name:
				self.tree.insert(
					"",
					"end",
					values=(filename, new_name)
				)
				
				files_found += 1
				
		self.status_label.config(
			text=f"{files_found} file(s) ready to rename."
		)
		
	# ==================================
	# Rename All
	# ==================================
	def rename_all(self):
		folder = self.folder_path.get()
		
		if not folder or not os.path.isdir(folder):
			messagebox.showwarning(
				"No Folder",
				"Please choose a valid folder."
			)
			return
		
		files_to_rename = []
		
		for filename in os.listdir(folder):
			old_path = os.path.join(folder, filename)
			
			if not os.path.isfile(old_path):
				continue
			
			new_name = self.generate_new_name(filename)
			
			if new_name:
				new_path = os.path.join(folder, new_name)
				
				files_to_rename.append(
					(filename, new_name, old_path, new_path)
				)
				
		if not files_to_rename:
			messagebox.showinfo(
				"Nothing to Rename",
				'No files containing three " - " separators were found.'
			)
			return
		
		# Check for duplicate filenames
		conflicts = []
		
		for old_name, new_name, old_path, new_path in files_to_rename:
			if os.path.exists(new_path) and old_path != new_path:
				conflicts.append(new_name)
				
		if conflicts:
			conflict_text = "\n".join(conflicts[:10])
			
			if len(conflicts) > 10:
				conflict_text += "\n..."
				
			messagebox.showerror(
				"Filename Conflict",
				"The following filenames already exist:\n\n"
				+ conflict_text
				+ "\n\nNo files were renamed."
			)
			return
		
		# Confirmation
		answer = messagebox.askyesno(
			"Confirm Rename",
			f"Rename {len(files_to_rename)} file(s)?\n\n"
			"Everything before the third \" - \" separator will be removed."
		)
		
		if not answer:
			return
		
		renamed_count = 0
		errors = []
		
		for old_name, new_name, old_path, new_path in files_to_rename:
			try:
				os.rename(old_path, new_path)
				renamed_count += 1
				
			except Exception as e:
				errors.append(
					f"{old_name}\n{e}"
				)
				
		# Refresh preview
		self.preview_files()
		
		if errors:
			messagebox.showwarning(
				"Completed With Errors",
				f"{renamed_count} file(s) renamed successfully.\n\n"
				f"{len(errors)} file(s) could not be renamed."
			)
			
		else:
			messagebox.showinfo(
				"Rename Complete",
				f"Successfully renamed {renamed_count} file(s)."
			)
			
			
# ======================================
# Start Application
# ======================================
if __name__ == "__main__":
	root = tk.Tk()
	app = BatchRenamer(root)
	root.mainloop()