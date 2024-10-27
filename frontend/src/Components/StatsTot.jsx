// StatsTot.js
import { useState, useEffect } from "react";
import axios from "axios";

const apiUrl = import.meta.env.VITE_API_URL;

const StatsTot = () => {
    const [total, setTotal] = useState(0);

    useEffect(() => {
        const fetchTotal = async () => {
            try {
                const response = await axios.get(`${apiUrl}/getall`);
                setTotal(response.data.total); // Assumes response.data.total contains the total feed data
            } catch (error) {
                console.error("Error fetching total:", error);
            }
        };

        fetchTotal();
    }, []); // Empty dependency array to run only on mount

    return (
        <div className="flex flex-col items-start p-4 border rounded-lg shadow-lg bg-white">
            <p className="text-[16px] font-semibold">Total Feed Data</p>
            <span className="text-[36px] font-bold">
                <span className={`${total ? 'opacity-100' : 'opacity-0'}`}>{total}</span>
            </span>
        </div>
    );
}

export default StatsTot;
