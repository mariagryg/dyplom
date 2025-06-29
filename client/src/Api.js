import {createContext} from "react";

const ApiUrlContext = createContext(null)

export const ApiProvider = ({ children }) =>{
    const apiUrl = process.env.REACT_APP_API_URL
    return (
        <ApiUrlContext.Provider value={apiUrl}> 
            {children}
        </ApiUrlContext.Provider>
    )
}

export default ApiUrlContext
