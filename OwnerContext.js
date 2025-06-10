import {createContext, useState} from "react";

const OwnerContext = createContext(null)

export const OwnerProvider = ({ children }) =>{

    const [owner, setOwner] = useState(null)

    return (
        <OwnerContext.Provider value={[owner, setOwner]}> 
            {children}
        </OwnerContext.Provider>
    );
}

export default OwnerContext