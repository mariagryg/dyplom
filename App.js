import React, { useContext, useState, useEffect } from 'react';
import { useNavigate, Route, Routes } from 'react-router-dom';

import './App.css';
//---------------------Homepage / Navbar / Footer-------------
import HomePage from './HomePageComponents/HomePage';
import NavBar from './HeaderFooterComponents/NavBar';
import Footer from './HeaderFooterComponents/Footer'

//---------------------Collections--------------------
import ProductCollection from './EquipmentComponents/ProductCollection';
import OwnerCollection from './OwnerComponents/OwnerCollection';
import RentalAgreementsCollection from './RentalComponents/RentalAgreementsCollection'
import UserCollection from './UserComponents/UserCollection';

//-------------------------Display Pages-----------------------------------
import ProductDisplay from './EquipmentComponents/ProductDisplay';
import OwnerDisplay from './OwnerComponents/OwnerDisplay';

//-------------------------UserForms----------------------------------------
import UserForm from './UserComponents/UserForm';

//-------------------------OwnerForms---------------------------------------
import OwnerForm from './OwnerComponents/OwnerForm';
import OwnerEditForm from './OwnerComponents/OwnerEditForm'

//------------------------ProductForm-------------------------------------
import ProductForm from './EquipmentComponents/ProductForm';
import ProductEditForm from './EquipmentComponents/ProductEditForm';
import RentalForm from './RentalComponents/RentalForm';
import OwnerEquipmentListing from './RentalComponents/OwnerEquipmentListing'

//----------------------User Login Functionality-----------------------------
import UserLogin from './UserComponents/UserLogin';
import { UserProvider } from './UserComponents/UserContext';

//----------------------Owner Login Functionality-----------------------------
import OwnerLogin from './OwnerComponents/OwnerLogin';
import { OwnerProvider } from './OwnerComponents/OwnerContext';

//----------------------API Functionality-----------------------------
import { ApiProvider } from './Api';

//----------------------Check Session Context -----------------------------
import { SessionProvider } from './UserComponents/SessionContext';

//---------------------- Calculate # of items ready for checkout Context -----------------------------
import { CartTotalNumbProvider } from './CheckoutComponents/AvailToCheckoutContext';

//----------------------Bar Chart Data Session Context -----------------------------
import {EquipmentDataProvider} from './ChartComponents/BarChartDataContext';

//----------------------User Functionality-----------------------------
import UserProfile from './UserComponents/UserProfile';
import UserCard from './UserComponents/UserCard';

//----------------------Owner Dashboard-----------------------------
import OwnerDashboard from './OwnerComponents/OwnerDashboardComponents/OwnerDashboard';


//----------------------Temporary Calendar-----------------------------
import Calendar from './CalendarComponents/Calendar';


//----------------------Temporary File Uploader for Equipment Images-----------------------------
import EquipmentImageFileUpload from './EquipmentComponents/EquipmentImageFileUpload' 
import ProductImageForm from './EquipmentComponents/ProductImageForm';
import BulkEquipmentUpload from './EquipmentComponents/BulkEquipmentUpload';

//---------------------- Messaging Component-----------------------------
import NewMessageThreads from './MessagingComponents/NewMessageThreads';

//---------------------- Checkout -----------------------------
// import Checkout from './CheckoutComponents/Checkout';
import StripeCheckout from './CheckoutComponents/StripeCheckout';
import AfterCheckout from './CheckoutComponents/AfterCheckout';
import Cart from './CheckoutComponents/Cart';
import OrderHistory from './CheckoutComponents/OrderHistory';

//---------------------- Rental Agreement Display -----------------------------
import RentalAgreementDisplay from './RentalComponents/RentalAgreementDisplay'

//---------------------- Extra Pages -----------------------------
import AboutUsPage from './ExtraPageComponents/AboutUs';
import CookiesPolicy from './ExtraPageComponents/Cookies';
import TermsAndConditionsPage from './ExtraPageComponents/TermsAndConditions';
import ContactUsPage from './ExtraPageComponents/ContactPage';

//---------------------- Toastify -----------------------------
import { ToastContainer, toast } from 'react-toastify'
import 'react-toastify/dist/ReactToastify.css';



function App() {

  const navigate = useNavigate()


  const [currentUser, setCurrentUser] = useState([])
  const [role, setRole] = useState('')

  const [equipmentArray, setEquipmentArray] = useState([])
  const [searchTerm, setSearchTerm] = useState("")

  const [users, setUsers] = useState([])
  const [owners, setOwners] = useState([])
  const [rentalAgreement, setRentalAgreement] = useState([])

  const [ownerToEdit, setOwnerToEdit] = useState([])
  const [equipmentToEdit, setEquipmentToEdit] = useState([])
  const [featuredRental, setFeaturedRental] = useState([])

  const [fromOwnerDash, setFromOwnerDash] = useState(false)


  const apiUrl = process.env.REACT_APP_API_URL
  


  useEffect(() => {
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
      } else {
      }
    })
    .then(data => {
      if (data.role === 'user' || data.role === 'owner') {
        setCurrentUser(data.details)
        setRole(data.role)
      } else if (!data){
      } else {
        console.log("No valid role found!")
      }
    })
    .catch(error => {
    })
  }, [apiUrl, setCurrentUser])
  
  useEffect(() => {
    fetch(`${apiUrl}equipment`)
      .then((resp) => resp.json())
      .then((data) => {
        setEquipmentArray(data)
      })
  }, [])

  const addEquipment = (equipment) => {
    setEquipmentArray(equipmentArray => [...equipmentArray, equipment])
  }


  useEffect(() => {
    fetch(`${apiUrl}users`)
      .then((resp) => resp.json())
      .then((data) => {
        setUsers(data)
      })
  }, [])

  const addUser = (user) => {
    setUsers(users => [...users, user])
  }

  useEffect(() => {
    fetch(`${apiUrl}equipment_owners`)
      .then((resp) => resp.json())
      .then((data) => {
        setOwners(data)
      })
  }, [])

  const addOwner = (owner) => {
    setOwners(owners => [...owners, owner])
  }

    const deleteOwner = (ownerToDelete) => {
      setOwners(owners =>
        owners.filter(owner => owner.id !== ownerToDelete.id))
    }
  
  
    const handleOwnerDelete = (owner) => {
      fetch(`${apiUrl}equipment_owner/${owner.id}`, {
        method: "DELETE"
      })
        .then(() => {
          deleteOwner(owner)
          navigate('/equipment_owners')
        })
    }

  const updateOwner = (ownerToUpdate) => {
    setOwners(owners => owners.map(owner => {
      if (owner.id === ownerToUpdate.id) {
        return ownerToUpdate
      } else {
        return owner
      }
    }))
  }

  const handleEditOwner = (owner) => {
    setOwnerToEdit(owner)
    navigate(`/owner/${owner.id}/edit`)
  }


  const addRentalAgreement = (rentalAgreement) => {
    setRentalAgreement(rentalAgreements => [...rentalAgreements, rentalAgreement])
  }


  const updateEquipment = (equipmentToUpdate) => {
    setEquipmentArray(equipments => equipments.map(equipment => {
      if (equipment.id === equipmentToUpdate.id) {
        return equipmentToUpdate
      } else {
        return equipment
      }
    }))

  }

  const handleEditEquipment = (equipment) => {
    setEquipmentToEdit(equipment)
    navigate(`/equipment/${equipment.id}/edit`)
  }



  const deleteEquipment = (equipmentToDelete) => {
    setEquipmentArray(equipments =>
      equipments.filter(equipment => equipment.id !== equipmentToDelete.id))
  }

  const handleEquipmentDelete = (equipment) => {
    fetch(`${apiUrl}equipment/${equipment.id}`, {
      method: "DELETE"
    })
      .then(() => {
        deleteEquipment(equipment)
        navigate('/equipment')
      })
  }

  let actualEquipmentArray = Array.isArray(equipmentArray) ? equipmentArray : Object.values(equipmentArray)
  const filteredEquipmentArray = actualEquipmentArray?.filter((item) => {
    return item.model?.toLowerCase().includes(searchTerm?.toLowerCase()) || item.location?.toLowerCase().includes(searchTerm?.toLowerCase()) || item.make?.toLowerCase().includes(searchTerm?.toLowerCase()) || item.name?.toLowerCase().includes(searchTerm?.toLowerCase())
  })

  return (
    <SessionProvider>
      <CartTotalNumbProvider>
      <EquipmentDataProvider>
        <ApiProvider>
        <>
          <NavBar setSearchTerm={setSearchTerm} />

          <Routes>
            {/* Home Page */}
            <Route path='/' element={<HomePage equipmentArray={equipmentArray} setFeaturedRental={setFeaturedRental} />} />

            {/* COLLECTION ROUTES */}
            <Route path='/equipment' element={<ProductCollection equipmentArray={filteredEquipmentArray} handleEquipmentDelete={handleEquipmentDelete} handleEditEquipment={handleEditEquipment} />} />
            <Route path='/equipment_owners' element={<OwnerCollection searchTerm={searchTerm} handleEditOwner={handleEditOwner} handleOwnerDelete={handleOwnerDelete} equipmentOwnerArray={owners} />} />
            <Route path='/rental_agreements' element={<RentalAgreementsCollection />} />
            <Route path='/users' element={<UserCollection searchTerm={searchTerm} users={users}/>} />
    
            {/* ID / INDIVIDUAL / DISPLAY ROUTES */}
            <Route path='/equipment/:id' element={<ProductDisplay/>} />
            <Route path='/equipment_owner/:id' element={<OwnerDisplay setFromOwnerDash={setFromOwnerDash} fromOwnerDash={fromOwnerDash}/>} />

            {/* Respective Posts */}
            <Route path='/renter_signup' element={<UserForm addUser={addUser} />} />
            <Route path='/owner_signup' element={<OwnerForm addOwner={addOwner} />} />
            {/* need to rename the below to equipment_post */}
            <Route path='/list_equipment' element={<ProductForm addEquipment={addEquipment} />} />

            {/* Starting rentals, likely just going to use the prepop as it makes more sense than to do a "rental signup", in which a user sifts through all of the owners lol. This might not be the worst idea to incorporate into a search though. For example, filter by location, and then equipment type. The owner shouldn't really matter. But we can take into consideration the owners reviews / ratings and filter by lets say 3+ star renters. */}
            {/* I definitely don't need both of these. Likely going to remove OwnerEquipMentListing */}
            <Route path='/rental_signup' element={<RentalForm addRentalAgreement={addRentalAgreement} owners={owners} equipmentArray={equipmentArray} />} />
            {/* <Route path='/rental_signup_prepop' element={<OwnerEquipmentListing addRentalAgreement={addRentalAgreement} owners={owners} equipmentArray={equipmentArray} featuredRental={featuredRental} />} /> */}
            {/* Rename this too ^^^ */}

            {/* Respective Edit Routes */}
            <Route path='/owner/:id/edit' element={<OwnerEditForm ownerToEdit={ownerToEdit} updateOwner={updateOwner} />} />
            <Route path='/equipment/:id/edit' element={<ProductEditForm equipmentToEdit={equipmentToEdit} updateEquipment={updateEquipment} setEquipmentArray={setEquipmentArray} />} />

            {/* Login Page Route */}
            <Route path='/login' element={<UserLogin/>} />
            {/* <Route path='/owner/login' element={<OwnerLogin />} /> */}

            {/* User Profile Page*/}
            <Route path='/user/profile/:id' element={<UserProfile setFromOwnerDash={setFromOwnerDash} fromOwnerDash={fromOwnerDash}/>} />

            {/* Temp Route for CSV File Upload*/}
            <Route path='/temp/bulk_equipment_upload' element={<BulkEquipmentUpload setEquipmentArray={setEquipmentArray}/>} />

            {/* Owner Dashboard Page
            Likely converting this to just a general dashboard. Dashboards for everyone!
            */}
            <Route path='/dashboard' element={<OwnerDashboard updateOwner={updateOwner} ownerToEdit={ownerToEdit} fromOwnerDash={fromOwnerDash} setFromOwnerDash={setFromOwnerDash} searchTerm={searchTerm}/>} />

            {/* Temporary calendar routing */}
            <Route path='/calendar' element={<Calendar />} />

            {/* Temporary file upload routing */}
            <Route path='/temp/upload' element={<EquipmentImageFileUpload />} />
            <Route path='/temp/equipment/upload' element={<ProductImageForm />} />

            {/* Messaging routing  */}
            <Route path='/messaging' element={<NewMessageThreads fromOwnerDash={fromOwnerDash} setFromOwnerDash={setFromOwnerDash}/>} />
            <Route path='/user/card/:id' element={<UserCard/>} />

            {/* Temporary Checkout Routing */}
            <Route path='/checkout' element={<StripeCheckout/>} />
            <Route path='/checkout/successful/return' element={<AfterCheckout/>} />
            <Route path='/cart' element={<Cart/>} />
            <Route path='/order/history' element={<OrderHistory/>}/>

            {/* Rental Display */}
            <Route path='/handle/agreements/:rental_agreement_id' element={<RentalAgreementDisplay/>} />

            {/* Extra pages like contact us, cookies, about us, etc */}
            <Route path='/about/us' element={<AboutUsPage/>} />
            <Route path='/cookies' element={<CookiesPolicy/>} />
            <Route path='/terms/and/conditions' element={<TermsAndConditionsPage/>} />
            <Route path='/contact/us' element={<ContactUsPage/>} />
            

          </Routes>
          <ToastContainer
          position="bottom-right"
          autoClose={3000}
          hideProgressBar={false}
          newestOnTop={false}
          closeOnClick
          rtl={false}
          pauseOnFocusLoss
          draggable
          pauseOnHover
          theme="light"
          />

          <Footer />
        </>
        </ApiProvider>
      </EquipmentDataProvider>
      </CartTotalNumbProvider>
    </SessionProvider>
  );
}

export default App;
