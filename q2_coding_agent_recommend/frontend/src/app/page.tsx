"use client";

import { useState } from 'react';

type TaskRequest = {
  description: string;
  language: string;
  complexity: string;
};

type AgentRecommendation = {
  id: string;
  name: string;
  score: number;
  explanation: string;
  analysis?: {
    required_skills?: string[];
    task_type?: string;
    recommended_features?: string[];
  };
};

export default function Home() {
  const [description, setDescription] = useState('');
  const [language, setLanguage] = useState('');
  const [complexity, setComplexity] = useState('medium');
  const [isLoading, setIsLoading] = useState(false);
  const [recommendations, setRecommendations] = useState<AgentRecommendation[]>([]);
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!description.trim()) {
      setError('Please enter a task description');
      return;
    }

    setIsLoading(true);
    setError('');

    try {
      const taskRequest: TaskRequest = {
        description,
        language,
        complexity,
      };

      const response = await fetch('http://localhost:8000/recommend', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(taskRequest),
      });

      if (!response.ok) {
        throw new Error('Failed to get recommendations');
      }

      const data = await response.json();
      setRecommendations(data);
    } catch (err) {
      setError('An error occurred while fetching recommendations');
      console.error('Error:', err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-3xl mx-auto">
        <div className="text-center mb-12">
          <h1 className="text-4xl font-extrabold text-gray-900 mb-4">
            AI Coding Agent Recommender
          </h1>
          <p className="text-xl text-gray-600">
            Find the perfect coding assistant for your task
          </p>
        </div>

        <div className="bg-white shadow rounded-lg p-6 mb-8">
          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label htmlFor="description" className="block text-sm font-medium text-gray-700 mb-1">
                Task Description *
              </label>
              <textarea
                id="description"
                rows={4}
                className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500"
                placeholder="Describe your coding task or project..."
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                required
              />
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label htmlFor="language" className="block text-sm font-medium text-gray-700 mb-1">
                  Programming Language (optional)
                </label>
                <input
                  type="text"
                  id="language"
                  className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500"
                  placeholder="e.g., Python, JavaScript"
                  value={language}
                  onChange={(e) => setLanguage(e.target.value)}
                />
              </div>

              <div>
                <label htmlFor="complexity" className="block text-sm font-medium text-gray-700 mb-1">
                  Task Complexity
                </label>
                <select
                  id="complexity"
                  className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500"
                  value={complexity}
                  onChange={(e) => setComplexity(e.target.value)}
                >
                  <option value="low">Low</option>
                  <option value="medium">Medium</option>
                  <option value="high">High</option>
                </select>
              </div>
            </div>

            {error && (
              <div className="text-red-500 text-sm mt-2">{error}</div>
            )}

            <div className="flex justify-end">
              <button
                type="submit"
                disabled={isLoading}
                className="px-6 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {isLoading ? 'Finding Recommendations...' : 'Get Recommendations'}
              </button>
            </div>
          </form>
        </div>

        {recommendations.length > 0 && (
          <div className="space-y-6">
            <h2 className="text-2xl font-bold text-gray-900">Recommended Agents</h2>
            
            <div className="grid gap-6 md:grid-cols-3">
              {recommendations.map((agent, index) => (
                <div 
                  key={agent.id}
                  className={`bg-white rounded-lg shadow-md overflow-hidden border-l-4 ${
                    index === 0 ? 'border-l-green-500' : 
                    index === 1 ? 'border-l-blue-500' : 'border-l-purple-500'
                  }`}
                >
                  <div className="p-6">
                    <div className="flex justify-between items-start">
                      <h3 className="text-lg font-semibold text-gray-900">{agent.name}</h3>
                      <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-indigo-100 text-indigo-800">
                        {Math.round(agent.score * 10)}%
                      </span>
                    </div>
                    <p className="mt-2 text-sm text-gray-600">{agent.explanation}</p>
                    
                    {agent.analysis && (
                      <div className="mt-4 pt-4 border-t border-gray-100">
                        <h4 className="text-sm font-medium text-gray-900 mb-2">Task Analysis:</h4>
                        
                        {agent.analysis.task_type && (
                          <div className="mb-2">
                            <span className="text-xs font-medium text-gray-500">Task Type:</span>
                            <span className="ml-2 text-sm text-gray-700">
                              {agent.analysis.task_type.replace(/_/g, ' ')}
                            </span>
                          </div>
                        )}
                        
                        {agent.analysis.required_skills && agent.analysis.required_skills.length > 0 && (
                          <div className="mb-2">
                            <span className="text-xs font-medium text-gray-500">Key Skills:</span>
                            <div className="flex flex-wrap gap-1 mt-1">
                              {agent.analysis.required_skills.slice(0, 3).map((skill, i) => (
                                <span key={i} className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-blue-100 text-blue-800">
                                  {skill}
                                </span>
                              ))}
                            </div>
                          </div>
                        )}
                        
                        {agent.analysis.recommended_features && agent.analysis.recommended_features.length > 0 && (
                          <div>
                            <span className="text-xs font-medium text-gray-500">Key Features:</span>
                            <ul className="mt-1 space-y-1">
                              {agent.analysis.recommended_features.slice(0, 3).map((feature, i) => (
                                <li key={i} className="text-sm text-gray-600 flex items-start">
                                  <svg className="h-4 w-4 text-green-500 mr-1.5 mt-0.5 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                                  </svg>
                                  {feature}
                                </li>
                              ))}
                            </ul>
                          </div>
                        )}
                      </div>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
