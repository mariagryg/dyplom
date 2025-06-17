import React, { useContext, useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { UserSessionContext } from './SessionContext';
import ApiUrlContext from '../Api';
import LoadingPage from '../ExtraPageComponents/LoadingPage';
import Reviews from '../ReviewComponents/Reviews';
import EquipmentMap from '../MapComponents/EquipmentMap';

const ProfilePage = ({ fromOwnerDash, setFromOwnerDash }) => {
  const { currentUser, role, checkSession } = useContext(UserSessionContext);
  const apiUrl = useContext(ApiUrlContext);
  const { id } = useParams();
  const navigate = useNavigate();

  const [profileData, setProfileData] = useState({});
  const [isFavorited, setIsFavorited] = useState(false);
  const [loading, setLoading] = useState(true);
  const [ownerReviews, setOwnerReviews] = useState([]);
  const [heartColor, setHeartColor] = useState('white');

  // Fetch user profile
  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const res = await fetch(`${apiUrl}user/${id}`);
        const data = await res.json();
        setProfileData(data);
        const favorite = currentUser?.owner_favorite?.some(fav => fav.user_id === +id);
        setIsFavorited(favorite);
        setHeartColor(favorite ? 'red' : 'white');
      } catch (err) {
        console.error('Error fetching profile:', err);
      } finally {
        setLoading(false);
      }
    };
    fetchProfile();
  }, [id, apiUrl, currentUser]);

  // Calculate review and agreement counts
  const getReviewCount = profileData?.review?.filter(r => r.reviewer_type === 'user').length || 0;
  const getAgreementCount = profileData?.cart?.reduce((count, cart) => {
    return count + (cart.cart_item?.filter(item => item.agreements?.some(agr => agr.agreement_status === 'both-accepted')).length || 0);
  }, 0);

  const { firstName, lastName, email, phone, address, city, state, postal_code, profileImage, review } = profileData || {};
  const userLocation = `${address}, ${city}, ${state} ${postal_code}`;

  useEffect(() => {
    setOwnerReviews(review?.filter(r => r.reviewer_type === 'owner') || []);
  }, [review]);

  // Handle favorite selection
  const toggleFavorite = async () => {
    const method = isFavorited ? 'DELETE' : 'POST';
    const url = isFavorited
      ? `${apiUrl}remove/owner/${currentUser.id}/favorite/user/${id}`
      : `${apiUrl}owner/${currentUser.id}/favorite/user/${id}`;

    try {
      const res = await fetch(url, {
        method,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ owner_id: currentUser.id, user_id: id }),
      });
      if (!res.ok) throw new Error('Failed to update favorite status');
      setIsFavorited(prev => !prev);
      setHeartColor(prev => (prev === 'white' ? 'red' : 'white'));
      checkSession();
    } catch (error) {
      console.error('Error toggling favorite:', error);
    }
  };

  // Navigate back to dashboard
  const goBackToDashboard = () => {
    setFromOwnerDash(prev => !prev);
    navigate('/dashboard');
  };

  // Loading state
  if (loading) return <LoadingPage loadDetails="Loading User Profile..." />;

  // Render user reviews
  const reviews = ownerReviews.length
    ? ownerReviews.map((reviewItem) => <Reviews key={reviewItem.id} {...reviewItem} />)
    : <div>No reviews available.</div>;

  return (
    <div className="profile-container">
      <div className="profile-header">
        <img src={profileImage} alt={`${firstName} ${lastName}`} className="profile-img" />
        <div className="profile-details">
          <h2>{firstName} {lastName}</h2>
          <p>{userLocation}</p>
          <p>{email}</p>
          <p>Phone: {phone}</p>

          {currentUser && role !== 'user' && currentUser.id !== profileData.id && (
            <button className="favorite-btn" onClick={toggleFavorite}>
              <svg
                fill={heartColor}
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth="2"
                className="heart-icon"
                viewBox="0 0 24 24"
              >
                <path d="M20.84 4.61a5.5 5.5 0 00-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 00-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 000-7.78z"></path>
              </svg>
            </button>
          )}
        </div>
      </div>

      <div className="profile-stats">
        <div className="stat-item">
          <span>{getAgreementCount}</span>
          <span>Rentals</span>
        </div>
        <div className="stat-item">
          <span>{profileData?.user_inboxes?.length}</span>
          <span>Connections</span>
        </div>
        <div className="stat-item">
          <span>{getReviewCount}</span>
          <span>Reviews</span>
        </div>
      </div>

      <div className="reviews-section">
        <h3>Owner Reviews</h3>
        {reviews}
      </div>

      <div className="map-section">
        <EquipmentMap location={userLocation} userDisplayHeight={300} userDisplayWidth={1500} userDisplayZoom={8} />
      </div>

      {fromOwnerDash && (
        <button className="back-to-dash-btn" onClick={goBackToDashboard}>
          Return to Dashboard
        </button>
      )}
    </div>
  );
};

export default ProfilePage;
