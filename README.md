# Court Chosen
I extracted data from the Delhi High Court Website (https://delhihighcourt.nic.in/) to display them according to the chosen case type and number.

<img width="1919" height="913" alt="image" src="https://github.com/user-attachments/assets/72357d70-b60d-4ab2-9b1c-e6ecce51f505" />

<img width="1919" height="910" alt="image" src="https://github.com/user-attachments/assets/5eacae4c-d18a-46ee-8b64-9cf47caaa7c7" />

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
I simply scraped the Captcha using its XPATH and sent the keys to its input button to bypass it.

# Error Handling 
The system detects and handles:
Invalid case numbers
Website downtime (DNS, TCP, HTTP, Selenium levels)
CAPTCHA failures
Network issues

