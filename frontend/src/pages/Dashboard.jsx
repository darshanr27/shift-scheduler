import { useNavigate } from "react-router-dom";
import { useState, useEffect } from "react";
import axios from "axios";

function Dashboard() {
    const navigate = useNavigate();
    const [shifts, setShift] = useState([]);
    const [showForm, setShowForm] = useState(false);

    const [facilityName, setFacilityName] = useState('');
    const [shiftDate, setShiftDate] = useState('');
    const [startTime, setStartTime] = useState('');
    const [endTime, setEndTime] = useState('');
    const [currentUser, setCurrentUser] = useState(null);
    const [assignments, setAssignment] = useState([])

    useEffect(() => {
        const token = localStorage.getItem('token')
        const headers = { Authorization: `Bearer ${token}` };

        axios.get('/auth/me', { headers })
            .then(res => setCurrentUser(res.data))
            .catch(() => navigate('/'));

        axios.get('/shifts', { headers })
            .then(res => setShift(res.data))
            .catch(() => navigate('/'));
    }, []);

    // Second useEffect — runs only after currentUser is set
    useEffect(() => {
        if (!currentUser) return;
        const token = localStorage.getItem('token');
        const headers = { Authorization: `Bearer ${token}` };

        axios.get(`/users/${currentUser.id}/shifts`, { headers })
            .then(async (res) => {
                const assignmentWithShifts = await Promise.all(
                    res.data.map(async (a) => {
                        const shiftRes = await axios.get(`/shifts/${a.shift_id}`, { headers });
                        return {...a, shift: shiftRes.data };
                    })
                );
                setAssignment(assignmentWithShifts);
            })
            .catch(() => {});
    }, [currentUser]);

    const handleLogout = () => {
        localStorage.removeItem('token')
        navigate('/');
    }

    const handleCreateShift = async (e) => {
        e.preventDefault();
        const token = localStorage.getItem('token');
        try {
            await axios.post('/shifts', {
                facility_name: facilityName,
                shift_date: shiftDate,
                start_time: startTime,
                end_time: endTime
            }, {
                headers: {Authorization: `Bearer ${token}`}
            });
            setShowForm(false)
            // refresh shift list
            const res = await axios.get('/shifts', {
                headers: {Authorization: `Bearer ${token}`}
            });
            setShift(res.data);
        } catch(err) {
            alert(err.response?.data?.detail || 'Failed to create the shift')
        }
    };

    const handleExport = async () => {
        const token = localStorage.getItem('token');
        const res = await axios.get('/export/shifts', {
            headers: { Authorization: `Bearer ${token}`},
            responseType: 'blob'
        });
        const url = window.URL.createObjectURL(new Blob([res.data]));
        const link = document.createElement('a');
        link.href = url;
        const timestamp = new Date().toISOString().replace(/[:.]/g, '-')
        link.setAttribute('download', `shift_export_${timestamp}.csv`);
        document.body.appendChild(link);
        link.click();
        link.remove();
    };

    if (!currentUser) return <div>Loading....</div>

    return (
        <div>
            <button onClick={handleLogout}>Logout</button>
            <h2>Welcome, {currentUser.first_name}</h2>

            {currentUser.role === 'admin' ? (
                <div>
                    <h2>Shifts</h2>
                    <table>
                        <thead>
                            <tr>
                                <th>Date</th>
                                <th>Facility</th>
                                <th>Start Time</th>
                                <th>End Time</th>
                            </tr>
                        </thead>
                        <tbody>
                            { shifts.map(shift => (
                                <tr key={shift.id} onClick={ () => navigate(`/shifts/${shift.id}`) } style={{cursor: "pointer"}}>
                                    <td>{shift.shift_date}</td>
                                    <td>{shift.facility_name}</td>
                                    <td>{shift.start_time}</td>
                                    <td>{shift.end_time}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                    <button onClick={() => setShowForm(!showForm)}>Create Shift</button>
                    <button onClick={handleExport}>Export CSV</button>
                    { showForm && (
                        <form onSubmit={handleCreateShift}>
                            <input 
                                type="text"
                                placeholder="Facility Name"
                                value={facilityName}
                                onChange={ (e) => setFacilityName(e.target.value)}
                                required
                            />
                            <input
                                type="date"
                                value={shiftDate}
                                onChange={ (e) => setShiftDate(e.target.value)}
                                required
                            />
                            <input 
                                type="time" 
                                value={startTime}
                                onChange={ (e) => setStartTime(e.target.value)}
                                required
                            />
                            <input 
                                type="time" 
                                value={endTime}
                                onChange={ (e) => setEndTime(e.target.value)}
                                required
                            />
                            <button type="submit">Create Shift</button>
                        </form>
                    )}
                </div>
            ) : (
                <div>
                    <h2>My Shifts</h2>
                    <table>
                        <thead>
                            <tr>
                                <th>Shift date</th>
                                <th>Facility name</th>
                                <th>Start time</th>
                                <th>End time</th>
                            </tr>
                        </thead>
                        <tbody>
                            { assignments.map(a => (
                                <tr key={a.id}>
                                    <td>{a.shift?.shift_date}</td>
                                    <td>{a.shift?.facility_name}</td>
                                    <td>{a.shift?.start_time}</td>
                                    <td>{a.shift?.end_time}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            )
            }
        </div>
    )
}

export default Dashboard;