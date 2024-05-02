import '@fontsource/material-icons';
import { Link } from 'react-router-dom';
import './Banner.css';

export default function Banner() {
    return (
        <>
          <nav id="navbar">
            <section id="navbar-title">
                CatConnect
            </section>
            <section id="navbar-links">
                <Link to="/" className="button-link">
                    <button className="navbar-link">
                        <span className="icons">show_chart</span>
                        Trending
                    </button>
                </Link>
                <Link to="/MakePost" className="button-link">
                    <button className="navbar-link">
                        <span className="icons">center_focus_strong</span>
                        New Post
                    </button>
                </Link>
                <Link to="/MyPosts" className="button-link">
                    <button className="navbar-link">
                        <span className="icons">save</span>
                        My Posts
                    </button>
                </Link>
                <Link to="/Profile" className="button-link">
                    <button className="navbar-link">
                        <span className="icons">pets</span>
                        Profile
                    </button>
                </Link>
            </section>
        </nav> 
    </>);
}