import React, { useState, useEffect } from "react";
import './MyPosts.css'; // Using the same stylesheet for styling consistency
import GetCookie from "./GetCookie";

function formatDate(dateString) {
    const options = { year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit' };
    return new Date(dateString).toLocaleDateString(undefined, options);
}

export default function Trending() {
    const [trendingPosts, setTrendingPosts] = useState([]);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        async function getTrendingPosts() {
            try {
                const response = await fetch('/trending/', {
                    method: 'GET',
                    credentials: 'include',
                    headers: {
                        'Accept': 'application/json',
                        'Content-Type': 'application/json'
                    }
                });
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                const data = await response.json();
                setTrendingPosts(data.posts);
            } catch (error) {
                setError(error);
            } finally {
                setIsLoading(false);
            }
        }
        getTrendingPosts();
    }, []);

    if (isLoading) {
        return <div>Loading...</div>;
    }
    if (error) {
        return <div>Error: {error.message}</div>;
    }

    const handleLike = async (postId) => {
        const csrfToken = GetCookie('csrftoken');  // Retrieve CSRF token from cookies
        try {
            const response = await fetch(`/toggle_like_post/${postId}/`, {
                method: 'POST',
                credentials: 'include',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken  // Include the CSRF token in the request headers
                }
            });
            if (!response.ok) {
                throw new Error(`Network response was not ok: ${response.statusText}`);
            }
            const updatedPost = await response.json();
            setTrendingPosts(trendingPosts.map(post => {
                if (post.id === postId) {
                    return { ...post, likes: updatedPost.likes, liked_by_user: !post.liked_by_user };
                }
                return post;
            }));
        } catch (error) {
            console.error('Failed to toggle like on the post:', error);
        }
    };

    return (
        <div>
            <ul>
                {trendingPosts.map((post) => (
                    <li className="post-item" key={post.id} id="user-posts">
                        <div className="user-info">
                            <img className="profile-pic" src={post.profile_picture} alt="Profile" />
                            <span className="username">{post.username}</span>
                            <span className="date">{formatDate(post.created_at)}</span>
                        </div>
                        <div className="bio-container">User bio: {post.bio}</div>
                        <img className="post-image" src={post.link_to_image} alt="Post Image" />
                        <div id="descriptions">
                            <div className="caption-container">Caption: {post.caption}</div>
                            <div id="post-likes">
                                <button 
                                    id="like-button" 
                                    className={`icons ${post.liked_by_user ? 'liked' : 'not-liked'}`} 
                                    onClick={() => handleLike(post.id)}
                                    >
                                    thumb_up
                                </button>
                                <div id="num-likes">{post.likes}</div>
                            </div>
                        </div>
                    </li>
                ))}
            </ul>
        </div>
    );
}
