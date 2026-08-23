import { useState } from "react";
import { useNavigate } from "react-router-dom";
import toast from "react-hot-toast";
import axios from 'axios';
function LoginPage() {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate();

    const handleLogin = async (e) => {
        e.preventDefault();
        setLoading(true);
        try {
            const payload = {email: email, password: password};
            const res = await axios.post('/auth/login', payload);
            toast.success('Login successful');
            localStorage.setItem('token', res.data.access_token)
            navigate('/dashboard')

        } catch(err)  {
            toast.error(err.response?.data?.message || 'Login failed');
        } finally {
            setLoading(false);
        }

    };
    return (
     <div>
        <h2>Login</h2>
        <form onSubmit={handleLogin}>
            <input
                type="email"
                placeholder="Email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
            />
            <input
                type="password"
                placeholder="Password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
            />
            <button type="submit" disabled={loading}>
                {loading? 'Logging in...' : 'Login'}
            </button>
        </form>
     </div>   
    )
};

export default LoginPage;