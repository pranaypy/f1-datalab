# 🏎️ F1 DataLab

A Formula 1 Data Analysis and Visualization app built with Python and Streamlit.

![Python](https://img.shields.io/badge/Python-3.12-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.45-red)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 📌 Features

- 🔍 Search any F1 driver by name
- 📊 View complete career statistics
- 🏆 World championship count
- 📈 Points per season chart
- 📉 Wins per season chart
- 🥇 Championship years highlighted with trophy indicators

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| Python | Core language |
| Streamlit | Web UI |
| pandas | Data processing |
| Plotly | Interactive charts |
| Jolpica API | F1 historical data |
| Git + GitHub | Version control |

---

## 🚀 Setup & Installation

**1. Clone the repository**
```bash
git clone https://github.com/pranaypy/f1-datalab.git
cd f1-datalab
```

**2. Create virtual environment**
```bash
python -m venv f1venv
f1venv\Scripts\activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Run the app**
```bash
streamlit run app/main.py
```

---

## 📁 Project Structure

```
f1-datalab/
├── app/                  # Streamlit UI
│   └── main.py
├── services/             # API calls
│   └── ergast_api.py
├── visualizations/       # Plotly charts
│   └── driver_charts.py
├── analysis/             # Data processing
├── utils/                # Helper functions
├── .streamlit/           # Theme config
│   └── config.toml
└── requirements.txt
```

---

## 📊 Data Source

All F1 data is fetched from the
[Jolpica F1 API](https://api.jolpi.ca/ergast/f1/)
— a community maintained replacement for the original Ergast API.

---

## 🗺️ Roadmap

- [x] Driver search
- [x] Career statistics
- [x] Season performance charts
- [ ] Lap time telemetry (FastF1)
- [ ] Driver comparison
- [ ] Race result analysis
- [ ] Local data caching

---

## 👤 Author

Built by [@pranaypy](https://github.com/pranaypy)
as a portfolio project to learn Python, APIs, and data visualization.