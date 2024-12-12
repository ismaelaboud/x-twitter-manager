import React, { Suspense, lazy } from 'react'
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { AuthProvider } from './contexts/AuthContext'
import { ProtectedRoute } from './components/ProtectedRoute'
import Layout from './components/Layout'
import { Toaster } from 'react-hot-toast'

// Lazy load pages
const Dashboard = lazy(() => import('./pages/Dashboard'))
const Login = lazy(() => import('./pages/Login'))
const SignUp = lazy(() => import('./pages/SignUp'))
const AccountManager = lazy(() => import('./pages/AccountManager'))
const Analytics = lazy(() => import('./pages/Analytics'))
const TweetComposer = lazy(() => import('./pages/TweetComposer'))
const ScheduleManager = lazy(() => import('./pages/ScheduleManager'))
const Settings = lazy(() => import('./pages/Settings'))
const AITweetGenerator = lazy(() => import('./pages/AITweetGenerator'))

const App: React.FC = () => {
  return (
    <Router>
      <AuthProvider>
        <Suspense fallback={<div>Loading...</div>}>
          <Routes>
            <Route path="/login" element={<Login />} />
            <Route path="/signup" element={<SignUp />} />
            <Route element={<Layout />}>
              <Route 
                path="/dashboard" 
                element={
                  <ProtectedRoute>
                    <Dashboard />
                  </ProtectedRoute>
                } 
              />
              <Route 
                path="/accounts" 
                element={
                  <ProtectedRoute>
                    <AccountManager />
                  </ProtectedRoute>
                } 
              />
              <Route 
                path="/tweet-composer" 
                element={
                  <ProtectedRoute>
                    <TweetComposer />
                  </ProtectedRoute>
                } 
              />
              <Route 
                path="/ai-tweet-generator" 
                element={
                  <ProtectedRoute>
                    <AITweetGenerator />
                  </ProtectedRoute>
                } 
              />
              <Route 
                path="/schedule-manager" 
                element={
                  <ProtectedRoute>
                    <ScheduleManager />
                  </ProtectedRoute>
                } 
              />
              <Route 
                path="/analytics" 
                element={
                  <ProtectedRoute>
                    <Analytics />
                  </ProtectedRoute>
                } 
              />
              <Route 
                path="/settings" 
                element={
                  <ProtectedRoute>
                    <Settings />
                  </ProtectedRoute>
                } 
              />
              <Route 
                path="/" 
                element={<Navigate to="/dashboard" replace />} 
              />
            </Route>
          </Routes>
        </Suspense>
        {/* React Hot Toast Configuration */}
        <Toaster 
          position="top-right"
          toastOptions={{
            success: {
              style: {
                background: '#4CAF50',
                color: 'white',
              },
            },
            error: {
              style: {
                background: '#F44336',
                color: 'white',
              },
            },
          }}
        />
      </AuthProvider>
    </Router>
  )
}

export default App
