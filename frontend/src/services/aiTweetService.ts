import axios from 'axios';

// Define the interface for tweet generation request
export interface TweetGenerationRequest {
  topic: string;
  tone: string;
  generationType: 'single' | 'thread';
}

// Define the interface for tweet generation response
export interface TweetGenerationResponse {
  tweets: string[];
  error?: string;
}

// Base URL for API - adjust as needed
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

/**
 * Service for generating AI tweets
 */
export const aiTweetService = {
  /**
   * Generate tweets using AI
   * @param request Tweet generation parameters
   * @returns Promise with generated tweets
   */
  generateTweets: async (request: TweetGenerationRequest): Promise<TweetGenerationResponse> => {
    try {
      console.log('Sending tweet generation request:', request);  
      const response = await axios.post<TweetGenerationResponse>(
        `${API_BASE_URL}/ai/generate-tweets`, 
        request,
        {
          headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Access-Control-Allow-Origin': 'http://localhost:3000'
          },
          withCredentials: true  
        }
      );

      console.log('Received tweet generation response:', response);  
      return response.data;
    } catch (error) {
      console.error('Detailed error generating tweets:', error);
      
      // Handle different types of errors
      if (axios.isAxiosError(error)) {
        console.error('Axios Error Details:', {
          response: error.response,
          request: error.request,
          config: error.config
        });

        return {
          tweets: [],
          error: error.response?.data?.detail || 'Failed to generate tweets'
        };
      }

      return {
        tweets: [],
        error: 'An unexpected error occurred'
      };
    }
  }
};
