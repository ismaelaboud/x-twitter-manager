import React, { useState } from 'react';
import { motion } from 'framer-motion';

interface TwitterAccount {
  username: string;
  apiKey: string;
  apiSecret: string;
  accessToken: string;
  accessTokenSecret: string;
}

const AccountManager: React.FC = () => {
  const [accounts, setAccounts] = useState<TwitterAccount[]>([]);
  const [newAccount, setNewAccount] = useState<TwitterAccount>({
    username: '',
    apiKey: '',
    apiSecret: '',
    accessToken: '',
    accessTokenSecret: ''
  });

  const handleAddAccount = () => {
    if (newAccount.username && newAccount.apiKey) {
      setAccounts([...accounts, newAccount]);
      // Reset form
      setNewAccount({
        username: '',
        apiKey: '',
        apiSecret: '',
        accessToken: '',
        accessTokenSecret: ''
      });
    }
  };

  return (
    <motion.div 
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.5 }}
      className="p-6 bg-gray-100 min-h-screen"
    >
      <h1 className="text-3xl font-bold mb-6">Account Management</h1>
      
      {/* Add Account Form */}
      <div className="bg-white shadow-md rounded-lg p-6 mb-6">
        <h2 className="text-xl font-semibold mb-4">Add Twitter Account</h2>
        <div className="grid grid-cols-2 gap-4">
          <input 
            type="text" 
            placeholder="Username" 
            value={newAccount.username}
            onChange={(e) => setNewAccount({...newAccount, username: e.target.value})}
            className="border p-2 rounded"
          />
          <input 
            type="text" 
            placeholder="API Key" 
            value={newAccount.apiKey}
            onChange={(e) => setNewAccount({...newAccount, apiKey: e.target.value})}
            className="border p-2 rounded"
          />
          <input 
            type="text" 
            placeholder="API Secret" 
            value={newAccount.apiSecret}
            onChange={(e) => setNewAccount({...newAccount, apiSecret: e.target.value})}
            className="border p-2 rounded"
          />
          <input 
            type="text" 
            placeholder="Access Token" 
            value={newAccount.accessToken}
            onChange={(e) => setNewAccount({...newAccount, accessToken: e.target.value})}
            className="border p-2 rounded"
          />
          <input 
            type="text" 
            placeholder="Access Token Secret" 
            value={newAccount.accessTokenSecret}
            onChange={(e) => setNewAccount({...newAccount, accessTokenSecret: e.target.value})}
            className="border p-2 rounded col-span-2"
          />
          <button 
            onClick={handleAddAccount}
            className="bg-blue-500 text-white p-2 rounded col-span-2"
          >
            Add Account
          </button>
        </div>
      </div>

      {/* Accounts List */}
      <div className="bg-white shadow-md rounded-lg p-6">
        <h2 className="text-xl font-semibold mb-4">Connected Accounts</h2>
        {accounts.length === 0 ? (
          <p className="text-gray-500">No accounts connected</p>
        ) : (
          <ul>
            {accounts.map((account, index) => (
              <li 
                key={index} 
                className="flex justify-between items-center border-b p-3"
              >
                <span>{account.username}</span>
                <button 
                  className="text-red-500 hover:bg-red-100 p-2 rounded"
                  onClick={() => setAccounts(accounts.filter((_, i) => i !== index))}
                >
                  Remove
                </button>
              </li>
            ))}
          </ul>
        )}
      </div>
    </motion.div>
  );
};

export default AccountManager;
