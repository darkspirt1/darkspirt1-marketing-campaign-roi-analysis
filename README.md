# 📊 Marketing Campaign Performance & ROI Analysis

An end-to-end data analytics project analyzing 200,000 marketing campaigns
across 6 channels, 5 cities, and a full year of data.

## 🔗 Live Dashboard
[👉 Click here to view the live dashboard](https://darkspirt1-marketing-campaign-roi-analysis-peulxfdn6tsjcs4zbpa.streamlit.app/)

## 📌 Project Overview
This project answers the key business question:
> *Which marketing campaigns actually work, and where should we invest more?*

## 🛠️ Tech Stack
- **Python** — Core language
- **Pandas & NumPy** — Data manipulation
- **Plotly** — Interactive visualizations
- **Streamlit** — Dashboard UI
- **Jupyter Notebook** — Exploratory analysis

## 📊 Key Insights
- Average ROI across all campaigns: **5.00x**
- Average Customer Acquisition Cost: **$12,504**
- Best performing channel: **Facebook**
- Best audience segment: **Men 25-34**
- Peak performance month: **September 2021**
- High impressions negatively correlate with CTR **(−0.66)**

## 📁 Project Structure
```
├── dashboard/
│   └── app.py                        # Streamlit dashboard
├── data/
│   └── marketing_campaign_dataset.csv
├── notebook/
│   └── marketing_analysis.ipynb
├── requirements.txt
└── README.md
```

## 🚀 Run Locally
```bash
git clone https://github.com/darkspirt1/marketing-campaign-roi-analysis.git
cd marketing-campaign-roi-analysis
pip install -r requirements.txt
streamlit run dashboard/app.py
```

