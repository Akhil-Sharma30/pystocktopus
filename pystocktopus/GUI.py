import tkinter as tk
from tkinter import messagebox
import os
from dotenv import load_dotenv
from datetime import datetime
import csv
import tkinter as tk
from tkcalendar import DateEntry

from .core import StockExtractor
from .news_analysis import News
from .stock_forecasting import ModelStockData
from .stock_csv import CSVDataHandler
from tkinter import filedialog, messagebox
import threading

def main():
    # Function to handle the submission of API keys
    def submit_keys():
        api_key1 = entry1.get()
        api_key2 = entry2.get()
        
        # Check if both API keys are provided
        if api_key1 and api_key2:
            # Set API keys as environment variables
            os.environ['POLYGON_API'] = api_key1
            os.environ['NEWS_API'] = api_key2
            
            # Optionally, save the keys to a .env file
            with open('.env', 'w') as env_file:
                env_file.write(f'POLYGON_API={api_key1}\nNEWS_API={api_key2}\n')
            
            # Clear the screen and display welcome message
            show_welcome_screen()
        else:
            # Show error if any field is empty
            messagebox.showerror("Error", "Please enter both API keys.")

    # Function to display the welcome screen
    def show_welcome_screen():
        # Clear the window content
        for widget in root.winfo_children():
            widget.destroy()
        
        # Display the welcome message
        welcome_label = tk.Label(root, text="Welcome to PYSTOCKTOPUS!", font=("Arial", 24))
        welcome_label.pack(pady=20)
        
        # Create buttons for button 1, button 2, button 3
        button1 = tk.Button(root, text="Generate a Stock Closing Price CSV", command=show_button_screen_CSV, width=30, height=2)
        button1.pack(pady=10)

        button2 = tk.Button(root, text="Prediction of Next Day Closing Price", command=show_button_screen_PRED, width=30, height=2)
        button2.pack(pady=10)

        button3 = tk.Button(root, text="News Analysis for a Stock", command=show_button_screen_NEWS, width=30, height=2)
        button3.pack(pady=10)

        # Optional: Add a footer with additional information or links
        footer_label = tk.Label(root, text="Developed by Akhil Sharma", bg="#f0f4f7", fg="#888888", font=("Helvetica Neue", 10))
        footer_label.pack(side=tk.BOTTOM, pady=10)

    def show_button_screen_CSV():
        # Clear the window content
        for widget in root.winfo_children():
            widget.destroy()
        
        # Display welcome message specific to the CSV Generator
        label = tk.Label(root, text="CSV Generator", font=("Arial", 24))
        label.pack(pady=20)
        
        # Frame for Start Date and End Date
        date_frame = tk.Frame(root)
        date_frame.pack(pady=10)

        # Start Date
        start_label = tk.Label(date_frame, text="Start Date (YYYY-MM-DD):")
        start_label.grid(row=0, column=0, padx=5, pady=5, sticky='e')
        
        # Use DateEntry for the start date
        start_entry = DateEntry(date_frame, date_pattern='yyyy-mm-dd')  # Set the date format
        start_entry.grid(row=0, column=1, padx=5, pady=5)

        # Frame for Name Entries
        name_frame = tk.Frame(root)
        name_frame.pack(pady=10)

        name_labels = ["Ticker Name:", "Timespan:", "Multiplier:"]
        name_entries = []
        for i, name in enumerate(name_labels):
            lbl = tk.Label(name_frame, text=name)
            lbl.grid(row=i, column=0, padx=5, pady=5, sticky='e')
            entry = tk.Entry(name_frame)
            entry.grid(row=i, column=1, padx=5, pady=5)
            name_entries.append(entry)

    # Function to generate CSV
        def generate_csv():
            start_date_str = start_entry.get()
            names = [entry.get() for entry in name_entries]
            print(names)

            # Validate date format
            try:
                # start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
                start_date = start_date_str
            except ValueError:
                messagebox.showerror("Error", "Please enter dates in YYYY-MM-DD format.")
                return

            # Validate names
            if not all(names):
                messagebox.showerror("Error", "Please enter all three names.")
                return

            # Define CSV filename
            filename = "GUI_GENERATED_DATA.csv"

            # Write data to CSV
            try:
                print(start_date)
                data = StockExtractor.ticker_data_collection([names[0]],names[1],int(names[2]),start_date.strip())
                print(data)

                CSVDataHandler.close_list_csv(data, csv_file_name=filename)
                messagebox.showinfo("Success", f"CSV file '{filename}' has been generated successfully.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to generate CSV file. Error: {e}")

        # Generate CSV button
        generate_button = tk.Button(root, text="Generate CSV", command=generate_csv, width=20)
        generate_button.pack(pady=10)

        # Back button to return to the welcome screen
        back_button = tk.Button(root, text="Back", command=show_welcome_screen, width=10)
        back_button.pack(pady=10)

    def show_button_screen_PRED():
        # Clear the window content
        for widget in root.winfo_children():
            widget.destroy()

        # Display welcome message specific to the News Analysis
        label = tk.Label(root, text="News Analysis", font=("Arial", 24))
        label.pack(pady=20)

        name_frame = tk.Frame(root)
        name_frame.pack(pady=10)

        # List of name labels
        name_labels = ["Epochs:", "Learning Rate:", "Stock Closing Price Column Name in CSV:"]
        name_entries = []

        # Create labels and entry fields for each name, setting default value
        for i, name in enumerate(name_labels):
            lbl = tk.Label(name_frame, text=name)
            lbl.grid(row=i, column=0, padx=5, pady=5, sticky='e')

            entry = tk.Entry(name_frame)

            # Set default values
            if i == 0:
                entry.insert(0, "650")
            if i == 1:  
                entry.insert(0, "0.0008")

            entry.grid(row=i, column=1, padx=5, pady=5)
            name_entries.append(entry)

        # Variable to store the file path
        file_path = tk.StringVar()

        # Function to handle file upload
        def upload_file():
            selected_file = filedialog.askopenfilename(
                title="Select a CSV file", 
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
            )
            if selected_file:
                file_path.set(selected_file)  # Set the file path

        # Create a label and button for file upload
        file_frame = tk.Frame(root)
        file_frame.pack(pady=10)

        file_label = tk.Label(file_frame, text="Upload CSV File:")
        file_label.grid(row=0, column=0, padx=5, pady=5, sticky='e')

        upload_button = tk.Button(file_frame, text="Browse", command=upload_file)
        upload_button.grid(row=0, column=1, padx=5, pady=5)

        # Display the selected file path
        file_display = tk.Label(file_frame, textvariable=file_path)
        file_display.grid(row=1, column=1, padx=5, pady=5)

        # Label for showing training progress
        progress_label = tk.Label(root, text="", font=("Arial", 12), fg="blue")
        progress_label.pack(pady=10)

        # Function to handle the news analysis based on entered names and the uploaded file
        def pred_value():
            names = [entry.get() for entry in name_entries]  # Get all user inputs from the entry fields
            file = file_path.get()  # Get the selected file path

            # Check if all fields have been filled and file is uploaded
            if not names[0] or not file:  
                messagebox.showerror("Error", "Please enter all fields and upload a file.")
                return

            try:
                epochs = int(names[0])
                lr = float(names[1])  # Convert learning rate to a float
            except ValueError:
                messagebox.showerror("Error", "Please enter valid numbers for Epochs and Learning Rate.")
                return

            # Function to run the prediction and update progress
            def run_training():
                try:
                    progress_label.config(text="Training started...")

                    # Mockup of a training process
                    prediction = ModelStockData.create_and_fit_lstm_model(
                        csv_file=file,
                        epochs=epochs,
                        lr=lr,
                        stock_closing_price_column_name=names[2],
                        progress_callback=update_progress  # Pass the callback for updates
                    )

                    # When training completes
                    progress_label.config(text="Training complete.")
                    messagebox.showinfo("Success", f"News analysis completed using file: {prediction}")
                except Exception as e:
                    progress_label.config(text="Training failed.")
                    messagebox.showerror("Error", f"An error occurred during analysis: {e}")

            # Function to update the progress label
            def update_progress(epoch, loss):
                progress_label.config(text=f"Epoch {epoch}, Loss: {loss:.4f}")

            # Start the training process in a separate thread
            threading.Thread(target=run_training).start()

        # Button to trigger news analysis
        analyze_button = tk.Button(root, text="Analyze News", command=pred_value, width=20)
        analyze_button.pack(pady=10)

        # Back button to return to the welcome screen
        back_button = tk.Button(root, text="Back", command=show_welcome_screen, width=10)
        back_button.pack(pady=10)


    # Function to display the News Analysis screen
    def show_button_screen_NEWS():
        # Clear the window content
        for widget in root.winfo_children():
            widget.destroy()
        
        # Display welcome message specific to the News Analysis
        label = tk.Label(root, text="News Analysis", font=("Arial", 24))
        label.pack(pady=20)

        # Frame for Date and Name Entries
        input_frame = tk.Frame(root)
        input_frame.pack(pady=10)

        name_frame = tk.Frame(root)
        name_frame.pack(pady=10)

        # Add a DateEntry widget for start_date selection
        start_date_label = tk.Label(input_frame, text="Today/Start Date (YYYY-MM-DD):")
        start_date_label.grid(row=0, column=0, padx=5, pady=5, sticky='e')
        
        start_date_entry = DateEntry(input_frame, date_pattern='yyyy-mm-dd')  # Calendar date picker
        start_date_entry.grid(row=0, column=1, padx=5, pady=5)

        # List of two name labels: Stock Name and Time stamp
        name_labels = ["Stock Name:", "Time stamp:"]
        name_entries = []

        # Create labels and entry fields for each name, setting default value for Time stamp
        for i, name in enumerate(name_labels):
            lbl = tk.Label(name_frame, text=name)
            lbl.grid(row=i, column=0, padx=5, pady=5, sticky='e')

            entry = tk.Entry(name_frame)

            # Set default value for Time stamp to "20"
            if i == 1:
                entry.insert(0, "20")  # Default value for Time stamp

            entry.grid(row=i, column=1, padx=5, pady=5)
            name_entries.append(entry)

        # Function to handle the news analysis based on entered names and start date
        def analyze_news():
            start_date = start_date_entry.get()  # Get the selected start date
            names = [entry.get() for entry in name_entries]  # Get all user inputs from the entry fields

            # Check if all fields have been filled
            if not names[0]:  # Validate Stock Name
                messagebox.showerror("Error", "Please enter a Stock Name.")
                return

            try:
                days = int(names[1])  # Convert Time stamp to an integer
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid number for Time stamp.")
                return

            # Now call the News extraction function with the user inputs
            try:
                result = News.new_data_extract(ticker_values=[names[0]], predict_date=start_date, days=days)
                print(result)
                ans = News.news_predict_analysis(result)
                print(ans)
                sentiment = list(ans.values())[0]
                messagebox.showinfo("Success", f"News analysis completed: {sentiment}")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred during analysis: {e}")

        # Button to trigger news analysis
        analyze_button = tk.Button(root, text="Analyze News", command=analyze_news, width=20)
        analyze_button.pack(pady=10)

        # Back button to return to the welcome screen
        back_button = tk.Button(root, text="Back", command=show_welcome_screen, width=10)
        back_button.pack(pady=10)

    # Main application window
    load_dotenv()
    root = tk.Tk()
    root.title("API Key Submission")
    root.geometry("400x500")

    # Check if the API keys are already set in the environment
    api_key1 = os.getenv('POLYGON_API')
    api_key2 = os.getenv('NEWS_API')

    if api_key1 and api_key2:
        # If keys are found, show the welcome screen
        show_welcome_screen()
    else:
        # If keys are not found, prompt the user to enter them
        label1 = tk.Label(root, text="Enter Polygon API KEY:", font=("Arial", 12))
        label1.pack(pady=10)
        entry1 = tk.Entry(root, width=40)
        entry1.pack(pady=5)

        label2 = tk.Label(root, text="Enter News API KEY:", font=("Arial", 12))
        label2.pack(pady=10)
        entry2 = tk.Entry(root, width=40)
        entry2.pack(pady=5)

        # Submit button
        submit_button = tk.Button(root, text="Submit", command=submit_keys, width=20)
        submit_button.pack(pady=20)

    # Run the application
    root.mainloop()

if __name__=="__main__":
    main()