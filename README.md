<div align="center">

# 🔮 GitHub Activity Analyzer

<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=28&duration=4000&pause=1000&color=58A6FF&center=true&vCenter=true&random=false&width=600&lines=Analyze+Any+GitHub+Profile+%F0%9F%94%8D;Visualize+Coding+Patterns+%F0%9F%93%8A;Track+Your+Progress+%F0%9F%9A%80;Discover+Insights+%F0%9F%92%A1" alt="Typing SVG" />

<br/>

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![GitHub API](https://img.shields.io/badge/GitHub-API-181717?style=for-the-badge&logo=github&logoColor=white)](https://docs.github.com/en/rest)
[![Matplotlib](https://img.shields.io/badge/Matplotlib-Visualizations-11557c?style=for-the-badge&logo=plotly&logoColor=white)](https://matplotlib.org/)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

<br/>

<img src="https://user-images.githubusercontent.com/74038190/212284100-561aa473-3905-4a80-b561-0d28506553ee.gif" width="700">

**🚀 A powerful Python tool that dives deep into any GitHub profile and reveals fascinating insights about coding habits, language preferences, and activity patterns.**

[Features](#-features) •
[Installation](#-installation) •
[Usage](#-usage) •
[Architecture](#-architecture) •
[Contributing](#-contributing)

<br/>

<img src="https://user-images.githubusercontent.com/74038190/212284115-f47cd8ff-2ffb-4b04-b5bf-4d1c14c0247f.gif" width="400">

</div>

---

## ✨ Features

<img align="right" src="https://user-images.githubusercontent.com/74038190/229223263-cf2e4b07-2615-4f87-9c38-e37600f8381a.gif" width="300">

### 📊 **Comprehensive Analysis**
- 🔍 Fetch **ALL** repositories (pagination support!)
- 📈 Language distribution breakdown
- ⭐ Top repositories by stars
- 📅 Monthly activity tracking
- 🚀 Recent activity (last 30 days)

### 💬 **Commit Intelligence**
- 🔤 Commit message word analysis
- 📊 Average commits per repository
- ⏰ Peak coding hours detection
- 🗓️ Day-of-week patterns

### 🎨 **Beautiful Visualizations**
- 📺 Terminal-based ASCII charts
- 🖼️ High-quality PNG/PDF exports
- 📊 Pie charts, bar graphs, histograms
- 🌈 Color-coded data representation

### 💾 **Smart Caching**
- 🧠 User-specific cache files
- ⚡ Lightning-fast repeated analysis
- 🔄 Automatic cache invalidation
- 📈 Progress tracking between sessions

<br clear="right"/>

---

## 🎬 Demo

<div align="center">

```
============================================================
                 📊 GITHUB ACTIVITY ANALYSIS                 
============================================================

📂 REPOSITORY OVERVIEW
------------------------------------------------------------
Total Repos : 47
Most Used Programming Language : Python

⭐ TOP REPOSITORIES
------------------------------------------------------------
1. awesome-project - ⭐142 stars
2. ml-toolkit - ⭐89 stars
3. api-framework - ⭐67 stars

📈 LANGUAGE BREAKDOWN
------------------------------------------------------------
🐍 Python        ████████████████████████████ 58%
📘 TypeScript    ████████████ 24%
☕ JavaScript    ██████ 12%
🦀 Rust          ███ 6%

⏰ PEAK ACTIVITY TIME
------------------------------------------------------------
Most Active Hour: 14:00 PM 🔥
```

</div>

---

## 🚀 Installation

<img align="right" src="https://user-images.githubusercontent.com/74038190/212257472-08e52665-c503-4bd9-aa20-f5a4dae769b5.gif" width="100">

### Prerequisites

```bash
# Python 3.8 or higher required
python --version
```

### Quick Start

```bash
# Clone the repository
git clone https://github.com/AnandVadgama/GitHub-Activity-Analyzer.git

# Navigate to project directory
cd GitHub-Activity-Analyzer

# Install dependencies
pip install -r requirements.txt

# Run the analyzer! 🎉
python main.py
```

### Dependencies

```
requests>=2.28.0
matplotlib>=3.5.0
```

---

## 💻 Usage

<div align="center">

<img src="https://user-images.githubusercontent.com/74038190/213910845-af37a709-8995-40d6-be59-724526e3c3d7.gif" width="600">

</div>

### Basic Usage

```bash
python main.py
```

```
Enter the username to analyze: torvalds
🔍 Fetching repositories for torvalds...
📄 Fetching page 1...
✅ Got 11 repositories from page 1
🎉 Total repositories fetched: 11
```

### Output Files

| File | Description |
|------|-------------|
| `📁 output/` | JSON analysis exports with timestamps |
| `📁 charts/` | PNG & PDF visualization files |
| `📄 commit_message_{user}.json` | User-specific commit cache |

---

## 🏗️ Architecture

<div align="center">

```mermaid
graph TD
    A[🎯 main.py] --> B[🌐 github_api.py]
    A --> C[📊 data_analyzer.py]
    A --> D[💾 file_handler.py]
    A --> E[🔧 utils.py]
    A --> F[🎨 visualizations.py]
    
    B --> |API Calls| G[(GitHub API)]
    D --> |Cache| H[(JSON Files)]
    F --> |Export| I[(Charts)]
    
    style A fill:#58A6FF,color:#fff
    style B fill:#238636,color:#fff
    style C fill:#8957E5,color:#fff
    style D fill:#F78166,color:#fff
    style E fill:#3FB950,color:#fff
    style F fill:#DB61A2,color:#fff
```

</div>

### 📁 Project Structure

```
📦 GitHub-Activity-Analyzer
├── 🎯 main.py              # Main entry point & orchestration
├── 🌐 github_api.py        # GitHub API interactions (with pagination!)
├── 📊 data_analyzer.py     # Data processing & analysis
├── 💾 file_handler.py      # File I/O & caching logic
├── 🔧 utils.py             # Utility functions
├── 🎨 visualizations.py    # Charts & visual output
├── 📁 output/              # Generated analysis JSON files
├── 📁 charts/              # Generated visualization images
└── 📄 README.md            # You are here! 👋
```

### 🧩 Module Responsibilities

| Module | Purpose |
|--------|---------|
| `main.py` | Entry point, orchestrates the analysis workflow |
| `github_api.py` | Handles all GitHub API calls with pagination & error handling |
| `data_analyzer.py` | Processes raw data into meaningful insights |
| `file_handler.py` | Manages JSON exports and smart caching |
| `utils.py` | Utility functions for calculations |
| `visualizations.py` | Creates terminal & image-based visualizations |

---

## 📊 What Gets Analyzed?

<div align="center">

| Metric | Description | Visualization |
|--------|-------------|---------------|
| 🔤 **Languages** | Distribution across all repos | Pie Chart |
| 📅 **Monthly Activity** | Repository creation patterns | Bar Chart |
| ⏰ **Commit Hours** | When you code most | Histogram |
| ⭐ **Top Repos** | Highest starred repositories | Horizontal Bar |
| 🔍 **Commit Words** | Common words in messages | Word Analysis |
| 📈 **Growth** | Progress between analyses | Comparison |

</div>

---

## 🛠️ Technical Highlights

<img align="right" src="https://user-images.githubusercontent.com/74038190/212284087-bbe7e430-757e-4901-90bf-4cd2ce3e1852.gif" width="200">

- **🔄 Pagination Support**: Fetches ALL repositories, not just 30!
- **🧠 Smart Caching**: User-specific cache with automatic invalidation
- **⚡ Efficient**: Minimal API calls with intelligent data reuse
- **🛡️ Robust Error Handling**: Graceful recovery from API issues
- **📊 Dual Visualization**: Both terminal ASCII and high-res images
- **🏗️ Modular Design**: Clean, maintainable code structure

---

## 🤝 Contributing

<div align="center">

<img src="https://user-images.githubusercontent.com/74038190/216120981-b9507c36-0e04-4469-8e27-c99271b45ba5.png" width="200">

</div>

Contributions are welcome! Here's how you can help:

1. 🍴 **Fork** the repository
2. 🌿 **Create** a feature branch (`git checkout -b feature/AmazingFeature`)
3. 💾 **Commit** your changes (`git commit -m 'Add AmazingFeature'`)
4. 📤 **Push** to the branch (`git push origin feature/AmazingFeature`)
5. 🎉 **Open** a Pull Request

---

## 📜 License

<div align="center">

Distributed under the **MIT License**. See `LICENSE` for more information.

<br/>

<img src="https://user-images.githubusercontent.com/74038190/212284158-e840e285-664b-44d7-b79b-e264b5e54825.gif" width="400">

---

### 💖 Made with Python and Passion

<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=500&size=18&duration=3000&pause=1000&color=58A6FF&center=true&vCenter=true&random=false&width=435&lines=Happy+Analyzing!+%F0%9F%9A%80;Star+%E2%AD%90+if+you+find+it+useful!" alt="Typing SVG" />

<br/>

[![GitHub stars](https://img.shields.io/github/stars/AnandVadgama/GitHub-Activity-Analyzer?style=social)](https://github.com/AnandVadgama/GitHub-Activity-Analyzer/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/AnandVadgama/GitHub-Activity-Analyzer?style=social)](https://github.com/AnandVadgama/GitHub-Activity-Analyzer/network/members)

</div>
