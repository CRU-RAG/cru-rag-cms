import { useState } from "react";

function DashBoard() {
    const [currentTab, setCurrentTab] = useState('dashboard');
    return (
        <div className="flex flex-col justify-between w-1/5 bg-gray-100 p-6 h-screen">
            {/* Top section */}
            <div className="text-sm">
                <div className=" mb-6">
                    <img src="/VerseWise.svg" alt="logo" className="mr-2" />
                    <span className="font-bold text-md">CRU-CMS</span>
                </div>
                
                <div className={`flex items-center mb-4 cursor-pointer ${currentTab === 'dashboard' ? 'font-semibold' : ''}`}
                    onClick={() => setCurrentTab('dashboard')}
                >
                    <img src="src/Assets/Images/barChart.svg" alt="bar" className="mr-2" />
                    <span>Dashboard</span>
                </div>
                
                <div className={`flex items-center mb-4 cursor-pointer ${currentTab === 'management' ? 'font-semibold' : ''}`}
                    onClick={() => setCurrentTab('management')}
                >
                    <img src="src/Assets/Images/users.svg" alt="users" className="mr-2" />
                    <span>Manage Users</span>
                </div>
            </div>

            {/* Bottom section */}
            
        </div>
    );
}

export default DashBoard;
