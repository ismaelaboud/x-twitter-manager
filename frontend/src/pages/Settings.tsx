import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { 
  Bell, 
  Lock, 
  User, 
  Palette, 
  Shield 
} from 'lucide-react';

const Settings: React.FC = () => {
  const [notifications, setNotifications] = useState({
    tweets: true,
    directMessages: false,
    accountActivity: true
  });

  const [privacySettings, setPrivacySettings] = useState({
    profileVisibility: 'public',
    dataSharing: false
  });

  const handleNotificationToggle = (key: keyof typeof notifications) => {
    setNotifications(prev => ({
      ...prev,
      [key]: !prev[key]
    }));
  };

  return (
    <motion.div 
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.5 }}
      className="p-6 bg-gray-50 min-h-screen"
    >
      <h1 className="text-3xl font-bold mb-6 text-gray-800">Settings</h1>

      {/* Notifications */}
      <div className="bg-white shadow-md rounded-lg p-6 mb-6">
        <div className="flex items-center mb-4">
          <Bell className="mr-3 text-blue-500" />
          <h2 className="text-xl font-semibold text-gray-800">Notifications</h2>
        </div>
        
        <div className="space-y-4">
          {Object.entries(notifications).map(([key, value]) => (
            <div key={key} className="flex justify-between items-center">
              <span className="capitalize text-gray-700">{key.replace(/([A-Z])/g, ' $1')}</span>
              <label className="switch">
                <input 
                  type="checkbox" 
                  checked={value}
                  onChange={() => handleNotificationToggle(key as keyof typeof notifications)}
                />
                <span className="slider round"></span>
              </label>
            </div>
          ))}
        </div>
      </div>

      {/* Privacy & Security */}
      <div className="bg-white shadow-md rounded-lg p-6">
        <div className="flex items-center mb-4">
          <Shield className="mr-3 text-purple-500" />
          <h2 className="text-xl font-semibold text-gray-800">Privacy & Security</h2>
        </div>
        
        <div className="space-y-4">
          <div className="flex justify-between items-center">
            <div>
              <span className="text-gray-700">Profile Visibility</span>
              <p className="text-sm text-gray-500">Control who can see your profile</p>
            </div>
            <select 
              value={privacySettings.profileVisibility}
              onChange={(e) => setPrivacySettings(prev => ({
                ...prev, 
                profileVisibility: e.target.value
              }))}
              className="border p-2 rounded bg-white text-gray-700"
            >
              <option value="public">Public</option>
              <option value="private">Private</option>
            </select>
          </div>
          
          <div className="flex justify-between items-center">
            <div>
              <span className="text-gray-700">Data Sharing</span>
              <p className="text-sm text-gray-500">Allow analytics and usage tracking</p>
            </div>
            <label className="switch">
              <input 
                type="checkbox" 
                checked={privacySettings.dataSharing}
                onChange={() => setPrivacySettings(prev => ({
                  ...prev, 
                  dataSharing: !prev.dataSharing
                }))}
              />
              <span className="slider round"></span>
            </label>
          </div>
        </div>
      </div>
    </motion.div>
  );
};

export default Settings;
