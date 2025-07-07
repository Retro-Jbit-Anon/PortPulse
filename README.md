# 🚢 NCLH Cruise Ship Fuel Analytics Dashboard

A Streamlit-based interactive analytics dashboard that analyzes fuel consumption, warm-up efficiency, and operational delays for cruise ships under major subsidiaries such as Norwegian Cruise Line (NCL), Oceania Cruises, and Regent Seven Seas.

🔗 [Live Demo](https://w9qpkw2wrmvjhrshyp6i4p.streamlit.app/ )

---

## 🔍 Overview

This dashboard provides insights into:
- Engine warm-up efficiency across different ships and subsidiaries
- Fuel usage patterns and associated costs
- Financial impact of port congestion and inefficient warm-ups

All data used in this application is **synthetically generated** using Python libraries like `numpy` and `pandas`. The generation process simulates real-world conditions such as:
- Varying port traffic levels
- Randomized fuel usage and cost values
- Engine warm-up times and their deviation from optimal thresholds
- Sailing delays caused by busy ports
---

## 🧰 Features

- **Interactive Filters**: Narrow down analysis by subsidiary or specific ship.
- **Warm-Up Efficiency Analysis**: Visualize optimal vs non-optimal engine warm-up times.
- **Fuel Consumption Metrics**: Track total fuel used and wasted due to inefficiencies.
- **Financial Loss Calculation**: Estimate USD loss from unnecessary fuel burn.
- **Dynamic Data Grouping**: View aggregated metrics grouped by Ship, Subsidiary, or Port Country.
- **Raw Data Inspection**: Toggle visibility of full dataset breakdown.

---

## 🛠️ Technologies Used

- [Streamlit](https://streamlit.io ) – For building interactive web apps in Python
- [Pandas & NumPy](https://pandas.pydata.org/ ) – For data manipulation and analysis
- [Plotly Express](https://plotly.com/python/ ) – For interactive visualizations

---

## ▶️ How to Run Locally

### 1. Clone the repository:
```bash
git clone https://github.com/yourusername/your-repo-name.git 
cd your-repo-name
```
### 2. Install dependencies:
Make sure you have Python installed, then run:

```bash
pip install -r requirements.txt
```

### 3. Launch the App:

```bash
streamlit run main.py
```

---

## 📦 Requirements File (`requirements.txt`)

```nginx
streamlit
pandas
numpy
plotly
```

---

## 📊 Dataset Details

The synthetic dataset contains **150 sample entries** representing simulated trips made by cruise ships across various European ports. Each entry includes:

### Columns in the Dataset

| Column Name                   | Description |
|-------------------------------|-------------|
| `Subsidiary`                  | Cruise line brand (e.g., NCL, Oceania, Regent Seven Seas) |
| `Ship_Name`                   | Name of the ship |
| `Port_Country`                | Country where the port is located |
| `Port_Name`                   | Name of the port |
| `Port_Status`                 | "Busy" or "Normal" indicating current port congestion |
| `Fuel_Used_MetricTons`        | Amount of fuel used during operation |
| `Fuel_Cost_Per_Ton ($)`       | Cost of fuel per metric ton |
| `Engine_WarmUp_Time (mins)`   | Time taken to warm up engines before departure |
| `Optimal_WarmUp_Time (mins)`  | Set threshold for optimal warm-up time (15 mins) |
| `Sailing_Delay_Due_To_Port_Busy` | Indicates whether sailing was delayed due to port congestion |

> ✅ **Note**: This dataset is entirely **synthetically generated** using Python (`numpy`, `pandas`) and does **not rely on any external datasets**, making it fully reproducible and customizable.

### Additional Calculated Fields

- `WarmUp_Status`: Whether warm-up time was optimal or not  
- `Extra_Fuel_Wasted`: Estimated extra fuel burned due to suboptimal warm-up  
- `Financial_Loss_USD`: Calculated financial loss based on wasted fuel and fuel cost

---


## 🤝 Contributing

Contributions are welcome! If you'd like to enhance this dashboard with new features, improve the UI, or add real-world datasets, feel free to fork this repo and submit a pull request.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

## 📞 Contact

If you have any questions, feedback, or suggestions, feel free to reach out:

- 💼 GitHub Profile: [GitHub Link]( https://github.com/Retro-Jbit-Anon )
- 📧 Email: [Retro-Jbit-Anon](mailto:jidaarabbas@gmail.com)
