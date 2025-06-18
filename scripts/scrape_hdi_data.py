import os
import csv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait

# ---------------------------------------
# 📊 Extract HDI values from UNDP chart
# ---------------------------------------

options = Options()
# options.add_argument("--headless=new")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

print("🚀 Launching browser...")
driver = webdriver.Chrome(options=options)

try:
    print("🌐 Loading HDI page...")
    driver.get("https://hdr.undp.org/data-center/human-development-index#/indicies/HDI")

    print("⌛ Waiting for chart data...")
    WebDriverWait(driver, 30).until(
        lambda d: d.execute_script("return typeof Highcharts !== 'undefined' && Highcharts.charts.length > 0")
    )

    print("📥 Extracting HDI data...")
    script = """
        const chart = Highcharts.charts[0];
        const result = [];
        chart.series.forEach(s => {
            const country = s.name;
            if (!country) return;
            s.data.forEach(point => {
                if (point.y !== null) {
                    result.push({
                        country: country,
                        year: point.x,
                        hdi: point.y
                    });
                }
            });
        });
        return result;
    """
    data = driver.execute_script(script)

    if not data:
        raise ValueError("⚠️ No HDI data extracted.")

    output_path = os.path.join("data", "external", "hdi_historical.csv")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["country", "year", "hdi"])
        writer.writeheader()
        writer.writerows(data)

    print(f"✅ HDI data saved to: {output_path}")

finally:
    driver.quit()