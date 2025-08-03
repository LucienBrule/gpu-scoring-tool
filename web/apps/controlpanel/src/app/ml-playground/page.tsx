"use client";

import React, { useState, useRef, useEffect } from "react";
import { useGpuClassification } from "@/hooks/useGpuClassification";
import { Sparkline } from "@/components/ui/Sparkline";

// Type for classification history items
interface ClassificationHistoryItem {
  id: string;
  text: string;
  isGpu: boolean;
  score: number;
  timestamp: Date;
}

export default function MLPlaygroundPage() {
  // State for input text and threshold
  const [inputText, setInputText] = useState("");
  const [confidenceThreshold, setConfidenceThreshold] = useState(0.5);
  const [history, setHistory] = useState<ClassificationHistoryItem[]>([]);
  const [isRealTime, setIsRealTime] = useState(false);
  const timeoutRef = useRef<NodeJS.Timeout | null>(null);

  // Use the GPU classification hook
  const {
    classify,
    data,
    isLoading,
    isError,
    error,
    isSuccess,
    reset,
    formatConfidence,
    meetsThreshold,
  } = useGpuClassification({
    confidenceThreshold,
    onSuccess: (result) => {
      // Add to history when classification is successful
      if (inputText.trim()) {
        const historyItem: ClassificationHistoryItem = {
          id: Date.now().toString(),
          text: inputText,
          isGpu: result.mlIsGpu,
          score: result.mlScore || 0,
          timestamp: new Date(),
        };
        setHistory((prev) => [historyItem, ...prev.slice(0, 9)]); // Keep last 10 items
      }
    },
  });

  // Handle real-time classification with debounce
  useEffect(() => {
    if (isRealTime && inputText.trim()) {
      if (timeoutRef.current) {
        clearTimeout(timeoutRef.current);
      }
      
      timeoutRef.current = setTimeout(() => {
        classify(inputText);
      }, 500); // 500ms debounce
    }
    
    return () => {
      if (timeoutRef.current) {
        clearTimeout(timeoutRef.current);
      }
    };
  }, [inputText, isRealTime, classify]);

  // Handle form submission
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (inputText.trim()) {
      classify(inputText);
    }
  };

  // Handle input change
  const handleInputChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setInputText(e.target.value);
    if (!isRealTime) {
      reset(); // Reset previous results when not in real-time mode
    }
  };

  // Handle threshold change
  const handleThresholdChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setConfidenceThreshold(parseFloat(e.target.value));
  };

  // Generate sample data for sparkline based on confidence
  const generateSparklineData = (score: number) => {
    const baseValue = score * 100;
    // Generate a series of values that trend toward the final score
    return [
      baseValue * 0.3 + Math.random() * 10,
      baseValue * 0.5 + Math.random() * 10,
      baseValue * 0.7 + Math.random() * 10,
      baseValue * 0.9 + Math.random() * 5,
      baseValue,
    ];
  };

  return (
    <div className="space-y-8">
      <div className="flex flex-col space-y-2">
        <h1 className="text-3xl font-bold">ML Classifier Playground</h1>
        <p className="text-gray-400">
          Test the GPU classification model by entering text descriptions and see if they&apos;re identified as GPU listings.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Input Section */}
        <div className="lg:col-span-2 space-y-4">
          <div className="bg-gray-800 rounded-lg p-6 shadow-md">
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label htmlFor="input-text" className="block text-sm font-medium mb-1">
                  Enter text to classify
                </label>
                <textarea
                  id="input-text"
                  rows={5}
                  className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  placeholder="Enter a product description or title to classify..."
                  value={inputText}
                  onChange={handleInputChange}
                />
              </div>

              <div className="flex flex-col sm:flex-row sm:justify-between sm:items-center space-y-4 sm:space-y-0">
                <div className="flex items-center space-x-2">
                  <input
                    type="checkbox"
                    id="real-time"
                    checked={isRealTime}
                    onChange={() => setIsRealTime(!isRealTime)}
                    className="h-4 w-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                  />
                  <label htmlFor="real-time" className="text-sm">
                    Real-time classification
                  </label>
                </div>
                
                {!isRealTime && (
                  <button
                    type="submit"
                    disabled={isLoading || !inputText.trim()}
                    className="px-4 py-2 bg-blue-600 text-white rounded-md shadow-sm hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    {isLoading ? "Classifying..." : "Classify"}
                  </button>
                )}
              </div>
            </form>
          </div>

          {/* Parameters Section */}
          <div className="bg-gray-800 rounded-lg p-6 shadow-md">
            <h2 className="text-lg font-medium mb-4">Classification Parameters</h2>
            <div className="space-y-4">
              <div>
                <label htmlFor="threshold" className="block text-sm font-medium mb-1">
                  Confidence Threshold: {(confidenceThreshold * 100).toFixed(0)}%
                </label>
                <input
                  id="threshold"
                  type="range"
                  min="0"
                  max="1"
                  step="0.05"
                  value={confidenceThreshold}
                  onChange={handleThresholdChange}
                  className="w-full h-2 bg-gray-700 rounded-lg appearance-none cursor-pointer"
                />
                <div className="flex justify-between text-xs text-gray-400 mt-1">
                  <span>0%</span>
                  <span>50%</span>
                  <span>100%</span>
                </div>
              </div>
            </div>
          </div>

          {/* History Section */}
          <div className="bg-gray-800 rounded-lg p-6 shadow-md">
            <h2 className="text-lg font-medium mb-4">Classification History</h2>
            {history.length === 0 ? (
              <p className="text-gray-400 text-sm">No classifications yet. Start by entering text above.</p>
            ) : (
              <div className="space-y-3 max-h-80 overflow-y-auto">
                {history.map((item) => (
                  <div
                    key={item.id}
                    className={`p-3 rounded-md border ${
                      item.isGpu && item.score >= confidenceThreshold
                        ? "bg-green-900/20 border-green-700"
                        : "bg-red-900/20 border-red-700"
                    }`}
                  >
                    <div className="flex justify-between items-start">
                      <div className="text-sm font-medium truncate max-w-[70%]">{item.text}</div>
                      <div className="text-xs text-gray-400">
                        {new Date(item.timestamp).toLocaleTimeString()}
                      </div>
                    </div>
                    <div className="flex justify-between items-center mt-2">
                      <div className="text-sm">
                        {item.isGpu && item.score >= confidenceThreshold
                          ? "GPU"
                          : "Not GPU"}
                        <span className="ml-2 text-xs">
                          ({formatConfidence(item.score)})
                        </span>
                      </div>
                      <div className="w-20 h-6">
                        <Sparkline
                          data={generateSparklineData(item.score)}
                          width={80}
                          height={24}
                          color={
                            item.isGpu && item.score >= confidenceThreshold
                              ? "#4ade80" // green-400
                              : "#f87171" // red-400
                          }
                          gradientFill
                        />
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>

        {/* Results Section */}
        <div className="space-y-4">
          <div className="bg-gray-800 rounded-lg p-6 shadow-md h-full">
            <h2 className="text-lg font-medium mb-4">Classification Results</h2>
            
            {isLoading && (
              <div className="flex items-center justify-center h-40">
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
              </div>
            )}
            
            {isError && (
              <div className="bg-red-900/20 border border-red-700 rounded-md p-4">
                <h3 className="text-red-400 font-medium">Error</h3>
                <p className="text-sm mt-1">{error?.message || "Failed to classify text. Please try again."}</p>
              </div>
            )}
            
            {!isLoading && !isError && !data && (
              <div className="flex flex-col items-center justify-center h-40 text-gray-400">
                <p>Enter text and click &quot;Classify&quot; to see results</p>
              </div>
            )}
            
            {!isLoading && !isError && data && (
              <div className="space-y-6">
                <div className="flex flex-col items-center">
                  <div
                    className={`text-2xl font-bold ${
                      data.mlIsGpu && meetsThreshold(data.mlScore)
                        ? "text-green-400"
                        : "text-red-400"
                    }`}
                  >
                    {data.mlIsGpu && meetsThreshold(data.mlScore) ? "GPU" : "Not GPU"}
                  </div>
                  
                  <div className="mt-2 text-sm text-gray-400">
                    Confidence: {formatConfidence(data.mlScore)}
                  </div>
                </div>
                
                <div>
                  <h3 className="text-sm font-medium mb-2">Confidence Score</h3>
                  <div className="h-4 w-full bg-gray-700 rounded-full overflow-hidden">
                    <div
                      className={`h-full ${
                        data.mlIsGpu ? "bg-green-500" : "bg-red-500"
                      }`}
                      style={{ width: `${(data.mlScore || 0) * 100}%` }}
                    ></div>
                  </div>
                  <div className="flex justify-between text-xs text-gray-400 mt-1">
                    <span>0%</span>
                    <span>50%</span>
                    <span>100%</span>
                  </div>
                </div>
                
                <div>
                  <h3 className="text-sm font-medium mb-2">Threshold</h3>
                  <div className="flex items-center">
                    <div className="h-4 w-full bg-gray-700 rounded-full overflow-hidden">
                      <div
                        className="h-full bg-blue-500"
                        style={{ width: `${confidenceThreshold * 100}%` }}
                      ></div>
                    </div>
                  </div>
                  <div className="mt-4 text-sm">
                    {meetsThreshold(data.mlScore) ? (
                      <span className="text-green-400">
                        ✓ Meets confidence threshold
                      </span>
                    ) : (
                      <span className="text-red-400">
                        ✗ Below confidence threshold
                      </span>
                    )}
                  </div>
                </div>
                
                <div className="pt-4">
                  <h3 className="text-sm font-medium mb-2">Confidence Trend</h3>
                  <div className="h-20">
                    <Sparkline
                      data={generateSparklineData(data.mlScore || 0)}
                      width={300}
                      height={80}
                      color={data.mlIsGpu ? "#4ade80" : "#f87171"}
                      gradientFill
                      strokeWidth={3}
                    />
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}