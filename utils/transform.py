import pandas as pd
import numpy as np
import re

def transform_to_DataFrame(data):
    # Mengubah data menjadi DataFrame
    try:
        fashion_df = pd.DataFrame(data)
        return fashion_df
    except Exception as e:
        print(f"Error saat mengubah data ke DataFrame: {e}")
        return pd.DataFrame()

def price_in_dollar(price_str):
    try:
        # Hapus simbol $ dan koma, lalu konversi ke float
        cleaned = re.sub(r'[\$,]', '', str(price_str))
        return float(cleaned)
    except (ValueError, TypeError) as e:
        print(f"Error saat membersihkan harga '{price_str}': {e}")
        return np.nan

def extract_rating(rating_str):
    try:
        match = re.search(r'(\d+\.\d+)', str(rating_str))
        if match:
            return float(match.group(1))
        return np.nan
    except (ValueError, TypeError, AttributeError) as e:
        print(f"Error saat mengekstrak rating '{rating_str}': {e}")
        return np.nan

def extract_colors(colors_str):
    try:
        match = re.search(r'(\d+)', str(colors_str))
        if match:
            return int(match.group(1))
        return 0
    except (ValueError, TypeError, AttributeError) as e:
        print(f"Error saat mengekstrak colors '{colors_str}': {e}")
        return 0

def transform_data(data, exchange_rate=16000):
    try:
        fashion_df = data.copy()

        # Menghapus baris duplikat
        fashion_df_clean = fashion_df.drop_duplicates()
        print(f"Menghapus {len(fashion_df) - len(fashion_df_clean)} baris duplikat")
        fashion_df = fashion_df_clean
        
        # Filter data dengan judul tidak valid
        valid_title_mask = fashion_df['Title'] != 'Unknown Product'
        df_clean = fashion_df[valid_title_mask]
        print(f"Menghapus {len(fashion_df) - len(df_clean)} baris dengan judul tidak valid")
        fashion_df = df_clean
        
        # Transformasi kolom Price
        fashion_df['Price'] = fashion_df['Price'].replace(['Price Not Found', 'Price Unavailable'], np.nan)
        fashion_df = fashion_df.infer_objects(copy=False)
        
        # Konversi Price ke float dan kali dengan exchange rate
        fashion_df['Price'] = fashion_df['Price'].apply(price_in_dollar) * exchange_rate
        
        # Hapus baris dengan Price yang tidak valid (NaN)
        before_len = len(fashion_df)
        fashion_df = fashion_df.dropna(subset=['Price'])
        print(f"Menghapus {before_len - len(fashion_df)} baris dengan harga tidak valid")
        
        # Hapus baris yang masih memiliki nilai kosong di kolom penting
        essential_cols = ['Title', 'Price', 'Rating', 'Colors', 'Size', 'Gender', 'Timestamp']
        before_null_removal = len(fashion_df)
        fashion_df = fashion_df.dropna(subset=essential_cols)
        print(f"Menghapus {before_null_removal - len(fashion_df)} baris yang memiliki nilai kosong di kolom penting")
        
        # Isi nilai null Rating dengan rata-rata jika ada
        if fashion_df['Rating'].isnull().any():
            rating_mean = fashion_df['Rating'].mean()
            fashion_df['Rating'] = fashion_df['Rating'].fillna(rating_mean)
            print(f"Menangani nilai null di kolom Rating, mengganti dengan rata-rata: {rating_mean}")
        
        # Extract nilai dari kolom Rating dan Colors
        fashion_df['Rating'] = fashion_df['Rating'].apply(extract_rating)
        fashion_df['Colors'] = fashion_df['Colors'].apply(extract_colors)

        # Bersihkan string Size dan Gender, ganti None jadi string kosong sebelum strip
        fashion_df['Size'] = fashion_df['Size'].fillna('').astype(str).str.replace('Size:', '').str.strip()
        fashion_df['Gender'] = fashion_df['Gender'].fillna('').astype(str).str.replace('Gender:', '').str.strip()
        
        # Validasi tipe data
        fashion_df['Title'] = fashion_df['Title'].astype(str)
        fashion_df['Price'] = fashion_df['Price'].astype(float)
        fashion_df['Rating'] = fashion_df['Rating'].astype(float)
        fashion_df['Colors'] = fashion_df['Colors'].astype(int)
        fashion_df['Size'] = fashion_df['Size'].astype(str)
        fashion_df['Gender'] = fashion_df['Gender'].astype(str)
        fashion_df['Timestamp'] = fashion_df['Timestamp'].astype(str)
        
        print(f"Transformasi selesai. Hasil: {len(fashion_df)} baris data bersih.")
        return fashion_df
        
    except Exception as e:
        print(f"Error saat melakukan transformasi data: {e}")
        return data
