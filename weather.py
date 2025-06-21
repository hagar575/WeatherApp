import sys
import requests
from PyQt5.QtWidgets import QApplication, QPushButton, QVBoxLayout, QWidget, QLabel, QLineEdit
from PyQt5.QtCore import Qt

class WeatherApp(QWidget): # Inherits from QWidget to create a window
    def __init__(self): 
        super().__init__()
        self.city_label = QLabel("Enter City:", self) # QLabel to display text
        self.city_input = QLineEdit(self) # QLineEdit for user input
        self.get_weather_button = QPushButton("Get Weather", self) # QPushButton to trigger weather retrieval
        self.tempearature_label = QLabel(self) # QLabel to display temperature
        self.emoji_label = QLabel(self) # QLabel to display weather emoji
        self.description_label = QLabel(self) # QLabel to display weather description
        self.initUI() # Initialize the user interface

    def initUI(self):
        self.setWindowTitle("Weather App") # Set the window title

        vbox = QVBoxLayout() # Create a vertical box layout to arrange widgets vertically

        vbox.addWidget(self.city_label) # Add city label to the layout
        vbox.addWidget(self.city_input) # Add city input field to the layout
        vbox.addWidget(self.get_weather_button) # Add button to get weather
        vbox.addWidget(self.tempearature_label) # Add temperature label to the layout
        vbox.addWidget(self.emoji_label) # Add emoji label to the layout
        vbox.addWidget(self.description_label) # Add description label to the layout

        self.setLayout(vbox) # Set the layout for the main window

        # Set the alignment for the labels and input field

        self.city_label.setAlignment(Qt.AlignCenter) 
        self.city_input.setAlignment(Qt.AlignCenter)
        self.tempearature_label.setAlignment(Qt.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignCenter)
        self.description_label.setAlignment(Qt.AlignCenter)

        # Set object names for styling
        self.city_label.setObjectName("cityLabel")
        self.city_input.setObjectName("cityInput")
        self.get_weather_button.setObjectName("getWeatherButton")
        self.tempearature_label.setObjectName("temperatureLabel")
        self.emoji_label.setObjectName("emojiLabel")
        self.description_label.setObjectName("descriptionLabel")

        # Set the stylesheet for the application
        self.setStyleSheet("""
            QLabel, QpushButton{
                font-family: Arial, sans-serif;
            }
            QLabel#cityLabel {
                font-size: 24px;
                font-weight: bold;
            }
            QLineEdit#cityInput {
                font-size: 18px;
            }
            QPushButton#getWeatherButton {
                font-size: 18px;
            }
            QLabel#temperatureLabel {
                font-size: 32px;
                font-weight: bold;
            }
            QLabel#emojiLabel {
                font-size: 100px;
                font-family: Segoe UI emoji;
            }
            QLabel#descriptionLabel {
                font-size: 24px;
            }

        """)

        self.get_weather_button.clicked.connect(self.get_weather)
                            
    def get_weather(self):
        api_key = "b9dba60a1caf90af48ad466ca6139298" # Replace with your actual API key
        city = self.city_input.text().strip() # Get the city name from the input field
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}" # Construct the API URL with the city name and API key

        try: 
            response = requests.get(url)
            response.raise_for_status()  # Raise an error for bad responses
            data = response.json()

            # Check if the response contains valid weather data
            if data["cod"] == 200:
                self.display_weather(data)

        # Handle HTTP errors
        except requests.exceptions.HTTPError as http_error:
            match response.status_code:
                case 400:
                    self.display_error("Bad Request: Please check the city name.")
                case 401:
                    self.display_error("Unauthorized: Please check your API key.")
                case 403:
                    self.display_error("Forbidden: Access denied. Please check your API key.")
                case 404:
                    self.display_error("City not found. Please try another city.")
                case 500:
                    self.display_error("Internal Server Error. Please try again later.")
                case 502:
                    self.display_error("Bad Gateway. Please try again later.")
                case 503:
                    self.display_error("Service Unavailable. Please try again later.")
                case 504:
                    self.display_error("Gateway Timeout. Please try again later.")
                case _:
                    self.display_error(f"HTTP error occured. {http_error}")

        except requests.exceptions.ConnectionError:
            self.display_error("Connection Error: Please check your internet connection.")

        except requests.exceptions.Timeout:
            self.display_error("Timeout Error: The request took too long to complete.")

        except requests.exceptions.TooManyRedirects:
            self.display_error("Too Many Redirects: The URL may be incorrect.")

        except requests.exceptions.RequestException as req_error:
            self.display_error(f"An error occurred: {req_error}")

        except requests.exceptions.RequestException:
            pass

    # Display error message in place of the temperature label
    def display_error(self, message):
        self.tempearature_label.setStyleSheet("font-size: 24px;")
        self.tempearature_label.setText(message)
        self.emoji_label.clear()
        self.description_label.clear()

    # Display weather data in the respective labels
    def display_weather(self,data):
        self.tempearature_label.setStyleSheet("font-size: 24px;")
        temperature_k = data["main"]["temp"]  # Temperature in Kelvin
        temperature_c = temperature_k - 273.15 # Convert Kelvin to Celsius
        temperature_f = (temperature_c * 9/5) + 32 # Convert Celsius to Fahrenheit

        weather_id = data["weather"][0]["id"] # Weather condition ID

        weather_description = data["weather"][0]["description"] # Get weather description
        
        self.tempearature_label.setText(f"Temperature: {temperature_c:.0f} °C / {temperature_f:.0f} °F") # Display temperature in Celsius and Fahrenheit
        self.emoji_label.setText(self.get_weather_emoji(weather_id)) # Get and display the weather emoji based on the weather ID
        self.description_label.setText(weather_description) # Display weather description

    # Get the appropriate weather emoji based on the weather condition ID
    @staticmethod 
    def get_weather_emoji(weather_id):
        if 200 <= weather_id <= 232:
            return "⛈️"
        elif 300 <= weather_id <= 321:
            return "🌦️"
        elif 500 <= weather_id <= 531:
            return "🌧️"
        elif 600 <= weather_id <= 622:
            return "❄️"
        elif 701 <= weather_id <= 781:
            return "🌫️"
        elif weather_id == 762:
            return "🌋"
        elif weather_id == 771:
            return "💨"
        elif weather_id == 781:
            return "🌪️"
        elif weather_id == 800:
            return "☀️"
        elif 801 <= weather_id <= 804:
            return "☁️"
        else:
            return " "

if __name__ == "__main__":
    app = QApplication(sys.argv)
    weather_app = WeatherApp()
    weather_app.show()
    sys.exit(app.exec_())