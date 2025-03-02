import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';
import moment from 'moment';

const PostList = () => {
  const [posts, setPosts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchPosts = async () => {
      try {
        const response = await axios.get('http://localhost:8000/api/posts');
        setPosts(response.data);
        setLoading(false);
      } catch (err) {
        setError('Failed to fetch posts');
        setLoading(false);
      }
    };

    fetchPosts();
  }, []);

  if (loading) return <div>Loading posts...</div>;
  if (error) return <div className="error">{error}</div>;

  return (
    <div className="post-list">
      {posts.length === 0 ? (
        <p>No posts yet. Create your first post!</p>
      ) : (
        posts.map(post => (
          <article key={post.id} className="post-preview">
            <h2><Link to={`/post/${post.slug}`}>{post.title}</Link></h2>
            <div className="post-meta">
              <time>{moment(post.created_at).format('MMMM D, YYYY')}</time>
            </div>
            <p className="post-excerpt">
              {post.content.substring(0, 150)}...
            </p>
            <Link to={`/post/${post.slug}`} className="read-more">
              Read More
            </Link>
          </article>
        ))
      )}
    </div>
  );
};

export default PostList;