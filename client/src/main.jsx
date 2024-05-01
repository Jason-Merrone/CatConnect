import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'
import './index.css'
import 'vite/modulepreload-polyfill'
import Trending from "./Trending.jsx"
import Post from "./Post.jsx"
import Catgpt from "./Catgpt.jsx"
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
        path: "/Post",
        element:<Post />
      },
      {
        path: "/Catgpt",
        element:<Catgpt />
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
