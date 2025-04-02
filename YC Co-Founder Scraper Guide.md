# 🚀 YC Co-Founder Scraper

This Python script uses Selenium to scrape profiles from Y Combinator's [Co-Founder Matching Tool](https://www.startupschool.org/cofounder-matching/candidate/next). It extracts key info like the founder’s name, LinkedIn URL, and their full profile text, and saves it to a CSV file for later use.

---

## 📦 What It Does

- Opens a Chrome browser and navigates to the YC co-founder match tool.
- Lets you log in manually (30-second pause).
- Scrapes founder details:
  - ✅ Name  
  - ✅ LinkedIn profile (from the profile card at the bottom)  
  - ✅ Full profile text (life story, intro, etc.)
- Clicks **"Skip for now"** and repeats until it reaches the desired number of profiles.
- Saves all data into a CSV file (and supports appending to an existing file).
- Skips profiles already saved to avoid duplicates.

---

## 🔧 Requirements

Make sure you have the following installed:

### 1. Python 3

Verify with:
```bash
python3 --version
```

### 2. Install Required Python Packages

Use pip to install everything:
```bash
pip install selenium pandas webdriver-manager
```

### 3. Google Chrome + ChromeDriver

This script uses your installed Google Chrome. You don’t need to manually install ChromeDriver thanks to `webdriver-manager`, which handles that automatically.

---

## ⚙️ Configuration

Open `scraper.py` and look for this section at the top of the file:

```python
# === CONFIG ===
MAX_PROFILES = 3              # Number of profiles to scrape in one run
CSV_FILENAME = "yc_profiles.csv"  # Name of the CSV file to write data into
APPEND_TO_CSV = True          # If True, appends to existing CSV file; if False, overwrites it
```

### Config Variables

| Variable         | Type    | Description |
|------------------|---------|-------------|
| `MAX_PROFILES`   | `int`   | How many new profiles you want to scrape this run. |
| `CSV_FILENAME`   | `str`   | Name of the CSV file you want the data saved in. |
| `APPEND_TO_CSV`  | `bool`  | `True` = keep adding to existing CSV. `False` = start fresh. |

---

## 🧪 How to Run

1. Open Terminal
2. Navigate to your project folder:
   ```bash
   cd path/to/your/folder
   ```
3. Run the script:
   ```bash
   python3 scraper.py
   ```
4. The browser will open and pause for **30 seconds** so you can **log in** manually.
5. After login, scraping begins automatically.
6. You’ll see progress logs in the terminal. Scraped data will be saved in `yc_profiles.csv`.

---

## ✅ Output Format

The script generates a CSV with the following columns:

- `Name`
- `LinkedIn`
- `ProfileText`

---

## 📌 Notes

- **Avoid scraping too many profiles too fast**. Human-like delays are built in to simulate real behavior.
- Profiles already scraped will be skipped automatically in future runs.
- You can stop and restart the script at any time — it will pick up where it left off if `APPEND_TO_CSV = True`.
