import React, { useState } from 'react';
import { motion } from 'framer-motion';

interface ScheduledTweet {
  id: string;
  content: string;
  account: string;
  scheduledTime: Date;
}

const ScheduleManager: React.FC = () => {
  const [scheduledTweets, setScheduledTweets] = useState<ScheduledTweet[]>([]);
  const [newTweet, setNewTweet] = useState({
    content: '',
    account: '',
    scheduledTime: new Date()
  });

  const handleScheduleTweet = () => {
    if (newTweet.content && newTweet.account) {
      const scheduledTweet: ScheduledTweet = {
        id: Date.now().toString(),
        ...newTweet
      };
      setScheduledTweets([...scheduledTweets, scheduledTweet]);
      // Reset form
      setNewTweet({
        content: '',
        account: '',
        scheduledTime: new Date()
      });
    }
  };

  const handleCancelSchedule = (id: string) => {
    setScheduledTweets(scheduledTweets.filter(tweet => tweet.id !== id));
  };

  return (
    <motion.div 
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.5 }}
      className="p-6 bg-gray-100 min-h-screen"
    >
      <h1 className="text-3xl font-bold mb-6">Tweet Scheduler</h1>
      
      {/* Schedule New Tweet */}
      <div className="bg-white shadow-md rounded-lg p-6 mb-6">
        <h2 className="text-xl font-semibold mb-4">Schedule New Tweet</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <select 
            value={newTweet.account}
            onChange={(e) => setNewTweet({...newTweet, account: e.target.value})}
            className="border p-2 rounded"
          >
            <option value="">Select Account</option>
            <option value="account1">@username1</option>
            <option value="account2">@username2</option>
          </select>
          
          <input 
            type="datetime-local" 
            value={newTweet.scheduledTime.toISOString().slice(0, 16)}
            onChange={(e) => setNewTweet({...newTweet, scheduledTime: new Date(e.target.value)})}
            className="border p-2 rounded"
          />
          
          <textarea 
            placeholder="Tweet content"
            value={newTweet.content}
            onChange={(e) => setNewTweet({...newTweet, content: e.target.value})}
            className="border p-2 rounded col-span-2 h-24"
            maxLength={280}
          />
          
          <button 
            onClick={handleScheduleTweet}
            className="bg-blue-500 text-white p-2 rounded col-span-2"
          >
            Schedule Tweet
          </button>
        </div>
      </div>

      {/* Scheduled Tweets List */}
      <div className="bg-white shadow-md rounded-lg p-6">
        <h2 className="text-xl font-semibold mb-4">Upcoming Tweets</h2>
        {scheduledTweets.length === 0 ? (
          <p className="text-gray-500">No scheduled tweets</p>
        ) : (
          <ul>
            {scheduledTweets.map((tweet) => (
              <li 
                key={tweet.id} 
                className="flex justify-between items-center border-b p-3"
              >
                <div>
                  <p className="font-medium">{tweet.account}</p>
                  <p className="text-sm text-gray-500">{tweet.content}</p>
                  <p className="text-xs text-gray-400">
                    {tweet.scheduledTime.toLocaleString()}
                  </p>
                </div>
                <button 
                  className="text-red-500 hover:bg-red-100 p-2 rounded"
                  onClick={() => handleCancelSchedule(tweet.id)}
                >
                  Cancel
                </button>
              </li>
            ))}
          </ul>
        )}
      </div>
    </motion.div>
  );
};

export default ScheduleManager;
