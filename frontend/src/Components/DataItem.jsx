import React, { useState } from "react";
import Popup from "./Popup";
import axios from 'axios';
const apiUrl = import.meta.env.VITE_API_URL;

const DataItem = ({ id, title, Shortcontent, isLast, onDelete, onUpdate }) => {
    const [isPopupDelete, setIsPopupDelete] = useState(false);
    const [isPopupOpen, setIsPopupOpen] = useState(false);
    const [titleInput, setTitleInput] = useState('');
    const [contentInput, setContentInput] = useState('');
    const [isConfermOpen, setIsConfirmOpen] = useState(false);

    const handleTitleChange = (event) => {
        setTitleInput(event.target.value);
    };

    const handleContentChange = (event) => {
        setContentInput(event.target.value);
    };
    
    const deletePopup = async () => {
        try {
            await axios.delete(`${apiUrl}/delete/${id}`);
            onDelete(id);
            setIsPopupDelete(false);
        } catch (err) {
            console.error("Error deleting item:", err.message);
            setIsPopupDelete(false);
        }
    };

    const toggleDeletePopup = () => {
        setIsPopupDelete(!isPopupDelete);
    };

    const handleSubmit = async(i, tit, cont) => {
        try {
            await axios.put(`${apiUrl}/update`, {
                id: i,
                title: tit,
                content: cont
            });
            
            setIsPopupOpen(false);
            toggleConfirm();
            onUpdate();  // Trigger a data fetch/update in DataTable to get the latest data
        } catch (error) {
            console.error("Error updating item:", error);
        }
    };
    
    
    const togglePopup = async(id) => {
        try {
            const response = await axios.get(`${apiUrl}/get/${id}`);
            setTitleInput(response.data.title);
            setContentInput(response.data.content);
        } catch (err) {
            console.error(err);
        }
        setIsPopupOpen(!isPopupOpen);
    };
    
    const toggleConfirm = () => setIsConfirmOpen(!isConfermOpen);
    return (
        <div className={`flex items-center justify-between py-4 px-6 border-b ${isLast ? 'border-b-0' : ''}`}>
            <div className="flex-1 flex flex-col">
                <div className="text-lg font-semibold text-gray-800">{title}</div>
                <div className="text-gray-600 truncate max-w-xs">{Shortcontent}</div>
            </div>
            <div className="flex items-center space-x-4">
                <img
                    className="w-12 h-12 cursor-pointer hover:scale-110 transition-transform"
                    src="src/assets/Images/Trash.svg"
                    alt="delete"
                    onClick={toggleDeletePopup}
                />
                <img
                    className="w-6 h-6 cursor-pointer hover:scale-110 transition-transform"
                    src="src/assets/Images/Edit.svg"
                    alt="edit"
                    onClick={() => togglePopup(id)}
                >
                    
                </img>
                {isPopupDelete && (
                    <Popup onClose={toggleDeletePopup} className="flex flex-col items-center">
                    <h2 className="text-lg font-semibold mb-4">Are you sure you want to delete?</h2>
                    <div className="flex space-x-2 justify-center">
                        <button
                            onClick={deletePopup}
                            className="bg-red-500 text-white px-4 py-2 rounded hover:bg-red-600 transition"
                        >
                            Confirm
                        </button>
                        <button
                            onClick={toggleDeletePopup}
                            className="bg-gray-300 text-gray-800 px-4 py-2 rounded hover:bg-gray-400 transition"
                        >
                            Cancel
                        </button>
                    </div>
                </Popup>
                
                )}
                
                {isPopupOpen && (
                    <Popup onClose={togglePopup} className="bg-gray-100 p-4 rounded-md shadow-md w-[800px] h-[575px] flex flex-col">
                    <h2 className="text-lg font-semibold mb-2" style={{ color: '#EF4E25' }}>Edit Item</h2>
                
                    <div className="flex flex-col mb-4">
                        <label className="block mb-2 text-left">Title:</label>
                        <input
                            type="text"
                            value={titleInput}
                            onChange={handleTitleChange}
                            className="w-full max-w-[400px] p-2 border border-gray-300 rounded focus:outline-none focus:ring focus:border-blue-300"
                        />
                    </div>
                
                    <div className="flex flex-col mb-4">
                        <label className="block mb-2 text-left">Content:</label>
                        <textarea
                            rows="5"
                            value={contentInput}
                            onChange={handleContentChange}
                            className="w-full max-w-[700px] p-2 border border-gray-300 rounded focus:outline-none focus:ring focus:border-blue-300"
                        ></textarea>
                    </div>
                
                    <div className="flex justify-end gap-2">
                        <button
                            onClick={() => handleSubmit(id, titleInput, contentInput)}
                            className="bg-red-500 text-white px-4 py-2 rounded hover:bg-red-600 transition"
                        >
                            Update
                        </button>
                        <button
                            onClick={togglePopup}
                            className="bg-gray-300 text-gray-800 px-4 py-2 rounded hover:bg-gray-400 transition"
                        >
                            Cancel
                        </button>
                    </div>
                </Popup>
                
                
                )}

                {isConfermOpen && (
                <Popup className="bg-gray-100 p-4 rounded-md shadow-md mt-4 w-[800px] h-[575px] flex flex-col items-center">
                    <h2 className="text-3xl font-bold mb-4 " style={{ color: '#EF4E25' }}>Successfully Edited</h2>
                
                    <div className="flex justify-center items-center mb-6">
                        <img src="src/assets/Images/confirm.svg" alt="confirmation" className="w-60 h-60" />
                    </div>
                
                    <div className="flex justify-center w-full">
                        <button
                            onClick={toggleConfirm}
                            className="bg-[#EF4E25] text-white text-lg px-6 py-3 rounded-[10px] hover:bg-orange-600 transition"
                        >
                            OK
                        </button>
                    </div>
                </Popup>
                
                
                
                )}
            </div>
        </div>
    );
};

export default DataItem;
