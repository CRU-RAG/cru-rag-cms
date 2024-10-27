import { useState } from "react";

function DashBoard() {
    const [currentTab, setCurrentTab] = useState('dashboard');
    return (
        <div className="flex flex-col justify-between w-1/5 bg-gray-100 p-6 h-screen">
            {/* Top section */}
            <div className="text-sm">
                <div className=" mb-6">
                    <img src="../../public/VerseWise.svg" alt="logo" className="mr-2" />
                    <span className="font-bold text-md">CRU-CMS</span>
                </div>
                <div className={`flex items-center mb-4 cursor-pointer ${currentTab === 'home' ? 'font-semibold' : ''}`}
                    onClick={() => setCurrentTab('home')}
                >
                    <img src="src/Assets/Images/home.svg" alt="home" className="mr-2" />
                    <span>Home</span>
                </div>
                <div className={`flex items-center mb-4 cursor-pointer ${currentTab === 'dashboard' ? 'font-semibold' : ''}`}
                    onClick={() => setCurrentTab('dashboard')}
                >
                    <img src="src/Assets/Images/barChart.svg" alt="bar" className="mr-2" />
                    <span>Dashboard</span>
                </div>
                <div className={`flex items-center mb-4 cursor-pointer ${currentTab === 'tasks' ? 'font-semibold' : ''}`}
                    onClick={() => setCurrentTab('tasks')}
                >
                    <img src="src/Assets/Images/checkSquare.svg" alt="check" className="mr-2" />
                    <span>Tasks</span>
                </div>
                <div className={`flex items-center mb-4 cursor-pointer ${currentTab === 'management' ? 'font-semibold' : ''}`}
                    onClick={() => setCurrentTab('management')}
                >
                    <img src="src/Assets/Images/users.svg" alt="users" className="mr-2" />
                    <span>Manage Users</span>
                </div>
            </div>

            {/* Bottom section */}
            <div>
                <div className="flex items-center mb-4 cursor-pointer">
                    <img src="src/Assets/Images/settings.svg" alt="setting" className="mr-2" />
                    <span>Settings</span>
                </div>
                <div className="mb-4">
                    <span className="font-semibold">Used space</span>
                    <p className="text-sm mt-1 mb-3">Your team has used 80% of your available space. Need more?</p>
                    <img src="src/Assets/Images/progress.svg" alt="progress" />
                    <div className="flex gap-5 mt-2 text-sm px-2 font-semibold">
                        <span className="text-blue-500 cursor-pointer">Dismiss</span>
                        <span className="text-[#EF4E25] cursor-pointer">Upgrade plan</span>
                    </div>
                </div>

                <div className="flex items-center">
                    <img src="src/Assets/Images/prof.svg" alt="profile" className="mr-3" />
                    <div className="text-xs">
                        <span>Team RAG</span>
                        <span>Ragitup@HACKATON</span>
                    </div>
                    <img src="src/Assets/Images/Button.svg" alt="button" className="ml-4" />
                </div>
            </div>
        </div>
    );
}

export default DashBoard;
