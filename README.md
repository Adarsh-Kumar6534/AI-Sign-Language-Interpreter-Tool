# AI-Powered Deadlock Detection System

## Project Overview
Welcome to the **AI-Powered Deadlock Detection System**, an innovative tool designed to detect, analyze, and resolve deadlocks in process management systems with an intuitive GUI and advanced AI integration. This project was developed to enhance operating system efficiency by providing real-time deadlock detection and visualization, making it a valuable asset for students, researchers, and professionals in computer science.

## Features
- **Dynamic Deadlock Detection**: Identifies deadlock conditions (Circular Wait, Mutual Exclusion, No Preemption) using a customizable process dependency matrix.
- **Interactive Visualization**: Offers multiple 3D graph types (Bar Plot, Scatter Plot, Surface Plot, Circular Layout) to visualize dependencies with clickable bars for detailed insights.
- **Simulation Mode**: Simulates deadlock scenarios with recovery options (Preemption, Random Kill, Resource Timeout) and AI-driven suggestions using the Gemini API.
- **Banker's Algorithm**: Implements the Banker's Algorithm for safe state analysis with configurable resource allocation.
- **AI Prediction**: Predicts potential deadlocks based on user scenarios and historical data, leveraging machine learning clustering.
- **Export Capabilities**: Export dependency graphs as PNG and tables as CSV for reporting and analysis.

## Technologies Used
- **Python**: Core programming language (Version 3.13.1 recommended).
- **PyQt6**: For building the modern, responsive GUI.
- **NetworkX**: For graph-based deadlock analysis and visualization.
- **NumPy**: For numerical computations and matrix operations.
- **Matplotlib**: For creating interactive 3D charts and plots.
- **Requests**: For API calls to the Gemini model.
- **Scikit-learn**: For ML-based deadlock pattern recognition.

## Installation
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Adarsh-Kumar6534/AI-Powered-Deadlock-Detection-System.git
   cd AI-Powered-Deadlock-Detection-System
   ```
2. **Install Dependencies**: Ensure you have Python 3.13.1 installed. Then, install the required packages:
   ```bash
   pip install -r requirements.txt
   ```
3. **Set Up Gemini API Key**:
   - Obtain an API key from Google Gemini.
   - Set it as an environment variable: `export GEMINI_API_KEY='your_api_key_here'`.
4. **Run the Application**:
   ```bash
   python main.py
   ```

## Usage
- **Deadlock Detection Tab**: Input process dependencies (1 for wait, 0 for no wait) in the table and click "Detect Deadlock" to analyze.
- **Dependency Visualization Tab**: Choose a graph type to visualize dependencies and rotate the view for better insight.
- **Simulation Mode Tab**: Start a simulation with selected or AI-recommended recovery methods to resolve deadlocks dynamically.
- **AI Prediction Tab**: Enter a scenario to get AI-based predictions and prevention strategies.

## Contributing Guidelines
We welcome contributions to enhance this tool! Please follow these steps:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -m "Add new feature"`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a Pull Request with a clear description of your changes.

## Contributors
- **Adarsh Kumar** - Project Lead & Developer ([Adarsh-Kumar6534](https://github.com/Adarsh-Kumar6534)) - adarshsingh6534@gmail.com
- **Anurag Anand Jha** 
- **Sukhpreet Kaur** 

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Screenshots
(Insert screenshots of the GUI tabs here to showcase the tool's interface and functionality.)

## Contact
For inquiries, collaboration, or patent-related discussions, please reach out to Adarsh Kumar at adarshsingh6534@gmail.com.

## Future Scope
- Integrate real-time process monitoring from operating systems.
- Expand AI capabilities with deeper learning models for predictive analytics.
- Add support for multi-threading deadlock detection.

```
