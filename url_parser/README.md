# 🔗 URL Parser & Status Checker

A Streamlit web application that parses URLs into their components and checks their HTTP status. The app provides an interactive interface to analyze, edit, and test URLs with real-time status checking.

## ✨ Features

### URL Parsing
- **Component Breakdown**: Breaks down URLs into 6 key components:
  - **Scheme**: Protocol (http, https, ftp, etc.)
  - **Netloc**: Network location (domain, port, credentials)
  - **Path**: URL path
  - **Params**: URL parameters
  - **Query**: Query string parameters
  - **Fragment**: URL fragment (hash)

### Interactive Editing
- **Editable Table**: Modify URL components in real-time
- **Live Reconstruction**: See the reconstructed URL as you edit
- **Test Functionality**: Test the modified URL to verify it works

### Status Checking
- **HTTP Status**: Get status codes and response details
- **Content Analysis**: View content type and size
- **Redirect Tracking**: See if URLs redirect and where they end up
- **Error Handling**: Graceful handling of timeouts and connection errors

### User Experience
- **Modern UI**: Clean, responsive design with emojis and intuitive layout
- **Session State**: Preserves data between interactions
- **Real-time Feedback**: Loading spinners and success/error messages
- **Help Documentation**: Built-in instructions and usage guide

## 🚀 Quick Start

### Prerequisites
- Python 3.7 or higher
- pip package manager

### Installation

1. **Clone or download the project**
   ```bash
   git clone <repository-url>
   cd url_parser
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   streamlit run app.py
   ```

4. **Open your browser**
   - The app will automatically open at `http://localhost:8501`
   - If it doesn't open automatically, navigate to the URL shown in your terminal

## 📖 How to Use

### Parse Button (🔍)
1. Enter a URL in the text input field
2. Click the **Parse** button
3. View the URL components in the editable table
4. Edit any component values as needed
5. See the reconstructed URL update in real-time

### Go Button (🚀)
1. Enter a URL in the text input field
2. Click the **Go** button
3. View the HTTP status information including:
   - Status code and text
   - Content type and size
   - Whether the URL was redirected
   - Final URL after redirects

### Advanced Features
- **Test Reconstructed URL**: After editing URL components, test the new URL
- **Error Handling**: The app gracefully handles various error conditions
- **Responsive Design**: Works on desktop, tablet, and mobile devices

## 🛠️ Technical Details

### Dependencies
- **Streamlit** (≥1.28.0): Web application framework
- **Pandas** (≥2.0.0): Data manipulation and table editing
- **Requests** (≥2.31.0): HTTP library for status checking

### Architecture
- **Frontend**: Streamlit web interface
- **Backend**: Python functions for URL parsing and HTTP requests
- **State Management**: Streamlit session state for data persistence

### Key Functions
- `parse_url()`: Breaks down URLs into components using `urllib.parse`
- `check_url_status()`: Performs HTTP requests with error handling
- `reconstruct_url()`: Rebuilds URLs from modified components

## 🔧 Configuration

### Timeout Settings
The app uses a 10-second timeout for HTTP requests. To modify this, edit the `timeout` parameter in the `check_url_status()` function:

```python
response = requests.get(url, timeout=10, allow_redirects=True)
```

### Error Handling
The app handles several types of errors:
- **Timeout**: Requests that take too long
- **Connection Error**: Network connectivity issues
- **Request Exception**: Other HTTP-related errors
- **URL Parse Error**: Malformed URLs

## 📁 Project Structure

```
url_parser/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── README.md          # This documentation
└── repos.code-workspace # VS Code workspace file
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 🐛 Troubleshooting

### Common Issues

**App won't start:**
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Check Python version compatibility (3.7+)

**URL parsing errors:**
- Make sure URLs include the protocol (http:// or https://)
- Check for special characters that might need encoding

**Status check failures:**
- Verify internet connectivity
- Some URLs might be blocked by firewalls or require authentication
- Check if the target server is responding

**Port already in use:**
- Streamlit defaults to port 8501
- Use `streamlit run app.py --server.port 8502` to use a different port

## 🔮 Future Enhancements

- [ ] URL validation and sanitization
- [ ] Batch URL processing
- [ ] Export functionality for parsed data
- [ ] URL shortening integration
- [ ] Historical URL analysis
- [ ] API endpoint for programmatic access
- [ ] Custom timeout settings in UI
- [ ] URL component validation

## 📞 Support

If you encounter any issues or have questions:
1. Check the troubleshooting section above
2. Review the built-in help in the app
3. Open an issue on the project repository
4. Check Streamlit documentation for framework-specific questions

---

**Happy URL parsing! 🔗✨**
