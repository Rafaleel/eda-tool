# 📊 Automatic EDA Report Generator

A command-line tool that takes any CSV file and automatically generates
a complete interactive HTML report with statistics, distributions,
correlations, and missing value analysis — powered by Plotly and Jinja2.

---

## 📸 Report Sections

- **Overview** — row count, column types, duplicates, memory usage
- **Missing Values** — table + bar chart with severity classification
- **Descriptive Statistics** — mean, std, min, max, quartiles
- **Skewness & Kurtosis** — with log transform recommendations
- **Distributions** — interactive histogram per numeric column
- **Correlation Matrix** — annotated heatmap with dynamic text color
- **Categorical Columns** — top 10 values per categorical column

---

## 🚀 How to Run

### Local

```bash
# Clone the repository
git clone https://github.com/Rafaleel/eda-tool
cd eda-tool

# Create environment
conda create -n eda-tool python=3.11
conda activate eda-tool
pip install -r requirements.txt

# Generate report
python eda_report.py path/to/your/file.csv

# Custom output name
python eda_report.py path/to/your/file.csv --output my_report.html

# CSV with different separator (semicolon)
python eda_report.py path/to/your/file.csv --sep ";"
```

### Docker

```bash
# Build
docker build -t eda-tool .

# Run
docker run --rm \
  -v $(pwd)/data:/app/data \
  -v $(pwd):/app/output \
  eda-tool python eda_report.py data/your_file.csv --output output/report.html
```

---

## 🛠️ Stack

| Tool | Purpose |
|---|---|
| Python 3.11 | Core language |
| pandas | Data loading and analysis |
| plotly | Interactive charts |
| jinja2 | HTML report templating |
| Docker | Containerization |

---

## 📁 Project Structure

<pre>
eda-tool/
├── templates/
│   └── template.html
├── analyzer.py
├── charts.py
├── eda_report.py
├── requirements.txt
├── Dockerfile
└── README.md
</pre>
---

## 💡 Technical Decisions

**Plotly over Matplotlib** — generates interactive HTML charts (zoom,
hover, filter) with no extra dependencies at render time.

**Jinja2 templating** — same engine used by Flask and Django, keeps
HTML and Python completely separated.

**go.Histogram over px.histogram** — more stable serialization with
custom dark themes and no subplot conflicts.

**Dynamic annotation colors** — correlation matrix uses dark text for
light cells and white text for dark cells, ensuring readability at
any value.
