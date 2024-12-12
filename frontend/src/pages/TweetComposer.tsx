import React, { useState } from 'react';
import { motion } from 'framer-motion';

const TweetComposer: React.FC = () => {
  const [tweet, setTweet] = useState('');
  const [selectedAccount, setSelectedAccount] = useState('');
  const [isThread, setIsThread] = useState(false);
  const [threadTweets, setThreadTweets] = useState<string[]>(['']);

  const handleTweetChange = (value: string) => {
    setTweet(value);
  };

  const handlePostTweet = () => {
    // TODO: Implement tweet posting logic
    console.log('Posting tweet:', tweet);
  };

  const handleAddThreadTweet = () => {
    setThreadTweets([...threadTweets, '']);
  };

  const updateThreadTweet = (index: number, value: string) => {
    const updatedThreadTweets = [...threadTweets];
    updatedThreadTweets[index] = value;
    setThreadTweets(updatedThreadTweets);
  };

  return (
    <motion.div 
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.5 }}
      className="p-6 bg-gray-100 min-h-screen"
    >
      <h1 className="text-3xl font-bold mb-6">Tweet Composer</h1>
      
      <div className="bg-white shadow-md rounded-lg p-6">
        {/* Account Selection */}
        <div className="mb-4">
          <label className="block text-sm font-medium text-gray-700">
            Select Account
          </label>
          <select 
            value={selectedAccount}
            onChange={(e) => setSelectedAccount(e.target.value)}
            className="mt-1 block w-full border p-2 rounded"
          >
            <option value="">Select an account</option>
            <option value="account1">@username1</option>
            <option value="account2">@username2</option>
          </select>
        </div>

        {/* Thread Toggle */}
        <div className="mb-4 flex items-center">
          <input 
            type="checkbox" 
            checked={isThread}
            onChange={() => setIsThread(!isThread)}
            className="mr-2"
          />
          <label>Create Thread</label>
        </div>

        {/* Single Tweet Composer */}
        {!isThread && (
          <div>
            <textarea 
              value={tweet}
              onChange={(e) => handleTweetChange(e.target.value)}
              placeholder="What's happening?"
              className="w-full border p-2 rounded h-32"
              maxLength={280}
            />
            <div className="text-right text-sm text-gray-500">
              {tweet.length}/280
            </div>
          </div>
        )}

        {/* Thread Composer */}
        {isThread && (
          <div>
            {threadTweets.map((threadTweet, index) => (
              <div key={index} className="mb-4">
                <textarea 
                  value={threadTweet}
                  onChange={(e) => updateThreadTweet(index, e.target.value)}
                  placeholder={`Thread Tweet ${index + 1}`}
                  className="w-full border p-2 rounded h-24"
                  maxLength={280}
                />
                <div className="text-right text-sm text-gray-500">
                  {threadTweet.length}/280
                </div>
              </div>
            ))}
            <button 
              onClick={handleAddThreadTweet}
              className="bg-blue-100 text-blue-600 p-2 rounded mb-4"
            >
              Add Tweet to Thread
            </button>
          </div>
        )}

        {/* Post Button */}
        <button 
          onClick={handlePostTweet}
          disabled={!selectedAccount || (isThread ? threadTweets.some(t => !t.trim()) : !tweet.trim())}
          className="w-full bg-blue-500 text-white p-2 rounded disabled:bg-gray-300"
        >
          {isThread ? 'Post Thread' : 'Post Tweet'}
        </button>
      </div>
    </motion.div>
  );
};

export default TweetComposer;
