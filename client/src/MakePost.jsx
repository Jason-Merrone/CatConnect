import GetCookie from './GetCookie.jsx'
import './MakePost.css';
import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';

export default function MakePost(){     
    const [imageLink, setImageLink] = useState('');     
    const [caption, setCaption] = useState('');     
    // Set character limit
    const MAX_CAPTION_LENGTH = 150;

    const handleImgChange = (event) => {        
        setImageLink(event.target.value);    
    };    

    const handleCaptionChange = (event) => {
        // Limit caption length
        if (event.target.value.length <= MAX_CAPTION_LENGTH) {
            setCaption(event.target.value);
        }    
    };    

    const submit = async () => {        
        const csrfToken = GetCookie('csrftoken');        
        const res = await fetch('/make_post/', {            
            method: 'POST',            
            credentials: 'same-origin',            
            headers: {                
                'Content-Type': 'application/json',                
                'X-CSRFToken': csrfToken,            
            },            
            body: JSON.stringify({                
                caption: caption,                
                link_to_image: imageLink,                
                likes: 0            
            })        
        });        
        if (res.ok) {            
            console.log("Submission successful!");        
        } else {            
            console.error("Submission failed");        
        }    
    };    

    return (    
        <>        
            <div id="new-post">New Post</div>        
            <div id="make-caption">
                <label htmlFor="Caption">Caption: </label>       
                <input 
                    id="bio" 
                    value={caption} 
                    onChange={handleCaptionChange} 
                    maxLength={MAX_CAPTION_LENGTH} // Set maxLength attribute
                /> 
                {/* Display remaining characters */}
                <span>{caption.length}/{MAX_CAPTION_LENGTH}</span>       
            </div>        
            <div>            
                <label htmlFor="Image-Link">Link to image: </label>            
                <input id="bio" value={imageLink} onChange={handleImgChange} />        
            </div>        
            <div>            
                {imageLink ? (                
                    <img className="img" src={imageLink} alt="No image detected" />            
                ) : (                
                    <div>No image detected</div>            
                )}        
            </div>        
            <Link to="/MyPosts">            
                <button onClick={submit} id="pfp-update">Upload</button>        
            </Link>    
        </>    
    );
}