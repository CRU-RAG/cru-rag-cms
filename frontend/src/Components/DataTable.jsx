import { useState, useEffect } from "react";
import axios from 'axios'; 
import DataItem from "./DataItem";
import Popup from './Popup';
import Header from "./Header";
const apiUrl = import.meta.env.VITE_API_URL;

const DataTable = () => {
    const [data, setData] = useState([]);
    const [noOfPages, setNoOfPages] = useState(0);
    const [isPopupOpen, setIsPopupOpen] = useState(false);
    const [isConfermOpen, setIsConfirmOpen] = useState(false);
    const [title, setTitle] = useState('');
    const [content, setContent] = useState('');
    const [currentPage, setCurrentPage] = useState(1);
    const [total, setTotal] = useState(0);

    const handleDelete = async (id) => {
        try {
            const response = await axios.get(`${apiUrl}/getall`);
            setData(response.data.items);
            setNoOfPages(response.data.pages);
            const countResponse = await axios.get(`${apiUrl}/getall`);
            setTotal(countResponse.data.total); // Assumes response.data.total contains the total feed data
                
        } catch (error) {
            console.error("Error deleting item:", error);
        }
    };

    useEffect(() => {
        const fetchPosts = async () => {
            try {
                const response = await axios.get(`${apiUrl}/getall`);
                setData(response.data.items);
                setNoOfPages(response.data.pages);
            } catch (err) {
                console.error(err);
            }
        };
        fetchPosts();
        const fetchTotal = async () => {
            try {
                const response = await axios.get(`${apiUrl}/getall`);
                setTotal(response.data.total); // Assumes response.data.total contains the total feed data
            } catch (error) {
                console.error("Error fetching total:", error);
            }
        };

        fetchTotal();
    }, []);

    const handelNext = async () => {
        const nextPage = currentPage + 1;
        if (nextPage <= noOfPages) {
            try {
                const response = await axios.get(`${apiUrl}/getall?page=${nextPage}`);
                setData(response.data.items);
                setCurrentPage(nextPage);
            } catch (err) {
                console.error(err);
            }
        }
    };
    
    const handelPrev = async () => {
        const prevPage = currentPage - 1;
        if (prevPage >= 1) {
            try {
                const response = await axios.get(`${apiUrl}/getall?page=${prevPage}`);
                setData(response.data.items);
                setCurrentPage(prevPage);
            } catch (err) {
                console.error(err);
            }
        }
    };

    const handleTitleChange = (event) => setTitle(event.target.value);
    const handleContentChange = (event) => setContent(event.target.value);

    const togglePopup = () => setIsPopupOpen(!isPopupOpen);

    const toggleConfirm = () => setIsConfirmOpen(!isConfermOpen);


    const fetchPosts = async () => {
        try {
            const response = await axios.get(`${apiUrl}/getall?page=${currentPage}`);
            setData(response.data.items);
            setNoOfPages(response.data.pages);
        } catch (err) {
            console.error(err);
        }
    };

    const fetchTotal = async () => {
        try {
            const response = await axios.get(`${apiUrl}/getall`);
            setTotal(response.data.total); // Assumes response.data.total contains the total feed data
        } catch (error) {
            console.error("Error fetching total:", error);
        }
    };

    useEffect(() => {
        fetchPosts(); // Fetch posts on component mount
    }, []);

    const handleSubmit = async (tit, cont) => {
        try {
            await axios.post(`${apiUrl}/create`, { title: tit, content: cont });
            setTitle('');
            setContent('');

            fetchPosts();
            setIsPopupOpen(false);
            toggleConfirm();
            fetchTotal();
        } catch (error) {
            console.error("Error submitting item:", error);
        }
    };
    

    const onUpdate = async () => {
        try {
            const response = await axios.get(`${apiUrl}/getall?page=${currentPage}`);
            setData(response.data.items);  // Update the data with the latest list
        } catch (err) {
            console.error("Error fetching updated data:", err);
        }
    };
    

    const pageIndexes = Array.from({ length: noOfPages }, (_, i) => i + 1);

    return (
        <div>
        <Header total={total} />
        <div className="flex flex-col items-center p-6">
            <div className="w-full max-w-4xl bg-white shadow-lg rounded-lg">
                <div className="flex items-center justify-between p-4 border-b">
                    <h2 className="text-xl font-semibold">Title</h2>
                    
                    <button
                        onClick={togglePopup}
                        className="flex items-center px-4 py-2 text-white text-[18px] rounded-[10px] bg-[#EF4E25]"
                    >
                        <img src="src/Assets/Images/add.svg" alt="add" className="w-5 h-5 mr-2" />
                        New
                    </button>
                </div>
                {isPopupOpen && (
                    <Popup className="bg-gray-100 p-4 rounded-md shadow-md mt-4 w-[800px] h-[575px] flex flex-col">
                    <h2 className="text-lg font-semibold mb-2" style={{ color: '#EF4E25' }}>Add Content</h2>
                
                    <div className="flex flex-col items-start mb-4">
                        <label className="block mb-2 text-left">Title</label>
                        <input
                            type="text"
                            value={title}
                            onChange={handleTitleChange}
                            placeholder="Title"
                            className="w-[400px] p-2 border border-gray-300 rounded"
                        />
                    </div>
                
                    <div className="flex flex-col items-start mb-4">
                        <label className="block mb-2 text-left">Content</label>
                        <textarea
                            rows="5"
                            value={content}
                            onChange={handleContentChange}
                            placeholder="Content"
                            className="w-full max-w-[700px] p-2 border border-gray-300 rounded"
                        ></textarea>
                    </div>
                
                    <div className="flex justify-end gap-2">
                        <button
                            onClick={() => handleSubmit(title, content)}
                            className="bg-[#EF4E25] text-white px-4 py-2 rounded-[8px] hover:bg-orange-600 transition"
                        >
                            Submit
                        </button>
                        <button
                            onClick={togglePopup}
                            className="bg-white text-[#EF4E25] border border-[#D5D7DA] px-4 py-2 rounded-[8px] hover:bg-gray-100 transition"
                        >
                            Cancel
                        </button>
                    </div>
                </Popup>

                

)}

                    {isConfermOpen && (
                    <Popup className="bg-gray-100 p-4 rounded-md shadow-md mt-4 w-[800px] h-[575px] flex flex-col items-center">
                    <h2 className="text-3xl font-bold mb-4" style={{ color: '#EF4E25' }}>Successful Added</h2>
                
                    <div className="flex justify-center items-center mb-6">
                        <img src="src/Assets/Images/confirm.svg" alt="confirmation" className="w-60 h-60" />
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
                <div className="p-4">
                    {data.map((item, index) => (
                        <DataItem
                            key={item.id}
                            isLast={index === data.length - 1}
                            id={item.id}
                            title={item.title}
                            Shortcontent={item.short_content}
                            onDelete={handleDelete}
                            onUpdate={onUpdate}
                        />
                    ))}
                </div>
                <div className="flex justify-between items-center p-4 border-t">
                    <button
                        onClick={handelPrev}
                        disabled={currentPage === 1}
                        className="flex items-center text-blue-500 hover:text-blue-700 transition disabled:opacity-50"
                        >
                        <img src="src/Assets/Images/arrowLeft.svg" alt="previous" className="w-4 h-4 mr-2" />
                        Previous
                    </button>
                    <div className="flex space-x-2">

                    {pageIndexes.map((item) => (
                    <span
                        key={item}
                        className={`px-3 py-1 rounded ${item === currentPage ? 'bg-blue-500 text-white' : 'bg-gray-200 text-gray-800'} cursor-pointer`}
                        onClick={async () => {
                        setCurrentPage(item);
                        try {
                            const response = await axios.get(`${apiUrl}/getall?page=${item}`);
                            setData(response.data.items);
                        } catch (err) {
                            console.error(err);
                        }
                    }}
        >
            {item}
        </span>
    ))}
</div>

                    <button
                        onClick={handelNext}
                        disabled={currentPage === noOfPages}
                        className="flex items-center text-blue-500 hover:text-blue-700 transition disabled:opacity-50"
                    >
                        Next
                        <img src="src/Assets/Images/arrowRight.svg" alt="next" className="w-4 h-4 ml-2" />
                    </button>
                </div>
            </div>
            
        </div>
    </div>
    );
};

export default DataTable;
