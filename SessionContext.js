import React, { createContext, useState, useContext, useEffect } from 'react';

const SessionContext = createContext();

export const UserSessionContext = () => useContext(SessionContext)

export const SessionProvider = ({ children }) => {
  const [currentUser, setCurrentUser] = useState()
  const [role, setRole] = useState('')
  const apiUrl=process.env.REACT_APP_API_URL

const checkSession = () => {
  return new Promise((resolve, reject) => {
    fetch(`${apiUrl}check_session`, {
      credentials: 'include'
    })
    .then(response => {
      if (response.ok) {
        return response.json();
      } else if (response.status === 401) {
        console.log('User is not logged in.');
        setCurrentUser(null)
        setRole('')
        return Promise.reject(new Error('Invalid session or role'))
      } else {
        throw new Error(`Session check failed with status: ${response.status}`);
      }
    })
    .then(data => {
      if (data.role === 'user' || data.role === 'owner') {
        setCurrentUser(data.details)
        setRole(data.role)
        resolve(data.details) // Resolve with the updated user details
      } else if (!data){
        reject(new Error('No data received'))
      } else {
        reject(new Error('No valid user role found'))
      }
    })
    .catch(error => {
      console.error('Error during session check:', error)
    })
  })
}
  useEffect(() => {
    checkSession()
  }, [])

  return (
    <SessionContext.Provider value={{ currentUser, role, setCurrentUser, setRole, checkSession }}>
      {children}
    </SessionContext.Provider>
  )
}

export default SessionContext;