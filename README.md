# Mediscope AI

Mediscope AI is a Streamlit application designed to assist healthcare professionals in predicting various diseases using advanced machine learning models. The application provides a user-friendly interface for disease prediction, including heart attack, breast cancer, diabetes, and lung cancer.

## Project Structure

```
mediscope-ai
├── src
│   ├── app.py                  # Main entry point for the Streamlit application
│   ├── models
│   │   └── __init__.py         # Initializes the models package
│   ├── components
│   │   ├── home.py              # Home page of the application
│   │   ├── auth.py              # User authentication functionality
│   │   └── disease_pages
│   │       ├── heart_attack.py   # Heart attack prediction page
│   │       ├── breast_cancer.py   # Breast cancer prediction page
│   │       ├── diabetes.py        # Diabetes prediction page
│   │       └── lung_cancer.py     # Lung cancer prediction page
│   ├── utils
│   │   ├── __init__.py          # Initializes the utils package
│   │   ├── constants.py         # Constant values used in the application
│   │   └── helpers.py           # Helper functions for various tasks
│   └── styles
│       └── styles.css           # Custom CSS styles for the application
├── requirements.txt             # Python dependencies for the project
├── config.toml                  # Configuration settings for the application
└── README.md                    # Documentation for the project
```

## Installation

To run the Mediscope AI application, follow these steps:

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd mediscope-ai
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the Streamlit application:
   ```bash
   streamlit run src/app.py
   ```

## Usage

- Upon launching the application, users will be greeted with a home page that provides navigation options.
- Users can log in or create an account to access the disease prediction features.
- The application includes separate pages for predicting heart attack, breast cancer, diabetes, and lung cancer, where users can input relevant features and view prediction results.

## Contributing

Contributions are welcome! If you have suggestions for improvements or new features, please open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.