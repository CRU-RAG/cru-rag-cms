function StatsTot() {
    return (
        <div className="flex flex-col items-start p-4 border rounded-lg shadow-lg bg-white"> {/* Changed items-center to items-start */}
            <p className="text-[16px] font-semibold">Total Feed Data</p> {/* Remains unchanged */}
            <span className="text-[36px] font-bold">2,420</span> {/* Remains unchanged */}
            <span className="flex items-center space-x-2">
                <img
                    className="w-[20px] h-[20px] cursor-pointer hover:scale-110 transition-transform"
                    src="src/Assets/Images/arrow-up.svg"
                    alt="up"
                />
                <p className="whitespace-nowrap"><span className="text-[#027A48]">40% </span> vs last month</p> {/* Remains unchanged */}
                <img
                    className="w-[96px] h-[48px] cursor-pointer hover:scale-110 transition-transform" // Remains unchanged
                    src="src/Assets/Images/lineGreen.svg"
                    alt="line"
                />
            </span>
        </div>
    );
}

export default StatsTot;
