import React, { useState } from 'react';
import { 
  Home, 
  Send, 
  Calendar, 
  BarChart2, 
  Settings, 
  LogOut,
  X,
  Menu,
  Sparkles
} from 'lucide-react';
import { Link, useLocation, Outlet } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';

const Layout: React.FC = () => {
  const [isCollapsed, setIsCollapsed] = useState(true);
  const location = useLocation();

  const toggleSidebar = () => {
    setIsCollapsed(!isCollapsed);
  };

  const sidebarLinks = [
    { 
      name: 'Dashboard', 
      path: '/dashboard', 
      icon: <Home className="w-6 h-6" /> 
    },
    { 
      name: 'Tweet Composer', 
      path: '/tweet-composer', 
      icon: <Send className="w-6 h-6" /> 
    },
    { 
      name: 'AI Tweet Generator', 
      path: '/ai-tweet-generator', 
      icon: <Sparkles className="w-6 h-6 text-purple-500" /> 
    },
    { 
      name: 'Schedule Manager', 
      path: '/schedule-manager', 
      icon: <Calendar className="w-6 h-6" /> 
    },
    { 
      name: 'Analytics', 
      path: '/analytics', 
      icon: <BarChart2 className="w-6 h-6" /> 
    },
    { 
      name: 'Settings', 
      path: '/settings', 
      icon: <Settings className="w-6 h-6" /> 
    }
  ];

  return (
    <div className="flex h-screen bg-gray-50 text-gray-900">
      {/* Sidebar */}
      <div 
        className={`bg-white border-r shadow-md flex flex-col justify-between transition-all duration-300 ease-in-out ${
          isCollapsed ? 'w-[80px]' : 'w-[250px]'
        } ${isCollapsed ? 'items-center' : 'items-start'}`}
      >
        {/* Top Section */}
        <div className="w-full">
          {/* Logo or App Name */}
          <div className="p-4 border-b flex items-center justify-between">
            {!isCollapsed && (
              <h1 className="text-xl font-bold text-gray-800 opacity-0 transition-opacity duration-300 delay-200">X-Twitter Bot</h1>
            )}
            <button 
              onClick={toggleSidebar}
              className="text-gray-600 hover:text-gray-800 mx-auto"
            >
              {isCollapsed ? (
                <Menu className="w-6 h-6" />
              ) : (
                <X className="w-6 h-6" />
              )}
            </button>
          </div>

          {/* Navigation Links */}
          <nav className="mt-4 w-full">
            <AnimatePresence>
              {sidebarLinks.map((link) => (
                <motion.div
                  key={link.path}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ 
                    opacity: 1, 
                    x: !isCollapsed ? 0 : -20 
                  }}
                  exit={{ opacity: 0, x: -20 }}
                  transition={{ duration: 0.2 }}
                  className="w-full"
                >
                  <Link 
                    to={link.path}
                    className={`flex items-center p-3 hover:bg-gray-100 transition-colors group ${
                      location.pathname === link.path 
                        ? 'bg-blue-50 text-blue-600' 
                        : 'text-gray-600'
                    } ${isCollapsed ? 'justify-center' : 'justify-start'}`}
                    title={link.name}
                  >
                    <div className={`flex items-center ${isCollapsed ? 'mx-auto' : ''}`}>
                      {link.icon}
                      {!isCollapsed && (
                        <motion.span 
                          initial={{ opacity: 0, x: -10 }}
                          animate={{ opacity: 1, x: 0 }}
                          exit={{ opacity: 0, x: -10 }}
                          transition={{ duration: 0.2, delay: 0.1 }}
                          className="ml-3 text-sm whitespace-nowrap"
                        >
                          {link.name}
                        </motion.span>
                      )}
                    </div>
                  </Link>
                </motion.div>
              ))}
            </AnimatePresence>
          </nav>
        </div>

        {/* Bottom Section */}
        <div className="w-full border-t">
          {/* Logout */}
          <button 
            className="w-full flex items-center p-3 hover:bg-gray-100 text-red-600 hover:text-red-800 transition-colors justify-center"
            title="Logout"
          >
            <LogOut className="w-5 h-5" />
            {!isCollapsed && (
              <motion.span 
                initial={{ opacity: 0, x: -10 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: -10 }}
                transition={{ duration: 0.2, delay: 0.1 }}
                className="ml-3 text-sm"
              >
                Logout
              </motion.span>
            )}
          </button>
        </div>
      </div>

      {/* Main Content */}
      <main className="flex-1 overflow-y-auto bg-gray-50 p-6 text-gray-900">
        <React.Suspense fallback={<div>Loading...</div>}>
          <Outlet />
        </React.Suspense>
      </main>
    </div>
  );
};

export default Layout;
