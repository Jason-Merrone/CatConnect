import { useState, useEffect } from 'react';
import './Profile.css';
import GetCookie from './GetCookie.jsx'

export default function Profile(){
    const [user, setUser] = useState(null);
    const [bio, setBio] = useState('');
    const [imageLink, setImageLink] = useState('');
    const [catBreed, setCatBreed] = useState('');
    const [loading, setLoading] = useState(true);
  
    useEffect(() => {
        const fetchData = async () => {
            const resUser = await fetch('/me/', { credentials: 'same-origin' });
            const userBody = await resUser.json();
            
            const resProfile = await fetch('/my_profile/', { credentials: 'same-origin' });
            const profileBody = await resProfile.json();
            
            // Assuming `userBody.user` and `profileBody.profile` can be merged
            const fullUserProfile = {
                ...userBody.user,
                ...profileBody.profile
            };
            
            setUser(fullUserProfile);
            setBio(fullUserProfile.bio);
            setCatBreed(fullUserProfile.cat_breed)
            setImageLink(fullUserProfile.link_to_pfp)
            setLoading(false);
        };

        fetchData();
    }, []);
  
    async function logout() {
      const res = await fetch("/registration/logout/", {
        credentials: "same-origin",
      });
      if (res.ok) {
        window.location = "/registration/sign_in/";
      }
    }

    const handleBioChange = (event) => {
        setBio(event.target.value);
    };

    const handlePfpChange = (event) => {
        setImageLink(event.target.value);
    };

    const handleBreedChange = (event) => {
        setCatBreed(event.target.value);
    };

    const updateBio = async () => {
        const csrfToken = GetCookie('csrftoken');
        const res = await fetch('/my_profile/', {
            method: 'POST',
            credentials: 'same-origin',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,
            },
            body: JSON.stringify({ bio })
        });

        if (res.ok) {
            console.log("Bio updated successfully!");
        } else {
            console.error("Failed to update bio");
        }
    };

    const updateCatBreed = async () => {
        const csrfToken = GetCookie('csrftoken');
        const res = await fetch('/my_profile/', {
            method: 'POST',
            credentials: 'same-origin',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,
            },
            body: JSON.stringify({ cat_breed: catBreed })
        });

        if (res.ok) {
            console.log("Breed updated successfully!");
        } else {
            console.error("Failed to update breed");
        }
    };

    const updatePfp = async () => {
        const csrfToken = GetCookie('csrftoken');
        const res = await fetch('/my_profile/', {
            method: 'POST',
            credentials: 'same-origin',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,
            },
            body: JSON.stringify({ link_to_pfp: imageLink})
        });

        if (res.ok) {
            console.log("Pfp updated successfully!");
        } else {
            console.error("Failed to update pfp");
        }
    };
  
    if (loading) {
        return <div>Loading...</div>;
    }
    return (
      <>
        <div id="greeting">{user.first_name} {user.last_name}'s Profile</div>

        <div id="change-bio">
            <label htmlFor="Bio">Bio:</label>
            <input id="bio" value={bio} onChange={handleBioChange} />
            <button onClick={updateBio} id="bio-update">Update</button>
        </div>

        <div id="change-breed">
            <label htmlFor="Cat-Breed">Cat Breed:</label>
            <input id="bio" value={catBreed} onChange={handleBreedChange} />
            <button onClick={updateCatBreed} id="bio-update">Update</button>
        </div>

        <div id="change-pfp">
        <label htmlFor="Image-Link">Link to PFP Image:</label>
        <input id="bio" value={imageLink} onChange={handlePfpChange} />
        <button onClick={updatePfp} id="pfp-update">Update</button>
        <div>
            {imageLink ? (
                <img className="img-profile" src={imageLink} alt="Profile Picture" />
            ) : (
                <div>No profile picture available</div>
            )}
        </div>
        </div>
        <button onClick={logout} id="logout">Logout</button>
      </>
    );
}