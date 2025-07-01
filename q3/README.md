# Adaptive Prompt Optimizer

A sophisticated web application that optimizes prompts for specific AI coding tools using Google Gemini AI for intelligent analysis and optimization.

## Features

- **Multi-Tool Support**: Supports 7+ AI coding tools including:

  - GitHub Copilot
  - Cursor AI
  - Replit AI
  - Amazon CodeWhisperer
  - Tabnine
  - Sourcegraph Cody
  - Claude (Anthropic)

- **Intelligent Analysis**: Uses Google Gemini AI to analyze prompt intent, complexity, and requirements

- **Tool-Specific Optimization**: Generates optimized prompts based on each tool's strengths and best practices

- **Beautiful Web Interface**: Modern, responsive UI with glassmorphism design

- **Before/After Comparison**: Clear display of original vs optimized prompts with detailed explanations

- **Copy to Clipboard**: Easy copying of optimized prompts for immediate use

## Installation

1. **Clone the repository**:

   ```bash
   git clone <repository-url>
   cd adaptive-prompt-optimizer
   ```

2. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Set up Google Gemini API**:

   - Get your API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Set the environment variable:

     ```bash
     # Windows
     set GEMINI_API_KEY=your_api_key_here

     # Linux/Mac
     export GEMINI_API_KEY=your_api_key_here
     ```

   Or create a `.env` file:

   ```env
   GEMINI_API_KEY=your_api_key_here
   ```

## Usage

1. **Start the application**:

   ```bash
   python app.py
   ```

2. **Open your browser** and navigate to `http://localhost:8000`

3. **Enter your prompt** in the text area

4. **Select your target AI tool** from the dropdown

5. **Click "Optimize Prompt"** to get your optimized version

6. **Review the results**:
   - Compare original vs optimized prompts
   - Read the detailed analysis
   - See what optimizations were applied
   - Copy the optimized prompt to use in your chosen AI tool

## API Endpoints

### `GET /`

Returns the main web interface

### `POST /api/optimize`

Optimizes a prompt for a specific tool

**Request Body**:

```json
{
  "prompt": "Your original prompt here",
  "tool": "copilot"
}
```

**Response**:

```json
{
  "original_prompt": "Your original prompt here",
  "optimized_prompt": "The optimized version",
  "tool": "GitHub Copilot",
  "analysis": {
    "primary_intent": "code_generation",
    "complexity_level": 3,
    "key_requirements": ["..."],
    "missing_context": ["..."],
    "technical_domains": ["..."]
  },
  "optimizations_made": ["..."],
  "timestamp": "2024-01-01T12:00:00"
}
```

### `GET /api/tools`

Returns information about all supported tools

## Supported Tools

| Tool                 | Strengths                                                   | Best Practices                                          |
| -------------------- | ----------------------------------------------------------- | ------------------------------------------------------- |
| GitHub Copilot       | Code completion, Function generation, Bug fixes             | Use descriptive names, Add type hints, Be specific      |
| Cursor AI            | Code editing, Refactoring, Multi-file operations            | Describe current/desired state, Be explicit about files |
| Replit AI            | Full-stack development, Interactive coding, Deployment      | Specify language, Mention deployment needs              |
| Amazon CodeWhisperer | AWS integration, Security-focused code, Enterprise patterns | Mention AWS services, Include security considerations   |
| Tabnine              | Code completion, Pattern recognition, Team consistency      | Use consistent naming, Provide team context             |
| Sourcegraph Cody     | Code search, Large codebase navigation, Code understanding  | Reference specific files, Use precise terminology       |
| Claude (Anthropic)   | Code analysis, Architecture design, Complex reasoning       | Provide comprehensive context, Ask for explanations     |

## Project Structure

```
adaptive-prompt-optimizer/
├── app.py                 # Main FastAPI application
├── requirements.txt       # Python dependencies
├── templates/
│   └── index.html        # Main web interface
├── static/               # Static files (CSS, JS, images)
└── README.md            # This file
```

## Technology Stack

- **Backend**: FastAPI, Python 3.8+
- **AI Integration**: Google Gemini AI API
- **Frontend**: HTML5, Tailwind CSS, Vanilla JavaScript
- **Server**: Uvicorn ASGI server

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Troubleshooting

### Common Issues

1. **API Key Error**: Make sure your `GEMINI_API_KEY` is set correctly
2. **Import Errors**: Ensure all dependencies are installed with `pip install -r requirements.txt`
3. **Port Already in Use**: Change the port in `app.py` or kill the process using the port

### Getting Help

- Check the console output for error messages
- Ensure your internet connection is stable (required for Gemini AI API)
- Verify your API key has sufficient quota

## Future Enhancements

- [ ] Add more AI coding tools
- [ ] Implement prompt history and favorites
- [ ] Add bulk optimization for multiple prompts
- [ ] Create browser extension for quick optimization
- [ ] Add prompt templates for common use cases
- [ ] Implement user accounts and saved preferences
