import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { UserSessionContextProvider } from './SessionContext';
import { ApiUrlContextProvider } from '../Api';
import ProfilePage from './ProfilePage';
import Dashboard from './Dashboard';
import NotFound from './NotFound';
import NavBar from './NavBar';
import Footer from './Footer';
import LoadingPage from '../ExtraPageComponents/LoadingPage';
import { checkSessionStatus } from '../utils/auth';

const App = () => {
  const [loading, setLoading] = useState(true);
  const [fromOwnerDash, setFromOwnerDash] = useState(false);
  const [currentUser, setCurrentUser] = useState(null);

  useEffect(() => {
    const fetchSession = async () => {
      try {
        const session = await checkSessionStatus(); // Your API call for session check
        setCurrentUser(session.user);
        setLoading(false);
      } catch (err) {
        console.error('Error checking session:', err);
        setLoading(false);
      }
    };

    fetchSession();
  }, []);

  // If still loading, show loading page
  if (loading) return <LoadingPage loadDetails="Loading Application..." />;

  return (
    <UserSessionContextProvider value={{ currentUser, setCurrentUser }}>
      <ApiUrlContextProvider value={{ apiUrl: process.env.REACT_APP_API_URL }}>
        <Router>
          <NavBar />
          <main>
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route
                path="/user/:id"
                element={<ProfilePage fromOwnerDash={fromOwnerDash} setFromOwnerDash={setFromOwnerDash} />}
              />
              <Route path="*" element={<NotFound />} />
            </Routes>
          </main>
          <Footer />
        </Router>
      </ApiUrlContextProvider>
    </UserSessionContextProvider>
  );
};

export default App;
