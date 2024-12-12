import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { BarChartIcon, RocketIcon, HeartIcon } from '@radix-ui/react-icons';

interface AccountAnalytics {
  username: string;
  followers: number;
  engagement: number;
  totalTweets: number;
}

const Analytics: React.FC = () => {
  const [selectedAccount, setSelectedAccount] = useState('');
  const [analytics, setAnalytics] = useState<AccountAnalytics | null>(null);

  const mockAnalytics: {[key: string]: AccountAnalytics} = {
    'account1': {
      username: '@username1',
      followers: 5342,
      engagement: 12.5,
      totalTweets: 256
    },
    'account2': {
      username: '@username2',
      followers: 3214,
      engagement: 8.7,
      totalTweets: 178
    }
  };

  const handleFetchAnalytics = () => {
    if (selectedAccount) {
      setAnalytics(mockAnalytics[selectedAccount]);
    }
  };

  return (
    <motion.div 
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.5 }}
      className="p-6 bg-gray-100 min-h-screen"
    >
      <h1 className="text-3xl font-bold mb-6">Analytics Dashboard</h1>
      
      {/* Account Selection */}
      <div className="bg-white shadow-md rounded-lg p-6 mb-6">
        <div className="flex space-x-4">
          <select 
            value={selectedAccount}
            onChange={(e) => setSelectedAccount(e.target.value)}
            className="flex-grow border p-2 rounded"
          >
            <option value="">Select an account</option>
            <option value="account1">@username1</option>
            <option value="account2">@username2</option>
          </select>
          <button 
            onClick={handleFetchAnalytics}
            className="bg-blue-500 text-white p-2 rounded"
          >
            Fetch Analytics
          </button>
        </div>
      </div>

      {/* Analytics Display */}
      {analytics && (
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="grid grid-cols-1 md:grid-cols-3 gap-6"
        >
          <AnalyticsCard 
            icon={<BarChartIcon />}
            title="Followers"
            value={analytics.followers.toLocaleString()}
            color="bg-blue-100 text-blue-600"
          />
          <AnalyticsCard 
            icon={<HeartIcon />}
            title="Engagement Rate"
            value={`${analytics.engagement}%`}
            color="bg-pink-100 text-pink-600"
          />
          <AnalyticsCard 
            icon={<RocketIcon />}
            title="Total Tweets"
            value={analytics.totalTweets.toLocaleString()}
            color="bg-green-100 text-green-600"
          />
        </motion.div>
      )}

      {/* Recent Performance Graph Placeholder */}
      {analytics && (
        <div className="bg-white shadow-md rounded-lg p-6 mt-6">
          <h2 className="text-xl font-semibold mb-4">Recent Performance</h2>
          <div className="h-64 bg-gray-100 flex items-center justify-center rounded">
            <p className="text-gray-500">Performance Graph Placeholder</p>
          </div>
        </div>
      )}
    </motion.div>
  );
};

interface AnalyticsCardProps {
  icon: React.ReactNode;
  title: string;
  value: string;
  color: string;
}

const AnalyticsCard: React.FC<AnalyticsCardProps> = ({ 
  icon, 
  title, 
  value, 
  color 
}) => {
  return (
    <div className={`${color} p-6 rounded-lg flex items-center justify-between`}>
      <div>
        <h3 className="text-sm font-medium">{title}</h3>
        <p className="text-2xl font-bold">{value}</p>
      </div>
      <span className="text-3xl opacity-50">{icon}</span>
    </div>
  );
};

export default Analytics;
