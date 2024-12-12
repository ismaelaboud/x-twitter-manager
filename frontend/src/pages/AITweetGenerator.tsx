import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { 
  Bot, 
  Copy, 
  Twitter, 
  Lightbulb, 
  Wand2,
  AlertTriangle 
} from 'lucide-react';
import { aiTweetService, TweetGenerationRequest } from '../services/aiTweetService';
import { toast } from 'react-hot-toast';

// Mock service (we'll replace with actual API call later)
const mockTopicSuggestions = [
  'AI Innovation',
  'Tech Trends',
  'Future of Work',
  'Climate Change',
  'Digital Transformation'
];

const mockToneOptions = [
  { value: 'professional', label: 'Professional' },
  { value: 'casual', label: 'Casual' },
  { value: 'witty', label: 'Witty' },
  { value: 'inspirational', label: 'Inspirational' }
];

const AITweetGenerator: React.FC = () => {
  // State Management
  const [topic, setTopic] = useState('');
  const [generationType, setGenerationType] = useState<'single' | 'thread'>('single');
  const [tone, setTone] = useState('professional');
  const [generatedTweets, setGeneratedTweets] = useState<string[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Generate Tweet Handler (API Integration)
  const handleGenerateTweet = async () => {
    // Input validation
    if (!topic.trim()) {
      setError('Please enter a topic');
      toast.error('Please enter a topic');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      // Prepare request payload
      const request: TweetGenerationRequest = {
        topic,
        tone,
        generationType
      };

      // Call AI Tweet Generation Service
      const response = await aiTweetService.generateTweets(request);

      if (response.error) {
        // Handle service-level errors
        setError(response.error);
        toast.error(response.error);
      } else {
        // Successfully generated tweets
        setGeneratedTweets(response.tweets);
        toast.success(`Generated ${generationType === 'single' ? 'tweet' : 'thread'}`);
      }
    } catch (err) {
      // Handle unexpected errors
      const errorMessage = err instanceof Error ? err.message : 'An unexpected error occurred';
      setError(errorMessage);
      toast.error(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  // Copy to Clipboard
  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text).then(() => {
      toast.success('Tweet copied to clipboard!');
    }).catch(() => {
      toast.error('Failed to copy tweet');
    });
  };

  return (
    <motion.div 
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.5 }}
      className="p-6 bg-gray-100 min-h-screen"
    >
      <div className="container mx-auto max-w-2xl">
        <h1 className="text-3xl font-bold mb-6 flex items-center">
          <Bot className="mr-3 text-blue-500" /> 
          AI Tweet Generator
        </h1>

        {/* Topic Input */}
        <div className="bg-white shadow-md rounded-lg p-6 mb-4">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Tweet Topic
          </label>
          <input 
            type="text"
            value={topic}
            onChange={(e) => setTopic(e.target.value)}
            placeholder="Enter your tweet topic"
            className="w-full p-2 border rounded focus:ring-2 focus:ring-blue-500"
          />
          {error && (
            <p className="text-red-500 text-sm mt-2 flex items-center">
              <AlertTriangle className="mr-2" /> {error}
            </p>
          )}

          {/* Topic Suggestions */}
          <div className="mt-4 flex flex-wrap gap-2">
            {mockTopicSuggestions.map((suggestionTopic) => (
              <button
                key={suggestionTopic}
                onClick={() => setTopic(suggestionTopic)}
                className="bg-blue-100 text-blue-700 px-3 py-1 rounded-full text-sm hover:bg-blue-200 transition flex items-center"
              >
                <Lightbulb className="mr-2" />
                {suggestionTopic}
              </button>
            ))}
          </div>
        </div>

        {/* Generation Options */}
        <div className="bg-white shadow-md rounded-lg p-6 mb-4 grid md:grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Generation Type
            </label>
            <select 
              value={generationType}
              onChange={(e) => setGenerationType(e.target.value as 'single' | 'thread')}
              className="w-full p-2 border rounded"
            >
              <option value="single">Single Tweet</option>
              <option value="thread">Tweet Thread</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Tone
            </label>
            <select 
              value={tone}
              onChange={(e) => setTone(e.target.value)}
              className="w-full p-2 border rounded"
            >
              {mockToneOptions.map((option) => (
                <option key={option.value} value={option.value}>
                  {option.label}
                </option>
              ))}
            </select>
          </div>
        </div>

        {/* Generate Button */}
        <button
          onClick={handleGenerateTweet}
          disabled={loading || !topic}
          className={`w-full p-3 rounded text-white font-bold flex items-center justify-center ${
            loading || !topic 
              ? 'bg-gray-400 cursor-not-allowed' 
              : 'bg-blue-500 hover:bg-blue-600 transition'
          }`}
        >
          {loading ? (
            <>
              <Wand2 className="mr-2 animate-spin" /> Generating...
            </>
          ) : (
            <>
              <Bot className="mr-2" /> Generate Tweet
            </>
          )}
        </button>

        {/* Generated Tweets */}
        {generatedTweets.length > 0 && (
          <div className="mt-6 bg-white shadow-md rounded-lg p-6">
            <h2 className="text-xl font-semibold mb-4">
              Generated {generationType === 'single' ? 'Tweet' : 'Thread'}
            </h2>
            {generatedTweets.map((tweet, index) => (
              <div 
                key={index} 
                className="bg-gray-100 p-4 rounded-lg mb-4 flex justify-between items-center"
              >
                <p>{tweet}</p>
                <div className="flex space-x-2">
                  <button 
                    onClick={() => copyToClipboard(tweet)}
                    className="text-gray-600 hover:text-blue-500"
                    title="Copy to Clipboard"
                  >
                    <Copy />
                  </button>
                  <button 
                    className="text-blue-500 hover:text-blue-700"
                    title="Post to Twitter"
                  >
                    <Twitter />
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </motion.div>
  );
};

export default AITweetGenerator;
