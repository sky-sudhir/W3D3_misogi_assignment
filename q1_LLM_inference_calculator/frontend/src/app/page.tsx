"use client";

import { useState } from "react";

type ModelSize = "7B" | "13B" | "GPT-4";
type HardwareType = "cpu" | "gpu" | "tpu";
type DeploymentMode = "cloud" | "on_prem" | "edge";

interface InferenceResult {
  latency_seconds: number;
  memory_gb: number;
  cost_per_request: number;
  hardware_compatibility: string;
  model_size: string;
  hardware_type: string;
  deployment_mode: string;
}

export default function InferenceCalculator() {
  const [modelSize, setModelSize] = useState<ModelSize>("7B");
  const [inputTokens, setInputTokens] = useState<number>(1000);
  const [outputTokens, setOutputTokens] = useState<number>(500);
  const [batchSize, setBatchSize] = useState<number>(1);
  const [hardwareType, setHardwareType] = useState<HardwareType>("gpu");
  const [deploymentMode, setDeploymentMode] = useState<DeploymentMode>("cloud");
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [result, setResult] = useState<InferenceResult | null>(null);
  const [error, setError] = useState<string | null>(null);

  const calculateInference = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError(null);

    try {
      const response = await fetch(
        "http://localhost:8000/calculate-inference",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            model_size: modelSize,
            input_tokens: inputTokens,
            output_tokens: outputTokens,
            batch_size: batchSize,
            hardware_type: hardwareType,
            deployment_mode: deploymentMode,
          }),
        }
      );

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || "Failed to calculate inference");
      }

      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError(
        err instanceof Error ? err.message : "An unknown error occurred"
      );
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-4xl mx-auto">
        <div className="text-center mb-10">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            LLM Inference Calculator
          </h1>
          <p className="text-gray-600">
            Estimate the cost, latency, and resource requirements for LLM
            inference
          </p>
        </div>

        <div className="bg-white shadow rounded-lg p-6 mb-8">
          <form onSubmit={calculateInference} className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {/* Model Size */}
              <div>
                <label
                  htmlFor="modelSize"
                  className="block text-sm font-medium text-gray-700 mb-1"
                >
                  Model Size
                </label>
                <select
                  id="modelSize"
                  value={modelSize}
                  onChange={(e) => setModelSize(e.target.value as ModelSize)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                >
                  <option value="7B">7B Parameters</option>
                  <option value="13B">13B Parameters</option>
                  <option value="GPT-4">GPT-4 (Estimated)</option>
                </select>
              </div>

              {/* Hardware Type */}
              <div>
                <label
                  htmlFor="hardwareType"
                  className="block text-sm font-medium text-gray-700 mb-1"
                >
                  Hardware Type
                </label>
                <select
                  id="hardwareType"
                  value={hardwareType}
                  onChange={(e) =>
                    setHardwareType(e.target.value as HardwareType)
                  }
                  className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                >
                  <option value="cpu">CPU</option>
                  <option value="gpu">GPU</option>
                  <option value="tpu">TPU</option>
                </select>
              </div>

              {/* Input Tokens */}
              <div>
                <label
                  htmlFor="inputTokens"
                  className="block text-sm font-medium text-gray-700 mb-1"
                >
                  Input Tokens
                </label>
                <input
                  type="number"
                  id="inputTokens"
                  min="1"
                  value={inputTokens}
                  onChange={(e) => setInputTokens(Number(e.target.value))}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                />
              </div>

              {/* Output Tokens */}
              <div>
                <label
                  htmlFor="outputTokens"
                  className="block text-sm font-medium text-gray-700 mb-1"
                >
                  Output Tokens
                </label>
                <input
                  type="number"
                  id="outputTokens"
                  min="1"
                  value={outputTokens}
                  onChange={(e) => setOutputTokens(Number(e.target.value))}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                />
              </div>

              {/* Batch Size */}
              <div>
                <label
                  htmlFor="batchSize"
                  className="block text-sm font-medium text-gray-700 mb-1"
                >
                  Batch Size
                </label>
                <input
                  type="number"
                  id="batchSize"
                  min="1"
                  value={batchSize}
                  onChange={(e) => setBatchSize(Number(e.target.value))}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                />
              </div>

              {/* Deployment Mode */}
              <div>
                <label
                  htmlFor="deploymentMode"
                  className="block text-sm font-medium text-gray-700 mb-1"
                >
                  Deployment Mode
                </label>
                <select
                  id="deploymentMode"
                  value={deploymentMode}
                  onChange={(e) =>
                    setDeploymentMode(e.target.value as DeploymentMode)
                  }
                  className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                >
                  <option value="cloud">Cloud</option>
                  <option value="on_prem">On-Premises</option>
                  <option value="edge">Edge</option>
                </select>
              </div>
            </div>

            <div className="flex justify-center">
              <button
                type="submit"
                disabled={isLoading}
                className={`px-6 py-3 rounded-md text-white font-medium ${
                  isLoading
                    ? "bg-blue-400 cursor-not-allowed"
                    : "bg-blue-600 hover:bg-blue-700"
                } focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-colors`}
              >
                {isLoading ? "Calculating..." : "Calculate"}
              </button>
            </div>
          </form>
        </div>

        {error && (
          <div className="bg-red-50 border-l-4 border-red-400 p-4 mb-8">
            <div className="flex">
              <div className="flex-shrink-0">
                <svg
                  className="h-5 w-5 text-red-400"
                  xmlns="http://www.w3.org/2000/svg"
                  viewBox="0 0 20 20"
                  fill="currentColor"
                >
                  <path
                    fillRule="evenodd"
                    d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
                    clipRule="evenodd"
                  />
                </svg>
              </div>
              <div className="ml-3">
                <p className="text-sm text-red-700">{error}</p>
              </div>
            </div>
          </div>
        )}

        {result && (
          <div className="bg-white shadow rounded-lg overflow-hidden">
            <div className="px-6 py-5 border-b border-gray-200">
              <h2 className="text-lg font-medium text-gray-900">
                Inference Results
              </h2>
              <p className="mt-1 text-sm text-gray-500">
                Model: {result.model_size} • Hardware:{" "}
                {result.hardware_type.toUpperCase()} • Deployment:{" "}
                {result.deployment_mode.replace("_", "-")}
              </p>
            </div>
            <div className="bg-gray-50 px-6 py-5">
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                <div className="bg-white p-4 rounded-lg shadow">
                  <p className="text-sm font-medium text-gray-500">Latency</p>
                  <p className="mt-1 text-2xl font-semibold text-blue-600">
                    {result.latency_seconds.toFixed(2)}s
                  </p>
                  <p className="mt-1 text-xs text-gray-500">per request</p>
                </div>
                <div className="bg-white p-4 rounded-lg shadow">
                  <p className="text-sm font-medium text-gray-500">
                    Memory Usage
                  </p>
                  <p className="mt-1 text-2xl font-semibold text-green-600">
                    {result.memory_gb} GB
                  </p>
                  <p className="mt-1 text-xs text-gray-500">VRAM required</p>
                </div>
                <div className="bg-white p-4 rounded-lg shadow">
                  <p className="text-sm font-medium text-gray-500">Cost</p>
                  <p className="mt-1 text-2xl font-semibold text-purple-600">
                    ${result.cost_per_request.toFixed(6)}
                  </p>
                  <p className="mt-1 text-xs text-gray-500">per 1K tokens</p>
                </div>
                <div className="bg-white p-4 rounded-lg shadow">
                  <p className="text-sm font-medium text-gray-500">
                    Compatibility
                  </p>
                  <div className="mt-1">
                    <span
                      className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                        result.hardware_compatibility.includes(
                          "Not recommended"
                        )
                          ? "bg-yellow-100 text-yellow-800"
                          : "bg-green-100 text-green-800"
                      }`}
                    >
                      {result.hardware_compatibility}
                    </span>
                  </div>
                  <p className="mt-1 text-xs text-gray-500">
                    {result.hardware_type.toUpperCase()} with{" "}
                    {result.model_size}
                  </p>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Information Section */}
        <div className="mt-12 bg-white shadow rounded-lg p-6">
          <h2 className="text-lg font-medium text-gray-900 mb-4">
            About This Calculator
          </h2>
          <div className="prose max-w-none text-gray-600">
            <p className="mb-4">
              This calculator provides estimates for LLM inference based on
              model size, hardware type, and deployment mode. The calculations
              are based on approximate benchmarks and may vary based on specific
              implementations and optimizations.
            </p>
            <h3 className="text-md font-medium text-gray-900 mt-6 mb-2">
              Model Sizes
            </h3>
            <ul className="list-disc pl-5 space-y-1 mb-4">
              <li>
                <strong>7B:</strong> Small models like LLaMA-7B, suitable for
                most consumer GPUs
              </li>
              <li>
                <strong>13B:</strong> Medium-sized models like LLaMA-13B,
                requiring high-end GPUs
              </li>
              <li>
                <strong>GPT-4:</strong> Estimated values based on public
                information about large language models
              </li>
            </ul>
            <h3 className="text-md font-medium text-gray-900 mt-6 mb-2">
              Hardware Types
            </h3>
            <ul className="list-disc pl-5 space-y-1 mb-4">
              <li>
                <strong>CPU:</strong> General-purpose processors, not
                recommended for large models
              </li>
              <li>
                <strong>GPU:</strong> Graphics processing units, commonly used
                for deep learning
              </li>
              <li>
                <strong>TPU:</strong> Tensor processing units, specialized for
                machine learning workloads
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
}
