function StatsTot() {
    return (
        <div className="flex flex-col items-start p-4 border rounded-lg shadow-lg bg-white">
            <p className="text-[16px] font-semibold">Total Feed Data</p>
            <span className="text-[36px] font-bold">3</span>
            <span className="flex items-center space-x-2 text-sm">
                <img
                    className="w-[20px] h-[20px] cursor-pointer hover:scale-110 transition-transform"
                    src="src/Assets/Images/Icon.svg"
                    alt="up"
                />
                <span className="text-[#B42318]">10%</span> {/* Text with color */}
                <p className="whitespace-nowrap"><span> vs last month</span></p> {/* Added a new span for proper spacing */}
                <img
                    className="w-[96px] h-[48px] cursor-pointer hover:scale-110 transition-transform"
                    src="src/Assets/Images/lineRed.svg"
                    alt="line"
                />
            </span>
        </div>
    );
}

export default StatsTot;
