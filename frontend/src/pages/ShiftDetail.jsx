import { useParams, useNavigate } from 'react-router-dom';
import { useState, useEffect } from 'react';
import axios from 'axios';

function ShiftDetail() {
    const { id } = useParams();
    const navigate = useNavigate();
    const [shift, setShift] = useState(null);
    const [assignment, setAssignment] = useState([]);
    const [userId, setUserId] = useState('');

    const token = localStorage.getItem('token');
    const headers = { Authorization: `Bearer ${token}` };

    useEffect(() => {
        axios.get(`/shifts/${id}`, {headers})
        .then(res => setShift(res.data))
        .catch(() => navigate('/dashboard'));

        axios.get(`/shifts/${id}/assignments`, {headers})
        .then(res => setAssignment(res.data))
        .catch(() => {});
    }, [id]);

    const handleAssign = async (e) => {
        try {
            e.preventDefault();
            await axios.post(`/shifts/${id}/assign/${userId}`, {}, { headers });
            const res = await axios.get(`/shifts/${id}/assignments`, { headers });
            setAssignment(res.data);
            setUserId('');
        } catch  (err) {
            alert(err.response?.data?.detail || 'Failed to Assign');
        }
    };

    const handleUnassign = async (assignedUserId) => {
        try {
            await axios.delete(`/shifts/${id}/unassign/${assignedUserId}`, { headers });
            const res = await axios.get(`/shifts/${id}/assignments`, { headers });
            setAssignment(res.data);
        } catch(err) {
            alert(err.response?.data?.detail || 'Failed to unassign');
        }
    };

    if (!shift) return <div>Loading...</div>

    return (
        <div>
            <button onClick={() => navigate('/dashboard')}>Back</button>
            <h2>{shift.facility_name}</h2>
            <p>Date: {shift.shift_date}</p>
            <p>Time: {shift.start_time} - {shift.end_time}</p>
            
            <h3>Assigned Staff</h3>
            { assignment.length == 0 && <p>No staff assigned yet</p>}
            { assignment.map(a => (
                <div key={a.id}>
                    <span>User ID: {a.user_id}</span>
                    <button onClick={() => handleUnassign(a.user_id)}>unassign</button>
                </div>
            ))}

            <h3>Assign Staff</h3>
            <form onSubmit={handleAssign}>
                <input
                    type="number"
                    placeholder="Enter User ID"
                    value={userId}
                    onChange={(e) => setUserId(e.target.value)}
                    required
                />
                <button type='submit'>Assign</button>
            </form>
        </div>
    )
};

export default ShiftDetail;