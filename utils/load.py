import os
import pandas as pd
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

def save_to_csv(df, filename="products.csv"):
    try:
        # Buat direktori jika belum ada
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        df.to_csv(filename, index=False)
        print(f"Data berhasil disimpan ke {filename}")
        return True
    except Exception as e:
        print(f"Gagal menyimpan ke CSV: {e}")
        return False
        
def load_to_gsheet(fashion_df, spreadsheet_id='1zYB0DG5UUEohaKnHZNB2BCVaWZRlWq_eJ3_as8wiPN4', worksheet_range='Sheet1!A1'):
    """
    Mengunggah DataFrame ke Google Sheets menggunakan Google Sheets API.
    
    - spreadsheet_id: ID Google Spreadsheet (bukan nama).
    - worksheet_range: range awal tempat data ditulis (contoh: 'Sheet1!A1').
    """
    try:
        # Cek file kredensial
        if not os.path.exists('google-sheets-api.json'):
            print("File 'google-sheets-api.json' tidak ditemukan.")
            return False

        # Autentikasi
        scopes = ['https://www.googleapis.com/auth/spreadsheets']
        creds = Credentials.from_service_account_file('google-sheets-api.json', scopes=scopes)
        service = build('sheets', 'v4', credentials=creds)

        # Konversi DataFrame ke format list of lists
        values = [fashion_df.columns.tolist()] + fashion_df.values.tolist()
        body = {
            'values': values
        }

        # Update isi sheet
        result = service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id,
            range=worksheet_range,
            valueInputOption='RAW',
            body=body
        ).execute()

        print(f"{result.get('updatedCells')} sel berhasil diperbarui di Google Sheets.")
        return True

    except Exception as e:
        print(f"Gagal mengirim ke Google Sheets: {e}")
        return False