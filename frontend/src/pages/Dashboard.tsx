import React from 'react';
import { motion } from 'framer-motion';
import { 
  Users, 
  Calendar, 
  BarChart2 
} from 'lucide-react';

const Dashboard: React.FC = () => {
  return (
    <motion.div 
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.5 }}
      className="p-6 bg-gray-50 min-h-screen"
    >
      <h1 className="text-3xl font-bold mb-6 text-gray-800">Dashboard</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <DashboardCard 
          title="Connected Accounts" 
          value="3" 
          icon={<Users className="text-blue-500" />}
        />
        <DashboardCard 
          title="Tweets Scheduled" 
          value="12" 
          icon={<Calendar className="text-green-500" />}
        />
        <DashboardCard 
          title="Total Engagement" 
          value="5,342" 
          icon={<BarChart2 className="text-purple-500" />}
        />
      </div>
    </motion.div>
  );
};

interface DashboardCardProps {
  title: string;
  value: string;
  icon: React.ReactNode;
}

const DashboardCard: React.FC<DashboardCardProps> = ({ title, value, icon }) => {
  return (
    <div className="bg-white shadow-md rounded-lg p-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-gray-500 text-sm mb-2">{title}</h2>
          <p className="text-2xl font-bold text-gray-800">{value}</p>
        </div>
        <div className="text-4xl opacity-70">
          {icon}
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
