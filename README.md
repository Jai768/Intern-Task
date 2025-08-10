## Court Chosen
**Delhi High Court**  
Data extracted from: [https://delhihighcourt.nic.in/](https://delhihighcourt.nic.in/)

<img width="1919" height="913" alt="image" src="https://github.com/user-attachments/assets/72357d70-b60d-4ab2-9b1c-e6ecce51f505" />

<img width="1919" height="910" alt="image" src="https://github.com/user-attachments/assets/5eacae4c-d18a-46ee-8b64-9cf47caaa7c7" />

## Features ✨
- Real-time case data retrieval from Delhi High Court
- Comprehensive case metadata display
- Document links with download capability
- Responsive dashboard interface

## Tech Stack 🛠️
- **Backend**: Python (Flask), Selenium
- **Frontend**: HTML5, CSS3
- **Database**: SQLite
- **Containerization**: Docker

### Prerequisites
- Docker installed
- ChromeDriver compatible with your Docker Chrome version

# Setup Steps
1. Clone the repository:
   git clone https://github.com/Jai768/Intern-Task.git
   cd Intern-Task
   
2. Build the Docker Image:
   docker build -t intern-task-1 .
   
3. Run the container:
   docker run -p 5000:5000 intern-task-1
   
4. Open in Browser:
   http://127.0.0.1:5000
   
# Captcha Strategy
The system automatically handles CAPTCHA by:

1. Locating the CAPTCHA text element using XPATH

2. Extracting the displayed text

3. Entering it into the verification field

# Error Handling 
The system detects and handles:
-**Invalid case numbers**
-**Website downtime (DNS, TCP, HTTP, Selenium levels)**
-**CAPTCHA failures**
-**Network issues**

