import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'
import './index.css'
import 'vite/modulepreload-polyfill'
import Trending from "./Trending.jsx"
import MakePost from "./MakePost.jsx"
import MyPosts from "./MyPosts.jsx"
import Profile from "./Profile.jsx"
import {
  createHashRouter,
  RouterProvider
} from 'react-router-dom';

const router = createHashRouter([
  {
    path: "/",
    element: <App />,
    children: [
      {
        path: "/",
        element:<Trending />
      },
      {
        path: "/MakePost",
        element:<MakePost />
      },
      {
        path: "/MyPosts",
        element:<MyPosts />
      },
      {
        path: "/Profile",
        element:<Profile />
      }
    ]
  }
]);

ReactDOM.createRoot(document.getElementById('root')).render(
  <RouterProvider router = {router} />
)
