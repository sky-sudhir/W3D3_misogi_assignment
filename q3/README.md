# AI Coding Agent Recommendation System

A web application that helps developers find the best AI coding assistant for their specific programming tasks by analyzing task requirements and matching them with the most suitable AI coding agents.

## Features

- **Smart Task Analysis**: Uses Google's Gemini 2.0 Flash model to understand programming tasks
- **Agent Matching**: Recommends the top 3 AI coding assistants based on task requirements
- **Detailed Explanations**: Provides clear reasoning for each recommendation
- **Multiple Agent Support**: Includes popular coding assistants like GitHub Copilot, Cursor, Replit AI, and more
- **Responsive Design**: Works on both desktop and mobile devices

## Tech Stack

### Frontend
- Next.js 14 (App Router)
- TypeScript
- Tailwind CSS
- shadcn/ui

### Backend
- FastAPI
- Google's Gemini 2.0 Flash model
- Python 3.8+

## Getting Started

### Prerequisites

- Node.js 18+ and npm/yarn/pnpm
- Python 3.8+
- Google API key with access to Gemini API

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   # On Windows:
   .\venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the backend directory with your Google API key:
   ```
   GOOGLE_API_KEY=your_api_key_here
   ```

5. Start the backend server:
   ```bash
   uvicorn main:app --reload --port 8000
   ```

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```

4. Open [http://localhost:3000](http://localhost:3000) in your browser

## How to Use

1. Enter a description of your coding task in the text area
2. (Optional) Specify the programming language
3. Select the task complexity (Low, Medium, High)
4. Click "Get Recommendations"
5. View the top 3 recommended AI coding assistants with detailed explanations

## Example Prompts

- "Build a responsive e-commerce website with React and Node.js"
- "Analyze sales data to find trends and create visualizations"
- "I'm learning Python and want to build a simple calculator"
- "Fix memory leaks in my React application"
- "Implement Dijkstra's algorithm for shortest path finding"

## API Endpoints

### POST /recommend

Recommends AI coding agents based on task requirements.

**Request:**
```json
{
  "description": "Build a REST API with user authentication",
  "language": "Python",
  "complexity": "medium"
}
```

**Response:**
```json
[
  {
    "id": "copilot",
    "name": "GitHub Copilot",
    "score": 8.7,
    "explanation": "Recommended because it supports Python, excels at general coding, and offers code completion.",
    "analysis": {
      "task_type": "api_development",
      "required_skills": ["Python", "API Design", "Authentication"],
      "recommended_features": ["code completion", "documentation"]
    }
  }
  // ... more recommendations
]
```

## Project Structure

```
.
├── backend/               # FastAPI backend
│   ├── main.py           # Main application file
│   ├── agentdb.json      # Database of AI coding agents
│   ├── requirements.txt  # Python dependencies
│   └── .env             # Environment variables
├── frontend/             # Next.js frontend
│   ├── src/
│   │   ├── app/         # Next.js app directory
│   │   └── components/   # React components
│   ├── public/           # Static files
│   └── package.json      # Node.js dependencies
└── README.md             # This file
```

## Contributing

1. Fork the repository
2. Create a new branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Google Gemini API](https://ai.google.dev/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Next.js](https://nextjs.org/)
- [shadcn/ui](https://ui.shadcn.com/)