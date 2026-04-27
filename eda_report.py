import argparse
import os
import pandas as pd
from jinja2 import Environment, FileSystemLoader

from analyzer import analyze
from charts import generate_all_charts

def parse_args():
    parser = argparse.ArgumentParser(
        description="Generate an automatic EDA report from a CSV file."
    )
    parser.add_argument(
        "csv_path",
        type=str,
        help="Path to the CSV file"
    )
    parser.add_argument(
        "--output",
        type=str,
        default="report.html",
        help="Output HTML file name (default: report.html)"
    )
    parser.add_argument(
        "--sep",
        type=str,
        default=",",
        help="CSV separator (default: ',')"
    )
    return parser.parse_args()

def generate_report(csv_path: str, output: str, sep: str):
    print(f"📂 Loading {csv_path}...")
    df = pd.read_csv(csv_path, sep=sep)
    print(f"✅ Loaded — {df.shape[0]} rows × {df.shape[1]} columns")

    print("🔍 Analyzing dataset...")
    analysis = analyze(df)

    print("📊 Generating charts...")
    charts = generate_all_charts(df, analysis)

    print("🎨 Rendering template...")
    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template("template.html")

    html = template.render(
        filename=os.path.basename(csv_path),
        overview=analysis["overview"],
        nulls=analysis["nulls"],
        descriptive=analysis["descriptive"],
        skewness=analysis["skewness"],
        categorical=analysis["categorical"],
        charts=charts,
    )

    with open(output, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"✅ Report saved → {output}")
    print(f"   Open in browser: file://{os.path.abspath(output)}")


if __name__ == "__main__":
    args = parse_args()
    generate_report(args.csv_path, args.output, args.sep)
