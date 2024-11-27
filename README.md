# CustomBrowser
CustomBrowser is a lightweight Python-based browser interface inspired by Postman and web browsers. It focuses on HTTP requests/responses, HTTP status codes, and includes a cache management system. With it, users can view and delete cached data for specific URLs, making it a great educational tool for learning about HTTP caching and headers.

## Features

- **Custom Request/Response Handling**: Inspect HTTP responses and understand status codes.
- **Cache Management**:
  - View cached content for specific URLs.
  - Clear cache for individual URLs or the entire application.
- **Educational Focus**: Learn how caching works and how HTTP headers like `If-Modified-Since` and `Last-Modified` interact with server responses.

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Ahmed-Jedidi/CustomBrowser.git
   cd CustomBrowser
---

## Usage

### **HTTP Request/Response Exploration:**
- Enter a URL to fetch its HTTP response.
- View status codes and headers in the interface.

### **Cache Management:**
- Use the "View Cache" button to inspect cached content for a specific URL.
- Use the "Clear Cache" button to delete cached data for a specific URL or all URLs.

---

## Screenshots

### Main Interface
![image](https://github.com/user-attachments/assets/3832eb8f-ca3e-484b-8f5d-36c8821e839d)

![image](https://github.com/user-attachments/assets/3230a4c3-7d6c-445a-be6a-08e872f1db07)

### Viewing Cookies Content
![image](https://github.com/user-attachments/assets/976db94e-cac4-4f68-bfba-7f37fb87d174)


---

## Development

### **Code Structure**
- `CustomBrowser.py`: Entry point of the application. It handles the graphical user interface using PyQt.
- `CacheManager.py`: Manages the caching system.
- `CookiesManager.py`: Manages the caching system.

### **Extending the Project**
Feel free to fork the project and add new features! Suggestions include:
- Support for custom HTTP methods like POST, PUT, DELETE.
- Advanced HTTP headers management.
- Persistent caching using a database or file storage.

---

## Contributing

We welcome contributions! Please fork the repository, make your changes, and submit a pull request.

---

## License

This project is licensed under the [MIT License](LICENSE). See the `LICENSE` file for details.

---

## Acknowledgments

- Inspired by tools like Postman and basic web browsers.
- Built with ❤️ using Python and PyQt.

---

## Contact

For questions or feedback, please open an issue on the GitHub repository.
```
