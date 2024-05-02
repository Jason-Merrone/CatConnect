import '@fontsource/material-icons';
import React, { useState, useEffect } from "react";
import './MyPosts.css';

export default function MyPosts() {
    const [posts, setPosts] = useState([]);

    useEffect(() => {
        async function getMyPosts() {
            const response = await fetch('/user_posts/', {
                method: 'GET',
                credentials: 'include'
            });
            const data = await response.json();
            setPosts(data.posts);
        }
        getMyPosts();
    }, []);

    // Function to extract and format the date
    const formatDate = (dateString) => {
        const date = new Date(dateString);
        return date.toLocaleDateString(); // Adjust formatting as needed
    };

    return (
        <>
            <div>
                <ul>
                    {posts.map((post, index) => (
                        <div id="user-posts" key={index}>
                            <div className="user-info">
                                <img className="profile-pic" src={post.profile_picture} alt="Profile" />
                                <span className="username">{post.username} </span>
                                <span className="date"> {formatDate(post.created_at)}</span> 
                            </div>
                            <img className="post-image" src={post.link_to_image} alt="Post Image Not Available" />
                            <div id="descriptions">
                                <div className="post-caption">{post.caption}</div>
                                <div id="post-likes">
                                    <span className="icons">thumb_up</span>
                                    {post.likes}
                                </div>
                            </div>
                        </div>
                    ))}
                </ul>
            </div>
        </>
    );
}